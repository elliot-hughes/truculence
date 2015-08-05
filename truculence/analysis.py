import os
import ROOT
from ROOT import TFile, TTree, TChain, TCanvas, TH1F, TH2F, TGraphErrors, TLegend, TList
from array import array
from subprocess import Popen, PIPE
from re import search
from truculence import packing, color

# VARIABLES:
colors = [ROOT.kBlue, ROOT.kRed]
# /VARIABLES

# CLASSES:
class dataset:
	# Construction:
	def __init__(self, name="", sigma=1):
		self.name = name
		self.sigma = sigma
		info = get_files(name=self.name)
		self.dir = info["dir"]
		self.files = info["files"]
		self.files_full = ["{0}/{1}".format(self.dir, f) for f in self.files]
	# /Construction
	
	# Properties:
	def __nonzero__(self):
		return self.name != ""
	# /Properties
	
	# Methods:
	def get_nevents(self):
		n = 0
		for f in self.files_full:
			n += get_nevents(f)
		return n
	# /Methods
# /CLASSES

# FUNCTIONS:
def test():
	return "Hello world! (analysis)"

## Dataset functions:
def get_files(name="QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8", username="tote"):
	ds_path = "/eos/uscms/store/user/{0}/{1}".format(username, name)
	ds_dir = ""
	files = []
	custom_names = os.listdir(ds_path)
	if len(custom_names) > 1:
		print "WARNING: There were multiple \"custom names\"!"
	ds_path += "/{0}".format(custom_names[0])
	dates = os.listdir(ds_path)
	if len(dates) > 1:
		print "WARNING: It's unclear what files you want to run over. I'm going to run over the following directory:\n{0}/{1}".format(ds_path, dates[-1])
	ds_dir = "{0}/{1}/0000".format(ds_path, dates[-1])
	files = [f for f in os.listdir(ds_dir) if ".root" in f]
	return {
		"dir": ds_dir,
		"files": files,
	}

def get_nevents(f=""):
	raw_output = Popen(['echo "Events->GetEntries()" | root -l {0}'.format(f)], shell = True, stdout = PIPE, stderr = PIPE).communicate()
	match = search("\(Long64_t\) (\d+)\s", raw_output[0])
	if match:
		return int(match.group(1))
	else:
		return False

## ROOT functions:
def setup_root():
	ROOT.gROOT.SetBatch()
	tcanvas = TCanvas("c1", "c1", 500, 500)
	tcanvas.SetCanvasSize(500, 500)
	return tcanvas

def list_file(full_path):		# This isn't quite complete, it's basically just for listing all histograms in the highest directory of a root file (at "full_path").
	tfile = TFile(full_path)
	return list_tfile(tfile)

def get_tfile(full_path):		# This is so pointless ...
	return TFile(full_path)

def list_tfile(tfile):
	tlist = tfile.GetListOfKeys()
	return [item.GetName() for item in tlist]

def get_tobject(tfile, name):
	ROOT.SetOwnership(tfile, 0)
	return tfile.Get(name)

def get_tobjects_all(tfile, kind=""):
	names = list_tfile(tfile)
	ROOT.SetOwnership(tfile, 0)
	tobjects = [tfile.Get(name) for name in names]
	if not kind or kind.lower() == "all":
		return tobjects
	else:
		return [tobject for tobject in tobjects if tobject.ClassName().lower() == kind.lower()]

def get_ttree(full_path, ttree_name="analyzer/events"):
	tfile = TFile(full_path)
	ROOT.SetOwnership(tfile, 0)
	ttree = TTree()
	tfile.GetObject(ttree_name, ttree)
#	ROOT.SetOwnership(ttree, 0)
#	print ttree
	return ttree

#def merge_ttrees(list_of_ttrees, ttree_name="T", ttree_title=""):		# This doesn't work because TList takes pointers ...
#	tl = TList
#	for tt in list_of_ttrees:
#		tl.Add(tt)
#	tt_out = TTree(ttree_name, ttree_title)
#	tt_out.MergeTrees(tl)
#	return tt_out

def setup_th1(info):
	th1 = {}
	for key, values in info.iteritems():
		if len(values) == 2:
			values.append("Events")
			th1[key] = TH1F(key, values[0], 50, 0, 0)
		elif len(values) == 3:
			th1[key] = TH1F(key, values[0], 50, 0, 0)
		elif len(values) == 5:
			values.insert(2, "Events")
			th1[key] = TH1F(key, values[0], values[3], values[4], values[5])
		elif len(values) == 6:
			th1[key] = TH1F(key, values[0], values[3], values[4], values[5])
		else:
			print "ERROR: setup_th1 takes 2, 3, or 6 arguments."
		try:
			th1[key].Sumw2()
			th1[key].GetXaxis().CenterTitle(1)
			th1[key].GetXaxis().SetTitle(values[1])
			th1[key].GetYaxis().CenterTitle(1)
			th1[key].GetYaxis().SetTitle(values[2])
			th1[key].GetYaxis().SetTitleOffset(1.3)
			th1[key].SetLineWidth(2)
			th1[key].SetLineColor(ROOT.kRed)
		except Exception as ex:
			print ">> Setup wasn't completed."
	return th1

def setup_th2(info):
	th2 = {}
	for key, values in info.iteritems():
		if len(values) == 3:
			values.append("Events")
			th2[key] = TH2F(key, values[0], 50, 0, 0, 50, 0, 0)
		elif len(values) == 4:
			th2[key] = TH2F(key, values[0], 50, 0, 0, 50, 0, 0)
		elif len(values) == 9:
			values.insert(3, "Events")
			th2[key] = TH2F(key, values[0], values[4], values[5], values[6], values[7], values[8], values[9])
		elif len(values) == 10:
			th2[key] = TH2F(key, values[0], values[4], values[5], values[6], values[7], values[8], values[9])
		else:
			print "ERROR: setup_th2 takes 3, 4, or 10 arguments."
		try:
			th2[key].Sumw2()
			th2[key].GetXaxis().CenterTitle(1)
			th2[key].GetXaxis().SetTitle(values[1])
			th2[key].GetYaxis().CenterTitle(1)
			th2[key].GetYaxis().SetTitle(values[2])
			th2[key].GetZaxis().CenterTitle(1)
			th2[key].GetZaxis().SetTitle(values[3])
			th2[key].GetZaxis().SetTitleOffset(1.3)
		except Exception as ex:
			print ">> Setup wasn't completed."
	return th2

def print_th1(th1, name, tcanvas):
	ROOT.gStyle.SetOptStat("nemrou")
	keys = th1.keys()
	if len(keys) == 1:
		tcanvas.Clear()
		th1[keys[0]].Draw()
		tcanvas.Print("{0}.pdf(".format(name), "pdf")
		tcanvas.Clear()
		tcanvas.Print("{0}.pdf)".format(name), "pdf")
	else:
		for key, histogram in th1.iteritems():
			histogram.Draw()
			if key == keys[0]:
				tcanvas.Print("{0}.pdf(".format(name), "pdf")
			elif key == keys[-1]:
				tcanvas.Print("{0}.pdf)".format(name), "pdf")
			else:
				tcanvas.Print("{0}.pdf".format(name), "pdf")

def print_th2(th2, name, tcanvas):
	for key, histogram in th2.iteritems():
		tcanvas.Clear()
		histogram.Draw("colz")
		if key == th2.keys()[0]:
			tcanvas.Print("{0}.pdf(".format(name), "pdf")
		elif key == th2.keys()[-1]:
			tcanvas.Print("{0}.pdf)".format(name), "pdf")
		else:
			tcanvas.Print("{0}.pdf".format(name), "pdf")

def save_histograms(ths, file_name):		# "ths" is a list of th1, th2, etc.
	if file_name[-5:] != ".root":
		file_name += ".root"
	if os.path.exists(file_name):
		tf = TFile(file_name, "RECREATE")
	else:
		tf = TFile(file_name, "NEW")
	for th in ths:
		for key, histogram in th.iteritems():
			histogram.Write()
	tf.Close()

def print_th(th1, th2, name, tcanvas):
	if not os.path.exists("plots/{0}".format(name)):
		os.makedirs("plots/{0}".format(name))
	for key, histogram in th1.iteritems():
		tcanvas.Clear()
		tcanvas.SetRightMargin(0.1)
		tcanvas.SetBottomMargin(0.1)
		ROOT.gStyle.SetOptStat("nemr")
		histogram.Draw()
		if key == th1.keys()[0]:
			tcanvas.Print("{0}.pdf(".format(name), "pdf")
		else:
			tcanvas.Print("{0}.pdf".format(name), "pdf")
		tcanvas.SaveAs("plots/{0}/h1-{1}.pdf".format(name, key))
		tcanvas.SaveAs("plots/{0}/h1-{1}.svg".format(name, key))
	for key, histogram in th2.iteritems():
		tcanvas.Clear()
		tcanvas.SetRightMargin(0.15)
		tcanvas.SetBottomMargin(0.15)
		ROOT.gStyle.SetOptStat("ne")
		histogram.Draw("colz")
		if key == th2.keys()[-1]:
			tcanvas.Print("{0}.pdf)".format(name), "pdf")
		else:
			tcanvas.Print("{0}.pdf".format(name), "pdf")
		tcanvas.SaveAs("plots/{0}/h2-{1}.pdf".format(name, key))
		tcanvas.SaveAs("plots/{0}/h2-{1}.svg".format(name, key))

def make_tlegend(th1s, labels=[], key="lpe", corner=1):		# "corner" puts the legend in corner 0-3, starting from top left.
	if not labels:
#		labels = [th1.GetTitle() for th1 in th1s]
		labels = [th1.GetName() for th1 in th1s]
	if corner == 0:
		tl = TLegend(0.3, 0.7, 0.1, 0.9)		#East edge, S, W, N
	if corner == 1:
		tl = TLegend(0.9, 0.7, 0.7, 0.9)		#East edge, S, W, N
	if corner == 2:
		tl = TLegend(0.9, 0.1, 0.7, 0.3)		#East edge, S, W, N
	if corner == 3:
		tl = TLegend(0.3, 0.1, 0.1, 0.3)		#East edge, S, W, N
	for i, th1 in enumerate(th1s):
		tl.AddEntry(th1, labels[i], key)
	ROOT.SetOwnership(tl, 0)
	return tl

def make_tg(x_title="", x=[], x_e=[], y_title="", y=[], y_e=[], title=""):
	tcanvas = TCanvas("z", "z", 500, 500)
	tcanvas.SetCanvasSize(500, 500)
	x = array("d", x)
	if x_e:
		x_e = array("d", x_e)
	else:
		x_e = array("d", [0 for i in x])
	y = array("d", y)
	if y_e:
		y_e = array("d", y_e)
	else:
		y_e = array("d", [0 for i in y])
	tg = TGraphErrors(len(x), x, y, x_e, y_e)
	tg.Draw("ALP")
	tg.SetMarkerStyle(9)
	tg.SetMarkerSize(0.4)
	tg.GetXaxis().CenterTitle(1)
	tg.GetXaxis().SetTitle(x_title)
	tg.GetXaxis().SetTitleSize(0.045)
	tg.GetYaxis().CenterTitle(1)
	tg.GetYaxis().SetTitle(y_title)
	tg.GetYaxis().SetTitleSize(0.045)
	tg.SetTitle(title)
#	tcanvas.SaveAs("tg_{0}.pdf".format(name))
#	print tg
	return tg

def superimpose(th1s, logy=False):		# Add a legend!
	n = len(th1s)
	colors = color.pick(n)
	tcolors = [c.tcolor() for c in colors]
#	make_palette(colors, sq=0.4)
	tc = setup_root()
	for i, th1 in enumerate(th1s):
		th1.SetLineColor(tcolors[i].GetNumber())
		th1.SetMarkerColor(tcolors[i].GetNumber())
		if i == 0:
			th1.Draw()
		else:
			th1.Draw("same")
	tc.SetLogy(logy)
	tl = make_tlegend(th1s)
	print tl
	tl.Draw()
	tc.Modified()
	tc.Update()
	ROOT.gStyle.SetOptStat(0)
	return tc

def make_palette(colors, f="palette.pdf", sq=0.5):
	tc = setup_root()
	n = len(colors)
	print n, packing.squareness(n)
	while packing.squareness(n) > sq:
		n += 1
	print n, packing.squareness(n)
	factors = packing.factorize(n)[-1]
	tc.SetCanvasSize(500, int(500*float(factors[0])/factors[1]))
	tc.Divide(factors[1], factors[0], 0.01, 0.01)
	for i, c in enumerate(colors):
		tc.cd(i + 1)
		tcolor = c.tcolor()
		ROOT.gPad.SetFillColor(tcolor.GetNumber())
	tc.SaveAs(f)





import os
import ROOT
from ROOT import TFile, TTree, TCanvas, TH1F, TH2F, TGraphErrors
from array import array

# CLASSES:
class dataset:
	# Construction:
	def __init__(self, name="", sigma=1):
		self.name = name
		self.sigma = sigma
		info = get_files(name=self.name)
		self.dir = info["dir"]
		self.files = info["files"]
	# /Construction
	
	# Properties:
	def __nonzero__(self):
		return self.name != ""
	# /Properties
	
	# Methods:
#	def get_ttree(self, name=None):
#		if name == None:
#			name = self.ttree_name_default
#		return analysis.get_ttree("{0}/{1}".format(self.directory, self.file), name)
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
#	elif dataset == "qcd":

## ROOT functions:
def setup_root():
	ROOT.gROOT.SetBatch()
	tcanvas = TCanvas("c1", "c1", 500, 500)
	tcanvas.SetCanvasSize(500, 500)
	return tcanvas

def get_ttree(full_path, ttree_name):
	tfile = TFile(full_path)
	ROOT.SetOwnership(tfile, 0)
	ttree = TTree()
	tfile.GetObject(ttree_name, ttree)
#	ROOT.SetOwnership(ttree, 0)
#	print ttree
	return ttree

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

def save_histograms(th1, th2, name):
	file_name = "{0}.root".format(name)
	if os.path.exists(file_name):
		tf = TFile(file_name, "RECREATE")
	else:
		tf = TFile(file_name, "NEW")
	for key, histogram in th1.iteritems():
		histogram.Write()
	for key, histogram in th2.iteritems():
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









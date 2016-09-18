# IMPORTS:
import os, sys, re
import xml.etree.ElementTree as ET
from truculence import lhe
import ROOT
# :IMPORTS

# VARIABLES:
#lhe_in = "/users/h2/tote/madgraph/sqto4j/Events/sq150to4j_cutht700/unweighted_events.lhe"
#lhe_in = "out.lhe"
ROOT.gROOT.SetBatch()
tc = ROOT.TCanvas("tc", "tc")
th1_pt = ROOT.TH1D("pt", "pt", 50, 0, 1000)
th1_ht = ROOT.TH1D("ht", "ht", 50, 0, 2000)
#plot_out = "pt.pdf"
# :VARIABLES

# CLASSES:
# :CLASSES

# FUNCTIONS:
def main():
	# Arguments and variables:
	assert len(sys.argv) == 2
	lhe_in = sys.argv[1]
	fname = lhe_in.split("/")[-1]
	
	if not os.path.exists(lhe_in):
		print "ERROR: There's no file called '{}'".format(lhe_in)
		return False
	
	cut_ht = 700
	cut_pt = 200
	n_total = 0
	n_passed_ht = 0
	n_passed_pt = 0
	tree = ET.parse(lhe_in)
	for i, event in enumerate(tree.findall("event")):
		e = lhe.event(event)
		n_total += 1
		if min([sq["pt"] for sq in e.squarks]) > cut_pt:
			n_passed_pt += 1
		if e.ht > cut_ht:
			n_passed_ht += 1
	print "Events:", n_total
	print "pT cut:", n_passed_pt
	print "HT cut:", n_passed_ht
	
	return True
	
	
	
	
	
	
	
	
	
	
	
	sys.exit()
	
	n_inits = 0
	n_events = 0
	n_events_accepted = 0

	tags = ["event", "init"]
	controls = {}
	raws = {}
	for tag in tags:
		controls[tag] = {}
		controls[tag]["begin"] = False
		controls[tag]["end"] = False
		controls[tag]["inside"] = False
		raws[tag] = ""
	
	# Start looping over the input file:
	with open(lhe_in, "r") as file_in:
		for line in file_in:                 # This method is good on memory, acting as an iterator.
	#		print line
			for tag, control in controls.iteritems():     # Tag is "event" or "init".
				if "<{}>".format(tag) in line:
					control["begin"] = True
					control["inside"] = True
				else:
					control["begin"] = False
				if "</{}>".format(tag) in line:
					control["end"] = True
					control["inside"] = False
				else:
					control["end"] = False
		
				if control["begin"]:
					raws[tag] = line
				elif control["inside"] or control["end"]:
					raws[tag] += line
		
			if controls["init"]["end"]:
				init = lhe.init(raws["init"])
				if init:
					if n_inits == 0:
						n_inits += 1
#						with open(lhe_out, "a") as file_out:
#							file_out.write(init.raw + "\n")
					else:
						print "ERROR: There is more than one \"init\" in the LHE file."
						sys.exit()
		
			if controls["event"]["end"]:
				event = lhe.event(raws["event"])
				if event:
					n_events += 1
					pts = [squark["pt"] for squark in event.squarks]
					ht = sum([quark["pt"] for quark in event.quarks])
					for pt in pts:
						th1_pt.Fill(pt)
					th1_ht.Fill(ht)
	
	tc.SetLogy(1)
	th1_pt.Draw()
	tc.SaveAs("{}.pdf".format(th1_pt.GetName()))
	tc.Clear()
	th1_ht.Draw()
	tc.SaveAs("{}.pdf".format(th1_ht.GetName()))
	
	print n_inits, n_events
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN

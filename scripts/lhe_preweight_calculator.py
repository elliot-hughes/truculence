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
#ptc = ROOT.TCanvas("pt", "pt")
#htc = ROOT.TCanvas("ht", "ht") 
#msc = ROOT.TCanvas("ms", "ms")

# FUNCTIONS:
def main():
	# Arguments and variables:
	cut_ht = 700
	assert len(sys.argv) == 2
	lhe_in = sys.argv[1]
	
	if not os.path.exists(lhe_in):
		print "ERROR: LHE file '{}' doesn't exist.".format(lhe_in)
		return False
	
	n_total = 0
	n_passed_ht = 0
	n_passed_pt = 0
	n_odd_squark_count = 0
	tree = ET.parse(lhe_in)
	for i, event in enumerate(tree.findall("event")):
		n_total += 1
		e = lhe.event(event)
		ht = e.ht
		if ht > cut_ht: n_passed_ht += 1
	
	print "{}/{} passed the HT cut of {} Gev.".format(n_passed_ht, n_total, cut_ht)
	print "preweight = {:.5f}".format(float(n_passed_ht)/n_total)

# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN

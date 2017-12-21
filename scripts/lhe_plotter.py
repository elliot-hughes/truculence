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
def construct_histograms():
	hs = {}
	
	hs["ht"] = ROOT.TH1D("ht", "", 50, 0, 2000)
	hs["pt_sg"] = ROOT.TH1D("pt_sg", "", 50, 0, 1000)
	hs["pt_sq"] = ROOT.TH1D("pt_sq", "", 50, 0, 1000)
	hs["pt_t"] = ROOT.TH1D("pt_t", "", 50, 0, 1000)
	hs["m_sg"] = ROOT.TH1D("m_sg", "", 50, 0, 1000)
	hs["m_sq"] = ROOT.TH1D("m_sq", "", 50, 0, 1000)
	hs["m_t"] = ROOT.TH1D("m_t", "", 50, 0, 1000)
	hs["m_sh"] = ROOT.TH1D("m_sh", "", 50, 0, 1000)
	hs["eta_sq"] = ROOT.TH1D("eta_sq", "", 50, -6, 6)
	hs["eta_t"] = ROOT.TH1D("eta_t", "", 50, -6, 6)
	
	return hs

def main():
	# Arguments and variables:
	assert len(sys.argv) == 2
	lhe_in = sys.argv[1]
	fname = lhe_in.split("/")[-1]
	
	if not os.path.exists(lhe_in):
		print "ERROR: There's no file called '{}'".format(lhe_in)
		return False
		
	tf_out = ROOT.TFile(fname.replace(".lhe", "") + ".root", "recreate")
	
	hs = construct_histograms()

	n_total = 0
	n_passed_ht = 0
	n_passed_pt = 0
	n_odd_squark_count = 0
	tree = ET.parse(lhe_in)
	for i, event in enumerate(tree.findall("event")):
		e = lhe.event(event)
		if len(e.squarks) > 2:
			if n_odd_squark_count == 0: 
				print "Event {}:".format(i)
				print e.raw
			n_odd_squark_count += 1
		pts_sg = [sg["pt"] for sg in e.gluinos]
		pts_sq = [sq["pt"] for sq in e.squarks]
		pts_t = [q["pt"] for q in e.tops]
		ms_sg = [sg["m"] for sg in e.gluinos]
		ms_sq = [sq["m"] for sq in e.squarks]
		ms_t = [q["m"] for q in e.tops]
		ms_sh = [sh["m"] for sh in e.higgsinos]
		etas_sq = [sq["eta"] for sq in e.squarks]
		etas_t = [q["eta"] for q in e.tops]
		ht = e.ht
		
		hs["ht"].Fill(ht)
		for pt in pts_sg: hs["pt_sg"].Fill(pt)
		for pt in pts_sq: hs["pt_sq"].Fill(pt)
		for pt in pts_t: hs["pt_t"].Fill(pt)
		for m in ms_sg: hs["m_sg"].Fill(m)
		for m in ms_sq: hs["m_sq"].Fill(m)
		for m in ms_t: hs["m_t"].Fill(m)
		for m in ms_sh: hs["m_sh"].Fill(m)
		for eta in etas_sq: hs["eta_sq"].Fill(eta)
		for eta in etas_t: hs["eta_t"].Fill(eta)
	
	for name, h in hs.items(): tf_out.WriteTObject(h)
	
	print "Odd squark count = {}".format(n_odd_squark_count)

# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN

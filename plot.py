from truculence import *
from ROOT import TCanvas

if __name__ == "__main__":
	raw = []
	with open("link_on.log") as f_raw:
		raw = f_raw.readlines()
	points = [[] for i in raw[0].split()]
	row = -1
	for line in raw:
		row += 1
		for i, value in enumerate(line.split()):
			try:
				result = float(value)
			except:
				result = row
			points[i].append(result)
	print points

	tc = analysis.setup_root()
	tg = analysis.make_tg(x=points[0], y=points[1])
	tg.Draw("ALP")
	tc.SaveAs("graph.pdf")

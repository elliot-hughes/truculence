from truculence import *
from array import array
from ROOT import TCanvas
from optparse import OptionParser



if __name__ == "__main__":
	# Script arguments:
	parser = OptionParser()
	parser.add_option("-d", "--data", dest="d",
		default="",
		help="The location of the data you want to plot.",
		metavar="STR"
	)
	(options, args) = parser.parse_args()
	d = options.d

	# Turn data into arrays:
	with open(d) as f_raw:
		data = [line.split() for line in f_raw.readlines()]
#	print data
	axes = [array("d", [float(j) for j in i]) for i in zip(*data)]
#	print axes
	
	
#	points = [[] for i in raw[0].split()]
#	row = -1
#	for line in raw:
#		row += 1
#		for i, value in enumerate(line.split()):
#			try:
#				result = float(value)
#			except:
#				result = row
#			points[i].append(result)
#	print points

	
	tc = analysis.setup_root()
	tg = analysis.make_tg(x=axes[0], y=axes[1])
	tg.Draw("ALP")
	tc.SaveAs("graph.pdf")

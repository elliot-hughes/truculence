from array import array

# Make sure not having pyROOT doesn't break importing (it'll still break functions); fix this some day:
try:
	from ROOT import TMultiGraph
except Exception as ex:
	print ex

def graph(out="graph.pdf"):
	x = array("d", range(100))
	y = array("d", range(100))
	mg = TMultiGraph(len(x), x, y)
	

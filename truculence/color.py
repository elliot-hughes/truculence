import ROOT
from truculence import analysis

class color:
	def __init__(self, r=0, g=0, b=0):
		self.r=r
		self.g=g
		self.b=b
		self.rgb_i=[self.r, self.g, self.b]
		self.rgb_f=rgb_itof(self.rgb_i)
		self.R=self.rgb_f[0]
		self.G=self.rgb_f[1]
		self.B=self.rgb_f[2]

def rgb_itof(I):
	return [i/float(255) for i in I]

def rgb_ftoi(F):
	return [f*float(255) for f in F]

def make_palette(colors, f="palette.pdf"):
# Make use of this: http://stackoverflow.com/questions/339939/stacking-rectangles-to-into-the-most-square-like-arrangement-possible
	tc = analysis.setup_root()
	tc.Divide(10, 10, 0.01, 0.01)
	for i, c in enumerate(colors):
		tc.cd(i + 1)
		tcolor = ROOT.TColor(1001 + i, c.R, c.G, c.B)
		ROOT.SetOwnership(tcolor, 0)
#		tcolor.SetRGB(c.R, c.G, c.B)
		ROOT.gPad.SetFillColor(tcolor.GetNumber())
	tc.SaveAs(f)

#def get_n_colors(n):
#	return

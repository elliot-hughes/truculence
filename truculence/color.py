import ROOT
from truculence import packing

class color:
	# Variables:
	id_recent = 1000
	# /Variables
	
	# Construction:
	def __init__(self, R=0, G=0, B=0):
		# Meta:
		color.id_recent += 1
		self.id = color.id_recent
		
		# RGB:
		self.R=R
		self.G=G
		self.B=B
		self.RGB = [R, G, B]
		self.rgb = rgb_itof(self.RGB)
		self.r=self.rgb[0]
		self.g=self.rgb[1]
		self.b=self.rgb[2]
		
		# HSL:
		## To do: construct function rgb_to_hsl.
	# /Construction
	
	# Methods:
	def tcolor(self):
		tc = ROOT.TColor(self.id, self.r, self.g, self.b)
		ROOT.SetOwnership(tc, 0)
		return tc
	# /Methods

def rgb_itof(I):
	return [i/float(255) for i in I]

def rgb_ftoi(F):
	return [f*float(255) for f in F]

def hsl_to_rgb(HSL):		# See https://en.wikipedia.org/wiki/HSL_and_HSV#From_HSL
	H = float(HSL[0])
	S = float(HSL[1])
	L = float(HSL[2])
	if S > 1:
		S /= 100
	if L > 1:
		L /= 100
	C = (1 - abs(2*L - 1))*S
#	print C
	X = (1 - abs((H/60)%2 - 1))*C
	m = L - C/2
#	print X
#	print H
	if H >= 0 and H < 60:
		RGB_temp = [C, X, 0]
	elif H >= 60 and H < 120:
		RGB_temp = [X, C, 0]
	elif H >= 120 and H < 180:
		RGB_temp = [0, C,X]
	elif H >= 180 and H < 240:
		RGB_temp = [0, X, C]
	elif H >= 240 and H < 300:
		RGB_temp = [X, 0, C]
	elif H >= 300 and H <= 360:
		RGB_temp = [C, 0, X]
	else:
		RGB_temp = False
	if RGB_temp:
		return [int((i + m)*255) for i in RGB_temp]
	else:
		return False

def pick(n):
	colors = []
	for i in range(n):
		H = i*360/n
		S = 50
		L = 50
		RGB = hsl_to_rgb([H, S, L])
		colors.append(color(RGB[0], RGB[1], RGB[2]))
	return colors


#def get_n_colors(n):
#	return

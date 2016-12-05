####################################################################
# Type: MODULE                                                     #
#                                                                  #
# Description: [description]                                       #
####################################################################

# IMPORTS:
from truculence import analysis
import math
# /IMPORTS

# VARIABLES:
# /VARIABLES

# CLASSES:
class jet:
	def __init__(self, px, py, pz, e, jec=1, jmc=1, tau=None, bd=None, index=None):
		# Basics:
		self.px_uncorrected = px
		self.py_uncorrected = py
		self.pz_uncorrected = pz
		self.e_uncorrected = e
		self.p_uncorrected = (self.px_uncorrected**2 + self.py_uncorrected**2 + self.pz_uncorrected**2)**(0.5)
		try: self.m_uncorrected = (self.e_uncorrected**2 - self.p_uncorrected**2)**(0.5)
		except: self.m_uncorrected = 0
		self.pt_uncorrected = (self.px_uncorrected**2 + self.py_uncorrected**2)**(0.5)
		self.et_uncorrected = (self.e_uncorrected**2 - self.p_uncorrected**2 + self.pt_uncorrected**2)**(0.5)
		self.eta = math.log((self.p_uncorrected + self.pz_uncorrected)/(self.p_uncorrected - self.pz_uncorrected))/2
		self.theta = 2*math.atan(math.exp(-1*self.eta))
		self.phi = math.acos(self.px_uncorrected/self.pt_uncorrected) if self.py_uncorrected >= 0 else -math.acos(self.px_uncorrected/self.pt_uncorrected)
		
		self.set_jec(jec)
		self.set_jmc(jmc)
		
		self.bd = bd
		if tau != None:
			self.tau = tau
			for i, t in enumerate(tau):
				setattr(self, "tau{}".format(i+1), t)
		self.index = index
		self.i = index
#		self.update()
	
	
#	def update(self):
#		self.pt = (self.px**2 + self.py**2)**(0.5)
#		self.et = (self.m**2 + self.pt**2)**(0.5)
#		self.eta = math.log( (self.p + self.pz)/(self.p - self.pz) )/2
#		self.theta = 2*math.atan(math.exp(-1*self.eta))
#		self.phi = math.acos(self.px/self.pt) if self.py >= 0 else -math.acos(self.px/self.pt)
	
	
	def set_jec(self, jec):
		self.jec = jec
		self.px = self.px_uncorrected*jec
		self.py = self.py_uncorrected*jec
		self.pz = self.pz_uncorrected*jec
		self.e = self.e_uncorrected*jec
		self.p = (self.px**2 + self.py**2 + self.pz**2)**(0.5)
		self.pt = (self.px**2 + self.py**2)**(0.5)
		self.et = (self.e**2 - self.p**2 + self.pt**2)**(0.5)
	
	
	def set_jmc(self, jmc):
		self.jmc = jmc
		self.m = self.m_uncorrected*jmc
# /CLASSES

# FUNCTIONS
def delta_m(jets, groom=False):
	var = "m"
	if groom in ["t", "p", "s", "f"]:
		var += "_" + groom
	if len(jets) == 2:
		return abs(getattr(jets[0], var) - getattr(jets[1], var))
	else:
		print "ERROR (physics.delta_m): I don't understand the arguments: {}".format(jets)
		return False

def delta_phi(j0, j1):
	d = j0.phi - j1.phi
	if d > math.pi:
		d -= 2*math.pi
	elif d <= -math.pi:
		d += 2*math.pi
	return d

def delta_r(j0, j1, physical=False):
	return ((j0.eta - j1.eta)**2 + delta_phi(j0, j1)**2)**(0.5)

# /FUNCTIONS

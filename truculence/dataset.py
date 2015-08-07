####################################################################
# Type: MODULE                                                     #
#                                                                  #
# Description: [description]                                       #
####################################################################

# IMPORTS:
import analysis
# /IMPORTS

# CLASSES:
class dataset:
	# Construction:
	def __init__(self, name_full="", sigma=None, m=None, pts=()):
		# Basic name things:
		self.name_full = name_full
		name_parts = [i for i in name_full.split("/") if i]
		if len(name_parts) == 3:
			self.name = name_parts[0]
			self.version = name_parts[1]
			self.type = name_parts[2]
		else:
			self.name = False
			self.version = False
			self.type = False
		
		# Local info:
		info = analysis.get_files(name=self.name, v=False)
		self.dir = info["dir"]
		self.files = info["files"]
		self.files_full = ["{0}/{1}".format(self.dir, f) for f in self.files]
		
		# Parameters:
		self.sigma = sigma
		self.m = m
		if not pts:
			pts = ()
		self.pts = pts
	# /Construction
	
	# Properties:
	def __nonzero__(self):
		return self.name != False
	# /Properties
	
	# Methods:
	def get_nevents(self):
		n = 0
		for f in self.files_full:
			n += analysis.get_nevents(f)
		return n
	# /Methods
# /CLASSES

# FUNCTIONS:
# /FUNCTIONS

# VARIABLES:
# /VARIABLES

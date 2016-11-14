####################################################################
# Type: MODULE                                                     #
#                                                                  #
# Description: [description]                                       #
####################################################################

# IMPORTS:
from ROOT import TFile, TChain, SetOwnership
# /IMPORTS

# VARIABLES:
# /VARIABLES

# CLASSES:
class rfile:
	def __init__(self, path):
		self.path = path
		self.tf = TFile(path)
	
	def ls(self):		# Gets a list of the top directory.
		tlist = self.tf.GetListOfKeys()
		return [item.GetName() for item in tlist]
	
	def get_tobjects(self, kind=""):
		names = self.ls()
		tobjects = [self.tf.Get(name) for name in names]
		if not kind or kind.lower() == "all":
			return tobjects
		else:
			return [tobject for tobject in tobjects if tobject.ClassName().lower() == kind.lower()]
	
	def get_ttrees(self):		# So far, this only gets them from the top directory (160419).
		return self.get_tobjects(kind="ttree")
# /CLASSES

# FUNCTIONS:
def list_tfile(tfile):
	tlist = tfile.GetListOfKeys()
	return [item.GetName() for item in tlist]

def get_tobjects(f, kind=""):
	tf_in = TFile.Open(f)
	SetOwnership(tf_in, 0)
	names = list_tfile(tf_in)
	tobjects = [tf_in.Get(name) for name in names]
	if not kind or kind.lower() == "all":
		return tobjects
	else:
		return [tobject for tobject in tobjects if tobject.ClassName().lower() == kind.lower()]

def get_ttrees(f):
	return get_tobjects(f, kind="ttree")


def listdir(tf):
	if tf:
		tkeys = tf.GetListOfKeys()
		return [tkey.GetName() for tkey in tkeys]
	else:
		return False


def make_tc(files, name="tc"):
	tc = TChain(name)
	for f in files:
		tc.Add(f)
	SetOwnership(tc, 0)
	return tc


def tc_nevents(tc):
	nevents = []
	bad = []
	for i, tce in enumerate(tc.GetListOfFiles()):
		f = tce.GetTitle()                 # This is the file name (GetName() returns the ttree name)
		tf = TFile.Open(f)
		try:
			tt = tf.Get(tce.GetName())
		except:
			bad.append(i)
			nevents.append(0)
			print "WARNING: Something is wrong with File {} in the TChain.".format(i)
		else:
			nevents.append(tt.GetEntries())
	if bad:
		print "WARNING (root.tc_nevents): Some of the files in the TChain are bad:"
		print bad
	return nevents
# /FUNCTIONS

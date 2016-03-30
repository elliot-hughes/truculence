####################################################################
# Type: MODULE                                                     #
#                                                                  #
# Description: [description]                                       #
####################################################################

# IMPORTS:
from ROOT import TFile
# /IMPORTS

# VARIABLES:
# /VARIABLES

# CLASSES:
# /CLASSES

# FUNCTIONS:
def listdir(tf):
	if tf:
		tkeys = tf.GetListOfKeys()
		return [tkey.GetName() for tkey in tkeys]
	else:
		return False

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
	print bad
	return nevents
# /FUNCTIONS

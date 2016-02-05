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
	for tce in tc.GetListOfFiles():
		f = tce.GetTitle()                 # This is the file name (GetName() returns the ttree name)
		tf = TFile.Open(f)
		tt = tf.Get(tce.GetName())
		nevents.append(tt.GetEntries())
	return nevents
# /FUNCTIONS

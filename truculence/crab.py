####################################################################
# Type: MODULE                                                     #
#                                                                  #
# Description: [description]                                       #
####################################################################

# IMPORTS:
from decortication import eos
# /IMPORTS

# VARIABLES:
# /VARIABLES

# CLASSES:
# /CLASSES

# FUNCTIONS:
def find_files(d):
	results = {}
	dates = eos.listdir(d)
	results["files"] = []
	results["dir"] = ""
	if dates:
		path = d + "/" + dates[-1]
		results["dir"] = path
		contents = eos.listdir(path)
		results["files"].extend([path + "/" + f for f in contents if ".root" in f])
		subdirs = [d for d in contents if ".root" not in d]		# "0000", "0001", etc.
		if subdirs:
			for subdir in subdirs:
				path_dir = path + "/" + subdir
				results["files"].extend([path_dir + "/" + f for f in eos.listdir(path_dir) if ".root" in f])
#	else:
#		print "ERROR (crab.find_files): Nonexistent {}".format(d)
	return results
	
# /FUNCTIONS

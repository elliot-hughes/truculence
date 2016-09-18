####################################################################
# Type: SCRIPT                                                     #
#                                                                  #
# Description: Print information about an LHE file.                #
# Usage: python lhe_info.py path_to_lhe_file                       #
####################################################################

# IMPORTS:
import sys, os
from truculence import lhe
import xml.etree.ElementTree as ET
# /IMPORTS

# CLASSES:
# /CLASSES

# VARIABLES:
# /VARIABLES

# FUNCTIONS:
def main():
	f = sys.argv[1]
	if os.path.exists(f):
#		pieces = lhe.parse(f)
#		print pieces
		
		tree = ET.parse(f)
		nevents = len(tree.findall("event"))
		fname = f.split("/")[-1]
		print "Information for {}:".format(fname)
		print "\tEvents: {}".format(nevents)
		
		return True
	else:
		print "ERROR: There's no file called '{}'".format(f)
		return False
# /FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# /MAIN


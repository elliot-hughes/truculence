####################################################################
# Type: SCRIPT                                                     #
#                                                                  #
# Description: [description]                                       #
####################################################################

# IMPORTS:
import sys, os
from truculence import lhe
# /IMPORTS

# CLASSES:
# /CLASSES

# VARIABLES:
# /VARIABLES

# FUNCTIONS:
def main():
	f = sys.argv[1]
	if os.path.exists(f):
		pieces = lhe.parse(f)
		print pieces
		return True
	else:
		print "ERROR: There's no file called '{}'".format(f)
		return False
# /FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# /MAIN


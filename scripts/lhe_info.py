####################################################################
# Type: SCRIPT                                                     #
#                                                                  #
# Description: Print information about an LHE file.                #
# Usage: python lhe_info.py path_to_lhe_file                       #
####################################################################

# IMPORTS:
import sys, os, re
from truculence import lhe
import xml.etree.ElementTree as ET
# /IMPORTS

# CLASSES:
# /CLASSES

# VARIABLES:
# /VARIABLES

# FUNCTIONS:
def parse_card_run(header):
	info = {}
	for line in header.find("MGRunCard").text.split("\n"):
		match = re.search("^\s*([\w+-.]+)\s+=\s+(\w+)", line)
		if match:
			info[match.group(2)] = match.group(1).split()
	return info

#def get_iseed(header):
#	card_run = header.find("MGRunCard")
#	match = re.search("\s*(\d+)\s+=\s+iseed", card_run.text)
#	if match:
#		return int(match.group(1))
#	else:
#		return 0

def main():
	f = sys.argv[1]
	if os.path.exists(f):
#		pieces = lhe.parse(f)
#		print pieces
		
		tree = ET.parse(f)
		nevents = len(tree.findall("event"))
		header = tree.find("header")
		info_card_run = parse_card_run(header)
#		print info_card_run
		iseed = int(info_card_run["iseed"][0])
		nevents_exp = int(info_card_run["nevents"][0])
		ihtmin = float(info_card_run["ihtmin"][0])
		ptheavy = float(info_card_run["ptheavy"][0])

		# Print information:
		fname = f.split("/")[-1]
		print "Information for {}:".format(fname)
		print "\tEvents: {}{}".format(nevents, " ({} expected!)".format(nevents_exp) if nevents_exp != nevents else "")
		print "\tiseed: {}".format(iseed)
		print "\tihtmin: {} GeV".format(ihtmin)
		print "\tptheavy: {} GeV".format(ptheavy)		

		return True
	else:
		print "ERROR: There's no file called '{}'".format(f)
		return False
# /FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# /MAIN


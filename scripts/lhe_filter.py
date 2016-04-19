# IMPORTS:
import sys
import re
from truculence import lhe
# :IMPORTS

# VARIABLES:
cut_pt = 200
#lhe_in = "/users/h2/tote/madgraph/sqtojjjj_trial1/Events/sqto4j_200_01/unweighted_events.lhe"
lhe_in = "/users/h2/tote/lhe/sq150to4j.lhe"
lhe_out = "/users/h2/tote/lhe/sq150to4j_cutpt{}.lhe".format(cut_pt)
# :VARIABLES

# CLASSES:
# :CLASSES

# FUNCTIONS:
def main():
	n_inits = 0
	n_events = 0
	n_events_accepted = 0

	tags = ["event", "init"]
	controls = {}
	raws = {}
	for tag in tags:
		controls[tag] = {}
		controls[tag]["begin"] = False
		controls[tag]["end"] = False
		controls[tag]["inside"] = False
		raws[tag] = ""

	# Blank/create the output file:
	with open(lhe_out, "w") as file_out:
		file_out.write("<LesHouchesEvents version=\"1.0\">\n")

	# Start looping over the input file:
	with open(lhe_in, "r") as file_in:
		for line in file_in:                 # This method is good on memory, acting as an iterator.
	#		print line
			for tag, control in controls.iteritems():     # Tag is "event" or "init".
				if "<{}>".format(tag) in line:
					control["begin"] = True
					control["inside"] = True
				else:
					control["begin"] = False
				if "</{}>".format(tag) in line:
					control["end"] = True
					control["inside"] = False
				else:
					control["end"] = False
		
				if control["begin"]:
					raws[tag] = line
				elif control["inside"] or control["end"]:
					raws[tag] += line
		
			if controls["init"]["end"]:
				init = lhe.init(raws["init"])
				if init:
					if n_inits == 0:
						n_inits += 1
						with open(lhe_out, "a") as file_out:
							file_out.write(init.raw + "\n")
					else:
						print "ERROR: There is more than one \"init\" in the LHE file."
						sys.exit()
		
			if controls["event"]["end"]:
				event = lhe.event(raws["event"])
				if event:
					n_events += 1
					pts = [squark["pt"] for squark in event.squarks]
					if min(pts) >= cut_pt:
						n_events_accepted += 1
						with open(lhe_out, "a") as file_out:
							file_out.write(event.raw + "\n")

	with open(lhe_out, "a") as file_out:
		file_out.write("</LesHouchesEvents>")

	print n_inits, n_events, n_events_accepted, float(n_events_accepted)/n_events*100
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN

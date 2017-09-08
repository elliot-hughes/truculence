# IMPORTS:
import os, re
import xml.etree.ElementTree as ET
#from xml.etree.ElementTree import Element
import utilities
# :IMPORTS


# VARIABLES:
tags = {
	"LesHouchesEvents": {
		"event": {},
		"init": {},
		"header": {
			"MGVersion": {},
			"MG5ProcCard": {},
			"MGProcCard": {},
			"MGRunCard": {},
			"slha": {},
			"MCGenerationInfo": {},
		},
	},
}
tags_full = utilities.flatten(tags).keys()
tags_all = [tag_full.split("_")[-1] for tag_full in tags_full]
# :VARIABLES


# CLASSES:
class header:
	def __init__(self, lhe_string):
		match = re.search("(<header>[\s\S]*</header>)", lhe_string)
#		print lhe_string
#		print match
		if match:
			self.raw = match.group(1)
		else:
			self.raw = False
	
	def __nonzero__(self):
		return bool(self.raw)

class init:
	def __init__(self, lhe_string):
		match = re.search("(<init>[\s\S]*</init>)", lhe_string)
#		print lhe_string
#		print match
		if match:
			self.raw = match.group(1)
		else:
			self.raw = False
	
	def __nonzero__(self):
		return bool(self.raw)


class event:
	def __init__(self, event):
		if isinstance(event, ET.Element):
			self.raw = event.text
		elif isinstance(event, str):
			match = re.search("(<event>[\s\S]*</event>)", event)
			if match:
				self.raw = match.group(1)
		else:
			print "ERROR (lhe.event): I don't understand the type of the input."
		
		if self.raw:
			lines = [line for line in self.raw.split("\n") if not re.search("^#", line.strip()) and not line.strip() in ["<event>", "</event>"] and line.strip()]
			self.meta_raw = lines[1]
			particles_raw = lines[2:]
			self.particles = []
			for particle_raw in particles_raw:
				pieces = particle_raw.split()
#				print particle_raw
#				print pieces
				particle = {}
				particle["pdgid"] = int(pieces[0])
				particle["p"] = (float(pieces[9]), float(pieces[6]), float(pieces[7]), float(pieces[8]))
				particle["e"] = particle["p"][0]
				particle["px"] = particle["p"][1]
				particle["py"] = particle["p"][2]
				particle["pz"] = particle["p"][3]
				particle["pt"] = (particle["px"]**2 + particle["py"]**2)**(0.5)
				particle["m"] = float(pieces[10])
				self.particles.append(particle)
			self.quarks = [particle for particle in self.particles if abs(particle["pdgid"]) in range(-6, 0) + range(1, 7)]
			self.squarks = [particle for particle in self.particles if abs(particle["pdgid"]) in range(1000001, 1000007)]
			self.gluinos = [particle for particle in self.particles if abs(particle["pdgid"]) == 1000021]
			self.higgsinos = [particle for particle in self.particles if abs(particle["pdgid"]) == 1000022]  
			self.ht = sum([quark["pt"] for quark in self.quarks])
		else:
			self.raw = False
	
	def __nonzero__(self):
		return bool(self.raw)
# :CLASSES






# FUNCTIONS:
def get_info(f, v=True):
	if v: print "[..] Getting info for {}".format(f)
	if os.path.exists(f):
		info = {}
		tree = ET.parse(f)
		info["nevents"] = len(tree.findall("event"))
		return info
	else:
		if v: print "[!!] File doesn't exist."
		return False


def parse(lhe_in, function=None):		# This is old. I should use "elementtree". See "get_info".
	whatever = 0
	# Set up meta information:
	pieces = {}
	controls = {}
	raws = {}
	ns = {}
	for tag_full in tags_full:
		controls[tag_full] = {}
		controls[tag_full]["start"] = False
		controls[tag_full]["end"] = False
		controls[tag_full]["open"] = False
#		raws[tag_full] = ""
		ns[tag_full] = 0
	controls_internal = {}
	for tag in tags_all:
		controls_internal[tag] = {}
		controls_internal[tag]["start"] = False
		controls_internal[tag]["end"] = False
		controls_internal[tag]["open"] = False
	tags_full_open = []

	# Start looping over the input file:
	with open(lhe_in, "r") as file_in:
		for line in file_in:                 # This method is good on memory, acting as an iterator.
			# Count tag beginnings and endings:
			complete = {}
			counts = {}
			for tag in tags_all:
				starts = line.count("<{}".format(tag))
				ends = line.count("</{}".format(tag))
				if starts or ends:
					counts[tag] = (starts, ends)
				
				# This is an LHE-specific kludge:
				assert(starts < 2)
				assert(ends < 2)
				# :
			
			# Deal with openings:
			for tag, start_end in counts.iteritems():
				starts = start_end[0]
				
				if starts:
					if tags_full_open:
						tags_full_open += ["{}_{}".format(tag_full, tag) for tag_full in tags_full_open]
					else:
						tags_full_open.append(tag)
			## Record open raw info:
			for tag_full in tags_full_open:
				if tag_full.split("_") > 1:
					if tag_full not in raws:
						raws[tag_full] = line
					else:
						raws[tag_full] += line
			
			# Deal with endings:
			tags_full_closed = []
			for tag, start_end in counts.iteritems():
				ends = start_end[1]
				
				if ends:
					for tag_full in tags_full_open:
						tag_open = tag_full.split("_")[-1]
						if tag == tag_open:
							if tag_full in pieces:
								pieces[tag_full] += 1
							else:
								pieces[tag_full] = 1
							# Form objects:
							if tag == "event":
								complete[tag] = event(raws[tag_full])
							elif tag == "init":
								complete[tag] = init(raws[tag_full])
							elif tag == "header":
								complete[tag] = header(raws[tag_full])
							tags_full_closed.append(tag_full)
			for tag_full in tags_full_closed:
				tags_full_open.remove(tag_full)
				del raws[tag_full]
			
			## Inside loop function:
			if function:
				function(complete)
	return pieces

def get_nevents(f):
	pieces = parse(f)
#	print pieces
	return pieces["event"]
# :FUNCTIONS





# OLD FUNCTIONS:
#def get_info(f=""):
##	labels = ["event", "init", "header", "MGVersion", "MG5ProcCard", "MGProcCard", "MGRunCard", "slha", "MGGenerationInfo", "other"]
#	n = {}
#	with open(f) as file_in:		# This won't load the entire file into memory, which is important since LHE files can be enormous.
#		for line in file_in:
#			match_start = re.search("<(\w+)\s?.*>", line)
#			match_end = re.search("</(\w+)\s?.*>", line)
#			if match_start:
#				label = match_start.group(1)
##				if label != "event":
##					print label
#				if label not in n:
#					n[label] = [0]*2
#				n[label][0] += 1
#			elif match_end:
#				label = match_end.group(1)
#				n[label][1] += 1
#	for label, count in n.iteritems():
#		print "{0}: {1}".format(label, count)

def simplify(f="", o="simple.lhe"):		# This function removes metadata from an LHE file.
	# Delete the output file if it already exists:
	if os.path.exists(o):
		os.remove(o)
	
	# Simplify the input file:
	n = 0
	z_inside = False
	with open(o, "a") as file_out:
		with open(f) as file_in:		# This won't load the entire file into memory, which is important since LHE files can be enormous.
			for line in file_in:
				n += 1
#				if n < 50:
#					print z_inside
				if "<header>" in line:
					z_inside = True
				elif "</header>" in line:
					z_inside = False
				elif not z_inside:
					file_out.write(line)

def change_process_code(f="", o="", code=9999):		# This is extremely experimental, since I have no idea what this number means nor where else it's repeated.
	if f:
		if not o:
			o = f[:-4] + "_modified.lhe"
		if os.path.exists(o):
			os.remove(o)
		
		with open(o, "a") as file_out:
			with open(f) as file_in:		# This won't load the entire file into memory, which is important since LHE files can be enormous.
				nevent = 0
				z_inside = False
				for line in file_in:
					if "<event>" in line:
						z_inside = True
						nevent += 1
						if nevent % 20000 == 0:
							print nevent
					elif "</event>" in line:
						z_inside = False
					if z_inside and len(line.strip().split()) == 6:
						line_modified = line.strip().split()
						line_modified[1] = str(code)
						file_out.write(" " + "  ".join(line_modified) + "\n")
					else:
						file_out.write(line)

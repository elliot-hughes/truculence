# IMPORTS:
import os, re
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
	def __init__(self, lhe_string):
		match = re.search("(<event>[\s\S]*</event>)", lhe_string)
#		print lhe_string
#		print match
		if match:
			self.raw = match.group(1)
			lines = [line for line in self.raw.split("\n") if not re.search("^#", line.strip()) and not line.strip() in ["<event>", "</event>"]]
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
			self.squarks = [particle for particle in self.particles if abs(particle["pdgid"]) in range(1000001, 1000007)]
		else:
			self.raw = False
	
	def __nonzero__(self):
		return bool(self.raw)
# :CLASSES












# OLD FUNCTIONS:
def get_info(f=""):
#	labels = ["event", "init", "header", "MGVersion", "MG5ProcCard", "MGProcCard", "MGRunCard", "slha", "MGGenerationInfo", "other"]
	n = {}
	with open(f) as file_in:		# This won't load the entire file into memory, which is important since LHE files can be enormous.
		for line in file_in:
			match_start = re.search("<(\w+)\s?.*>", line)
			match_end = re.search("</(\w+)\s?.*>", line)
			if match_start:
				label = match_start.group(1)
#				if label != "event":
#					print label
				if label not in n:
					n[label] = [0]*2
				n[label][0] += 1
			elif match_end:
				label = match_end.group(1)
				n[label][1] += 1
	for label, count in n.iteritems():
		print "{0}: {1}".format(label, count)

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

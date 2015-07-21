from re import search
import os

def get_info(f=""):
#	labels = ["event", "init", "header", "MGVersion", "MG5ProcCard", "MGProcCard", "MGRunCard", "slha", "MGGenerationInfo", "other"]
	n = {}
	with open(f) as file_in:		# This won't load the entire file into memory, which is important since LHE files can be enormous.
		for line in file_in:
			match_start = search("<(\w+)\s?.*>", line)
			match_end = search("</(\w+)\s?.*>", line)
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

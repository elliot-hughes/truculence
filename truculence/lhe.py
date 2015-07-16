def parse_lhe(f="", verbose=False):
	if (verbose): print "> Parsing the LHE file at {0}".format(f)
	
	# Open and read the LHE file:
	raw = open(f, "r").read().split("<event>")
	meta = raw[0]
	raw = raw[1:]		# The first element is the metadata, so I ignore it.

	if (verbose): print "This LHE file contains {} events.".format(len(raw_in)-1)
	count = -1
	n = 0
	save = 0
	for event in raw:
		count += 1
	#	if count < 4:
	#		print "=========="
	#		print event.strip()
	#		print "=========="
		lines = event.strip().split("\n")
#		particles = []
#		meta = []
#		protons = []
#		for line in lines:
#	#		print "> {0}".format(len(line.split()))
#			particles.append(line) if len(line.split()) == 13 else meta.append(line)		# Get the particle lines from the event.
#		if count == 10:
#	#		print particles
#			for particle in particles:
#				print particle
#			print meta
#		pt_squarks = []
#		for particle in particles:
#			variables = particle.split()
#			pdgid = int(variables[0])
#			mass = float(variables[10])
#			p = []
#			p.append(float(variables[6]))
#			p.append(float(variables[7]))
#			p.append(float(variables[8]))
#			e = float(variables[9])
#			pt = (p[0]**2 + p[1]**2)**(0.5)
#			if count == 3:
#				print "> {0}".format(pt)
#			if (abs(pdgid) == 1000005):
#				pt_squarks.append(pt)
#				if (pt >= cut_pt):
#					save = 1		# Both squarks should have the same pT...
#		h1_min.Fill(min(pt_squarks))
#		h1_max.Fill(max(pt_squarks))
#		if save:
#			n += 1
#			raw_out += "<event>" + thing
#			save = 0

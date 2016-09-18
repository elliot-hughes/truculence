####################################################################
# Type: MODULE                                                     #
#                                                                  #
# Description: [description]                                       #
####################################################################

# IMPORTS:
import json
from subprocess import Popen, PIPE
# /IMPORTS

# VARIABLES:
# /VARIABLES

# CLASSES:
# /CLASSES

# FUNCTIONS:
def get_datasets(name_query, instance="global"):
	raw_output = Popen(['das_client --query "dataset={} instance=prod/{}" --format=json --limit=0'.format(name_query, instance)], shell=True, stdout=PIPE, stderr=PIPE).communicate()
	if not raw_output[1]:		# No error
		info = json.loads(raw_output[0])
		return [ds["dataset"][0]["name"] for ds in info["data"]]
	else:
		print "ERROR (das.get_info): There was a problem with the DAS query:"
		print raw_output[1]
		return []

def get_info(name, instance="global"):
# Get information about a dataset named "name".
#	print name, instance
	results = {}
	raw_output = Popen(['das_client --query "file dataset={} instance=prod/{}" --format=json --limit=0'.format(name, instance)], shell=True, stdout=PIPE, stderr=PIPE).communicate()
#	print raw_output
	if not raw_output[1]:		# No error
		info = json.loads(raw_output[0])
		
		results["raw"] = raw_output[0]
		results["files"] = []
		results["ns"] = []
		for i, f in enumerate(info["data"]):
			nevents = 0
			filename = ""
			for entry in f["file"]:
				if "nevents" in entry:
					results["ns"].append(entry["nevents"])
					results["files"].append(entry["name"])
					break
	else:
		print "ERROR (das.get_info): There was a problem with the DAS query:"
		print raw_output[1]
	return results

def get_files(name, n=-1, instance="global"):
	info = get_info(name, instance=instance)
	if info:
		if n == -1:
			return info["files"]
		else:
			files = []
			total = n
			for i, n_file in enumerate(info["ns"]):
				files.append(info["files"][i])
				total -= n_file
				if total <= 0:
					break
			return files
	return []
# /FUNCTIONS

# IMPORTS:
import os, requests, json
from collections import OrderedDict
from subprocess import Popen, PIPE
from re import search
# :IMPORTS

# VARIABLES:
# :VARIABLES

# FUNCTIONS:
def get_version(parsed=True):
	# Returns the active CMSSW version. parsed == True: "xxyyzzpp", parsed == False: "CMSSW_x_y_z_patchp
	cmssw_raw = Popen(['echo $CMSSW_VERSION'], shell = True, stdout = PIPE, stderr = PIPE).communicate()[0].strip()
	if not cmssw_raw:
		return False
	if parsed:
		return ''.join([(i.replace("patch", "")).zfill(2) for i in cmssw_raw.split("_")[1:]])
	return cmssw_raw


def convert_lumi_json(f):
	# Converts a lumi mask JSON to a list for CMSSW configuration files.
	j = {}
	if "https://" in f or "http://" in f:
		r = requests.get(f)
		if not r:
			return []
		j = json.loads(r.text, object_pairs_hook=OrderedDict)
	else:
		with open(f) as fin:
			j = json.loads(fin.read(), object_pairs_hook=OrderedDict)
	if not j:
		return []
	return ["{run}:{lumi_start}-{run}:{lumi_end}".format(run=r, lumi_start=l[0], lumi_end=l[1]) for r, ls in j.items() for l in ls]
# :FUNCTIONS

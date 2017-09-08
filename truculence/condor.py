####################################################################
# Type: MODULE                                                     #
#                                                                  #
# Description: [description]                                       #
####################################################################

# IMPORTS:
import os, re
from subprocess import Popen, PIPE, check_output, check_call, STDOUT
from truculence import utilities
# /IMPORTS

# VARIABLES:
error_codes = {
	-1: "empty",
	0: "job completed successfully",
	1: "unknown",
	2: "error detected",
	3: "last two lines empty",
}
queue_codes = {
	1: "idle",
	2: "running",
}
# /VARIABLES

# CLASSES:
# /CLASSES

# FUNCTIONS:

def list_logs(indir):
	results = {}
	logs = os.listdir(indir + "/logs")
	results["log"] = [f for f in logs if ".log" in f]
	results["stdout"] = [f for f in logs if ".stdout" in f]
	results["stderr"] = [f for f in logs if ".stderr" in f]
	return results


def get_job_info(indir, v=False):
	if v: print "[..] Scanning the condor directory."
	jdls = [f for f in os.listdir(indir) if ".jdl" in f]
	njobs = len(jdls)

	log_dict = list_logs(indir)
	logs_log = log_dict["log"]
	logs_stdout = log_dict["stdout"]
	logs_stderr = log_dict["stderr"]

	print "[OK] Total jobs: {}".format(njobs)
	good = True
	if len(log_dict["log"]) != njobs:
		if v: print "[!!] There are only {} .log logs".format(len(logs_log))
		good = False
	if len(log_dict["stdout"]) != njobs:
		if v: print "[!!] There are only {} .stdout logs".format(len(logs_stdout))
		good = False
	if len(log_dict["stderr"]) != njobs:
		if v: print "[!!] There are only {} .stderr logs".format(len(logs_stderr))
		good = False
	if good and v: print "[OK] All logs accounted for."
	if good: return njobs
	else: return False


def analyze_log_stderr(path):
	n_lines = utilities.wcl(path)
	if n_lines == 0: return {"code": -1, "n": n_lines}
	last = check_output(["tail", "-n1", path]).strip()
	if not last: last = check_output(["tail", "-n1", path]).strip()
	
	if not last: return {"code": 3, "n": n_lines}
	if "[100%][==================================================]" in last: return {"code": 0, "n": n_lines}
	if "error" in last.lower() or "End Fatal Exception" in last or "system" in last.lower() or "%MSG" in last: return {"code": 2, "n": n_lines}
	else: return {"code": 1, "n": n_lines}

def check_stderr_logs(indir, logs_stderr=None):
	if not logs_stderr: logs_stderr = list_logs(indir)["stderr"]
	
	results = {}
	for l in logs_stderr:
		path = indir + "/logs/" + l
		match = re.search("[a-zA-Z0-9_]+_job(\d+)_[a-zA-Z0-9_]+.stderr", l)
		if not match: match = re.search("[a-zA-Z0-9_]+_(\d+).stderr", l)
		njob = int(match.group(1))
		
		stderr_analysis = analyze_log_stderr(path)
		code = stderr_analysis["code"]
		if code not in results: results[code] = []
		results[code].append(njob)
	
	return results


def parse_job_name(name):
	name = name.split("/")[-1]
	result = {}
	info, result["ext"] = name.split(".")
	name_pieces = info.split("_")[1:]
	result["n"] = int(name_pieces[-1])
	result["prefix"] = "_".join(name_pieces[:-1])
	return result

def check_queue(prefix, user="tote"):
	results = {}
	
	raw_output = Popen(['condor_q -submitter {} -format "%s " jobstatus -format "%s\\n" cmd'.format(user)], shell=True, stdout=PIPE, stderr=PIPE).communicate()
	if raw_output[1]: return False
	lines = raw_output[0].split("\n")
	for line in lines:
		if not line: continue
		pieces = line.split()
		status = int(pieces[0])
		job_info = parse_job_name(pieces[1])
		if prefix == job_info["prefix"]:
			if status not in results: results[status] = []
			results[status].append(job_info["n"])
	return results

def clean():
	try:
		check_call("rm -rf $CMSSW_BASE/python/decortication $CMSSW_BASE/python/truculence $CMSSW_BASE/python/resources", shell=True)
	except Exception as ex:
		print ex
		return False
	return True

def unclean():
	try:
		check_call("cp -r $HOME/{decortication/decortication,decortication/resources,truculence/truculence} $CMSSW_BASE/python", shell=True)
	except Exception as ex:
		print ex
		return False
	return True

def tar_cmssw(indir="."):
#	if not clean(): return False
#	if not unclean(): return False
	try:
		check_call("tar --exclude-caches-all -czf " + indir + "/${CMSSW_VERSION}.tar.gz -C ${CMSSW_BASE}/.. ${CMSSW_VERSION}", shell=True)
	except Exception as ex:
		print ex
		return False
#	if not clean(): return False
	return True


def submit_jobs(indir, n_jobs, prefix):
	os.chdir(indir)
	jlist = ["{}_{}.jdl".format(prefix, n) for n in n_jobs]
	FNULL = open(os.devnull, 'w')
	for j in jlist:
		Popen(["condor_submit", j], stdout=FNULL, stderr=STDOUT)

def submit_jobs_by_name(indir, job_files):
	os.chdir(indir)
	jlist = job_files
	FNULL = open(os.devnull, 'w')
	for j in jlist:
		Popen(["condor_submit", j], stdout=FNULL, stderr=STDOUT)
# /FUNCTIONS

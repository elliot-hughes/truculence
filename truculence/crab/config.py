####################################################################
# Type: MODULE                                                     #
#                                                                  #
# Description: [description]                                       #
####################################################################

# IMPORTS:
from truculence import analysis
# /IMPORTS

# VARIABLES:
template_signal = '''from CRABClient.UserUtilities import config
configure = config()

# Variables
process = "%%PROCESS%%"
m = %%MASS%%
n = 10000		# Number of events per job.
# /Variables

configure.General.requestName = '{0}_{1}_fatjets'.format(process, m)
configure.General.workArea = 'crab_projects'
configure.JobType.pluginName = 'Analysis'
configure.JobType.psetName = '%%CMSSWCONFIG%%'
configure.JobType.pyCfgParams = [
	'crab=True',
	'dataset={0}'.format(process),
	'm={0}'.format(m),
	'cmssw=%%CMSSW%%',
]

configure.Data.inputDataset = '%%DATASET%%'
configure.Data.inputDBS = '%%INSTANCE%%'

configure.Data.splitting = 'EventAwareLumiBased'
configure.Data.unitsPerJob = n
configure.Data.totalUnits = 200000
configure.Data.outLFNDirBase = '/store/user/elhughes' # or '/store/group/<groupname>/<subdir>'
configure.Data.publication = True
configure.Data.outputDatasetTag = '{0}_{1}_fatjets'.format(process, m)

configure.JobType.maxMemoryMB = 5000

configure.Site.storageSite = 'T3_US_FNALLPC'
'''

template_pythia = '''from CRABClient.UserUtilities import config
configure = config()

# Variables
process = "%%PROCESS%%"
pt_low = %%PTLOW%%
pt_high = %%PTHIGH%%
n = 10000		# Number of events per job.
# /Variables

configure.General.requestName = '{0}_pt{1}to{2}_fatjets'.format(process, pt_low, pt_high)
configure.General.workArea = 'crab_projects'
configure.JobType.pluginName = 'Analysis'
configure.JobType.psetName = '%%CMSSWCONFIG%%'
configure.JobType.pyCfgParams = [
	'crab=True',
	'dataset={0}'.format(process),
	'method=pt{0}to{1}'.format(pt_low, pt_high),
	'cmssw=%%CMSSW%%',
]

configure.Data.inputDataset = '%%DATASET%%'
configure.Data.inputDBS = '%%INSTANCE%%'

configure.Data.splitting = 'EventAwareLumiBased'
configure.Data.unitsPerJob = n
configure.Data.totalUnits = 200000
configure.Data.outLFNDirBase = '/store/user/elhughes' # or '/store/group/<groupname>/<subdir>'
configure.Data.publication = True
configure.Data.outputDatasetTag = '{0}_pt{1}to{2}_fatjets'.format(process, pt_low, pt_high)

configure.JobType.maxMemoryMB = 5000

configure.Site.storageSite = 'T3_US_FNALLPC'
'''

template_madgraph = '''from CRABClient.UserUtilities import config
configure = config()

# Variables
process = "%%PROCESS%%"
ht_low = %%PTLOW%%
ht_high = %%PTHIGH%%
n = 10000		# Number of events per job.
# /Variables

configure.General.requestName = '{0}_ht{1}to{2}_fatjets'.format(process, ht_low, ht_high)
configure.General.workArea = 'crab_projects'
configure.JobType.pluginName = 'Analysis'
configure.JobType.psetName = '%%CMSSWCONFIG%%'
configure.JobType.pyCfgParams = [
	'crab=True',
	'dataset={0}'.format(process),
	'method=ht{0}to{1}'.format(ht_low, ht_high),
	'cmssw=%%CMSSW%%',
]

configure.Data.inputDataset = '%%DATASET%%'
configure.Data.inputDBS = '%%INSTANCE%%'

configure.Data.splitting = 'EventAwareLumiBased'
configure.Data.unitsPerJob = n
configure.Data.totalUnits = %%UNITS%%
configure.Data.outLFNDirBase = '/store/user/elhughes' # or '/store/group/<groupname>/<subdir>'
configure.Data.publication = True
configure.Data.outputDatasetTag = '{0}_ht{1}to{2}_fatjets'.format(process, ht_low, ht_high)

configure.JobType.maxMemoryMB = 5000

configure.Site.storageSite = 'T3_US_FNALLPC'
'''
# /VARIABLES

# CLASSES:
# /CLASSES

# FUNCTIONS:
def get_config(dataset=None, cmssw_config="fatjetproducer_cfg.py", units=200000):
	if dataset.process in ["sqtojj", "sqtojjjj"]:
		instance = "phys03"
		return template_signal.replace("%%PROCESS%%", dataset.process).replace("%%DATASET%%", dataset.name_full).replace("%%MASS%%", str(dataset.m)).replace("%%CMSSW%%", analysis.get_cmssw()).replace("%%INSTANCE%%", instance).replace("%%CMSSWCONFIG%%", cmssw_config).replace("%%UNITS%%", units)
	elif dataset.process in ["qcd"]:
		instance = "global"
		return template_pythia.replace("%%PROCESS%%", dataset.process).replace("%%DATASET%%", dataset.name_full).replace("%%PTLOW%%", str(dataset.pts[0])).replace("%%PTHIGH%%", str(dataset.pts[1])).replace("%%CMSSW%%", analysis.get_cmssw()).replace("%%INSTANCE%%", instance).replace("%%CMSSWCONFIG%%", cmssw_config).replace("%%UNITS%%", units)
	elif dataset.process in ["qcdmg"]:
		instance = "global"
		return template_madgraph.replace("%%PROCESS%%", dataset.process).replace("%%DATASET%%", dataset.name_full).replace("%%PTLOW%%", str(dataset.hts[0])).replace("%%PTHIGH%%", str(dataset.hts[1])).replace("%%CMSSW%%", analysis.get_cmssw()).replace("%%INSTANCE%%", instance).replace("%%CMSSWCONFIG%%", cmssw_config).replace("%%UNITS%%", units)
# /FUNCTIONS

qcd_info = {
	"spring15": {
		"QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8": [19204300.0],
		"QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8": [2762530.0],
		"QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8": [471100],
		"QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8": [117276],
		"QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8": [7823],
		"QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8": [648.2],
#		"QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8": [186.9],
		"QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8": [32.293],
		"QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8": [9.4183],
		"QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8": [0.84265],
	},
	"phys14": {
		"QCD_Pt-50to80_Tune4C_13TeV_pythia8": [22110000.0],
		"QCD_Pt-80to120_Tune4C_13TeV_pythia8": [3116000.0],
		"QCD_Pt-120to170_Tune4C_13TeV_pythia8": [486200.0],
		"QCD_Pt-170to300_Tune4C_13TeV_pythia8": [120300.0],
		"QCD_Pt-300to470_Tune4C_13TeV_pythia8": [7475.0],
		"QCD_Pt-470to600_Tune4C_13TeV_pythia8": [587.1],
		"QCD_Pt-600to800_Tune4C_13TeV_pythia8": [167.0],
		"QCD_Pt-800to1000_Tune4C_13TeV_pythia8": [28.25],
		"QCD_Pt-1000to1400_Tune4C_13TeV_pythia8": [8.195],
		"QCD_Pt-1400to1800_Tune4C_13TeV_pythia8": [0.7346],
	},
}

samples = {j: k for key, value in qcd_info.iteritems() for j, k in value.iteritems()}

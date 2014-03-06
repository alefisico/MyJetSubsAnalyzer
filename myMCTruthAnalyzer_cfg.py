import FWCore.ParameterSet.Config as cms 
import os

process = cms.Process('myprocess')
process.load('FWCore.MessageService.MessageLogger_cfi')

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'START53_V27::All'

process.TFileService=cms.Service("TFileService",fileName=cms.string('/cms/gomez/Stops/st_jj/MCTruth/rootFiles/stopUDD312_50_MCTruth_plots.root'))

##-------------------- Define the source  ----------------------------
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

########## search for input files
#list = os.popen('ls -1 /cms/gomez/Stops/AOD/st2_h_bb_st1_jj_250_100_AOD/*.root').read().splitlines()
#list = os.popen('ls -1 /cms/dfeld/dkolch/2013/STOP_100k_AODSIM/100k_stopUDD312_100/*.root').read().splitlines()
list = os.popen('ls -1 /cms/gomez/Substructure/Generation/Simulation/CMSSW_5_3_2_patch4/src/mySimulations/stop_UDD312_50/aodsim/*.root').read().splitlines()
outputList = [i if i.startswith('file') else 'file:' + i for i in list]
process.source = cms.Source("PoolSource",
fileNames = cms.untracked.vstring( outputList ) 
)

#############   Format MessageLogger #################
process.MessageLogger.cerr.FwkReport.reportEvery = 1000


##-------------------- User analyzer  --------------------------------
#### AK4 Jets
process.MCTruthAna = cms.EDAnalyzer('MCTruthAnalyzer',
		src = cms.string('genParticles'),
)



process.p = cms.Path( process.MCTruthAna )

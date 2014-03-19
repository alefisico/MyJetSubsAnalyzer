import FWCore.ParameterSet.Config as cms 
import os, sys, time

######### input parameters
numJob = int(sys.argv[2])
Job = int(sys.argv[3])
inputDir = sys.argv[4]
outputDir = sys.argv[5]
mass = sys.argv[6]

###### Trick for add date or month to plots
dateKey   = time.strftime("%y%m%d%H%M")
monthKey   = time.strftime("%y%m%d")

process = cms.Process('myprocess')
process.load('FWCore.MessageService.MessageLogger_cfi')

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'START53_V27::All'

if not ( os.path.exists( outputDir + monthKey ) ): os.makedirs( outputDir + monthKey )
process.TFileService=cms.Service("TFileService",fileName=cms.string( outputDir+ monthKey + '/stopUDD312_' + mass +'_'+str(Job)+'_tree.root'))

##-------------------- Define the source  ----------------------------
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

########## search for input files
list = os.popen('ls -1v '+inputDir+'*.root').read().splitlines()
outputList = [i if i.startswith('file') else 'file:' + i for i in list]

###### Trick to divide num of files 
filesPerJob = round(len(outputList)/numJob) + 1 
iniList = int(filesPerJob*Job)
finList = int(filesPerJob*(Job+1))
print outputList[iniList:finList]
#######################################################

process.source = cms.Source("PoolSource",
		fileNames = cms.untracked.vstring( outputList[iniList:finList] ),
)

#############   Format MessageLogger #################
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

########################### Loading PATtuplizers
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ak4jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ak5jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ak7jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ak1p1jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ca4jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ca8jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ca1p2jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_k4jets_simple_cff')

##-------------------- User analyzer  --------------------------------
#### MCTruth Plots
#process.MCTruthAna = cms.EDAnalyzer('MCTruthTreeProducer',
#		src = cms.InputTag('genParticles'),
#		stopMass = cms.double( mass ),
#)

######################################## AK4 Jets
process.PFJet_AK4 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK4CHSwithNsub'),
		jetsPruned       = cms.InputTag('patJetsAK4CHSpruned'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring(),#'Fat','PFHT650','HT750','HT550'),
		triggerSelection = cms.vstring(
		),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)
############################################################################################

###################################################################### AK5 Jets
###### NO JET CORRECTIONS
process.PFJet_AK5_NOJEC = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK5CHSNOJEC'),
		jetsPruned       = cms.InputTag('patJetsAK5CHSpruned'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring(),#'Fat','PFHT650','HT750','HT550'),
		triggerSelection = cms.vstring(
		),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)
##### With Jet Corrections
process.PFJet_AK5 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK5CHSwithNsub'),
		jetsPruned       = cms.InputTag('patJetsAK5CHSpruned'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring(),#'Fat','PFHT650','HT750','HT550'),
		triggerSelection = cms.vstring(
		),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)
############################################################################################

################################################################################# AK7 Jets
process.PFJet_AK7 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK7CHSwithNsub'),
		jetsPruned       = cms.InputTag('patJetsAK7CHSpruned'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring(),#'Fat','PFHT650','HT750','HT550'),
		triggerSelection = cms.vstring(
		),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)
###################################################################################################

########################################################################## AK1.1
process.PFJet_AK1p1 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK1p1CHSwithNsub'),
		jetsPruned       = cms.InputTag('patJetsAK1p1CHSpruned'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		#triggerAlias     = cms.vstring('Fat','PFHT650','PFNoPUHT650','HT750','HT550'),
		triggerAlias     = cms.vstring(),#'Fat','PFHT650','HT750','HT550'),
		triggerSelection = cms.vstring(
		#'HLT_FatDiPFJetMass750_DR1p1_Deta1p5_v*',
		#'HLT_PFHT650_v*',
		#'HLT_PFNoPUHT650_v*',
		#'HLT_HT750_v*',  
		#'HLT_HT550_v*'
		),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)
###################################################################################################

####################################################################################### CA4
process.PFJet_CA4 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA4CHSwithNsub'),
		jetsPruned       = cms.InputTag('patJetsCA4CHSpruned'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring(),
		triggerSelection = cms.vstring(
		),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)
###################################################################################################

################################################################################## CA8
process.PFJet_CA8 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA8CHSwithNsub'),
		jetsPruned       = cms.InputTag('patJetsCA8CHSpruned'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring(),
		triggerSelection = cms.vstring(
		),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)
###################################################################################################

################################################################################## CA1p2
process.PFJet_CA1p2 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA1p2CHSwithNsub'),
		jetsPruned       = cms.InputTag('patJetsCA1p2CHSpruned'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring(),
		triggerSelection = cms.vstring(
		),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)
###################################################################################################

##################################################################################### KT4
process.PFJet_KT4 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT4CHSwithNsub'),
		jetsPruned       = cms.InputTag('patJetsKT4CHSpruned'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring(),
		triggerSelection = cms.vstring(
		),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)
###################################################################################################


############################################## Run Process
process.p = cms.Path( #process.MCTruthAna *
		process.ak4Jets * process.PFJet_AK4 * 
		process.ak5Jets *process.PFJet_AK5_NOJEC * process.PFJet_AK5 *   ##### Add AK5_NOJEC just to compare
		process.ak7Jets * process.PFJet_AK7 * 
		process.ak1p1Jets * process.PFJet_AK1p1 * 
		process.ca4Jets * process.PFJet_CA4 *
		process.ca8Jets * process.PFJet_CA8 *
		process.ca1p2Jets * process.PFJet_CA1p2 *
		process.kt4Jets * process.PFJet_KT4
		)

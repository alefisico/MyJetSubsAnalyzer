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
process.GlobalTag.globaltag = 'START53_V7A::All'

#if not ( os.path.exists( outputDir + monthKey ) ): os.makedirs( outputDir + monthKey )
if not ( os.path.exists( outputDir ) ): os.makedirs( outputDir )
process.TFileService=cms.Service("TFileService",fileName=cms.string( outputDir+ '/RPVSt' + mass +'tojj_8TeV_HT500_0_'+str(Job)+'_tree.root'))
#process.TFileService=cms.Service("TFileService",fileName=cms.string( 'stopUDD312_' + mass +'_'+str(Job)+'_tree_TEST.root'))

##-------------------- Define the source  ----------------------------
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

########## search for input files
list = os.popen('ls -1v '+inputDir+'*.root').read().splitlines()
#list = [x.strip() for x in open('files_RPVSt100tojj_8TeV_HT500_8.txt').readlines()]
#list = os.popen('ll -1v '+inputDir+'*.root | awk \'{if ($5 < 90000000) print $9}\'').read().splitlines()
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
#### Pat for diff jet algos
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ak4jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ak5jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ak7jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ca4jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ca8jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_kt4jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_kt8jets_simple_cff')

##-------------------- User analyzer  --------------------------------
#### MCTruth Plots
#process.MCTruthAna = cms.EDAnalyzer('MCTruthTreeProducer',
#		src = cms.InputTag('genParticles'),
#		stopMass = cms.double( mass ),
#)

listTriggerAlias = [ 'HT350', 'HT750', 'PFHT350','PFHT650' ] 
listTrigger = [ 'HLT_HT350_v*',	'HLT_HT750_v*', 'HLT_PFHT350_v*', 'HLT_PFHT650_v*'] 

######################################## AK4 Jets
######  JET CORRECTIONS
process.PFJet_AK4_JEC = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK4CHSJEC'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
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
process.PFJet_AK4 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK4CHSwithNsub'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Pruning
process.PFJet_AK4Pruned = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK4CHSprunedwithNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Trimming
process.PFJet_AK4Trimmed = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK4CHStrimmedwithNsub'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Filtering
process.PFJet_AK4FilteredN2 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK4CHSfilteredN2withNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

process.PFJet_AK4FilteredN3 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK4CHSfilteredN3withNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Mass Drop Filtering
process.PFJet_AK4MassDropFiltered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK4CHSmassDropFilteredwithNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
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
######  JET CORRECTIONS
process.PFJet_AK5_JEC = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK5CHSJEC'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
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
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Pruning
process.PFJet_AK5Pruned = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK5CHSprunedwithNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Trimming
process.PFJet_AK5Trimmed = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK5CHStrimmedwithNsub'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Filtering
process.PFJet_AK5FilteredN2 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK5CHSfilteredN2withNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

process.PFJet_AK5FilteredN3 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK5CHSfilteredN3withNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Mass Drop Filtering
process.PFJet_AK5MassDropFiltered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK5CHSmassDropFilteredwithNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
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


###################################################################### AK7 Jets
######  JET CORRECTIONS
process.PFJet_AK7_JEC = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK7CHSJEC'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
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
process.PFJet_AK7 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK7CHSwithNsub'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Pruning
process.PFJet_AK7Pruned = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK7CHSprunedwithNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Trimming
process.PFJet_AK7Trimmed = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK7CHStrimmedwithNsub'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Filtering
process.PFJet_AK7FilteredN2 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK7CHSfilteredN2withNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

process.PFJet_AK7FilteredN3 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK7CHSfilteredN3withNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Mass Drop Filtering
process.PFJet_AK7MassDropFiltered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK7CHSmassDropFilteredwithNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
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

###################################################################### CA4 Jets
######  JET CORRECTIONS
process.PFJet_CA4_JEC = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA4CHSJEC'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
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
process.PFJet_CA4 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA4CHSwithNsub'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Pruning
process.PFJet_CA4Pruned = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA4CHSprunedwithNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Trimming
process.PFJet_CA4Trimmed = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA4CHStrimmedwithNsub'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Filtering
process.PFJet_CA4FilteredN2 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA4CHSfilteredN2withNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

process.PFJet_CA4FilteredN3 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA4CHSfilteredN3withNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Mass Drop Filtering
process.PFJet_CA4MassDropFiltered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA4CHSmassDropFilteredwithNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
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

###################################################################### CA8 Jets
######  JET CORRECTIONS
process.PFJet_CA8_JEC = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA8CHSJEC'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
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
process.PFJet_CA8 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA8CHSwithNsub'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Pruning
process.PFJet_CA8Pruned = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA8CHSprunedwithNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Trimming
process.PFJet_CA8Trimmed = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA8CHStrimmedwithNsub'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Filtering
process.PFJet_CA8FilteredN2 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA8CHSfilteredN2withNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

process.PFJet_CA8FilteredN3 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA8CHSfilteredN3withNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Mass Drop Filtering
process.PFJet_CA8MassDropFiltered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA8CHSmassDropFilteredwithNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
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

###################################################################### KT4 Jets
######  JET CORRECTIONS
process.PFJet_KT4_JEC = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT4CHSJEC'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
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
process.PFJet_KT4 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT4CHSwithNsub'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Pruning
process.PFJet_KT4Pruned = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT4CHSprunedwithNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Trimming
process.PFJet_KT4Trimmed = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT4CHStrimmedwithNsub'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Filtering
process.PFJet_KT4FilteredN2 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT4CHSfilteredN2withNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

process.PFJet_KT4FilteredN3 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT4CHSfilteredN3withNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Mass Drop Filtering
process.PFJet_KT4MassDropFiltered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT4CHSmassDropFilteredwithNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
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

###################################################################### KT8 Jets
######  JET CORRECTIONS
process.PFJet_KT8_JEC = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT8CHSJEC'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
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
process.PFJet_KT8 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT8CHSwithNsub'),
		jetsPruned	 = cms.bool(False),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Pruning
process.PFJet_KT8Pruned = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT8CHSprunedwithNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Trimming
process.PFJet_KT8Trimmed = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT8CHStrimmedwithNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Filtering
process.PFJet_KT8FilteredN2 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT8CHSfilteredN2withNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

process.PFJet_KT8FilteredN3 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT8CHSfilteredN3withNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
		triggerConfiguration = cms.PSet(
			hltResults            = cms.InputTag('TriggerResults','','HLT'),
			l1tResults            = cms.InputTag(''),
			daqPartitions         = cms.uint32(1),
			l1tIgnoreMask         = cms.bool(False),
			l1techIgnorePrescales = cms.bool(False),
			throw                 = cms.bool(False)
		)
)

##### With Jet Corrections and Mass Drop Filtering
process.PFJet_KT8MassDropFiltered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT8CHSmassDropFilteredwithNsub'),
		jetsPruned	 = cms.bool(True),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring( listTriggerAlias ), 
		triggerSelection = cms.vstring( listTrigger ),
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
		process.ak4Jets * process.PFJet_AK4 * process.PFJet_AK4Pruned * process.PFJet_AK4Trimmed * process.PFJet_AK4FilteredN2 * process.PFJet_AK4FilteredN3 * process.PFJet_AK4MassDropFiltered *  
		process.ak5Jets * process.PFJet_AK5 * process.PFJet_AK5Pruned * process.PFJet_AK5Trimmed * process.PFJet_AK5FilteredN2 * process.PFJet_AK5FilteredN3 * process.PFJet_AK5MassDropFiltered *  
		process.ak7Jets * process.PFJet_AK7 * process.PFJet_AK7Pruned * process.PFJet_AK7Trimmed * process.PFJet_AK7FilteredN2 * process.PFJet_AK7FilteredN3 * process.PFJet_AK7MassDropFiltered *  
		process.ca4Jets * process.PFJet_CA4 * process.PFJet_CA4Pruned * process.PFJet_CA4Trimmed * process.PFJet_CA4FilteredN2 * process.PFJet_CA4FilteredN3 * process.PFJet_CA4MassDropFiltered *  
		process.ca8Jets * process.PFJet_CA8 * process.PFJet_CA8Pruned * process.PFJet_CA8Trimmed * process.PFJet_CA8FilteredN2 * process.PFJet_CA8FilteredN3 * process.PFJet_CA8MassDropFiltered *  
		process.kt4Jets * process.PFJet_KT4 * process.PFJet_KT4Pruned * process.PFJet_KT4Trimmed * process.PFJet_KT4FilteredN2 * process.PFJet_KT4FilteredN3 * process.PFJet_KT4MassDropFiltered *  
		process.kt8Jets * process.PFJet_KT8 * process.PFJet_KT8Pruned * process.PFJet_KT8Trimmed * process.PFJet_KT8FilteredN2 * process.PFJet_KT8FilteredN3 * process.PFJet_KT8MassDropFiltered   
		)

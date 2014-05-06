import FWCore.ParameterSet.Config as cms 
import os, sys, time

######### input parameters
mass = 0

###### Trick for add date or month to plots
dateKey   = time.strftime("%y%m%d%H%M")
monthKey   = time.strftime("%y%m%d")

process = cms.Process('myprocess')
process.load('FWCore.MessageService.MessageLogger_cfi')

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'START53_V7E::All'

process.TFileService=cms.Service("TFileService",
		#fileName=cms.string( 'QCD_HT1000ToInf_8TeV_tree.root' ),
		fileName=cms.string( 'QCD_500To1000_8TeV_tree.root' ),
		)

##-------------------- Define the source  ----------------------------
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

process.source = cms.Source("PoolSource",
		fileNames = cms.untracked.vstring( '/store/mc/Summer12_DR53X/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/000FFBED-DA11-E211-B882-00A0D1EE8B08.root' ),
		#fileNames = cms.untracked.vstring( '/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM' ),
)

#############   Format MessageLogger #################
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

########################### Loading PATtuplizers
#### Jet Corrections
inputJetCorrLabel = ['L1FastJet', 'L2Relative', 'L3Absolute']
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

######################################## AK4 Jets
###### NO JET CORRECTIONS
process.PFJet_AK4_NOJEC = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK4CHSNOJEC'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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
process.PFJet_AK4 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK4CHSwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Pruning
process.PFJet_AK4Pruned = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK4CHSprunedwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Trimming
process.PFJet_AK4Trimmed = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK4CHStrimmedwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Filtering
process.PFJet_AK4Filtered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK4CHSfilteredwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Mass Drop Filtering
process.PFJet_AK4MassDropFiltered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK4CHSmassDropFilteredwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Pruning
process.PFJet_AK5Pruned = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK5CHSprunedwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Trimming
process.PFJet_AK5Trimmed = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK5CHStrimmedwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Filtering
process.PFJet_AK5Filtered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK5CHSfilteredwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Mass Drop Filtering
process.PFJet_AK5MassDropFiltered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK5CHSmassDropFilteredwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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


###################################################################### AK7 Jets
###### NO JET CORRECTIONS
process.PFJet_AK7_NOJEC = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK7CHSNOJEC'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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
process.PFJet_AK7 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK7CHSwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Pruning
process.PFJet_AK7Pruned = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK7CHSprunedwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Trimming
process.PFJet_AK7Trimmed = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK7CHStrimmedwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Filtering
process.PFJet_AK7Filtered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK7CHSfilteredwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Mass Drop Filtering
process.PFJet_AK7MassDropFiltered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK7CHSmassDropFilteredwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

###################################################################### CA4 Jets
###### NO JET CORRECTIONS
process.PFJet_CA4_NOJEC = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA4CHSNOJEC'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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
process.PFJet_CA4 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA4CHSwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Pruning
process.PFJet_CA4Pruned = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA4CHSprunedwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Trimming
process.PFJet_CA4Trimmed = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA4CHStrimmedwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Filtering
process.PFJet_CA4Filtered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA4CHSfilteredwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Mass Drop Filtering
process.PFJet_CA4MassDropFiltered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA4CHSmassDropFilteredwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

###################################################################### CA8 Jets
###### NO JET CORRECTIONS
process.PFJet_CA8_NOJEC = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA8CHSNOJEC'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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
process.PFJet_CA8 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA8CHSwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Pruning
process.PFJet_CA8Pruned = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA8CHSprunedwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Trimming
process.PFJet_CA8Trimmed = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA8CHStrimmedwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Filtering
process.PFJet_CA8Filtered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA8CHSfilteredwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Mass Drop Filtering
process.PFJet_CA8MassDropFiltered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA8CHSmassDropFilteredwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

###################################################################### KT4 Jets
###### NO JET CORRECTIONS
process.PFJet_KT4_NOJEC = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT4CHSNOJEC'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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
process.PFJet_KT4 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT4CHSwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Pruning
process.PFJet_KT4Pruned = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT4CHSprunedwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Trimming
process.PFJet_KT4Trimmed = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT4CHStrimmedwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Filtering
process.PFJet_KT4Filtered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT4CHSfilteredwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Mass Drop Filtering
process.PFJet_KT4MassDropFiltered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT4CHSmassDropFilteredwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

###################################################################### KT8 Jets
###### NO JET CORRECTIONS
process.PFJet_KT8_NOJEC = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT8CHSNOJEC'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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
process.PFJet_KT8 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT8CHSwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Pruning
process.PFJet_KT8Pruned = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT8CHSprunedwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Trimming
process.PFJet_KT8Trimmed = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT8CHStrimmedwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Filtering
process.PFJet_KT8Filtered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT8CHSfilteredwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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

##### With Jet Corrections and Mass Drop Filtering
process.PFJet_KT8MassDropFiltered = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT8CHSmassDropFilteredwithNsub'),
		met              = cms.InputTag('pfMet'),
		vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
		ptMin            = cms.double(20),
		etaMax          = cms.double(2.5),
		## MC ########################################
		pu               = cms.untracked.InputTag('addPileupInfo'),
		genSrc 		 = cms.InputTag('genParticles'),
		stopMass 	 = cms.double( mass ),
		## trigger ###################################
		triggerAlias     = cms.vstring('HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'),
		triggerSelection = cms.vstring(
			'HLT_HT250_v*',
			'HLT_HT300_v*',
			'HLT_HT350_v*',
			'HLT_HT400_v*',
			'HLT_HT450_v*',
			'HLT_HT500_v*',
			'HLT_HT550_v*',
			'HLT_HT650_v*',  
			'HLT_HT750_v*',  
			'HLT_PFHT350_v*',
			'HLT_PFHT650_v*',
			'HLT_PFHT700_v*',
			'HLT_PFHT750_v*',
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
		process.ak4Jets * process.PFJet_AK4 * process.PFJet_AK4Pruned * process.PFJet_AK4Trimmed * process.PFJet_AK4Filtered * process.PFJet_AK4MassDropFiltered *  
		process.ak5Jets * process.PFJet_AK5 * process.PFJet_AK5Pruned * process.PFJet_AK5Trimmed * process.PFJet_AK5Filtered * process.PFJet_AK5MassDropFiltered *  
		process.ak7Jets * process.PFJet_AK7 * process.PFJet_AK7Pruned * process.PFJet_AK7Trimmed * process.PFJet_AK7Filtered * process.PFJet_AK7MassDropFiltered *  
		process.ca4Jets * process.PFJet_CA4 * process.PFJet_CA4Pruned * process.PFJet_CA4Trimmed * process.PFJet_CA4Filtered * process.PFJet_CA4MassDropFiltered *  
		process.ca8Jets * process.PFJet_CA8 * process.PFJet_CA8Pruned * process.PFJet_CA8Trimmed * process.PFJet_CA8Filtered * process.PFJet_CA8MassDropFiltered *  
		process.kt4Jets * process.PFJet_KT4 * process.PFJet_KT4Pruned * process.PFJet_KT4Trimmed * process.PFJet_KT4Filtered * process.PFJet_KT4MassDropFiltered *  
		process.kt8Jets * process.PFJet_KT8 * process.PFJet_KT8Pruned * process.PFJet_KT8Trimmed * process.PFJet_KT8Filtered * process.PFJet_KT8MassDropFiltered   
		)

#process.out = cms.OutputModule("PoolOutputModule", 
#		fileName = cms.untracked.string('QCD_HT_TuneZ2star_8TeV-madgraph-pythia6_simplePAT.root') ,
##		outputCommands = cms.untracked.vstring(
##			"keep *_patJetsAK4CHSwithNsub_*_*", 
##			"keep *_patJetsAK5CHSwithNsub_*_*", 
##			"keep *_patJetsAK7CHSwithNsub_*_*", 
##			"keep *_patJetsCA4CHSwithNsub_*_*", 
##			"keep *_patJetsCA8CHSwithNsub_*_*", 
##			"keep *_patJetsKT4CHSwithNsub_*_*", 
##			"keep *_patJetsKT8CHSwithNsub_*_*", 
##			), 
#
#		)
#process.e = cms.EndPath(process.out)


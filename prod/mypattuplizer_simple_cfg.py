import FWCore.ParameterSet.Config as cms 
from FWCore.ParameterSet.VarParsing import VarParsing
import os, sys, time

###### Trick for add date or month to plots
dateKey   = time.strftime("%y%m%d%H%M")
monthKey   = time.strftime("%y%m%d")

options = VarParsing ('analysis')
process = cms.Process('myPAT')
process.load('FWCore.MessageService.MessageLogger_cfi')

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'START53_V27::All'

##-------------------- Define the source  ----------------------------
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

process.source = cms.Source("PoolSource",
		fileNames = cms.untracked.vstring( '/store/mc/Summer12_DR53X/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/000FFBED-DA11-E211-B882-00A0D1EE8B08.root' ),
)

#############   Format MessageLogger #################
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

########################### Loading PATtuplizers
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ak4jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ak5jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ak7jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ca4jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ca8jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_kt4jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_kt8jets_simple_cff')


############################################## Run Process
process.p = cms.Path( process.ak4Jets *
		#process.ak5Jets *
		process.ak7Jets *
		#process.ca4Jets *
		process.ca8Jets 
		#process.kt4Jets *
		#process.kt8Jets 
		)

## --------------------- Define the output ----------------------------
#if not ( os.path.exists( outputDir + monthKey ) ): os.makedirs( outputDir + monthKey )
process.out = cms.OutputModule("PoolOutputModule",
		#fileName=cms.untracked.string( options.outputFile ),
		fileName=cms.untracked.string( 'QCD_HT500To1000_8TeV_PAT.root'),
		#fileName=cms.untracked.string( 'myOutputFile.root' ),
		outputCommands = cms.untracked.vstring(
			"keep *_genParticles_*_*",
			"keep *_TriggerResults_*_*",
			"keep *_hltTriggerSummaryAOD_*_*",
			"keep *_addPileupInfo_*_*",
			"keep *_pfMet_*_*",
			"keep *_goodOfflinePrimaryVertices_*_*",
#			"keep *_patJetsAK4CHSNOJEC_*_*",
#			"keep *_patJetsAK4CHSwithNsub_*_*",
#			"keep *_patJetsAK4CHStrimmedwithNsub_*_*",
#			"keep *_patJetsAK4CHSprunedwithNsub_*_*",
#			"keep *_patJetsAK4CHSfilteredwithNsub_*_*",
#			"keep *_patJetsAK4CHSmassDropFilteredwithNsub_*_*",
#			"keep *_patJetsAK5CHSNOJEC_*_*",
#			"keep *_patJetsAK5CHSwithNsub_*_*",
#			"keep *_patJetsAK5CHStrimmedwithNsub_*_*",
#			"keep *_patJetsAK5CHSprunedwithNsub_*_*",
#			"keep *_patJetsAK5CHSfilteredwithNsub_*_*",
#			"keep *_patJetsAK5CHSmassDropFilteredwithNsub_*_*",
			"keep *_patJetsAK7CHSNOJEC_*_*",
			"keep *_patJetsAK7CHSwithNsub_*_*",
			"keep *_patJetsAK7CHStrimmedwithNsub_*_*",
			"keep *_patJetsAK7CHSprunedwithNsub_*_*",
			"keep *_patJetsAK7CHSfilteredwithNsub_*_*",
			"keep *_patJetsAK7CHSmassDropFilteredwithNsub_*_*",
#			"keep *_patJetsCA4CHSNOJEC_*_*",
#			"keep *_patJetsCA4CHSwithNsub_*_*",
#			"keep *_patJetsCA4CHStrimmedwithNsub_*_*",
#			"keep *_patJetsCA4CHSprunedwithNsub_*_*",
#			"keep *_patJetsCA4CHSfilteredwithNsub_*_*",
#			"keep *_patJetsCA4CHSmassDropFilteredwithNsub_*_*",
			"keep *_patJetsCA8CHSNOJEC_*_*",
			"keep *_patJetsCA8CHSwithNsub_*_*",
			"keep *_patJetsCA8CHStrimmedwithNsub_*_*",
			"keep *_patJetsCA8CHSprunedwithNsub_*_*",
			"keep *_patJetsCA8CHSfilteredwithNsub_*_*",
			"keep *_patJetsCA8CHSmassDropFilteredwithNsub_*_*",
#			"keep *_patJetsKT4CHSNOJEC_*_*",
#			"keep *_patJetsKT4CHSwithNsub_*_*",
#			"keep *_patJetsKT4CHStrimmedwithNsub_*_*",
#			"keep *_patJetsKT4CHSprunedwithNsub_*_*",
#			"keep *_patJetsKT4CHSfilteredwithNsub_*_*",
#			"keep *_patJetsKT4CHSmassDropFilteredwithNsub_*_*",
#			"keep *_patJetsKT8CHSNOJEC_*_*",
#			"keep *_patJetsKT8CHSwithNsub_*_*",
#			"keep *_patJetsKT8CHStrimmedwithNsub_*_*",
#			"keep *_patJetsKT8CHSprunedwithNsub_*_*",
#			"keep *_patJetsKT8CHSfilteredwithNsub_*_*",
#			"keep *_patJetsKT8CHSmassDropFilteredwithNsub_*_*",
			),
		)

process.e = cms.EndPath( process.out )


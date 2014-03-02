import FWCore.ParameterSet.Config as cms 
process = cms.Process('myprocess')
process.load('FWCore.MessageService.MessageLogger_cfi')

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'START53_V27::All'

#process.TFileService=cms.Service("TFileService",fileName=cms.string('dijetTree_QCD.root'))
process.TFileService=cms.Service("TFileService",fileName=cms.string('/cms/gomez/Stops/st_jj/patTuples/test_QCD_tree.root'))
##-------------------- Define the source  ----------------------------
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.source = cms.Source("PoolSource",
  #fileNames = cms.untracked.vstring('/store/cmst3/group/das2014/EXODijetsLE/test_QCD.root')
  fileNames = cms.untracked.vstring('file:/cms/gomez/Stops/st_jj/patTuples/test_QCD.root')
)

#############   Format MessageLogger #################
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.load('MySubsPATtuple.MyPATtuplizer.PAT_ca8jets_simple_cff')
#process.load('cmsdas2014.exo_dijets_exercise.PAT_ca8jets_simple_cff')


##-------------------- User analyzer  --------------------------------
process.dijets     = cms.EDAnalyzer('DijetTreeProducer',
  jets             = cms.InputTag('patJetsCA8CHSwithNsub'),
  jetsPruned       = cms.InputTag('patJetsCA8CHSpruned'),
  met              = cms.InputTag('pfMet'),
  vtx              = cms.InputTag('goodOfflinePrimaryVertices'),
  mjjMin           = cms.double(0),
  ptMin            = cms.double(40),
  dEtaMax          = cms.double(2.5),
  ## MC ########################################
  pu               = cms.untracked.InputTag('addPileupInfo'),
  ## trigger ###################################
  triggerAlias     = cms.vstring('Fat','PFHT650','PFNoPUHT650','HT750','HT550'),
  triggerSelection = cms.vstring(
    'HLT_FatDiPFJetMass750_DR1p1_Deta1p5_v*',
    'HLT_PFHT650_v*',
    'HLT_PFNoPUHT650_v*',
    'HLT_HT750_v*',  
    'HLT_HT550_v*'
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
process.p = cms.Path(process.ca8Jets * process.dijets)

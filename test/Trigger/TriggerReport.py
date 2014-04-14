import FWCore.ParameterSet.Config as cms
import os

process = cms.Process("DemoTriggerReport")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['TriggerReport.txt']
process.MessageLogger.categories.append('HLTrigReport')
process.MessageLogger.categories.append('L1GtTrigReport')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

inputDir = '/cms/gomez/Stops/st_jj/AOD/stop_UDD312_50/'
list = os.popen('ls -1v '+inputDir+'*.root').read().splitlines()
outputList = [i if i.startswith('file') else 'file:' + i for i in list]

process.source = cms.Source("PoolSource",
    # replace this file with the one you actually want to use
    fileNames = cms.untracked.vstring( outputList 
    #'file:/cms/gomez/Stops/st_jj/AOD/stop_UDD312_50/stop_UDD312_50_PU_532_1_aodsim.root',
    )
)

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:hltonline_8E33v2', '')


from HLTrigger.HLTanalyzers.hlTrigReport_cfi import hlTrigReport
process.hltTrigReport = cms.EDAnalyzer( 'HLTrigReport',
    HLTriggerResults = cms.InputTag( 'TriggerResults','','HLT') 
)
process.load("L1Trigger.GlobalTriggerAnalyzer.l1GtTrigReport_cfi")
process.l1GtTrigReport.L1GtRecordInputTag = 'gtDigis'

process.HLTAnalyzerEndpath = cms.EndPath( process.l1GtTrigReport + process.hltTrigReport )

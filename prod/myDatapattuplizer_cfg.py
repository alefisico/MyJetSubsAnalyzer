import FWCore.ParameterSet.Config as cms 
import os, sys, time

######### input parameters
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')			### For a simple set of parameters

options.register ('useData',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  'Run this on real data')

options.register ('globalTag',
                  'START53_V7A::All',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  'Overwrite defaul globalTag')

#options.register ('mass',
#                  False,
#                  VarParsing.multiplicity.singleton,
#                  VarParsing.varType.int,
#                  'Run this on real data')

options.parseArguments()
print options

#if not options.mass: mass = 0
#else: mass = options.mass
mass = 0
###### Trick for add date or month to plots
#dateKey   = time.strftime("%y%m%d%H%M")
#monthKey   = time.strftime("%y%m%d")

process = cms.Process('myprocess')
process.load('FWCore.MessageService.MessageLogger_cfi')

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = options.globalTag
#process.GlobalTag.globaltag = 'FT_R_53_V18::All'		### RunA, RunB, RunC
#process.GlobalTag.globaltag = 'FT_R_53_V21::All'		### RunD

process.TFileService=cms.Service("TFileService",
		fileName=cms.string( options.outputFile ),
		closeFileFast = cms.untracked.bool(True)
		)

##-------------------- Define the source  ----------------------------
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.source = cms.Source("PoolSource",
		fileNames = cms.untracked.vstring( '/store/data/Run2012A/HT/AOD/22Jan2013-v1/20000/001FD2A2-E781-E211-8428-003048FFD7A2.root' ),	### RunA
		#fileNames = cms.untracked.vstring( '/store/data/Run2012B/JetHT/AOD/22Jan2013-v1/20000/00BC8D92-7371-E211-B38E-003048678E80.root' ),
)

#############   Format MessageLogger #################
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

listHLTPaths = []
if options.tag is '':
	listTriggerAlias = [ 'HT350', 'HT750', 'PFHT350','PFHT650' ] 
	listTrigger = [ 'HLT_HT350_v*',	'HLT_HT750_v*', 'HLT_PFHT350_v*', 'HLT_PFHT650_v*'] 
	if options.useData :
		listHLTPaths = [ 'HLT_HT350_v*', 'HLT_HT750_v*', 'HLT_PFHT350_v*', 'HLT_PFHT650_v*' ]
else:
	listTriggerAlias = [ 'HT350', 'HT750','PFNoPUHT350', 'PFNoPUHT650'  ]
	listTrigger = [ 'HLT_HT350_v*',	'HLT_HT750_v*', 'HLT_PFNoPUHT350_v*', 'HLT_PFNoPUHT650_v*' ]
	if options.useData :
		listHLTPaths = [ 'HLT_HT550_v*', 'HLT_HT750_v*','HLT_PFNoPUHT350_v*', 'HLT_PFNoPUHT650_v*' ]

#listTriggerAlias = [ 'HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'] #, 'PFNoPUHT350', 'PFNoPUHT650', 'PFNoPUHT700', 'PFNoPUHT750' ]
#listTrigger = [ 'HLT_HT250_v*', 'HLT_HT300_v*',	'HLT_HT350_v*',	'HLT_HT400_v*',	'HLT_HT450_v*',	'HLT_HT500_v*',	'HLT_HT550_v*',	'HLT_HT650_v*', 'HLT_HT750_v*', 'HLT_PFHT350_v*', 'HLT_PFHT650_v*', 'HLT_PFHT700_v*', 'HLT_PFHT750_v*'] #,	'HLT_PFNoPUHT350_v*', 'HLT_PFNoPUHT650_v*', 'HLT_PFNoPUHT700_v*', 'HLT_PFNoPUHT750_v*' ]
###############################
####### Global Setup ##########
###############################

#from PhysicsTools.PatAlgos.patTemplate_cfg import *


### The beam scraping filter __________________________________________________||
process.noscraping = cms.EDFilter(
    "FilterOutScraping",
    applyfilter = cms.untracked.bool(True),
    debugOn = cms.untracked.bool(False),
    numtrack = cms.untracked.uint32(10),
    thresh = cms.untracked.double(0.25)
    )

### The iso-based HBHE noise filter ___________________________________________||
process.load('CommonTools.RecoAlgos.HBHENoiseFilter_cfi')

### The CSC beam halo tight filter ____________________________________________||
process.load('RecoMET.METAnalyzers.CSCHaloFilter_cfi')

###Claudia filter for jets at least 4 > 40 GeV_________________________________||
##
##process.filterJets = cms.EDFilter("CandViewSelector",
##                                  cut = cms.string  ('pt > 50.0'),
##                                  src = cms.InputTag("goodPatJetsPFlow"),
##                                  )
##
##process.countJets = cms.EDFilter("PATCandViewCountFilter",
##                                 minNumber = cms.uint32  (4),
##                                 maxNumber = cms.uint32  (999999),
##                                 src       = cms.InputTag("filterJets"),
##                                 )
#
#
### The HCAL laser filter _____________________________________________________||
process.load("RecoMET.METFilters.hcalLaserEventFilter_cfi")
process.hcalLaserEventFilter.vetoByRunEventNumber=cms.untracked.bool(False)
process.hcalLaserEventFilter.vetoByHBHEOccupancy=cms.untracked.bool(True)

### The ECAL dead cell trigger primitive filter _______________________________||
process.load('RecoMET.METFilters.EcalDeadCellTriggerPrimitiveFilter_cfi')
### For AOD and RECO recommendation to use recovered rechits
process.EcalDeadCellTriggerPrimitiveFilter.tpDigiCollection = cms.InputTag("ecalTPSkimNA")

######## Extra producer for ECAL dead cell
process.EcalTrigTowerConstituentsMapBuilder = cms.ESProducer("EcalTrigTowerConstituentsMapBuilder",
    MapFile = cms.untracked.string('Geometry/EcalMapping/data/EndCap_TTMap.txt')
)

process.CaloGeometryBuilder = cms.ESProducer("CaloGeometryBuilder",
    SelectedCalos = cms.vstring('HCAL', 
        'ZDC', 
        'CASTOR', 
        'EcalBarrel', 
        'EcalEndcap', 
        'EcalPreshower', 
        'TOWER')
)

process.CaloTopologyBuilder = cms.ESProducer("CaloTopologyBuilder")


process.CaloTowerHardcodeGeometryEP = cms.ESProducer("CaloTowerHardcodeGeometryEP")


process.CastorDbProducer = cms.ESProducer("CastorDbProducer")


process.CastorHardcodeGeometryEP = cms.ESProducer("CastorHardcodeGeometryEP")


process.DTGeometryESModule = cms.ESProducer("DTGeometryESModule",
    appendToDataLabel = cms.string(''),
    fromDDD = cms.bool(True),
    applyAlignment = cms.bool(True),
    alignmentsLabel = cms.string('')
)


process.EcalBarrelGeometryEP = cms.ESProducer("EcalBarrelGeometryEP",
    applyAlignment = cms.bool(False)
)


process.EcalElectronicsMappingBuilder = cms.ESProducer("EcalElectronicsMappingBuilder")


process.EcalEndcapGeometryEP = cms.ESProducer("EcalEndcapGeometryEP",
    applyAlignment = cms.bool(False)
)


process.EcalLaserCorrectionService = cms.ESProducer("EcalLaserCorrectionService")


process.EcalPreshowerGeometryEP = cms.ESProducer("EcalPreshowerGeometryEP",
    applyAlignment = cms.bool(False)
)


process.EcalTrigTowerConstituentsMapBuilder = cms.ESProducer("EcalTrigTowerConstituentsMapBuilder",
    MapFile = cms.untracked.string('Geometry/EcalMapping/data/EndCap_TTMap.txt')
)


process.GlobalTrackingGeometryESProducer = cms.ESProducer("GlobalTrackingGeometryESProducer")


process.HcalHardcodeGeometryEP = cms.ESProducer("HcalHardcodeGeometryEP")


process.HcalTopologyIdealEP = cms.ESProducer("HcalTopologyIdealEP")


process.MuonDetLayerGeometryESProducer = cms.ESProducer("MuonDetLayerGeometryESProducer")


process.MuonNumberingInitialization = cms.ESProducer("MuonNumberingInitialization")


process.ParametrizedMagneticFieldProducer = cms.ESProducer("ParametrizedMagneticFieldProducer",
    version = cms.string('OAE_1103l_071212'),
    parameters = cms.PSet(
        BValue = cms.string('3_8T')
    ),
    label = cms.untracked.string('parametrizedField')
)


process.RPCGeometryESModule = cms.ESProducer("RPCGeometryESModule",
    useDDD = cms.untracked.bool(True),
    compatibiltyWith11 = cms.untracked.bool(True)
)


process.SiStripRecHitMatcherESProducer = cms.ESProducer("SiStripRecHitMatcherESProducer",
    ComponentName = cms.string('StandardMatcher'),
    NSigmaInside = cms.double(3.0)
)


process.SteppingHelixPropagatorAlong = cms.ESProducer("SteppingHelixPropagatorESProducer",
    endcapShiftInZNeg = cms.double(0.0),
    PropagationDirection = cms.string('alongMomentum'),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    NoErrorPropagation = cms.bool(False),
    SetVBFPointer = cms.bool(False),
    AssumeNoMaterial = cms.bool(False),
    returnTangentPlane = cms.bool(True),
    useInTeslaFromMagField = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    useEndcapShiftsInZ = cms.bool(False),
    sendLogWarning = cms.bool(False),
    ComponentName = cms.string('SteppingHelixPropagatorAlong'),
    debug = cms.bool(False),
    ApplyRadX0Correction = cms.bool(True),
    useMagVolumes = cms.bool(True),
    endcapShiftInZPos = cms.double(0.0)
)


process.StripCPEfromTrackAngleESProducer = cms.ESProducer("StripCPEESProducer",
    ComponentName = cms.string('StripCPEfromTrackAngle')
)


process.TrackerDigiGeometryESModule = cms.ESProducer("TrackerDigiGeometryESModule",
    appendToDataLabel = cms.string(''),
    fromDDD = cms.bool(True),
    applyAlignment = cms.bool(True),
    alignmentsLabel = cms.string('')
)


process.TrackerGeometricDetESModule = cms.ESProducer("TrackerGeometricDetESModule",
    fromDDD = cms.bool(True)
)


process.TrackerRecoGeometryESProducer = cms.ESProducer("TrackerRecoGeometryESProducer")


process.TransientTrackBuilderESProducer = cms.ESProducer("TransientTrackBuilderESProducer",
    ComponentName = cms.string('TransientTrackBuilder')
)


process.VolumeBasedMagneticFieldESProducer = cms.ESProducer("VolumeBasedMagneticFieldESProducer",
    scalingVolumes = cms.vint32(14100, 14200, 17600, 17800, 17900, 
        18100, 18300, 18400, 18600, 23100, 
        23300, 23400, 23600, 23800, 23900, 
        24100, 28600, 28800, 28900, 29100, 
        29300, 29400, 29600, 28609, 28809, 
        28909, 29109, 29309, 29409, 29609, 
        28610, 28810, 28910, 29110, 29310, 
        29410, 29610, 28611, 28811, 28911, 
        29111, 29311, 29411, 29611),
    scalingFactors = cms.vdouble(1, 1, 0.994, 1.004, 1.004, 
        1.005, 1.004, 1.004, 0.994, 0.965, 
        0.958, 0.958, 0.953, 0.958, 0.958, 
        0.965, 0.918, 0.924, 0.924, 0.906, 
        0.924, 0.924, 0.918, 0.991, 0.998, 
        0.998, 0.978, 0.998, 0.998, 0.991, 
        0.991, 0.998, 0.998, 0.978, 0.998, 
        0.998, 0.991, 0.991, 0.998, 0.998, 
        0.978, 0.998, 0.998, 0.991),
    overrideMasterSector = cms.bool(False),
    useParametrizedTrackerField = cms.bool(True),
    label = cms.untracked.string(''),
    version = cms.string('grid_1103l_090322_3_8t'),
    debugBuilder = cms.untracked.bool(False),
    paramLabel = cms.string('parametrizedField'),
    geometryVersion = cms.int32(90322),
    cacheLastVolume = cms.untracked.bool(True)
)


process.ZdcHardcodeGeometryEP = cms.ESProducer("ZdcHardcodeGeometryEP")

process.XMLIdealGeometryESSource = cms.ESSource("XMLIdealGeometryESSource",
    geomXMLFiles = cms.vstring('Geometry/CMSCommonData/data/materials.xml', 
        'Geometry/CMSCommonData/data/rotations.xml', 
        'Geometry/CMSCommonData/data/normal/cmsextent.xml', 
        'Geometry/CMSCommonData/data/cms.xml', 
        'Geometry/CMSCommonData/data/cmsMother.xml', 
        'Geometry/CMSCommonData/data/cmsTracker.xml', 
        'Geometry/CMSCommonData/data/caloBase.xml', 
        'Geometry/CMSCommonData/data/cmsCalo.xml', 
        'Geometry/CMSCommonData/data/muonBase.xml', 
        'Geometry/CMSCommonData/data/cmsMuon.xml', 
        'Geometry/CMSCommonData/data/mgnt.xml', 
        'Geometry/CMSCommonData/data/beampipe.xml', 
        'Geometry/CMSCommonData/data/cmsBeam.xml', 
        'Geometry/CMSCommonData/data/muonMB.xml', 
        'Geometry/CMSCommonData/data/muonMagnet.xml', 
        'Geometry/TrackerCommonData/data/pixfwdMaterials.xml', 
        'Geometry/TrackerCommonData/data/pixfwdCommon.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq1x2.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq1x5.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq2x3.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq2x4.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq2x5.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPanelBase.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPanel.xml', 
        'Geometry/TrackerCommonData/data/pixfwdBlade.xml', 
        'Geometry/TrackerCommonData/data/pixfwdNipple.xml', 
        'Geometry/TrackerCommonData/data/pixfwdDisk.xml', 
        'Geometry/TrackerCommonData/data/pixfwdCylinder.xml', 
        'Geometry/TrackerCommonData/data/pixfwd.xml', 
        'Geometry/TrackerCommonData/data/pixbarmaterial.xml', 
        'Geometry/TrackerCommonData/data/pixbarladder.xml', 
        'Geometry/TrackerCommonData/data/pixbarladderfull.xml', 
        'Geometry/TrackerCommonData/data/pixbarladderhalf.xml', 
        'Geometry/TrackerCommonData/data/pixbarlayer.xml', 
        'Geometry/TrackerCommonData/data/pixbarlayer0.xml', 
        'Geometry/TrackerCommonData/data/pixbarlayer1.xml', 
        'Geometry/TrackerCommonData/data/pixbarlayer2.xml', 
        'Geometry/TrackerCommonData/data/pixbar.xml', 
        'Geometry/TrackerCommonData/data/tibtidcommonmaterial.xml', 
        'Geometry/TrackerCommonData/data/tibmaterial.xml', 
        'Geometry/TrackerCommonData/data/tibmodpar.xml', 
        'Geometry/TrackerCommonData/data/tibmodule0.xml', 
        'Geometry/TrackerCommonData/data/tibmodule0a.xml', 
        'Geometry/TrackerCommonData/data/tibmodule0b.xml', 
        'Geometry/TrackerCommonData/data/tibmodule2.xml', 
        'Geometry/TrackerCommonData/data/tibstringpar.xml', 
        'Geometry/TrackerCommonData/data/tibstring0ll.xml', 
        'Geometry/TrackerCommonData/data/tibstring0lr.xml', 
        'Geometry/TrackerCommonData/data/tibstring0ul.xml', 
        'Geometry/TrackerCommonData/data/tibstring0ur.xml', 
        'Geometry/TrackerCommonData/data/tibstring0.xml', 
        'Geometry/TrackerCommonData/data/tibstring1ll.xml', 
        'Geometry/TrackerCommonData/data/tibstring1lr.xml', 
        'Geometry/TrackerCommonData/data/tibstring1ul.xml', 
        'Geometry/TrackerCommonData/data/tibstring1ur.xml', 
        'Geometry/TrackerCommonData/data/tibstring1.xml', 
        'Geometry/TrackerCommonData/data/tibstring2ll.xml', 
        'Geometry/TrackerCommonData/data/tibstring2lr.xml', 
        'Geometry/TrackerCommonData/data/tibstring2ul.xml', 
        'Geometry/TrackerCommonData/data/tibstring2ur.xml', 
        'Geometry/TrackerCommonData/data/tibstring2.xml', 
        'Geometry/TrackerCommonData/data/tibstring3ll.xml', 
        'Geometry/TrackerCommonData/data/tibstring3lr.xml', 
        'Geometry/TrackerCommonData/data/tibstring3ul.xml', 
        'Geometry/TrackerCommonData/data/tibstring3ur.xml', 
        'Geometry/TrackerCommonData/data/tibstring3.xml', 
        'Geometry/TrackerCommonData/data/tiblayerpar.xml', 
        'Geometry/TrackerCommonData/data/tiblayer0.xml', 
        'Geometry/TrackerCommonData/data/tiblayer1.xml', 
        'Geometry/TrackerCommonData/data/tiblayer2.xml', 
        'Geometry/TrackerCommonData/data/tiblayer3.xml', 
        'Geometry/TrackerCommonData/data/tib.xml', 
        'Geometry/TrackerCommonData/data/tidmaterial.xml', 
        'Geometry/TrackerCommonData/data/tidmodpar.xml', 
        'Geometry/TrackerCommonData/data/tidmodule0.xml', 
        'Geometry/TrackerCommonData/data/tidmodule0r.xml', 
        'Geometry/TrackerCommonData/data/tidmodule0l.xml', 
        'Geometry/TrackerCommonData/data/tidmodule1.xml', 
        'Geometry/TrackerCommonData/data/tidmodule1r.xml', 
        'Geometry/TrackerCommonData/data/tidmodule1l.xml', 
        'Geometry/TrackerCommonData/data/tidmodule2.xml', 
        'Geometry/TrackerCommonData/data/tidringpar.xml', 
        'Geometry/TrackerCommonData/data/tidring0.xml', 
        'Geometry/TrackerCommonData/data/tidring0f.xml', 
        'Geometry/TrackerCommonData/data/tidring0b.xml', 
        'Geometry/TrackerCommonData/data/tidring1.xml', 
        'Geometry/TrackerCommonData/data/tidring1f.xml', 
        'Geometry/TrackerCommonData/data/tidring1b.xml', 
        'Geometry/TrackerCommonData/data/tidring2.xml', 
        'Geometry/TrackerCommonData/data/tid.xml', 
        'Geometry/TrackerCommonData/data/tidf.xml', 
        'Geometry/TrackerCommonData/data/tidb.xml', 
        'Geometry/TrackerCommonData/data/tibtidservices.xml', 
        'Geometry/TrackerCommonData/data/tibtidservicesf.xml', 
        'Geometry/TrackerCommonData/data/tibtidservicesb.xml', 
        'Geometry/TrackerCommonData/data/tobmaterial.xml', 
        'Geometry/TrackerCommonData/data/tobmodpar.xml', 
        'Geometry/TrackerCommonData/data/tobmodule0.xml', 
        'Geometry/TrackerCommonData/data/tobmodule2.xml', 
        'Geometry/TrackerCommonData/data/tobmodule4.xml', 
        'Geometry/TrackerCommonData/data/tobrodpar.xml', 
        'Geometry/TrackerCommonData/data/tobrod0c.xml', 
        'Geometry/TrackerCommonData/data/tobrod0l.xml', 
        'Geometry/TrackerCommonData/data/tobrod0h.xml', 
        'Geometry/TrackerCommonData/data/tobrod0.xml', 
        'Geometry/TrackerCommonData/data/tobrod1l.xml', 
        'Geometry/TrackerCommonData/data/tobrod1h.xml', 
        'Geometry/TrackerCommonData/data/tobrod1.xml', 
        'Geometry/TrackerCommonData/data/tobrod2c.xml', 
        'Geometry/TrackerCommonData/data/tobrod2l.xml', 
        'Geometry/TrackerCommonData/data/tobrod2h.xml', 
        'Geometry/TrackerCommonData/data/tobrod2.xml', 
        'Geometry/TrackerCommonData/data/tobrod3l.xml', 
        'Geometry/TrackerCommonData/data/tobrod3h.xml', 
        'Geometry/TrackerCommonData/data/tobrod3.xml', 
        'Geometry/TrackerCommonData/data/tobrod4c.xml', 
        'Geometry/TrackerCommonData/data/tobrod4l.xml', 
        'Geometry/TrackerCommonData/data/tobrod4h.xml', 
        'Geometry/TrackerCommonData/data/tobrod4.xml', 
        'Geometry/TrackerCommonData/data/tobrod5l.xml', 
        'Geometry/TrackerCommonData/data/tobrod5h.xml', 
        'Geometry/TrackerCommonData/data/tobrod5.xml', 
        'Geometry/TrackerCommonData/data/tob.xml', 
        'Geometry/TrackerCommonData/data/tecmaterial.xml', 
        'Geometry/TrackerCommonData/data/tecmodpar.xml', 
        'Geometry/TrackerCommonData/data/tecmodule0.xml', 
        'Geometry/TrackerCommonData/data/tecmodule0r.xml', 
        'Geometry/TrackerCommonData/data/tecmodule0s.xml', 
        'Geometry/TrackerCommonData/data/tecmodule1.xml', 
        'Geometry/TrackerCommonData/data/tecmodule1r.xml', 
        'Geometry/TrackerCommonData/data/tecmodule1s.xml', 
        'Geometry/TrackerCommonData/data/tecmodule2.xml', 
        'Geometry/TrackerCommonData/data/tecmodule3.xml', 
        'Geometry/TrackerCommonData/data/tecmodule4.xml', 
        'Geometry/TrackerCommonData/data/tecmodule4r.xml', 
        'Geometry/TrackerCommonData/data/tecmodule4s.xml', 
        'Geometry/TrackerCommonData/data/tecmodule5.xml', 
        'Geometry/TrackerCommonData/data/tecmodule6.xml', 
        'Geometry/TrackerCommonData/data/tecpetpar.xml', 
        'Geometry/TrackerCommonData/data/tecring0.xml', 
        'Geometry/TrackerCommonData/data/tecring1.xml', 
        'Geometry/TrackerCommonData/data/tecring2.xml', 
        'Geometry/TrackerCommonData/data/tecring3.xml', 
        'Geometry/TrackerCommonData/data/tecring4.xml', 
        'Geometry/TrackerCommonData/data/tecring5.xml', 
        'Geometry/TrackerCommonData/data/tecring6.xml', 
        'Geometry/TrackerCommonData/data/tecring0f.xml', 
        'Geometry/TrackerCommonData/data/tecring1f.xml', 
        'Geometry/TrackerCommonData/data/tecring2f.xml', 
        'Geometry/TrackerCommonData/data/tecring3f.xml', 
        'Geometry/TrackerCommonData/data/tecring4f.xml', 
        'Geometry/TrackerCommonData/data/tecring5f.xml', 
        'Geometry/TrackerCommonData/data/tecring6f.xml', 
        'Geometry/TrackerCommonData/data/tecring0b.xml', 
        'Geometry/TrackerCommonData/data/tecring1b.xml', 
        'Geometry/TrackerCommonData/data/tecring2b.xml', 
        'Geometry/TrackerCommonData/data/tecring3b.xml', 
        'Geometry/TrackerCommonData/data/tecring4b.xml', 
        'Geometry/TrackerCommonData/data/tecring5b.xml', 
        'Geometry/TrackerCommonData/data/tecring6b.xml', 
        'Geometry/TrackerCommonData/data/tecpetalf.xml', 
        'Geometry/TrackerCommonData/data/tecpetalb.xml', 
        'Geometry/TrackerCommonData/data/tecpetal0.xml', 
        'Geometry/TrackerCommonData/data/tecpetal0f.xml', 
        'Geometry/TrackerCommonData/data/tecpetal0b.xml', 
        'Geometry/TrackerCommonData/data/tecpetal3.xml', 
        'Geometry/TrackerCommonData/data/tecpetal3f.xml', 
        'Geometry/TrackerCommonData/data/tecpetal3b.xml', 
        'Geometry/TrackerCommonData/data/tecpetal6f.xml', 
        'Geometry/TrackerCommonData/data/tecpetal6b.xml', 
        'Geometry/TrackerCommonData/data/tecpetal8f.xml', 
        'Geometry/TrackerCommonData/data/tecpetal8b.xml', 
        'Geometry/TrackerCommonData/data/tecwheel.xml', 
        'Geometry/TrackerCommonData/data/tecwheela.xml', 
        'Geometry/TrackerCommonData/data/tecwheelb.xml', 
        'Geometry/TrackerCommonData/data/tecwheelc.xml', 
        'Geometry/TrackerCommonData/data/tecwheeld.xml', 
        'Geometry/TrackerCommonData/data/tecwheel6.xml', 
        'Geometry/TrackerCommonData/data/tecservices.xml', 
        'Geometry/TrackerCommonData/data/tecbackplate.xml', 
        'Geometry/TrackerCommonData/data/tec.xml', 
        'Geometry/TrackerCommonData/data/trackermaterial.xml', 
        'Geometry/TrackerCommonData/data/tracker.xml', 
        'Geometry/TrackerCommonData/data/trackerpixbar.xml', 
        'Geometry/TrackerCommonData/data/trackerpixfwd.xml', 
        'Geometry/TrackerCommonData/data/trackertibtidservices.xml', 
        'Geometry/TrackerCommonData/data/trackertib.xml', 
        'Geometry/TrackerCommonData/data/trackertid.xml', 
        'Geometry/TrackerCommonData/data/trackertob.xml', 
        'Geometry/TrackerCommonData/data/trackertec.xml', 
        'Geometry/TrackerCommonData/data/trackerbulkhead.xml', 
        'Geometry/TrackerCommonData/data/trackerother.xml', 
        'Geometry/EcalCommonData/data/eregalgo.xml', 
        'Geometry/EcalCommonData/data/ebalgo.xml', 
        'Geometry/EcalCommonData/data/ebcon.xml', 
        'Geometry/EcalCommonData/data/ebrot.xml', 
        'Geometry/EcalCommonData/data/eecon.xml', 
        'Geometry/EcalCommonData/data/eefixed.xml', 
        'Geometry/EcalCommonData/data/eehier.xml', 
        'Geometry/EcalCommonData/data/eealgo.xml', 
        'Geometry/EcalCommonData/data/escon.xml', 
        'Geometry/EcalCommonData/data/esalgo.xml', 
        'Geometry/EcalCommonData/data/eeF.xml', 
        'Geometry/EcalCommonData/data/eeB.xml', 
        'Geometry/HcalCommonData/data/hcalrotations.xml', 
        'Geometry/HcalCommonData/data/hcalalgo.xml', 
        'Geometry/HcalCommonData/data/hcalbarrelalgo.xml', 
        'Geometry/HcalCommonData/data/hcalendcapalgo.xml', 
        'Geometry/HcalCommonData/data/hcalouteralgo.xml', 
        'Geometry/HcalCommonData/data/hcalforwardalgo.xml', 
        'Geometry/HcalCommonData/data/average/hcalforwardmaterial.xml', 
        'Geometry/MuonCommonData/data/mbCommon.xml', 
        'Geometry/MuonCommonData/data/mb1.xml', 
        'Geometry/MuonCommonData/data/mb2.xml', 
        'Geometry/MuonCommonData/data/mb3.xml', 
        'Geometry/MuonCommonData/data/mb4.xml', 
        'Geometry/MuonCommonData/data/muonYoke.xml', 
        'Geometry/MuonCommonData/data/mf.xml', 
        'Geometry/ForwardCommonData/data/forward.xml', 
        'Geometry/ForwardCommonData/data/bundle/forwardshield.xml', 
        'Geometry/ForwardCommonData/data/brmrotations.xml', 
        'Geometry/ForwardCommonData/data/brm.xml', 
        'Geometry/ForwardCommonData/data/totemMaterials.xml', 
        'Geometry/ForwardCommonData/data/totemRotations.xml', 
        'Geometry/ForwardCommonData/data/totemt1.xml', 
        'Geometry/ForwardCommonData/data/totemt2.xml', 
        'Geometry/ForwardCommonData/data/ionpump.xml', 
        'Geometry/MuonCommonData/data/muonNumbering.xml', 
        'Geometry/TrackerCommonData/data/trackerStructureTopology.xml', 
        'Geometry/TrackerSimData/data/trackersens.xml', 
        'Geometry/TrackerRecoData/data/trackerRecoMaterial.xml', 
        'Geometry/EcalSimData/data/ecalsens.xml', 
        'Geometry/HcalCommonData/data/hcalsenspmf.xml', 
        'Geometry/HcalSimData/data/hf.xml', 
        'Geometry/HcalSimData/data/hfpmt.xml', 
        'Geometry/HcalSimData/data/hffibrebundle.xml', 
        'Geometry/HcalSimData/data/CaloUtil.xml', 
        'Geometry/MuonSimData/data/muonSens.xml', 
        'Geometry/DTGeometryBuilder/data/dtSpecsFilter.xml', 
        'Geometry/CSCGeometryBuilder/data/cscSpecsFilter.xml', 
        'Geometry/CSCGeometryBuilder/data/cscSpecs.xml', 
        'Geometry/RPCGeometryBuilder/data/RPCSpecs.xml', 
        'Geometry/ForwardCommonData/data/brmsens.xml', 
        'Geometry/HcalSimData/data/HcalProdCuts.xml', 
        'Geometry/EcalSimData/data/EcalProdCuts.xml', 
        'Geometry/EcalSimData/data/ESProdCuts.xml', 
        'Geometry/TrackerSimData/data/trackerProdCuts.xml', 
        'Geometry/TrackerSimData/data/trackerProdCutsBEAM.xml', 
        'Geometry/MuonSimData/data/muonProdCuts.xml', 
        'Geometry/ForwardSimData/data/ForwardShieldProdCuts.xml', 
        'Geometry/CMSCommonData/data/FieldParameters.xml'),
    rootNodeName = cms.string('cms:OCMS')
)


process.eegeom = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('EcalMappingRcd'),
    firstValid = cms.vuint32(1)
)


process.es_hardcode = cms.ESSource("HcalHardcodeCalibrations",
    toGet = cms.untracked.vstring('GainWidths')
)


process.magfield = cms.ESSource("XMLIdealGeometryESSource",
    geomXMLFiles = cms.vstring('Geometry/CMSCommonData/data/normal/cmsextent.xml', 
        'Geometry/CMSCommonData/data/cms.xml', 
        'Geometry/CMSCommonData/data/cmsMagneticField.xml', 
        'MagneticField/GeomBuilder/data/MagneticFieldVolumes_1103l.xml', 
        'MagneticField/GeomBuilder/data/MagneticFieldParameters_07_2pi.xml', 
        'Geometry/CMSCommonData/data/materials.xml'),
    rootNodeName = cms.string('cmsMagneticField:MAGF')
)


process.prefer("magfield")

process.AnomalousCellParameters = cms.PSet(
    maxRecoveredHcalCells = cms.uint32(9999999),
    maxBadEcalCells = cms.uint32(9999999),
    maxProblematicEcalCells = cms.uint32(9999999),
    maxBadHcalCells = cms.uint32(9999999),
    maxRecoveredEcalCells = cms.uint32(9999999),
    maxProblematicHcalCells = cms.uint32(9999999)
)

process.CondDBSetup = cms.PSet(
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string(''),
        enableReadOnlySessionOnUpdateConnection = cms.untracked.bool(False),
        idleConnectionCleanupPeriod = cms.untracked.int32(10),
        messageLevel = cms.untracked.int32(0),
        enablePoolAutomaticCleanUp = cms.untracked.bool(False),
        enableConnectionSharing = cms.untracked.bool(True),
        connectionRetrialTimeOut = cms.untracked.int32(60),
        connectionTimeOut = cms.untracked.int32(60),
        authenticationSystem = cms.untracked.int32(0),
        connectionRetrialPeriod = cms.untracked.int32(10)
    )
)


### The EE bad SuperCrystal filter ____________________________________________||
process.load('RecoMET.METFilters.eeBadScFilter_cfi')

### The Good vertices collection needed by the tracking failure filter ________||
process.goodVertices = cms.EDFilter(
  "VertexSelector",
  filter = cms.bool(False),
  src = cms.InputTag("offlinePrimaryVertices"),
  cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.rho < 2")
)

## The tracking failure filter _______________________________________________||
process.load('RecoMET.METFilters.trackingFailureFilter_cfi')


## switch on PAT trigger
##from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
##switchOnTrigger( process, hltProcess=options.hltProcess )
#


###############################
##### DD added trigger sel ####
###############################
##----------------- hlt filter -------------------------------------
process.hltFilter = cms.EDFilter('HLTHighLevel',
    TriggerResultsTag = cms.InputTag('TriggerResults','','HLT'),
    HLTPaths          = cms.vstring( listHLTPaths ),  
    eventSetupPathsKey = cms.string(''),
    andOr              = cms.bool(True), #---- True = OR, False = AND between the HLT paths
    throw              = cms.bool(False)
)
################################
######## DAF PV's     ##########
################################
#
pvSrc = 'offlinePrimaryVertices'
#
### The good primary vertex filter ____________________________________________||
process.primaryVertexFilter = cms.EDFilter(
    "VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake & ndof > 4 & abs(z) <= 24 & position.Rho <= 2"),
    filter = cms.bool(True)
    )

from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector

process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( maxZ = cms.double(24.0),
                                     minNdof = cms.double(4.0) # this is >= 4
                                     ),
    src=cms.InputTag(pvSrc)
    )




########################### Loading PATtuplizers
### Pat for diff jet algos
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ak4jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ak5jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ak7jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ca4jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_ca8jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_kt4jets_simple_cff')
process.load('jetSubs.MyJetSubsAnalyzer.PAT_kt8jets_simple_cff')

if options.useData:
	process.patJetCorrFactorsAK4CHS.levels.append('L2L3Residual')
	process.patJetCorrFactorsAK4CHSpruned.levels.append('L2L3Residual')
	process.patJetCorrFactorsAK4CHStrimmed.levels.append('L2L3Residual')
	process.patJetCorrFactorsAK4CHSfilteredN2.levels.append('L2L3Residual')
	process.patJetCorrFactorsAK4CHSfilteredN3.levels.append('L2L3Residual')
	process.patJetCorrFactorsAK4CHSmassDropFiltered.levels.append('L2L3Residual')

	process.patJetCorrFactorsAK5CHS.levels.append('L2L3Residual')
	process.patJetCorrFactorsAK5CHSpruned.levels.append('L2L3Residual')
	process.patJetCorrFactorsAK5CHStrimmed.levels.append('L2L3Residual')
	process.patJetCorrFactorsAK5CHSfilteredN2.levels.append('L2L3Residual')
	process.patJetCorrFactorsAK5CHSfilteredN3.levels.append('L2L3Residual')
	process.patJetCorrFactorsAK5CHSmassDropFiltered.levels.append('L2L3Residual')

	process.patJetCorrFactorsAK7CHS.levels.append('L2L3Residual')
	process.patJetCorrFactorsAK7CHSpruned.levels.append('L2L3Residual')
	process.patJetCorrFactorsAK7CHStrimmed.levels.append('L2L3Residual')
	process.patJetCorrFactorsAK7CHSfilteredN2.levels.append('L2L3Residual')
	process.patJetCorrFactorsAK7CHSfilteredN3.levels.append('L2L3Residual')
	process.patJetCorrFactorsAK7CHSmassDropFiltered.levels.append('L2L3Residual')

	process.patJetCorrFactorsCA4CHS.levels.append('L2L3Residual')
	process.patJetCorrFactorsCA4CHSpruned.levels.append('L2L3Residual')
	process.patJetCorrFactorsCA4CHStrimmed.levels.append('L2L3Residual')
	process.patJetCorrFactorsCA4CHSfilteredN2.levels.append('L2L3Residual')
	process.patJetCorrFactorsCA4CHSfilteredN3.levels.append('L2L3Residual')
	process.patJetCorrFactorsCA4CHSmassDropFiltered.levels.append('L2L3Residual')

	process.patJetCorrFactorsCA8CHS.levels.append('L2L3Residual')
	process.patJetCorrFactorsCA8CHSpruned.levels.append('L2L3Residual')
	process.patJetCorrFactorsCA8CHStrimmed.levels.append('L2L3Residual')
	process.patJetCorrFactorsCA8CHSfilteredN2.levels.append('L2L3Residual')
	process.patJetCorrFactorsCA8CHSfilteredN3.levels.append('L2L3Residual')
	process.patJetCorrFactorsCA8CHSmassDropFiltered.levels.append('L2L3Residual')

	process.patJetCorrFactorsKT4CHS.levels.append('L2L3Residual')
	process.patJetCorrFactorsKT4CHSpruned.levels.append('L2L3Residual')
	process.patJetCorrFactorsKT4CHStrimmed.levels.append('L2L3Residual')
	process.patJetCorrFactorsKT4CHSfilteredN2.levels.append('L2L3Residual')
	process.patJetCorrFactorsKT4CHSfilteredN3.levels.append('L2L3Residual')
	process.patJetCorrFactorsKT4CHSmassDropFiltered.levels.append('L2L3Residual')

	process.patJetCorrFactorsKT8CHS.levels.append('L2L3Residual')
	process.patJetCorrFactorsKT8CHSpruned.levels.append('L2L3Residual')
	process.patJetCorrFactorsKT8CHStrimmed.levels.append('L2L3Residual')
	process.patJetCorrFactorsKT8CHSfilteredN2.levels.append('L2L3Residual')
	process.patJetCorrFactorsKT8CHSfilteredN3.levels.append('L2L3Residual')
	process.patJetCorrFactorsKT8CHSmassDropFiltered.levels.append('L2L3Residual')

##-------------------- User analyzer  --------------------------------
#### MCTruth Plots
#process.MCTruthAna = cms.EDAnalyzer('MCTruthTreeProducer',
#		src = cms.InputTag('genParticles'),
#		stopMass = cms.double( mass ),
#)

######################################## AK4 Jets
process.PFJet_AK4 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK4CHSwithNsub'),
		jetsPruned       = cms.InputTag('patJetsAK4CHSprunedwithNsub'),
		jetsTrimmed      = cms.InputTag('patJetsAK4CHStrimmedwithNsub'),
		jetsFilteredN2   = cms.InputTag('patJetsAK4CHSfilteredN2withNsub'),
		jetsFilteredN3   = cms.InputTag('patJetsAK4CHSfilteredN3withNsub'),
		jetsMassDropFiltered       = cms.InputTag('patJetsAK4CHSmassDropFilteredwithNsub'),
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

######################################## AK5 Jets
process.PFJet_AK5 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK5CHSwithNsub'),
		jetsPruned       = cms.InputTag('patJetsAK5CHSprunedwithNsub'),
		jetsTrimmed      = cms.InputTag('patJetsAK5CHStrimmedwithNsub'),
		jetsFilteredN2   = cms.InputTag('patJetsAK5CHSfilteredN2withNsub'),
		jetsFilteredN3   = cms.InputTag('patJetsAK5CHSfilteredN3withNsub'),
		jetsMassDropFiltered       = cms.InputTag('patJetsAK5CHSmassDropFilteredwithNsub'),
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

######################################## AK7 Jets
process.PFJet_AK7 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsAK7CHSwithNsub'),
		jetsPruned       = cms.InputTag('patJetsAK7CHSprunedwithNsub'),
		jetsTrimmed      = cms.InputTag('patJetsAK7CHStrimmedwithNsub'),
		jetsFilteredN2   = cms.InputTag('patJetsAK7CHSfilteredN2withNsub'),
		jetsFilteredN3   = cms.InputTag('patJetsAK7CHSfilteredN3withNsub'),
		jetsMassDropFiltered       = cms.InputTag('patJetsAK7CHSmassDropFilteredwithNsub'),
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

######################################## CA4 Jets
process.PFJet_CA4 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA4CHSwithNsub'),
		jetsPruned       = cms.InputTag('patJetsCA4CHSprunedwithNsub'),
		jetsTrimmed      = cms.InputTag('patJetsCA4CHStrimmedwithNsub'),
		jetsFilteredN2   = cms.InputTag('patJetsCA4CHSfilteredN2withNsub'),
		jetsFilteredN3   = cms.InputTag('patJetsCA4CHSfilteredN3withNsub'),
		jetsMassDropFiltered       = cms.InputTag('patJetsCA4CHSmassDropFilteredwithNsub'),
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

######################################## CA8 Jets
process.PFJet_CA8 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsCA8CHSwithNsub'),
		jetsPruned       = cms.InputTag('patJetsCA8CHSprunedwithNsub'),
		jetsTrimmed      = cms.InputTag('patJetsCA8CHStrimmedwithNsub'),
		jetsFilteredN2   = cms.InputTag('patJetsCA8CHSfilteredN2withNsub'),
		jetsFilteredN3   = cms.InputTag('patJetsCA8CHSfilteredN3withNsub'),
		jetsMassDropFiltered       = cms.InputTag('patJetsCA8CHSmassDropFilteredwithNsub'),
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

######################################## KT4 Jets
process.PFJet_KT4 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT4CHSwithNsub'),
		jetsPruned       = cms.InputTag('patJetsKT4CHSprunedwithNsub'),
		jetsTrimmed      = cms.InputTag('patJetsKT4CHStrimmedwithNsub'),
		jetsFilteredN2   = cms.InputTag('patJetsKT4CHSfilteredN2withNsub'),
		jetsFilteredN3   = cms.InputTag('patJetsKT4CHSfilteredN3withNsub'),
		jetsMassDropFiltered       = cms.InputTag('patJetsKT4CHSmassDropFilteredwithNsub'),
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

######################################## KT8 Jets
process.PFJet_KT8 = cms.EDAnalyzer('PFJetTreeProducer',
		jets             = cms.InputTag('patJetsKT8CHSwithNsub'),
		jetsPruned       = cms.InputTag('patJetsKT8CHSprunedwithNsub'),
		jetsTrimmed      = cms.InputTag('patJetsKT8CHStrimmedwithNsub'),
		jetsFilteredN2   = cms.InputTag('patJetsKT8CHSfilteredN2withNsub'),
		jetsFilteredN3   = cms.InputTag('patJetsKT8CHSfilteredN3withNsub'),
		jetsMassDropFiltered       = cms.InputTag('patJetsKT8CHSmassDropFilteredwithNsub'),
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



############################################## Run Process
process.filtersSeq = cms.Sequence(
		process.hltFilter *
		process.primaryVertexFilter *
		process.noscraping *
		process.HBHENoiseFilter *
		process.CSCTightHaloFilter *
		process.hcalLaserEventFilter *
		process.EcalDeadCellTriggerPrimitiveFilter *
		process.goodVertices * process.trackingFailureFilter *
		process.eeBadScFilter
)

process.substructure = cms.Sequence( 
		process.ak4Jets * process.PFJet_AK4 * #process.PFJet_AK4Pruned * process.PFJet_AK4Trimmed * process.PFJet_AK4FilteredN2 * process.PFJet_AK4FilteredN3 * process.PFJet_AK4MassDropFiltered * 
		process.ak5Jets * process.PFJet_AK5 * #process.PFJet_AK5Pruned * process.PFJet_AK5Trimmed * process.PFJet_AK5FilteredN2 * process.PFJet_AK5FilteredN3 * process.PFJet_AK5MassDropFiltered *  
		process.ak7Jets * process.PFJet_AK7 * #process.PFJet_AK7Pruned * process.PFJet_AK7Trimmed * process.PFJet_AK7FilteredN2 * process.PFJet_AK7FilteredN3 * process.PFJet_AK7MassDropFiltered *  
		process.ca4Jets * process.PFJet_CA4 * #process.PFJet_CA4Pruned * process.PFJet_CA4Trimmed * process.PFJet_CA4FilteredN2 * process.PFJet_CA4FilteredN3 * process.PFJet_CA4MassDropFiltered *  
		process.ca8Jets * process.PFJet_CA8 * #process.PFJet_CA8Pruned * process.PFJet_CA8Trimmed * process.PFJet_CA8FilteredN2 * process.PFJet_CA8FilteredN3 * process.PFJet_CA8MassDropFiltered *  
		process.kt4Jets * process.PFJet_KT4 * #process.PFJet_KT4Pruned * process.PFJet_KT4Trimmed * process.PFJet_KT4FilteredN2 * process.PFJet_KT4FilteredN3 * process.PFJet_KT4MassDropFiltered *  
		process.kt8Jets * process.PFJet_KT8 #* process.PFJet_KT8Pruned * process.PFJet_KT8Trimmed * process.PFJet_KT8FilteredN2 * process.PFJet_KT8FilteredN3 * process.PFJet_KT8MassDropFiltered   
		)

if options.useData:
	process.p = cms.Path( process.filtersSeq * process.substructure )
else:
	process.p = cms.Path( process.substructure )


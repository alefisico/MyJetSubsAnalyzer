import FWCore.ParameterSet.Config as cms
from MySubsPATtuple.MyPATtuplizer.PAT_goodPV_cff import *

# JETS  AK1p1 ----------------------------

from RecoJets.JetProducers.ak5PFJets_cfi import ak5PFJets
ak1p1PFJetsCHS = ak5PFJets.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(30.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(1.1),
  #jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSource = 'ak1p1PFJetsCHS'

# corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactorsAK1p1CHS = patJetCorrFactors.clone()
patJetCorrFactorsAK1p1CHS.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsAK1p1CHS.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsAK1p1CHS.payload = 'AK7PFchs'
patJetCorrFactorsAK1p1CHS.useRho = True

from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cfi import *
patJetsAK1p1CHS = patJets.clone()
patJetsAK1p1CHS.jetSource = jetSource
patJetsAK1p1CHS.addJetCharge = False
patJetsAK1p1CHS.embedCaloTowers = False
patJetsAK1p1CHS.embedPFCandidates = False
patJetsAK1p1CHS.addAssociatedTracks = False
patJetsAK1p1CHS.addBTagInfo = False
patJetsAK1p1CHS.addDiscriminators = False
patJetsAK1p1CHS.addJetID = False
patJetsAK1p1CHS.addGenPartonMatch = False
patJetsAK1p1CHS.embedGenPartonMatch = False
patJetsAK1p1CHS.addGenJetMatch = False
patJetsAK1p1CHS.getJetMCFlavour = False
patJetsAK1p1CHS.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsAK1p1CHS'))

#### Adding Nsubjetiness

patJetsAK1p1CHSwithNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsAK1p1CHS"),
  cone=cms.double(0.8)
)

# JETS PRUNED AK1p1 ----------------------------

from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
ak1p1PFJetsCHSpruned = ak5PFJetsPruned.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(30.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(1.1),
  #jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSource = 'ak1p1PFJetsCHSpruned'

# corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactorsAK1p1CHSpruned = patJetCorrFactors.clone()
patJetCorrFactorsAK1p1CHSpruned.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsAK1p1CHSpruned.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsAK1p1CHSpruned.payload = 'AK7PFchs'
patJetCorrFactorsAK1p1CHSpruned.useRho = True


patJetsAK1p1CHSpruned = patJets.clone()
patJetsAK1p1CHSpruned.jetSource = jetSource
patJetsAK1p1CHSpruned.addJetCharge = False
patJetsAK1p1CHSpruned.embedCaloTowers = False
patJetsAK1p1CHSpruned.embedPFCandidates = False
patJetsAK1p1CHSpruned.addAssociatedTracks = False
patJetsAK1p1CHSpruned.addBTagInfo = False
patJetsAK1p1CHSpruned.addDiscriminators = False
patJetsAK1p1CHSpruned.addJetID = False
patJetsAK1p1CHSpruned.addGenPartonMatch = False
patJetsAK1p1CHSpruned.embedGenPartonMatch = False
patJetsAK1p1CHSpruned.addGenJetMatch = False
patJetsAK1p1CHSpruned.getJetMCFlavour = False
patJetsAK1p1CHSpruned.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsAK1p1CHSpruned'))

# JETS AK1p1 ----------------------------


ak1p1Jets = cms.Sequence(
  goodOfflinePrimaryVertices +
  pfNoPileUpSequence +
  ak1p1PFJetsCHS + 
  patJetCorrFactorsAK1p1CHS +
  patJetsAK1p1CHS +  
  patJetsAK1p1CHSwithNsub +
  ak1p1PFJetsCHSpruned +
  patJetCorrFactorsAK1p1CHSpruned +
  patJetsAK1p1CHSpruned
)

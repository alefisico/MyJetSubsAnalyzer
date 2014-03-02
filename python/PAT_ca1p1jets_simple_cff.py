import FWCore.ParameterSet.Config as cms
from MySubsPATtuple.MyPATtuplizer.PAT_goodPV_cff import *

# JETS  CA1p1 ----------------------------

from RecoJets.JetProducers.ak5PFJets_cfi import ak5PFJets
ca1p1PFJetsCHS = ak5PFJets.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(30.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(1.1),
  jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSource = 'ca1p1PFJetsCHS'

# corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactorsCA1p1CHS = patJetCorrFactors.clone()
patJetCorrFactorsCA1p1CHS.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsCA1p1CHS.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsCA1p1CHS.payload = 'AK7PFchs'
patJetCorrFactorsCA1p1CHS.useRho = True

from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cfi import *
patJetsCA1p1CHS = patJets.clone()
patJetsCA1p1CHS.jetSource = jetSource
patJetsCA1p1CHS.addJetCharge = False
patJetsCA1p1CHS.embedCaloTowers = False
patJetsCA1p1CHS.embedPFCandidates = False
patJetsCA1p1CHS.addAssociatedTracks = False
patJetsCA1p1CHS.addBTagInfo = False
patJetsCA1p1CHS.addDiscriminators = False
patJetsCA1p1CHS.addJetID = False
patJetsCA1p1CHS.addGenPartonMatch = False
patJetsCA1p1CHS.embedGenPartonMatch = False
patJetsCA1p1CHS.addGenJetMatch = False
patJetsCA1p1CHS.getJetMCFlavour = False
patJetsCA1p1CHS.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsCA1p1CHS'))

#### Adding Nsubjetiness

patJetsCA1p1CHSwithNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsCA1p1CHS"),
  cone=cms.double(0.8)
)

# JETS PRUNED CA1p1 ----------------------------

from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
ca1p1PFJetsCHSpruned = ak5PFJetsPruned.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(30.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(1.1),
  jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSource = 'ca1p1PFJetsCHSpruned'

# corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactorsCA1p1CHSpruned = patJetCorrFactors.clone()
patJetCorrFactorsCA1p1CHSpruned.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsCA1p1CHSpruned.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsCA1p1CHSpruned.payload = 'AK7PFchs'
patJetCorrFactorsCA1p1CHSpruned.useRho = True


patJetsCA1p1CHSpruned = patJets.clone()
patJetsCA1p1CHSpruned.jetSource = jetSource
patJetsCA1p1CHSpruned.addJetCharge = False
patJetsCA1p1CHSpruned.embedCaloTowers = False
patJetsCA1p1CHSpruned.embedPFCandidates = False
patJetsCA1p1CHSpruned.addAssociatedTracks = False
patJetsCA1p1CHSpruned.addBTagInfo = False
patJetsCA1p1CHSpruned.addDiscriminators = False
patJetsCA1p1CHSpruned.addJetID = False
patJetsCA1p1CHSpruned.addGenPartonMatch = False
patJetsCA1p1CHSpruned.embedGenPartonMatch = False
patJetsCA1p1CHSpruned.addGenJetMatch = False
patJetsCA1p1CHSpruned.getJetMCFlavour = False
patJetsCA1p1CHSpruned.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsCA1p1CHSpruned'))

# JETS CA1p1 ----------------------------


ca1p1Jets = cms.Sequence(
  goodOfflinePrimaryVertices +
  pfNoPileUpSequence +
  ca1p1PFJetsCHS + 
  patJetCorrFactorsCA1p1CHS +
  patJetsCA1p1CHS +  
  patJetsCA1p1CHSwithNsub +
  ca1p1PFJetsCHSpruned +
  patJetCorrFactorsCA1p1CHSpruned +
  patJetsCA1p1CHSpruned
)

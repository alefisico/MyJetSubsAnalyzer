import FWCore.ParameterSet.Config as cms
from jetSubs.MyJetSubsAnalyzer.PAT_goodPV_cff import *

# JETS  CA1p2 ----------------------------

from RecoJets.JetProducers.ak5PFJets_cfi import ak5PFJets
ca1p2PFJetsCHS = ak5PFJets.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(30.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(1.2),
  jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSource = 'ca1p2PFJetsCHS'

# corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactorsCA1p2CHS = patJetCorrFactors.clone()
patJetCorrFactorsCA1p2CHS.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsCA1p2CHS.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsCA1p2CHS.payload = 'AK7PFchs'
patJetCorrFactorsCA1p2CHS.useRho = True

from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cfi import *
patJetsCA1p2CHS = patJets.clone()
patJetsCA1p2CHS.jetSource = jetSource
patJetsCA1p2CHS.addJetCharge = False
patJetsCA1p2CHS.embedCaloTowers = False
patJetsCA1p2CHS.embedPFCandidates = False
patJetsCA1p2CHS.addAssociatedTracks = False
patJetsCA1p2CHS.addBTagInfo = False
patJetsCA1p2CHS.addDiscriminators = False
patJetsCA1p2CHS.addJetID = False
patJetsCA1p2CHS.addGenPartonMatch = False
patJetsCA1p2CHS.embedGenPartonMatch = False
patJetsCA1p2CHS.addGenJetMatch = False
patJetsCA1p2CHS.getJetMCFlavour = False
patJetsCA1p2CHS.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsCA1p2CHS'))

#### Adding Nsubjetiness

patJetsCA1p2CHSwithNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsCA1p2CHS"),
  cone=cms.double(0.8)
)

# JETS PRUNED CA1p2 ----------------------------

from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
ca1p2PFJetsCHSpruned = ak5PFJetsPruned.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(30.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(1.2),
  jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSource = 'ca1p2PFJetsCHSpruned'

# corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactorsCA1p2CHSpruned = patJetCorrFactors.clone()
patJetCorrFactorsCA1p2CHSpruned.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsCA1p2CHSpruned.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsCA1p2CHSpruned.payload = 'AK7PFchs'
patJetCorrFactorsCA1p2CHSpruned.useRho = True


patJetsCA1p2CHSpruned = patJets.clone()
patJetsCA1p2CHSpruned.jetSource = jetSource
patJetsCA1p2CHSpruned.addJetCharge = False
patJetsCA1p2CHSpruned.embedCaloTowers = False
patJetsCA1p2CHSpruned.embedPFCandidates = False
patJetsCA1p2CHSpruned.addAssociatedTracks = False
patJetsCA1p2CHSpruned.addBTagInfo = False
patJetsCA1p2CHSpruned.addDiscriminators = False
patJetsCA1p2CHSpruned.addJetID = False
patJetsCA1p2CHSpruned.addGenPartonMatch = False
patJetsCA1p2CHSpruned.embedGenPartonMatch = False
patJetsCA1p2CHSpruned.addGenJetMatch = False
patJetsCA1p2CHSpruned.getJetMCFlavour = False
patJetsCA1p2CHSpruned.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsCA1p2CHSpruned'))

# JETS CA1p2 ----------------------------


ca1p2Jets = cms.Sequence(
  goodOfflinePrimaryVertices +
  pfNoPileUpSequence +
  ca1p2PFJetsCHS + 
  patJetCorrFactorsCA1p2CHS +
  patJetsCA1p2CHS +  
  patJetsCA1p2CHSwithNsub +
  ca1p2PFJetsCHSpruned +
  patJetCorrFactorsCA1p2CHSpruned +
  patJetsCA1p2CHSpruned
)

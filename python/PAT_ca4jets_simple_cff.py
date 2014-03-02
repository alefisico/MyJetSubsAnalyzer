import FWCore.ParameterSet.Config as cms
from MySubsPATtuple.MyPATtuplizer.PAT_goodPV_cff import *

# JETS  CA4 ----------------------------

from RecoJets.JetProducers.ak5PFJets_cfi import ak5PFJets
ca4PFJetsCHS = ak5PFJets.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(30.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.4),
  jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSource = 'ca4PFJetsCHS'

# corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactorsCA4CHS = patJetCorrFactors.clone()
patJetCorrFactorsCA4CHS.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsCA4CHS.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsCA4CHS.payload = 'AK5PFchs'
patJetCorrFactorsCA4CHS.useRho = True

from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cfi import *
patJetsCA4CHS = patJets.clone()
patJetsCA4CHS.jetSource = jetSource
patJetsCA4CHS.addJetCharge = False
patJetsCA4CHS.embedCaloTowers = False
patJetsCA4CHS.embedPFCandidates = False
patJetsCA4CHS.addAssociatedTracks = False
patJetsCA4CHS.addBTagInfo = False
patJetsCA4CHS.addDiscriminators = False
patJetsCA4CHS.addJetID = False
patJetsCA4CHS.addGenPartonMatch = False
patJetsCA4CHS.embedGenPartonMatch = False
patJetsCA4CHS.addGenJetMatch = False
patJetsCA4CHS.getJetMCFlavour = False
patJetsCA4CHS.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsCA4CHS'))

#### Adding Nsubjetiness

patJetsCA4CHSwithNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsCA4CHS"),
  cone=cms.double(0.8)
)

# JETS PRUNED CA4 ----------------------------

from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
ca4PFJetsCHSpruned = ak5PFJetsPruned.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(30.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.4),
  jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSource = 'ca4PFJetsCHSpruned'

# corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactorsCA4CHSpruned = patJetCorrFactors.clone()
patJetCorrFactorsCA4CHSpruned.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsCA4CHSpruned.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsCA4CHSpruned.payload = 'AK5PFchs'
patJetCorrFactorsCA4CHSpruned.useRho = True


patJetsCA4CHSpruned = patJets.clone()
patJetsCA4CHSpruned.jetSource = jetSource
patJetsCA4CHSpruned.addJetCharge = False
patJetsCA4CHSpruned.embedCaloTowers = False
patJetsCA4CHSpruned.embedPFCandidates = False
patJetsCA4CHSpruned.addAssociatedTracks = False
patJetsCA4CHSpruned.addBTagInfo = False
patJetsCA4CHSpruned.addDiscriminators = False
patJetsCA4CHSpruned.addJetID = False
patJetsCA4CHSpruned.addGenPartonMatch = False
patJetsCA4CHSpruned.embedGenPartonMatch = False
patJetsCA4CHSpruned.addGenJetMatch = False
patJetsCA4CHSpruned.getJetMCFlavour = False
patJetsCA4CHSpruned.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsCA4CHSpruned'))

# JETS CA4 ----------------------------


ca4Jets = cms.Sequence(
  goodOfflinePrimaryVertices +
  pfNoPileUpSequence +
  ca4PFJetsCHS + 
  patJetCorrFactorsCA4CHS +
  patJetsCA4CHS +  
  patJetsCA4CHSwithNsub +
  ca4PFJetsCHSpruned +
  patJetCorrFactorsCA4CHSpruned +
  patJetsCA4CHSpruned
)

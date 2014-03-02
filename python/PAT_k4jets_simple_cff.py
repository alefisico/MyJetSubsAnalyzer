import FWCore.ParameterSet.Config as cms
from MySubsPATtuple.MyPATtuplizer.PAT_goodPV_cff import *


# JETS  KT4 ----------------------------

from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
kt4PFJetsCHS = kt4PFJets.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(30.0),
  doAreaFastjet = cms.bool(True),
  #rParam = cms.double(1.1),
  #jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSource = 'kt4PFJetsCHS'

# corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactorsKT4CHS = patJetCorrFactors.clone()
patJetCorrFactorsKT4CHS.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsKT4CHS.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsKT4CHS.payload = 'AK5PFchs'
patJetCorrFactorsKT4CHS.useRho = True

from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cfi import *
patJetsKT4CHS = patJets.clone()
patJetsKT4CHS.jetSource = jetSource
patJetsKT4CHS.addJetCharge = False
patJetsKT4CHS.embedCaloTowers = False
patJetsKT4CHS.embedPFCandidates = False
patJetsKT4CHS.addAssociatedTracks = False
patJetsKT4CHS.addBTagInfo = False
patJetsKT4CHS.addDiscriminators = False
patJetsKT4CHS.addJetID = False
patJetsKT4CHS.addGenPartonMatch = False
patJetsKT4CHS.embedGenPartonMatch = False
patJetsKT4CHS.addGenJetMatch = False
patJetsKT4CHS.getJetMCFlavour = False
patJetsKT4CHS.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsKT4CHS'))

#### Adding Nsubjetiness

patJetsKT4CHSwithNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsKT4CHS"),
  cone=cms.double(0.8)
)

# JETS PRUNED KT4 ----------------------------

from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
kt4PFJetsCHSpruned = ak5PFJetsPruned.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(30.0),
  doAreaFastjet = cms.bool(True),
  #rParam = cms.double(0.8),
  #jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSource = 'kt4PFJetsCHSpruned'

# corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactorsKT4CHSpruned = patJetCorrFactors.clone()
patJetCorrFactorsKT4CHSpruned.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsKT4CHSpruned.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsKT4CHSpruned.payload = 'AK5PFchs'
patJetCorrFactorsKT4CHSpruned.useRho = True


patJetsKT4CHSpruned = patJets.clone()
patJetsKT4CHSpruned.jetSource = jetSource
patJetsKT4CHSpruned.addJetCharge = False
patJetsKT4CHSpruned.embedCaloTowers = False
patJetsKT4CHSpruned.embedPFCandidates = False
patJetsKT4CHSpruned.addAssociatedTracks = False
patJetsKT4CHSpruned.addBTagInfo = False
patJetsKT4CHSpruned.addDiscriminators = False
patJetsKT4CHSpruned.addJetID = False
patJetsKT4CHSpruned.addGenPartonMatch = False
patJetsKT4CHSpruned.embedGenPartonMatch = False
patJetsKT4CHSpruned.addGenJetMatch = False
patJetsKT4CHSpruned.getJetMCFlavour = False
patJetsKT4CHSpruned.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsKT4CHSpruned'))

# JETS KT4 ----------------------------


kt4Jets = cms.Sequence(
  goodOfflinePrimaryVertices +
  pfNoPileUpSequence +
  kt4PFJetsCHS + 
  patJetCorrFactorsKT4CHS +
  patJetsKT4CHS +  
  patJetsKT4CHSwithNsub +
  kt4PFJetsCHSpruned +
  patJetCorrFactorsKT4CHSpruned +
  patJetsKT4CHSpruned
)

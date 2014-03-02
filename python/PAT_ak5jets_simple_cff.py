import FWCore.ParameterSet.Config as cms
from MySubsPATtuple.MyPATtuplizer.PAT_goodPV_cff import *


# JETS  AK5 ----------------------------

from RecoJets.JetProducers.ak5PFJets_cfi import ak5PFJets
ak5PFJetsCHS = ak5PFJets.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(30.0),
  doAreaFastjet = cms.bool(True),
  #rParam = cms.double(1.1),
  #jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSource = 'ak5PFJetsCHS'

# corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactorsAK5CHS = patJetCorrFactors.clone()
patJetCorrFactorsAK5CHS.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsAK5CHS.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsAK5CHS.payload = 'AK5PFchs'
patJetCorrFactorsAK5CHS.useRho = True

from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cfi import *
patJetsAK5CHS = patJets.clone()
patJetsAK5CHS.jetSource = jetSource
patJetsAK5CHS.addJetCharge = False
patJetsAK5CHS.embedCaloTowers = False
patJetsAK5CHS.embedPFCandidates = False
patJetsAK5CHS.addAssociatedTracks = False
patJetsAK5CHS.addBTagInfo = False
patJetsAK5CHS.addDiscriminators = False
patJetsAK5CHS.addJetID = False
patJetsAK5CHS.addGenPartonMatch = False
patJetsAK5CHS.embedGenPartonMatch = False
patJetsAK5CHS.addGenJetMatch = False
patJetsAK5CHS.getJetMCFlavour = False
patJetsAK5CHS.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsAK5CHS'))

#### Adding Nsubjetiness

patJetsAK5CHSwithNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsAK5CHS"),
  cone=cms.double(0.8)
)

# JETS PRUNED AK5 ----------------------------

from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
ak5PFJetsCHSpruned = ak5PFJetsPruned.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(30.0),
  doAreaFastjet = cms.bool(True),
  #rParam = cms.double(0.8),
  #jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSource = 'ak5PFJetsCHSpruned'

# corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactorsAK5CHSpruned = patJetCorrFactors.clone()
patJetCorrFactorsAK5CHSpruned.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsAK5CHSpruned.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsAK5CHSpruned.payload = 'AK5PFchs'
patJetCorrFactorsAK5CHSpruned.useRho = True


patJetsAK5CHSpruned = patJets.clone()
patJetsAK5CHSpruned.jetSource = jetSource
patJetsAK5CHSpruned.addJetCharge = False
patJetsAK5CHSpruned.embedCaloTowers = False
patJetsAK5CHSpruned.embedPFCandidates = False
patJetsAK5CHSpruned.addAssociatedTracks = False
patJetsAK5CHSpruned.addBTagInfo = False
patJetsAK5CHSpruned.addDiscriminators = False
patJetsAK5CHSpruned.addJetID = False
patJetsAK5CHSpruned.addGenPartonMatch = False
patJetsAK5CHSpruned.embedGenPartonMatch = False
patJetsAK5CHSpruned.addGenJetMatch = False
patJetsAK5CHSpruned.getJetMCFlavour = False
patJetsAK5CHSpruned.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsAK5CHSpruned'))

# JETS AK5 ----------------------------


ak5Jets = cms.Sequence(
  goodOfflinePrimaryVertices +
  pfNoPileUpSequence +
  ak5PFJetsCHS + 
  patJetCorrFactorsAK5CHS +
  patJetsAK5CHS +  
  patJetsAK5CHSwithNsub +
  ak5PFJetsCHSpruned +
  patJetCorrFactorsAK5CHSpruned +
  patJetsAK5CHSpruned
)

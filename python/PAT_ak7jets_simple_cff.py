import FWCore.ParameterSet.Config as cms
from MySubsPATtuple.MyPATtuplizer.PAT_goodPV_cff import *

# JETS  AK7 ----------------------------

from RecoJets.JetProducers.ak5PFJets_cfi import ak5PFJets
ak7PFJetsCHS = ak5PFJets.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(30.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.7),
  #jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSource = 'ak7PFJetsCHS'

# corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactorsAK7CHS = patJetCorrFactors.clone()
patJetCorrFactorsAK7CHS.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsAK7CHS.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsAK7CHS.payload = 'AK7PFchs'
patJetCorrFactorsAK7CHS.useRho = True

from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cfi import *
patJetsAK7CHS = patJets.clone()
patJetsAK7CHS.jetSource = jetSource
patJetsAK7CHS.addJetCharge = False
patJetsAK7CHS.embedCaloTowers = False
patJetsAK7CHS.embedPFCandidates = False
patJetsAK7CHS.addAssociatedTracks = False
patJetsAK7CHS.addBTagInfo = False
patJetsAK7CHS.addDiscriminators = False
patJetsAK7CHS.addJetID = False
patJetsAK7CHS.addGenPartonMatch = False
patJetsAK7CHS.embedGenPartonMatch = False
patJetsAK7CHS.addGenJetMatch = False
patJetsAK7CHS.getJetMCFlavour = False
patJetsAK7CHS.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsAK7CHS'))

#### Adding Nsubjetiness

patJetsAK7CHSwithNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsAK7CHS"),
  cone=cms.double(0.8)
)

# JETS PRUNED AK7 ----------------------------

from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
ak7PFJetsCHSpruned = ak5PFJetsPruned.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(30.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.7),
  #jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSource = 'ak7PFJetsCHSpruned'

# corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactorsAK7CHSpruned = patJetCorrFactors.clone()
patJetCorrFactorsAK7CHSpruned.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsAK7CHSpruned.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsAK7CHSpruned.payload = 'AK7PFchs'
patJetCorrFactorsAK7CHSpruned.useRho = True


patJetsAK7CHSpruned = patJets.clone()
patJetsAK7CHSpruned.jetSource = jetSource
patJetsAK7CHSpruned.addJetCharge = False
patJetsAK7CHSpruned.embedCaloTowers = False
patJetsAK7CHSpruned.embedPFCandidates = False
patJetsAK7CHSpruned.addAssociatedTracks = False
patJetsAK7CHSpruned.addBTagInfo = False
patJetsAK7CHSpruned.addDiscriminators = False
patJetsAK7CHSpruned.addJetID = False
patJetsAK7CHSpruned.addGenPartonMatch = False
patJetsAK7CHSpruned.embedGenPartonMatch = False
patJetsAK7CHSpruned.addGenJetMatch = False
patJetsAK7CHSpruned.getJetMCFlavour = False
patJetsAK7CHSpruned.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsAK7CHSpruned'))

# JETS AK7 ----------------------------


ak7Jets = cms.Sequence(
  goodOfflinePrimaryVertices +
  pfNoPileUpSequence +
  ak7PFJetsCHS + 
  patJetCorrFactorsAK7CHS +
  patJetsAK7CHS +  
  patJetsAK7CHSwithNsub +
  ak7PFJetsCHSpruned +
  patJetCorrFactorsAK7CHSpruned +
  patJetsAK7CHSpruned
)

import FWCore.ParameterSet.Config as cms
from MySubsPATtuple.MyPATtuplizer.PAT_goodPV_cff import *


# JETS  AK4 ----------------------------

from RecoJets.JetProducers.ak5PFJets_cfi import ak5PFJets
ak4PFJetsCHS = ak5PFJets.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(30.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.4),
  #jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSource = 'ak4PFJetsCHS'

# corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactorsAK4CHS = patJetCorrFactors.clone()
patJetCorrFactorsAK4CHS.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsAK4CHS.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsAK4CHS.payload = 'AK5PFchs'
patJetCorrFactorsAK4CHS.useRho = True

from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cfi import *
patJetsAK4CHS = patJets.clone()
patJetsAK4CHS.jetSource = jetSource
patJetsAK4CHS.addJetCharge = False
patJetsAK4CHS.embedCaloTowers = False
patJetsAK4CHS.embedPFCandidates = False
patJetsAK4CHS.addAssociatedTracks = False
patJetsAK4CHS.addBTagInfo = False
patJetsAK4CHS.addDiscriminators = False
patJetsAK4CHS.addJetID = False
patJetsAK4CHS.addGenPartonMatch = False
patJetsAK4CHS.embedGenPartonMatch = False
patJetsAK4CHS.addGenJetMatch = False
patJetsAK4CHS.getJetMCFlavour = False
patJetsAK4CHS.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsAK4CHS'))

#### Adding Nsubjetiness

patJetsAK4CHSwithNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsAK4CHS"),
  cone=cms.double(0.8)
)

# JETS PRUNED AK4 ----------------------------

from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
ak4PFJetsCHSpruned = ak5PFJetsPruned.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(30.0),
  doAreaFastjet = cms.bool(True),
  #rParam = cms.double(0.8),
  #jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSource = 'ak4PFJetsCHSpruned'

# corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactorsAK4CHSpruned = patJetCorrFactors.clone()
patJetCorrFactorsAK4CHSpruned.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsAK4CHSpruned.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsAK4CHSpruned.payload = 'AK5PFchs'
patJetCorrFactorsAK4CHSpruned.useRho = True


patJetsAK4CHSpruned = patJets.clone()
patJetsAK4CHSpruned.jetSource = jetSource
patJetsAK4CHSpruned.addJetCharge = False
patJetsAK4CHSpruned.embedCaloTowers = False
patJetsAK4CHSpruned.embedPFCandidates = False
patJetsAK4CHSpruned.addAssociatedTracks = False
patJetsAK4CHSpruned.addBTagInfo = False
patJetsAK4CHSpruned.addDiscriminators = False
patJetsAK4CHSpruned.addJetID = False
patJetsAK4CHSpruned.addGenPartonMatch = False
patJetsAK4CHSpruned.embedGenPartonMatch = False
patJetsAK4CHSpruned.addGenJetMatch = False
patJetsAK4CHSpruned.getJetMCFlavour = False
patJetsAK4CHSpruned.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsAK4CHSpruned'))

# JETS AK4 ----------------------------


ak4Jets = cms.Sequence(
  goodOfflinePrimaryVertices +
  pfNoPileUpSequence +
  ak4PFJetsCHS + 
  patJetCorrFactorsAK4CHS +
  patJetsAK4CHS +  
  patJetsAK4CHSwithNsub +
  ak4PFJetsCHSpruned +
  patJetCorrFactorsAK4CHSpruned +
  patJetsAK4CHSpruned
)

######## JETS  AK4 ----------------------------
import FWCore.ParameterSet.Config as cms
from jetSubs.MyJetSubsAnalyzer.PAT_goodPV_cff import *

############################################## NO GROOMING
from RecoJets.JetProducers.ak5PFJets_cfi import ak5PFJets
ak4PFJetsCHS = ak5PFJets.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.4),
)
jetSource = 'ak4PFJetsCHS'

#### Adding corrections 
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

####### Adding jets without JEC (just for comaprison)
#patJetCorrFactorsAK4CHSNOJEC = patJetCorrFactors.clone()
#patJetCorrFactorsAK4CHSNOJEC.src = jetSource
#patJetCorrFactorsAK4CHSNOJEC.levels = []
##patJetCorrFactorsAK4CHSNOJEC.payload = 'AK4PFchs'
##patJetCorrFactorsAK4CHSNOJEC.useRho = True
#patJetsAK4CHSNOJEC = patJets.clone()
#patJetsAK4CHSNOJEC.jetSource = jetSource
#patJetsAK4CHSNOJEC.addJetCharge = False
#patJetsAK4CHSNOJEC.embedCaloTowers = False
#patJetsAK4CHSNOJEC.embedPFCandidates = False
#patJetsAK4CHSNOJEC.addAssociatedTracks = False
#patJetsAK4CHSNOJEC.addBTagInfo = False
#patJetsAK4CHSNOJEC.addDiscriminators = False
#patJetsAK4CHSNOJEC.addJetID = False
#patJetsAK4CHSNOJEC.addGenPartonMatch = False
#patJetsAK4CHSNOJEC.embedGenPartonMatch = False
#patJetsAK4CHSNOJEC.addGenJetMatch = False
#patJetsAK4CHSNOJEC.getJetMCFlavour = False
#patJetsAK4CHSNOJEC.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsAK4CHSNOJEC'))

#### Adding Nsubjetiness
patJetsAK4CHSwithNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsAK4CHS"),
  cone=cms.double(0.4)
)

####################################################### PRUNNING
from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
ak4PFJetsCHSpruned = ak5PFJetsPruned.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.4),
  jetAlgorithm = cms.string("AntiKt"),
)
jetSourcePruned = 'ak4PFJetsCHSpruned'

# corrections 
patJetCorrFactorsAK4CHSpruned = patJetCorrFactors.clone()
patJetCorrFactorsAK4CHSpruned.src = jetSourcePruned
patJetCorrFactorsAK4CHSpruned.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsAK4CHSpruned.payload = 'AK5PFchs'
patJetCorrFactorsAK4CHSpruned.useRho = True

patJetsAK4CHSpruned = patJets.clone()
patJetsAK4CHSpruned.jetSource = jetSourcePruned
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

#### Adding Nsubjetiness
patJetsAK4CHSprunedwithNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsAK4CHSpruned"),
  cone=cms.double(0.4)
)

################################################################ TRIMMING
from RecoJets.JetProducers.ak5PFJetsTrimmed_cfi import ak5PFJetsTrimmed
ak4PFJetsCHStrimmed = ak5PFJetsTrimmed.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.4),
  jetAlgorithm = cms.string("AntiKt"),
)
jetSourceTrimmed = 'ak4PFJetsCHStrimmed'

# corrections 
patJetCorrFactorsAK4CHStrimmed = patJetCorrFactors.clone()
patJetCorrFactorsAK4CHStrimmed.src = jetSourceTrimmed
patJetCorrFactorsAK4CHStrimmed.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsAK4CHStrimmed.payload = 'AK5PFchs'
patJetCorrFactorsAK4CHStrimmed.useRho = True

### pats
patJetsAK4CHStrimmed = patJets.clone()
patJetsAK4CHStrimmed.jetSource = jetSourceTrimmed
patJetsAK4CHStrimmed.addJetCharge = False
patJetsAK4CHStrimmed.embedCaloTowers = False
patJetsAK4CHStrimmed.embedPFCandidates = False
patJetsAK4CHStrimmed.addAssociatedTracks = False
patJetsAK4CHStrimmed.addBTagInfo = False
patJetsAK4CHStrimmed.addDiscriminators = False
patJetsAK4CHStrimmed.addJetID = False
patJetsAK4CHStrimmed.addGenPartonMatch = False
patJetsAK4CHStrimmed.embedGenPartonMatch = False
patJetsAK4CHStrimmed.addGenJetMatch = False
patJetsAK4CHStrimmed.getJetMCFlavour = False
patJetsAK4CHStrimmed.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsAK4CHStrimmed'))

#### Adding Nsubjetiness
patJetsAK4CHStrimmedwithNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsAK4CHStrimmed"),
  cone=cms.double(0.4)
)

############################################################### FILTERING
from RecoJets.JetProducers.ak5PFJetsFiltered_cfi import ak5PFJetsFiltered
ak4PFJetsCHSfilteredN2 = ak5PFJetsFiltered.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  nFilt = cms.int32(2),
  rParam = cms.double(0.4),
  jetAlgorithm = cms.string("AntiKt"),
)

jetSourceFilteredN2 = 'ak4PFJetsCHSfilteredN2'

# corrections 
patJetCorrFactorsAK4CHSfilteredN2 = patJetCorrFactors.clone()
patJetCorrFactorsAK4CHSfilteredN2.src = jetSourceFilteredN2
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsAK4CHSfilteredN2.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsAK4CHSfilteredN2.payload = 'AK5PFchs'
patJetCorrFactorsAK4CHSfilteredN2.useRho = True

patJetsAK4CHSfilteredN2 = patJets.clone()
patJetsAK4CHSfilteredN2.jetSource = jetSourceFilteredN2
patJetsAK4CHSfilteredN2.addJetCharge = False
patJetsAK4CHSfilteredN2.embedCaloTowers = False
patJetsAK4CHSfilteredN2.embedPFCandidates = False
patJetsAK4CHSfilteredN2.addAssociatedTracks = False
patJetsAK4CHSfilteredN2.addBTagInfo = False
patJetsAK4CHSfilteredN2.addDiscriminators = False
patJetsAK4CHSfilteredN2.addJetID = False
patJetsAK4CHSfilteredN2.addGenPartonMatch = False
patJetsAK4CHSfilteredN2.embedGenPartonMatch = False
patJetsAK4CHSfilteredN2.addGenJetMatch = False
patJetsAK4CHSfilteredN2.getJetMCFlavour = False
patJetsAK4CHSfilteredN2.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsAK4CHSfilteredN2'))

#### Adding Nsubjetiness
patJetsAK4CHSfilteredN2withNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsAK4CHSfilteredN2"),
  cone=cms.double(0.4)
)

ak4PFJetsCHSfilteredN3 = ak5PFJetsFiltered.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  nFilt = cms.int32(3),
  rParam = cms.double(0.4),
  jetAlgorithm = cms.string("AntiKt"),
)

jetSourceFilteredN3 = 'ak4PFJetsCHSfilteredN3'

# corrections 
patJetCorrFactorsAK4CHSfilteredN3 = patJetCorrFactors.clone()
patJetCorrFactorsAK4CHSfilteredN3.src = jetSourceFilteredN3
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsAK4CHSfilteredN3.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsAK4CHSfilteredN3.payload = 'AK5PFchs'
patJetCorrFactorsAK4CHSfilteredN3.useRho = True

patJetsAK4CHSfilteredN3 = patJets.clone()
patJetsAK4CHSfilteredN3.jetSource = jetSourceFilteredN3
patJetsAK4CHSfilteredN3.addJetCharge = False
patJetsAK4CHSfilteredN3.embedCaloTowers = False
patJetsAK4CHSfilteredN3.embedPFCandidates = False
patJetsAK4CHSfilteredN3.addAssociatedTracks = False
patJetsAK4CHSfilteredN3.addBTagInfo = False
patJetsAK4CHSfilteredN3.addDiscriminators = False
patJetsAK4CHSfilteredN3.addJetID = False
patJetsAK4CHSfilteredN3.addGenPartonMatch = False
patJetsAK4CHSfilteredN3.embedGenPartonMatch = False
patJetsAK4CHSfilteredN3.addGenJetMatch = False
patJetsAK4CHSfilteredN3.getJetMCFlavour = False
patJetsAK4CHSfilteredN3.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsAK4CHSfilteredN3'))

#### Adding Nsubjetiness
patJetsAK4CHSfilteredN3withNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsAK4CHSfilteredN3"),
  cone=cms.double(0.4)
)


############################################################### MassDropFilter
from RecoJets.JetProducers.ak5PFJetsFiltered_cfi import ak5PFJetsMassDropFiltered
ak4PFJetsCHSmassDropFiltered = ak5PFJetsMassDropFiltered.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.4),
  jetAlgorithm = cms.string("AntiKt"),
)

jetSourceMassDropFiltered = 'ak4PFJetsCHSmassDropFiltered'

# corrections 
patJetCorrFactorsAK4CHSmassDropFiltered = patJetCorrFactors.clone()
patJetCorrFactorsAK4CHSmassDropFiltered.src = jetSourceMassDropFiltered
patJetCorrFactorsAK4CHSmassDropFiltered.levels == ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsAK4CHSmassDropFiltered.payload = 'AK5PFchs'
patJetCorrFactorsAK4CHSmassDropFiltered.useRho = True

patJetsAK4CHSmassDropFiltered = patJets.clone()
patJetsAK4CHSmassDropFiltered.jetSource = jetSourceMassDropFiltered
patJetsAK4CHSmassDropFiltered.addJetCharge = False
patJetsAK4CHSmassDropFiltered.embedCaloTowers = False
patJetsAK4CHSmassDropFiltered.embedPFCandidates = False
patJetsAK4CHSmassDropFiltered.addAssociatedTracks = False
patJetsAK4CHSmassDropFiltered.addBTagInfo = False
patJetsAK4CHSmassDropFiltered.addDiscriminators = False
patJetsAK4CHSmassDropFiltered.addJetID = False
patJetsAK4CHSmassDropFiltered.addGenPartonMatch = False
patJetsAK4CHSmassDropFiltered.embedGenPartonMatch = False
patJetsAK4CHSmassDropFiltered.addGenJetMatch = False
patJetsAK4CHSmassDropFiltered.getJetMCFlavour = False
patJetsAK4CHSmassDropFiltered.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsAK4CHSmassDropFiltered'))

#### Adding Nsubjetiness
patJetsAK4CHSmassDropFilteredwithNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsAK4CHSmassDropFiltered"),
  cone=cms.double(0.4)
)





# JETS AK4 ----------------------------

ak4Jets = cms.Sequence(
  goodOfflinePrimaryVertices +
  pfNoPileUpSequence +
  ak4PFJetsCHS + 
  patJetCorrFactorsAK4CHS +
  patJetsAK4CHS +  
#  patJetCorrFactorsAK4CHSNOJEC +
#  patJetsAK4CHSNOJEC +  
  patJetsAK4CHSwithNsub +
  ak4PFJetsCHSpruned +
  patJetCorrFactorsAK4CHSpruned +
  patJetsAK4CHSpruned +
  patJetsAK4CHSprunedwithNsub +
  ak4PFJetsCHStrimmed +
  patJetCorrFactorsAK4CHStrimmed +
  patJetsAK4CHStrimmed +
  patJetsAK4CHStrimmedwithNsub +
  ak4PFJetsCHSfilteredN2 +
  patJetCorrFactorsAK4CHSfilteredN2 +
  patJetsAK4CHSfilteredN2 +
  patJetsAK4CHSfilteredN2withNsub + 
  ak4PFJetsCHSfilteredN3 +
  patJetCorrFactorsAK4CHSfilteredN3 +
  patJetsAK4CHSfilteredN3 +
  patJetsAK4CHSfilteredN3withNsub + 
  ak4PFJetsCHSmassDropFiltered +
  patJetCorrFactorsAK4CHSmassDropFiltered +
  patJetsAK4CHSmassDropFiltered +
  patJetsAK4CHSmassDropFilteredwithNsub
)

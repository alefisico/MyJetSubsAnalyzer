######## JETS  CA4 ----------------------------
import FWCore.ParameterSet.Config as cms
from jetSubs.MyJetSubsAnalyzer.PAT_goodPV_cff import *

############################################## NO GROOMING
from RecoJets.JetProducers.ca4PFJets_cfi import ca4PFJets
ca4PFJetsCHS = ca4PFJets.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.4),
)
jetSource = 'ca4PFJetsCHS'

#### Adding corrections 
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

####### Adding jets without JEC (just for comaprison)
#patJetCorrFactorsCA4CHSNOJEC = patJetCorrFactors.clone()
#patJetCorrFactorsCA4CHSNOJEC.src = jetSource
#patJetCorrFactorsCA4CHSNOJEC.levels = []
##patJetCorrFactorsCA4CHSNOJEC.payload = 'CA4PFchs'
##patJetCorrFactorsCA4CHSNOJEC.useRho = True
#patJetsCA4CHSNOJEC = patJets.clone()
#patJetsCA4CHSNOJEC.jetSource = jetSource
#patJetsCA4CHSNOJEC.addJetCharge = False
#patJetsCA4CHSNOJEC.embedCaloTowers = False
#patJetsCA4CHSNOJEC.embedPFCandidates = False
#patJetsCA4CHSNOJEC.addAssociatedTracks = False
#patJetsCA4CHSNOJEC.addBTagInfo = False
#patJetsCA4CHSNOJEC.addDiscriminators = False
#patJetsCA4CHSNOJEC.addJetID = False
#patJetsCA4CHSNOJEC.addGenPartonMatch = False
#patJetsCA4CHSNOJEC.embedGenPartonMatch = False
#patJetsCA4CHSNOJEC.addGenJetMatch = False
#patJetsCA4CHSNOJEC.getJetMCFlavour = False
#patJetsCA4CHSNOJEC.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsCA4CHSNOJEC'))

#### Adding Nsubjetiness
patJetsCA4CHSwithNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsCA4CHS"),
  cone=cms.double(0.4)
)

####################################################### PRUNNING
from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
ca4PFJetsCHSpruned = ak5PFJetsPruned.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.4),
  jetAlgorithm = cms.string("CambridgeAachen"),
)
jetSourcePruned = 'ca4PFJetsCHSpruned'

# corrections 
patJetCorrFactorsCA4CHSpruned = patJetCorrFactors.clone()
patJetCorrFactorsCA4CHSpruned.src = jetSourcePruned
patJetCorrFactorsCA4CHSpruned.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsCA4CHSpruned.payload = 'AK5PFchs'
patJetCorrFactorsCA4CHSpruned.useRho = True

patJetsCA4CHSpruned = patJets.clone()
patJetsCA4CHSpruned.jetSource = jetSourcePruned
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

#### Adding Nsubjetiness
patJetsCA4CHSprunedwithNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsCA4CHSpruned"),
  cone=cms.double(0.4)
)

################################################################ TRIMMING
from RecoJets.JetProducers.ak5PFJetsTrimmed_cfi import ak5PFJetsTrimmed
ca4PFJetsCHStrimmed = ak5PFJetsTrimmed.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.4),
  jetAlgorithm = cms.string("CambridgeAachen"),
)
jetSourceTrimmed = 'ca4PFJetsCHStrimmed'

# corrections 
patJetCorrFactorsCA4CHStrimmed = patJetCorrFactors.clone()
patJetCorrFactorsCA4CHStrimmed.src = jetSourceTrimmed
patJetCorrFactorsCA4CHStrimmed.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsCA4CHStrimmed.payload = 'AK5PFchs'
patJetCorrFactorsCA4CHStrimmed.useRho = True

### pats
patJetsCA4CHStrimmed = patJets.clone()
patJetsCA4CHStrimmed.jetSource = jetSourceTrimmed
patJetsCA4CHStrimmed.addJetCharge = False
patJetsCA4CHStrimmed.embedCaloTowers = False
patJetsCA4CHStrimmed.embedPFCandidates = False
patJetsCA4CHStrimmed.addAssociatedTracks = False
patJetsCA4CHStrimmed.addBTagInfo = False
patJetsCA4CHStrimmed.addDiscriminators = False
patJetsCA4CHStrimmed.addJetID = False
patJetsCA4CHStrimmed.addGenPartonMatch = False
patJetsCA4CHStrimmed.embedGenPartonMatch = False
patJetsCA4CHStrimmed.addGenJetMatch = False
patJetsCA4CHStrimmed.getJetMCFlavour = False
patJetsCA4CHStrimmed.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsCA4CHStrimmed'))

#### Adding Nsubjetiness
patJetsCA4CHStrimmedwithNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsCA4CHStrimmed"),
  cone=cms.double(0.4)
)

############################################################### FILTERING
from RecoJets.JetProducers.ak5PFJetsFiltered_cfi import ak5PFJetsFiltered
ca4PFJetsCHSfilteredN2 = ak5PFJetsFiltered.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  nFilt = cms.int32(2),
  rParam = cms.double(0.4),
  jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSourceFilteredN2 = 'ca4PFJetsCHSfilteredN2'

# corrections 
patJetCorrFactorsCA4CHSfilteredN2 = patJetCorrFactors.clone()
patJetCorrFactorsCA4CHSfilteredN2.src = jetSourceFilteredN2
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsCA4CHSfilteredN2.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsCA4CHSfilteredN2.payload = 'AK5PFchs'
patJetCorrFactorsCA4CHSfilteredN2.useRho = True

patJetsCA4CHSfilteredN2 = patJets.clone()
patJetsCA4CHSfilteredN2.jetSource = jetSourceFilteredN2
patJetsCA4CHSfilteredN2.addJetCharge = False
patJetsCA4CHSfilteredN2.embedCaloTowers = False
patJetsCA4CHSfilteredN2.embedPFCandidates = False
patJetsCA4CHSfilteredN2.addAssociatedTracks = False
patJetsCA4CHSfilteredN2.addBTagInfo = False
patJetsCA4CHSfilteredN2.addDiscriminators = False
patJetsCA4CHSfilteredN2.addJetID = False
patJetsCA4CHSfilteredN2.addGenPartonMatch = False
patJetsCA4CHSfilteredN2.embedGenPartonMatch = False
patJetsCA4CHSfilteredN2.addGenJetMatch = False
patJetsCA4CHSfilteredN2.getJetMCFlavour = False
patJetsCA4CHSfilteredN2.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsCA4CHSfilteredN2'))

#### Adding Nsubjetiness
patJetsCA4CHSfilteredN2withNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsCA4CHSfilteredN2"),
  cone=cms.double(0.4)
)

ca4PFJetsCHSfilteredN3 = ak5PFJetsFiltered.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  nFilt = cms.int32(3),
  rParam = cms.double(0.4),
  jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSourceFilteredN3 = 'ca4PFJetsCHSfilteredN3'

# corrections 
patJetCorrFactorsCA4CHSfilteredN3 = patJetCorrFactors.clone()
patJetCorrFactorsCA4CHSfilteredN3.src = jetSourceFilteredN3
# will need to add L2L3 corrections in the cfg
patJetCorrFactorsCA4CHSfilteredN3.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsCA4CHSfilteredN3.payload = 'AK5PFchs'
patJetCorrFactorsCA4CHSfilteredN3.useRho = True

patJetsCA4CHSfilteredN3 = patJets.clone()
patJetsCA4CHSfilteredN3.jetSource = jetSourceFilteredN3
patJetsCA4CHSfilteredN3.addJetCharge = False
patJetsCA4CHSfilteredN3.embedCaloTowers = False
patJetsCA4CHSfilteredN3.embedPFCandidates = False
patJetsCA4CHSfilteredN3.addAssociatedTracks = False
patJetsCA4CHSfilteredN3.addBTagInfo = False
patJetsCA4CHSfilteredN3.addDiscriminators = False
patJetsCA4CHSfilteredN3.addJetID = False
patJetsCA4CHSfilteredN3.addGenPartonMatch = False
patJetsCA4CHSfilteredN3.embedGenPartonMatch = False
patJetsCA4CHSfilteredN3.addGenJetMatch = False
patJetsCA4CHSfilteredN3.getJetMCFlavour = False
patJetsCA4CHSfilteredN3.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsCA4CHSfilteredN3'))

#### Adding Nsubjetiness
patJetsCA4CHSfilteredN3withNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsCA4CHSfilteredN3"),
  cone=cms.double(0.4)
)


############################################################### MassDropFilter
from RecoJets.JetProducers.ak5PFJetsFiltered_cfi import ak5PFJetsMassDropFiltered
ca4PFJetsCHSmassDropFiltered = ak5PFJetsMassDropFiltered.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.4),
  jetAlgorithm = cms.string("CambridgeAachen"),
)

jetSourceMassDropFiltered = 'ca4PFJetsCHSmassDropFiltered'

# corrections 
patJetCorrFactorsCA4CHSmassDropFiltered = patJetCorrFactors.clone()
patJetCorrFactorsCA4CHSmassDropFiltered.src = jetSourceMassDropFiltered
patJetCorrFactorsCA4CHSmassDropFiltered.levels == ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactorsCA4CHSmassDropFiltered.payload = 'AK5PFchs'
patJetCorrFactorsCA4CHSmassDropFiltered.useRho = True

patJetsCA4CHSmassDropFiltered = patJets.clone()
patJetsCA4CHSmassDropFiltered.jetSource = jetSourceMassDropFiltered
patJetsCA4CHSmassDropFiltered.addJetCharge = False
patJetsCA4CHSmassDropFiltered.embedCaloTowers = False
patJetsCA4CHSmassDropFiltered.embedPFCandidates = False
patJetsCA4CHSmassDropFiltered.addAssociatedTracks = False
patJetsCA4CHSmassDropFiltered.addBTagInfo = False
patJetsCA4CHSmassDropFiltered.addDiscriminators = False
patJetsCA4CHSmassDropFiltered.addJetID = False
patJetsCA4CHSmassDropFiltered.addGenPartonMatch = False
patJetsCA4CHSmassDropFiltered.embedGenPartonMatch = False
patJetsCA4CHSmassDropFiltered.addGenJetMatch = False
patJetsCA4CHSmassDropFiltered.getJetMCFlavour = False
patJetsCA4CHSmassDropFiltered.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactorsCA4CHSmassDropFiltered'))

#### Adding Nsubjetiness
patJetsCA4CHSmassDropFilteredwithNsub = cms.EDProducer("NjettinessAdder",
  src=cms.InputTag("patJetsCA4CHSmassDropFiltered"),
  cone=cms.double(0.4)
)





# JETS CA4 ----------------------------

ca4Jets = cms.Sequence(
  goodOfflinePrimaryVertices +
  pfNoPileUpSequence +
  ca4PFJetsCHS + 
  patJetCorrFactorsCA4CHS +
  patJetsCA4CHS +  
#  patJetCorrFactorsCA4CHSNOJEC +
#  patJetsCA4CHSNOJEC +  
  patJetsCA4CHSwithNsub +
  ca4PFJetsCHSpruned +
  patJetCorrFactorsCA4CHSpruned +
  patJetsCA4CHSpruned +
  patJetsCA4CHSprunedwithNsub +
  ca4PFJetsCHStrimmed +
  patJetCorrFactorsCA4CHStrimmed +
  patJetsCA4CHStrimmed +
  patJetsCA4CHStrimmedwithNsub +
  ca4PFJetsCHSfilteredN2 +
  patJetCorrFactorsCA4CHSfilteredN2 +
  patJetsCA4CHSfilteredN2 +
  patJetsCA4CHSfilteredN2withNsub + 
  ca4PFJetsCHSfilteredN3 +
  patJetCorrFactorsCA4CHSfilteredN3 +
  patJetsCA4CHSfilteredN3 +
  patJetsCA4CHSfilteredN3withNsub + 
  ca4PFJetsCHSmassDropFiltered +
  patJetCorrFactorsCA4CHSmassDropFiltered +
  patJetsCA4CHSmassDropFiltered +
  patJetsCA4CHSmassDropFilteredwithNsub
)

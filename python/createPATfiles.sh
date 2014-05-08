#!/bin/bash 

jetAlgo=( AK CA KT )
jetalgo=( ak ca kt )
jetAlgoProd=( ak5 ca4 kt4 )
jetAlgoName=( "AntiKt" "CambridgeAachen" "Kt" )
coneSize=( 4 5 7 8 )
coneSizeCorr=( AK5 AK5 AK7 AK7 )

jetAlgo_elements=${#jetAlgo[@]}
coneSize_elements=${#coneSize[@]}

for ((j=0;j<$jetAlgo_elements;j++));
do 
	for ((i=0;i<$coneSize_elements;i++));
	do 
		OUTFILE='PAT_'${jetalgo[${j}]}${coneSize[${i}]}'jets_simple_cff.py'
		/bin/rm -f $OUTFILE
		echo "######## JETS  ${jetAlgo[${j}]}${coneSize[${i}]} ----------------------------
import FWCore.ParameterSet.Config as cms
from jetSubs.MyJetSubsAnalyzer.PAT_goodPV_cff import *

############################################## NO GROOMING
from RecoJets.JetProducers.${jetAlgoProd[${j}]}PFJets_cfi import ${jetAlgoProd[${j}]}PFJets
${jetalgo[${j}]}${coneSize[${i}]}PFJetsCHS = ${jetAlgoProd[${j}]}PFJets.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.${coneSize[${i}]}),
)
jetSource = '${jetalgo[${j}]}${coneSize[${i}]}PFJetsCHS'

#### Adding corrections 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHS = patJetCorrFactors.clone()
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHS.src = jetSource
# will need to add L2L3 corrections in the cfg
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHS.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHS.payload = '${coneSizeCorr[${i}]}PFchs'
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHS.useRho = True

from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cfi import *
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHS = patJets.clone()
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHS.jetSource = jetSource
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHS.addJetCharge = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHS.embedCaloTowers = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHS.embedPFCandidates = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHS.addAssociatedTracks = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHS.addBTagInfo = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHS.addDiscriminators = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHS.addJetID = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHS.addGenPartonMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHS.embedGenPartonMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHS.addGenJetMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHS.getJetMCFlavour = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHS.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHS'))

####### Adding jets without JEC (just for comaprison)
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC = patJetCorrFactors.clone()
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.src = jetSource
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.levels = []
#patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.payload = '${jetAlgo[${j}]}${coneSize[${i}]}PFchs'
#patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.useRho = True
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC = patJets.clone()
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.jetSource = jetSource
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.addJetCharge = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.embedCaloTowers = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.embedPFCandidates = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.addAssociatedTracks = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.addBTagInfo = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.addDiscriminators = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.addJetID = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.addGenPartonMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.embedGenPartonMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.addGenJetMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.getJetMCFlavour = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC'))

#### Adding Nsubjetiness
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSwithNsub = cms.EDProducer(\"NjettinessAdder\",
  src=cms.InputTag(\"patJets${jetAlgo[${j}]}${coneSize[${i}]}CHS\"),
  cone=cms.double(0.${coneSize[${i}]})
)

####################################################### PRUNNING
from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
${jetalgo[${j}]}${coneSize[${i}]}PFJetsCHSpruned = ak5PFJetsPruned.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.${coneSize[${i}]}),
  jetAlgorithm = cms.string(\"${jetAlgoName[${j}]}\"),
)
jetSourcePruned = '${jetalgo[${j}]}${coneSize[${i}]}PFJetsCHSpruned'

# corrections 
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned = patJetCorrFactors.clone()
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.src = jetSourcePruned
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.payload = '${coneSizeCorr[${i}]}PFchs'
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.useRho = True

patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned = patJets.clone()
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.jetSource = jetSourcePruned
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.addJetCharge = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.embedCaloTowers = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.embedPFCandidates = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.addAssociatedTracks = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.addBTagInfo = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.addDiscriminators = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.addJetID = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.addGenPartonMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.embedGenPartonMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.addGenJetMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.getJetMCFlavour = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned'))

#### Adding Nsubjetiness
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSprunedwithNsub = cms.EDProducer(\"NjettinessAdder\",
  src=cms.InputTag(\"patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned\"),
  cone=cms.double(0.${coneSize[${i}]})
)

################################################################ TRIMMING
from RecoJets.JetProducers.ak5PFJetsTrimmed_cfi import ak5PFJetsTrimmed
${jetalgo[${j}]}${coneSize[${i}]}PFJetsCHStrimmed = ak5PFJetsTrimmed.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.${coneSize[${i}]}),
  jetAlgorithm = cms.string(\"${jetAlgoName[${j}]}\"),
)
jetSourceTrimmed = '${jetalgo[${j}]}${coneSize[${i}]}PFJetsCHStrimmed'

# corrections 
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed = patJetCorrFactors.clone()
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.src = jetSourceTrimmed
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.payload = '${coneSizeCorr[${i}]}PFchs'
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.useRho = True

### pats
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed = patJets.clone()
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.jetSource = jetSourceTrimmed
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.addJetCharge = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.embedCaloTowers = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.embedPFCandidates = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.addAssociatedTracks = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.addBTagInfo = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.addDiscriminators = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.addJetID = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.addGenPartonMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.embedGenPartonMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.addGenJetMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.getJetMCFlavour = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed'))

#### Adding Nsubjetiness
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmedwithNsub = cms.EDProducer(\"NjettinessAdder\",
  src=cms.InputTag(\"patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed\"),
  cone=cms.double(0.${coneSize[${i}]})
)

############################################################### FILTERING
from RecoJets.JetProducers.ak5PFJetsFiltered_cfi import ak5PFJetsFiltered
${jetalgo[${j}]}${coneSize[${i}]}PFJetsCHSfiltered = ak5PFJetsFiltered.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  nFilt = cms.int32(2),
  rParam = cms.double(0.${coneSize[${i}]}),
  jetAlgorithm = cms.string(\"${jetAlgoName[${j}]}\"),
)

jetSourceFiltered = '${jetalgo[${j}]}${coneSize[${i}]}PFJetsCHSfiltered'

# corrections 
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered = patJetCorrFactors.clone()
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.src = jetSourceFiltered
# will need to add L2L3 corrections in the cfg
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.levels = ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.payload = '${coneSizeCorr[${i}]}PFchs'
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.useRho = True

patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered = patJets.clone()
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.jetSource = jetSourceFiltered
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.addJetCharge = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.embedCaloTowers = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.embedPFCandidates = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.addAssociatedTracks = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.addBTagInfo = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.addDiscriminators = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.addJetID = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.addGenPartonMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.embedGenPartonMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.addGenJetMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.getJetMCFlavour = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered'))

#### Adding Nsubjetiness
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfilteredwithNsub = cms.EDProducer(\"NjettinessAdder\",
  src=cms.InputTag(\"patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered\"),
  cone=cms.double(0.${coneSize[${i}]})
)


############################################################### MassDropFilter
from RecoJets.JetProducers.ak5PFJetsFiltered_cfi import ak5PFJetsMassDropFiltered
${jetalgo[${j}]}${coneSize[${i}]}PFJetsCHSmassDropFiltered = ak5PFJetsMassDropFiltered.clone(
  src = 'pfNoPileUp',
  jetPtMin = cms.double(20.0),
  doAreaFastjet = cms.bool(True),
  rParam = cms.double(0.${coneSize[${i}]}),
  jetAlgorithm = cms.string(\"${jetAlgoName[${j}]}\"),
)

jetSourceMassDropFiltered = '${jetalgo[${j}]}${coneSize[${i}]}PFJetsCHSmassDropFiltered'

# corrections 
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered = patJetCorrFactors.clone()
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.src = jetSourceMassDropFiltered
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.levels == ['L1FastJet', 'L2Relative', 'L3Absolute']
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.payload = '${coneSizeCorr[${i}]}PFchs'
patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.useRho = True

patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered = patJets.clone()
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.jetSource = jetSourceMassDropFiltered
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.addJetCharge = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.embedCaloTowers = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.embedPFCandidates = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.addAssociatedTracks = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.addBTagInfo = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.addDiscriminators = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.addJetID = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.addGenPartonMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.embedGenPartonMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.addGenJetMatch = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.getJetMCFlavour = False
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered.jetCorrFactorsSource = cms.VInputTag(cms.InputTag('patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered'))

#### Adding Nsubjetiness
patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFilteredwithNsub = cms.EDProducer(\"NjettinessAdder\",
  src=cms.InputTag(\"patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered\"),
  cone=cms.double(0.${coneSize[${i}]})
)





# JETS ${jetAlgo[${j}]}${coneSize[${i}]} ----------------------------

${jetalgo[${j}]}${coneSize[${i}]}Jets = cms.Sequence(
  goodOfflinePrimaryVertices +
  pfNoPileUpSequence +
  ${jetalgo[${j}]}${coneSize[${i}]}PFJetsCHS + 
  patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHS +
  patJets${jetAlgo[${j}]}${coneSize[${i}]}CHS +  
  patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC +
  patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSNOJEC +  
  patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSwithNsub +
  ${jetalgo[${j}]}${coneSize[${i}]}PFJetsCHSpruned +
  patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned +
  patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSpruned +
  patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSprunedwithNsub +
  ${jetalgo[${j}]}${coneSize[${i}]}PFJetsCHStrimmed +
  patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed +
  patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmed +
  patJets${jetAlgo[${j}]}${coneSize[${i}]}CHStrimmedwithNsub +
  ${jetalgo[${j}]}${coneSize[${i}]}PFJetsCHSfiltered +
  patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered +
  patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfiltered +
  patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSfilteredwithNsub + 
  ${jetalgo[${j}]}${coneSize[${i}]}PFJetsCHSmassDropFiltered +
  patJetCorrFactors${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered +
  patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFiltered +
  patJets${jetAlgo[${j}]}${coneSize[${i}]}CHSmassDropFilteredwithNsub
)" >> $OUTFILE
	done
done

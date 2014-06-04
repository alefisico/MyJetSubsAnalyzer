#!/usr/bin/env python

'''
File: MyAnalyzer.py --mass 50 (optional) --debug -- final --jetAlgo AK5
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Analyzer 
'''

import sys,os,time
import optparse
from collections import defaultdict
from ROOT import *
from DataFormats.FWLite import Events, Handle

gROOT.SetBatch()

###### Trick for add date or month to plots
dateKey   = time.strftime("%y%m%d%H%M")
monthKey   = time.strftime("%y%m%d")

######################################
def myTriggerAnalyzer( infile, outputDir, sample, couts, final, jetAlgo, grooming, weight, Job, FNAL, deltaRcut ):

	if FNAL:
		if final:
			if not ( os.path.exists( outputDir ) ): os.makedirs( outputDir )
			#if not ( os.path.exists( '/eos/uscms/'+outputDir ) ): os.makedirs( '/eos/uscms/'+outputDir )
			if 'QCD' in sample:
				outputFileName = outputDir + sample + '_'+jetAlgo+'_'+grooming+'_'+str(Job)+'_TriggerPlots.root'
			else:
				outputFileName = outputDir + sample + '_'+jetAlgo+'_'+grooming+'_TriggerPlots.root'
		else:
			outputFileName = sample + '_'+jetAlgo+'_'+grooming+'_TriggerPlots_TEST.root'

	else:
		if not final: 
			outputFileName = sample + '_'+jetAlgo+'_'+grooming+'_TriggerPlots_TEST.root'
		else:
			if not ( os.path.exists( outputDir + 'rootFiles/' + monthKey ) ): os.makedirs( outputDir + 'rootFiles/' + monthKey )
			if 'QCD' in sample:
				outputFileName = outputDir + 'rootFiles/' + monthKey + '/' + sample + '_'+jetAlgo+'_'+grooming+'_'+str(Job)+'_TriggerPlots.root'
			else:
				outputFileName = outputDir + 'rootFiles/' + monthKey + '/' + sample + '_'+jetAlgo+'_'+grooming+'_TriggerPlots.root'


	outputFile = TFile( outputFileName , 'RECREATE' )

	####################################################################################################################################### Histograms
	nBinsDeltaR = 50
	maxDeltaR = 5. 
	nBinsDeltaRCut = 20
	maxDeltaRCut = 1.
	maxMass = 500
	maxPt = 1000
	nBinsMass = 100  #int(round( maxMass/5 ))
	nBinsPt = 200  #int(round( maxPt/5 ))
	nBinsEta = 41
	maxEta = 4.1
	nBinsTau = 50
	maxTau = 1.
	nBinsHT = 200
	maxHT = 2000.
	nBinsMET = 15
	maxMET = 150.

	################################################################################################## Trigger Histos
	TriggerNames 	= TH1F('h_TriggerNames', 'h_TriggerNames', 4, 0, 4 )
	TriggerPass 	= TH1F('h_TriggerPass', 'h_TriggerPass', 8, 0, 8 )
	ht_HT350	= TH1F('h_ht_HT350_'+jetAlgo+'_'+grooming, 	'h_ht_HT350_'+jetAlgo, 	nBinsHT,  	0, 	maxHT)
	ht_HT750	= TH1F('h_ht_HT750_'+jetAlgo+'_'+grooming, 	'h_ht_HT750_'+jetAlgo, 	nBinsHT,  	0, 	maxHT)
	ht_PFHT350	= TH1F('h_ht_PFHT350_'+jetAlgo+'_'+grooming, 	'h_ht_PFHT350_'+jetAlgo, 	nBinsHT,  	0, 	maxHT)
	ht_PFHT650	= TH1F('h_ht_PFHT650_'+jetAlgo+'_'+grooming, 	'h_ht_PFHT650_'+jetAlgo, 	nBinsHT,  	0, 	maxHT)
	ht_PFHT650_1	= TH1F('h_ht_PFHT650_1_'+jetAlgo+'_'+grooming, 	'h_ht_PFHT650_1_'+jetAlgo, 	nBinsHT,  	0, 	maxHT)

	#####################################################
	#### Only kinematic cuts - (pt > 30, |eta| < 2.5 )
	################################################################################################### Event Variables
	ht 		= TH1F('h_ht_'+jetAlgo, 	'h_ht_'+jetAlgo, 	nBinsHT,  	0, 	maxHT)
	numberPV 	= TH1F('h_numberPV_'+jetAlgo, 	'h_numberPV_'+jetAlgo, 	50,  	0., 	50.)
	MET 		= TH1F('h_MET_'+jetAlgo, 	'h_MET_'+jetAlgo, 	nBinsMET,  	0, 	maxMET)
	numberJets 	= TH1F('h_numberJets_'+jetAlgo, 'h_numberJets_'+jetAlgo, 15,  0., 15.)
	jetPt	 	= TH1F('h_jetPt_'+jetAlgo, 'h_jetPt_'+jetAlgo, nBinsPt,  0., maxPt)
	jetEta	 	= TH1F('h_jetEta_'+jetAlgo, 'h_jetEta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jetPhi	 	= TH1F('h_jetPhi_'+jetAlgo, 'h_jetPhi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jetMass	 	= TH1F('h_jetMass_'+jetAlgo, 'h_jetMass_'+jetAlgo, nBinsMass,  0., maxMass)
	jetArea 	= TH1F('h_jetArea_'+jetAlgo, 'h_jetArea_'+jetAlgo, 50,  0., 5.)
	jet1Pt	 	= TH1F('h_jet1Pt_'+jetAlgo, 'h_jet1Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	jet1Eta	 	= TH1F('h_jet1Eta_'+jetAlgo, 'h_jet1Eta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jet1Phi	 	= TH1F('h_jet1Phi_'+jetAlgo, 'h_jet1Phi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jet1Mass	 	= TH1F('h_jet1Mass_'+jetAlgo, 'h_jet1Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	jet1PtvsMass	= TH2F('h_jet1PtvsMass_'+jetAlgo, 'h_jet1PtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	HTvsNPV 	= TH2F('h_HTvsNPV_'+jetAlgo, 'h_HTvsNPV_'+jetAlgo, nBinsHT,  0., maxHT, 50,  0., 50.)
	jet1Ptvsht 	= TH2F('h_jet1Ptvsht_'+jetAlgo, 'h_jet1Ptvsht_'+jetAlgo, nBinsPt,  0., maxPt, nBinsHT,  	0, 	maxHT)
	jet1Massvsht 	= TH2F('h_jet1Massvsht_'+jetAlgo, 'h_jet1Massvsht_'+jetAlgo, nBinsMass,  0., maxMass, nBinsHT,  	0, 	maxHT)
	jet1MassvsMET 	= TH2F('h_jet1MassvsMET_'+jetAlgo, 'h_jet1MassvsMET_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMET,  	0, 	maxMET)
	jet1MassvsNPV 	= TH2F('h_jet1MassvsNPV_'+jetAlgo, 'h_jet1MassvsNPV_'+jetAlgo, nBinsMass,  0., maxMass, 50,  	0, 	50)
	ht_groomed		= TH1F('h_ht_'+jetAlgo+'_'+grooming, 	'h_ht_'+jetAlgo+'_'+grooming, 	nBinsHT,  	0, 	maxHT)
	numberPV_groomed 	= TH1F('h_numberPV_'+jetAlgo+'_'+grooming, 	'h_numberPV_'+jetAlgo+'_'+grooming, 	50,  	0., 	50.)
	MET_groomed 		= TH1F('h_MET_'+jetAlgo+'_'+grooming, 	'h_MET_'+jetAlgo+'_'+grooming, 	nBinsMET,  	0, 	maxMET)
	numberJets_groomed 	= TH1F('h_numberJets_'+jetAlgo+'_'+grooming, 'h_numberJets_'+jetAlgo+'_'+grooming, 15,  0., 15.)
	jetPt_groomed	 	= TH1F('h_jetPt_'+jetAlgo+'_'+grooming, 'h_jetPt_'+jetAlgo+'_'+grooming, nBinsPt,  0., maxPt)
	jetEta_groomed	 	= TH1F('h_jetEta_'+jetAlgo+'_'+grooming, 'h_jetEta_'+jetAlgo+'_'+grooming, nBinsEta,  -maxEta, maxEta)
	jetPhi_groomed	 	= TH1F('h_jetPhi_'+jetAlgo+'_'+grooming, 'h_jetPhi_'+jetAlgo+'_'+grooming, nBinsEta,  -maxEta, maxEta)
	jetMass_groomed	 	= TH1F('h_jetMass_'+jetAlgo+'_'+grooming, 'h_jetMass_'+jetAlgo+'_'+grooming, nBinsMass,  0., maxMass)
	jetArea_groomed 	= TH1F('h_jetArea_'+jetAlgo+'_'+grooming, 'h_jetArea_'+jetAlgo+'_'+grooming, 50,  0., 5.)
	jet1Pt_groomed	 	= TH1F('h_jet1Pt_'+jetAlgo+'_'+grooming, 'h_jet1Pt_'+jetAlgo+'_'+grooming, nBinsPt,  0., maxPt)
	jet1Eta_groomed	 	= TH1F('h_jet1Eta_'+jetAlgo+'_'+grooming, 'h_jet1Eta_'+jetAlgo+'_'+grooming, nBinsEta,  -maxEta, maxEta)
	jet1Phi_groomed	 	= TH1F('h_jet1Phi_'+jetAlgo+'_'+grooming, 'h_jet1Phi_'+jetAlgo+'_'+grooming, nBinsEta,  -maxEta, maxEta)
	jet1Mass_groomed	= TH1F('h_jet1Mass_'+jetAlgo+'_'+grooming, 'h_jet1Mass_'+jetAlgo+'_'+grooming, nBinsMass,  0., maxMass)
	jet1PtvsMass_groomed	= TH2F('h_jet1PtvsMass_'+jetAlgo+'_'+grooming, 'h_jet1PtvsMass_'+jetAlgo+'_'+grooming, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	HTvsNPV_groomed 	= TH2F('h_HTvsNPV_'+jetAlgo+'_'+grooming, 'h_HTvsNPV_'+jetAlgo+'_'+grooming, nBinsHT,  0., maxHT, 50,  0., 50.)
	jet1Ptvsht_groomed 	= TH2F('h_jet1Ptvsht_groomed_'+jetAlgo+'_'+grooming, 'h_jet1Ptvsht_groomed_'+jetAlgo, nBinsPt,  0., maxPt, nBinsHT,  	0, 	maxHT)
	jet1Massvsht_groomed 	= TH2F('h_jet1Massvsht_groomed_'+jetAlgo+'_'+grooming, 'h_jet1Massvsht_groomed_'+jetAlgo, nBinsMass,  0., maxMass, nBinsHT,  	0, 	maxHT)
	jet1MassvsMET_groomed 	= TH2F('h_jet1MassvsMET_groomed_'+jetAlgo+'_'+grooming, 'h_jet1MassvsMET_groomed_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMET,  	0, 	maxMET)
	jet1MassvsNPV_groomed 	= TH2F('h_jet1MassvsNPV_groomed_'+jetAlgo+'_'+grooming, 'h_jet1MassvsNPV_groomed_'+jetAlgo, nBinsMass,  0., maxMass, 50,  	0, 	50)

	jetMassCmp	 	= TH1F('h_jetMassCmp_'+jetAlgo, 'h_jetMassCmp_'+jetAlgo, 50,  0., 5.)
	jet1MassCmp	 	= TH1F('h_jet1MassCmp_'+jetAlgo, 'h_jet1MassCmp_'+jetAlgo, 50,  0., 5.)
	HTCmp	 	= TH1F('h_HTCmp_'+jetAlgo, 'h_HTCmp_'+jetAlgo, 50,  0., 5.)

	###################################################
	######  Matching Plots
	######################################################################################################
	##### No Merged
	numberPartonsSameJet_DeltaRCut 		= TH1F('h_numberPartonsSameJet_DeltaRCut_'+jetAlgo, 	'h_numberPartonsSameJet_DeltaRCut_'+jetAlgo,	8,  		0.,8. )
	minDeltaRPartonJet_DeltaRCut 		= TH1F('h_minDeltaRPartonJet_DeltaRCut_'+jetAlgo, 	'h_minDeltaRPartonJet_DeltaRCut_'+jetAlgo,	nBinsDeltaRCut,	0.,maxDeltaRCut )
	minDeltaRPartonJet_NoMerged_DeltaRCut 	= TH1F('h_minDeltaRPartonJet_NoMerged_DeltaRCut_'+jetAlgo, 	'h_minDeltaRPartonJet_NoMerged_DeltaRCut_'+jetAlgo,		nBinsDeltaRCut,	0.,	maxDeltaRCut)
	jetMass_NoMerged_DeltaRCut 		= TH1F('h_jetMass_NoMerged_DeltaRCut_'+jetAlgo, 	'h_jetMass_NoMerged_DeltaRCut_'+jetAlgo, 	nBinsMass, 	0., maxMass )
	#### SIngly Merged
	minDeltaRPartonJet_SinglyMerged_Merged_DeltaRCut 	= TH1F('h_minDeltaRPartonJet_SinglyMerged_Merged_DeltaRCut_'+jetAlgo, 'h_minDeltaRPartonJet_SinglyMerged_Merged_DeltaRCut_'+jetAlgo,	nBinsDeltaRCut, 0.,	maxDeltaRCut )
	minDeltaRPartonJet_SinglyMerged_NOMerged_DeltaRCut 	= TH1F('h_minDeltaRPartonJet_SinglyMerged_NOMerged_DeltaRCut_'+jetAlgo, 'h_minDeltaRPartonJet_SinglyMerged_NOMerged_DeltaRCut_'+jetAlgo,	nBinsDeltaRCut, 0.,	maxDeltaRCut )
	jetMass_SinglyMerged_DeltaRCut_NOMerged 	= TH1F('h_jetMass_SinglyMerged_DeltaRCut_NOMerged_'+jetAlgo, 	'h_jetMass_SinglyMerged_DeltaRCut_NOMerged_'+jetAlgo, 	nBinsMass, 	0., 	maxMass )
	jetMass_SinglyMerged_DeltaRCut_Merged 	= TH1F('h_jetMass_SinglyMerged_DeltaRCut_Merged_'+jetAlgo, 	'h_jetMass_SinglyMerged_DeltaRCut_Merged_'+jetAlgo, 		nBinsMass, 	0., 	maxMass )
	jetPt_SinglyMerged_DeltaRCut_NOMerged	= TH1F('h_jetPt_SinglyMerged_DeltaRCut_NOMerged_'+jetAlgo, 'h_jetPt_SinglyMerged_DeltaRCut_NOMerged_'+jetAlgo, nBinsMass,  0., maxMass)
	jetPt_SinglyMerged_DeltaRCut_Merged	= TH1F('h_jetPt_SinglyMerged_DeltaRCut_Merged_'+jetAlgo, 'h_jetPt_SinglyMerged_DeltaRCut_Merged_'+jetAlgo, nBinsPt,  0., maxPt)
	ht_SinglyMerged_DeltaRCut		= TH1F('h_ht_SinglyMerged_DeltaRCut_'+jetAlgo, 	'h_ht_SinglyMerged_DeltaRCut_'+jetAlgo, 	nBinsHT,  	0, 	maxHT)
	ht_SinglyMerged_DeltaRCut_groomed	= TH1F('h_ht_SinglyMerged_DeltaRCut_'+jetAlgo+'_'+grooming, 	'h_ht_SinglyMerged_DeltaRCut_'+jetAlgo+'_'+grooming, 	nBinsHT,  	0, 	maxHT)
	jetPtvsMass_SinglyMerged	= TH2F('h_jetPtvsMass_SinglyMerged_'+jetAlgo, 'h_jetPtvsMass_SinglyMerged_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	HTvsNPV_SinglyMerged 	= TH2F('h_HTvsNPV_SinglyMerged_'+jetAlgo, 'h_HTvsNPV_SinglyMerged_'+jetAlgo, nBinsHT,  0., maxHT, 50,  0., 50.)
	jetPtvsht_SinglyMerged 	= TH2F('h_jetPtvsht_SinglyMerged_'+jetAlgo+'_'+grooming, 'h_jetPtvsht_SinglyMerged_'+jetAlgo, nBinsPt,  0., maxPt, nBinsHT,  	0, 	maxHT)
	jetMassvsht_SinglyMerged 	= TH2F('h_jetMassvsht_SinglyMerged_'+jetAlgo+'_'+grooming, 'h_jetMassvsht_SinglyMerged_'+jetAlgo, nBinsMass,  0., maxMass, nBinsHT,  	0, 	maxHT)
	jetMassvsMET_SinglyMerged 	= TH2F('h_jetMassvsMET_SinglyMerged_'+jetAlgo+'_'+grooming, 'h_jetMassvsMET_SinglyMerged_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMET,  	0, 	maxMET)
	jetMassvsNPV_SinglyMerged 	= TH2F('h_jetMassvsNPV_SinglyMerged_'+jetAlgo+'_'+grooming, 'h_jetMassvsNPV_SinglyMerged_'+jetAlgo, nBinsMass,  0., maxMass, 50,  	0, 	50)
	jetPtvsMass_SinglyMerged_groomed	= TH2F('h_jetPtvsMass_SinglyMerged_groomed_'+jetAlgo, 'h_jetPtvsMass_SinglyMerged_groomed_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	HTvsNPV_SinglyMerged_groomed 	= TH2F('h_HTvsNPV_SinglyMerged_groomed_'+jetAlgo, 'h_HTvsNPV_SinglyMerged_groomed_'+jetAlgo, nBinsHT,  0., maxHT, 50,  0., 50.)
	jetPtvsht_SinglyMerged_groomed 	= TH2F('h_jetPtvsht_SinglyMerged_groomed_'+jetAlgo+'_'+grooming, 'h_jetPtvsht_SinglyMerged_groomed_'+jetAlgo, nBinsPt,  0., maxPt, nBinsHT,  	0, 	maxHT)
	jetMassvsht_SinglyMerged_groomed 	= TH2F('h_jetMassvsht_SinglyMerged_groomed_'+jetAlgo+'_'+grooming, 'h_jetMassvsht_SinglyMerged_groomed_'+jetAlgo, nBinsMass,  0., maxMass, nBinsHT,  	0, 	maxHT)
	jetMassvsMET_SinglyMerged_groomed 	= TH2F('h_jetMassvsMET_SinglyMerged_groomed_'+jetAlgo+'_'+grooming, 'h_jetMassvsMET_SinglyMerged_groomed_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMET,  	0, 	maxMET)
	jetMassvsNPV_SinglyMerged_groomed 	= TH2F('h_jetMassvsNPV_SinglyMerged_groomed_'+jetAlgo+'_'+grooming, 'h_jetMassvsNPV_SinglyMerged_groomed_'+jetAlgo, nBinsMass,  0., maxMass, 50,  	0, 	50)
	#### Doubly Merged
	minDeltaRPartonJet_DoublyMerged_DeltaRCut_A 	= TH1F('h_minDeltaRPartonJet_DoublyMerged_DeltaRCut_A_'+jetAlgo, 	'h_minDeltaRPartonJet_DoublyMerged_DeltaRCut_A_'+jetAlgo,		nBinsDeltaRCut, 0.,	maxDeltaRCut )
	minDeltaRPartonJet_DoublyMerged_DeltaRCut_B 	= TH1F('h_minDeltaRPartonJet_DoublyMerged_DeltaRCut_B_'+jetAlgo, 	'h_minDeltaRPartonJet_DoublyMerged_DeltaRCut_B_'+jetAlgo,		nBinsDeltaRCut, 0.,	maxDeltaRCut )
	jetMass_DoublyMerged_DeltaRCut 		= TH1F('h_jetMass_DoublyMerged_DeltaRCut_'+jetAlgo, 	'h_jetMass_DoublyMerged_DeltaRCut_'+jetAlgo, 		nBinsMass, 	0., 	maxMass )
	jetPt_DoublyMerged_DeltaRCut		 	= TH1F('h_jetPt_DoublyMerged_DeltaRCut_'+jetAlgo, 'h_jetPt_DoublyMerged_DeltaRCut_'+jetAlgo, nBinsPt,  0., maxPt)
	ht_DoublyMerged_DeltaRCut		= TH1F('h_ht_DoublyMerged_DeltaRCut_'+jetAlgo, 	'h_ht_DoublyMerged_DeltaRCut_'+jetAlgo, 	nBinsHT,  	0, 	maxHT)
	ht_DoublyMerged_DeltaRCut_groomed	= TH1F('h_ht_DoublyMerged_DeltaRCut_'+jetAlgo+'_'+grooming, 	'h_ht_DoublyMerged_DeltaRCut_'+jetAlgo+'_'+grooming, 	nBinsHT,  	0, 	maxHT)
	jetPtvsMass_DoublyMerged	= TH2F('h_jetPtvsMass_DoublyMerged_'+jetAlgo, 'h_jetPtvsMass_DoublyMerged_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	HTvsNPV_DoublyMerged 	= TH2F('h_HTvsNPV_DoublyMerged_'+jetAlgo, 'h_HTvsNPV_DoublyMerged_'+jetAlgo, nBinsHT,  0., maxHT, 50,  0., 50.)
	jetPtvsht_DoublyMerged 	= TH2F('h_jetPtvsht_DoublyMerged_'+jetAlgo+'_'+grooming, 'h_jetPtvsht_DoublyMerged_'+jetAlgo, nBinsPt,  0., maxPt, nBinsHT,  	0, 	maxHT)
	jetMassvsht_DoublyMerged 	= TH2F('h_jetMassvsht_DoublyMerged_'+jetAlgo+'_'+grooming, 'h_jetMassvsht_DoublyMerged_'+jetAlgo, nBinsMass,  0., maxMass, nBinsHT,  	0, 	maxHT)
	jetMassvsMET_DoublyMerged 	= TH2F('h_jetMassvsMET_DoublyMerged_'+jetAlgo+'_'+grooming, 'h_jetMassvsMET_DoublyMerged_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMET,  	0, 	maxMET)
	jetMassvsNPV_DoublyMerged 	= TH2F('h_jetMassvsNPV_DoublyMerged_'+jetAlgo+'_'+grooming, 'h_jetMassvsNPV_DoublyMerged_'+jetAlgo, nBinsMass,  0., maxMass, 50,  	0, 	50)
	jetPtvsMass_DoublyMerged_groomed	= TH2F('h_jetPtvsMass_DoublyMerged_groomed_'+jetAlgo, 'h_jetPtvsMass_DoublyMerged_groomed_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	HTvsNPV_DoublyMerged_groomed 	= TH2F('h_HTvsNPV_DoublyMerged_groomed_'+jetAlgo, 'h_HTvsNPV_DoublyMerged_groomed_'+jetAlgo, nBinsHT,  0., maxHT, 50,  0., 50.)
	jetPtvsht_DoublyMerged_groomed 	= TH2F('h_jetPtvsht_DoublyMerged_groomed_'+jetAlgo+'_'+grooming, 'h_jetPtvsht_DoublyMerged_groomed_'+jetAlgo, nBinsPt,  0., maxPt, nBinsHT,  	0, 	maxHT)
	jetMassvsht_DoublyMerged_groomed 	= TH2F('h_jetMassvsht_DoublyMerged_groomed_'+jetAlgo+'_'+grooming, 'h_jetMassvsht_DoublyMerged_groomed_'+jetAlgo, nBinsMass,  0., maxMass, nBinsHT,  	0, 	maxHT)
	jetMassvsMET_DoublyMerged_groomed 	= TH2F('h_jetMassvsMET_DoublyMerged_groomed_'+jetAlgo+'_'+grooming, 'h_jetMassvsMET_DoublyMerged_groomed_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMET,  	0, 	maxMET)
	jetMassvsNPV_DoublyMerged_groomed 	= TH2F('h_jetMassvsNPV_DoublyMerged_groomed_'+jetAlgo+'_'+grooming, 'h_jetMassvsNPV_DoublyMerged_groomed_'+jetAlgo, nBinsMass,  0., maxMass, 50,  	0, 	50)

	###################################### Get GenTree 
	#events = TChain( 'PFJet_'+jetAlgo+grooming+'/events' )
	events = TChain( 'PFJet_'+jetAlgo+'/events' )

	# Loop over the filenames and add to tree.
	for filename in infile:
		print("Adding file: " + filename)
		events.Add(filename)

	##### read the tree & fill histosgrams 
	numEntries = events.GetEntries()
	print '------> Number of events: '+str(numEntries)
	d = 0

	for i in xrange(numEntries):
		events.GetEntry(i)

		#---- progress of the reading --------
		fraction = 10.*i/(1.*numEntries)
		if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
		d = TMath.FloorNint(fraction)

		#---- progress of the reading --------
		Run      = events.runNo
		Lumi     = events.lumi
		NumEvent = events.evtNo
		if couts: print 'Entry ', Run, ':', Lumi, ':', NumEvent

		############# Trigger Info
		###### Just for reference order of triggers in 
		###### Data, QCD, and Signal: HT350, HT750, PFHT350, PFHT650
		###### TriggerPass PFHT650, PFHT350, HT750, HT350
		###### There is a weird behavior in CRAB, that is why I am splitting this into categories

		if 'stop' in sample:
			if events.triggerResult[0]:
				ht_HT350.Fill( events.ht )			###### Weight should be 1
			if events.triggerResult[2]:
				ht_PFHT350.Fill( events.ht )
			if events.triggerResult[1] and events.triggerResult[0]:
				ht_HT750.Fill( events.ht )
			if events.triggerResult[3] and events.triggerResult[0]:
				ht_PFHT650.Fill( events.ht )
			if events.triggerResult[3] and events.triggerResult[2]:
				ht_PFHT650_1.Fill( events.ht )
		else:
			if not events.triggerResult[0]:
				ht_HT350.Fill( events.ht )
			if not events.triggerResult[2]:
				ht_PFHT350.Fill( events.ht )
			if events.triggerResult[1] and not events.triggerResult[0]:
				ht_HT750.Fill( events.ht )
			if events.triggerResult[3] and not events.triggerResult[0]:
				ht_PFHT650.Fill( events.ht )
			if events.triggerResult[3] and not events.triggerResult[2]:
				ht_PFHT650_1.Fill( events.ht )
		##########################################################################################

		###################################################################### Cuts
		HT = 0.0			### sanity clear
		HT_groomed = 0.0			### sanity clear
		listJetMass = []
		listJetMass_groomed = []
		for ijet in range( getattr( events, 'nJets'+grooming ) ):
			cut_simpleKinematic_groomed =  getattr( events, 'jet'+grooming+'Pt')[ijet] > 40 and abs( getattr( events, 'jet'+grooming+'Eta')[ijet] ) < 2.5 
		cut_minTwoJets = getattr( events, 'nJets'+grooming ) > 1
		cut_TwoJets = getattr( events, 'nJets'+grooming ) == 2
		cut_jet1pt = getattr( events, 'nJets'+grooming ) > 0 and getattr( events, 'jet'+grooming+'Pt')[0] > 200 
		cut_HT = HT > 850


		###################################################################### Filling Histograms

		############  Without Grooming
		listP4Jets = []
		#if len( getattr( events, 'jetPt' ) ) > 0:
		for k in range( getattr( events, 'nJets' ) ):
			if ( events.jetPt[k] > 40 ) and ( abs( events.jetEta[k] ) < 2.5 ):
				#if not 'QCD' in sample:
				tmpP4 = TLorentzVector()
				tmpP4.SetPtEtaPhiE( events.jetPt[k], events.jetEta[k], events.jetPhi[k], events.jetEnergy[k] )
				listP4Jets.append( tmpP4 )

				HT += events.jetPt[k]
				jetPt.Fill( events.jetPt[k], weight )
				jetEta.Fill( events.jetEta[k], weight )
				jetPhi.Fill( events.jetPhi[k], weight )
				jetMass.Fill( events.jetMass[k], weight )
				#listJetMass.append( getattr( events, 'jet'+'Mass')[k] )

		if len( listP4Jets ) > 0:
			numberJets.Fill( len( listP4Jets ), weight )
			ht.Fill( HT, weight )
			numberPV.Fill( events.nvtx, weight )
			MET.Fill( events.met, weight )
			HTvsNPV.Fill( HT, events.nvtx, weight )
			jet1Pt.Fill( listP4Jets[0].Pt()  )
			jet1Eta.Fill( listP4Jets[0].Eta() )
			jet1Phi.Fill( listP4Jets[0].Phi() )
			jet1Mass.Fill( listP4Jets[0].M() )
			jet1PtvsMass.Fill( listP4Jets[0].Pt(), listP4Jets[0].M() , weight )
			jet1Ptvsht.Fill( listP4Jets[0].Pt(), HT, weight )
			jet1Massvsht.Fill( listP4Jets[0].M(), HT, weight )
			jet1MassvsMET.Fill( listP4Jets[0].M(), events.met, weight )
			jet1MassvsNPV.Fill( listP4Jets[0].M(), events.nvtx, weight )

		############  With Grooming
		listP4Jets_groomed = []
		for q in range( getattr( events, 'nJets'+grooming ) ):
			if ( getattr( events, 'jet'+grooming+'Pt')[q] > 40 ) and ( abs( getattr( events, 'jet'+grooming+'Eta')[q] ) < 2.5 ):
					tmpP4_groomed = TLorentzVector()
					tmpP4_groomed.SetPtEtaPhiE( events.jetPt[q], events.jetEta[q], events.jetPhi[q], events.jetEnergy[q] )
					listP4Jets_groomed.append( tmpP4_groomed )

					HT_groomed += getattr( events, 'jet'+grooming+'Pt')[q]
					jetPt_groomed.Fill( getattr( events, 'jet'+grooming+'Pt')[q], weight )
					jetEta_groomed.Fill( getattr( events, 'jet'+grooming+'Eta')[q], weight )
					jetPhi_groomed.Fill( getattr( events, 'jet'+grooming+'Phi')[q], weight )
					jetMass_groomed.Fill( getattr( events, 'jet'+grooming+'Mass')[q], weight )
					#listJetMass_groomed.append( getattr( events, 'jet'+grooming+'Mass')[q] )

		if len( listP4Jets_groomed ) > 0:
			numberJets_groomed.Fill( len( listP4Jets_groomed ), weight )
			ht_groomed.Fill( HT_groomed, weight )
			numberPV_groomed.Fill( events.nvtx, weight )
			MET_groomed.Fill( events.met, weight )
			HTvsNPV_groomed.Fill( HT_groomed, events.nvtx )
			jet1Pt_groomed.Fill( listP4Jets_groomed[0].Pt()  )
			jet1Eta_groomed.Fill( listP4Jets_groomed[0].Eta() )
			jet1Phi_groomed.Fill( listP4Jets_groomed[0].Phi() )
			jet1Mass_groomed.Fill( listP4Jets_groomed[0].M() )
			jet1PtvsMass_groomed.Fill( listP4Jets_groomed[0].Pt(), listP4Jets_groomed[0].M(), weight )
			jet1Ptvsht_groomed.Fill( listP4Jets_groomed[0].Pt(), HT_groomed, weight )
			jet1Massvsht_groomed.Fill( listP4Jets_groomed[0].M(), HT_groomed, weight )
			jet1MassvsMET_groomed.Fill( listP4Jets_groomed[0].M(), events.met, weight )
			jet1MassvsNPV_groomed.Fill( listP4Jets_groomed[0].M(), events.nvtx, weight )

		###### testing
		try: 
			HTCmp.Fill( HT / HT_groomed, weight )
		except ZeroDivisionError: 
			HTCmp.Fill( -999, weight )
		if len(listJetMass) > 0 and  len( listJetMass ) == len( listJetMass_groomed ): 
			try:
				jet1MassCmp.Fill( listJetMass[0] / listJetMass_groomed[0], weight ) 
			except ZeroDivisionError: 
				jet1MassCmp.Fill( -999, weight )
			for a in range( len( listJetMass ) ):
				try:
					jetMassCmp.Fill( listJetMass[a] / listJetMass_groomed[a], weight ) 
				except ZeroDivisionError: 
					jetMassCmp.Fill( -999, weight ) 
		######## end testing
		
		if 'stop' in sample:

			####################################################### Store Parton information in list
			listP4PartonsFromStopA = []
			listP4PartonsFromStopB = []

			for k in range( events.numPartonsStopA ):
				tmpP4 = TLorentzVector()
				tmpP4.SetPtEtaPhiE( events.stopAPt[k], events.stopAEta[k], events.stopAPhi[k], events.stopAEnergy[k]  )
				listP4PartonsFromStopA.append( tmpP4 )
			for k in range( events.numPartonsStopB ):
				tmpP4 = TLorentzVector()
				tmpP4.SetPtEtaPhiE( events.stopBPt[k], events.stopBEta[k], events.stopBPhi[k], events.stopBEnergy[k]  )
				listP4PartonsFromStopB.append( tmpP4 )

			listP4PartonsFromStops = listP4PartonsFromStopA + listP4PartonsFromStopB

			################### Calculate DeltaR between each parton and each jet
			dictDeltaR = {}
			dictDeltaR1 = {}
			dictDeltaRCut = {}
			tmpListJetIndex = []
			tmpListJetIndexDeltaRCut = []
			for iparton in range( len( listP4PartonsFromStops ) ):
				listDeltaR = []
				#if debug: print '0 ', listP4PartonsFromStops[iparton].Pt()
				for ijet in range( len( listP4Jets ) ):
					deltaR = listP4PartonsFromStops[iparton].DeltaR( listP4Jets[ijet] )
					listDeltaR.append( deltaR )
				sortedListDeltaR = sorted( listDeltaR )
				jetIndex = []
				if len( listDeltaR ) > 0:
					for ii in sortedListDeltaR:
						tmpjetIndex = listDeltaR.index( ii )
						jetIndex.append( tmpjetIndex )
					dictDeltaR[ iparton ] = [ sortedListDeltaR, jetIndex ]
					tmpListJetIndex.append( jetIndex[0] )
					if ( sortedListDeltaR[0] < deltaRcut ): 
						dictDeltaRCut[ iparton ] = [ sortedListDeltaR, jetIndex ]
						tmpListJetIndexDeltaRCut.append( jetIndex[0] )



			#### check if cut is applied:
			for i,listParton in dictDeltaRCut.iteritems(): 
				if len( listParton[0] ) > 0: minDeltaRPartonJet_DeltaRCut.Fill( listParton[0][0], weight )

			#### check number of repetitions
			appearancesDeltaRCut = defaultdict(int)
			for curr in tmpListJetIndexDeltaRCut: appearancesDeltaRCut[curr] += 1
			listDuplicatesDeltaRCut = [ i for i, k in appearancesDeltaRCut.iteritems() if k > 1 ]
			numUniqueJetsDeltaRCut = len( set( tmpListJetIndexDeltaRCut ) )

			#################### if 4 jets after delta cut
			if len( tmpListJetIndexDeltaRCut ) == 4:		

				################### No Merged
				if ( len( listDuplicatesDeltaRCut ) == 0 ) and ( numUniqueJetsDeltaRCut == 4 ) and ( len( listP4Jets ) == len ( listP4Jets_groomed ) ):
					numberPartonsSameJet_DeltaRCut.Fill( 0 )
					for jparton, jLists in dictDeltaRCut.iteritems():
						minDeltaRPartonJet_NoMerged_DeltaRCut.Fill( jLists[0][0], weight )

					tmpStopA = ( listP4Jets[ tmpListJetIndexDeltaRCut[0] ] + listP4Jets[ tmpListJetIndexDeltaRCut[1] ] ).M()
					tmpStopB = ( listP4Jets[ tmpListJetIndexDeltaRCut[2] ] + listP4Jets[ tmpListJetIndexDeltaRCut[3] ] ).M()
					jetMass_NoMerged_DeltaRCut.Fill( tmpStopA, weight )
					jetMass_NoMerged_DeltaRCut.Fill( tmpStopB, weight )

				######################### Singly Merged
				elif ( len( listDuplicatesDeltaRCut ) == 1 ) and ( numUniqueJetsDeltaRCut == 3 ) and ( len( listP4Jets ) == len ( listP4Jets_groomed ) ):
					for jparton, jLists in dictDeltaRCut.iteritems():
						if ( listDuplicatesDeltaRCut[0] == jLists[1][0] ):
							minDeltaRPartonJet_SinglyMerged_Merged_DeltaRCut.Fill( jLists[0][0], weight )
						else:
							minDeltaRPartonJet_SinglyMerged_NOMerged_DeltaRCut.Fill( jLists[0][0], weight )

					if ( listDuplicatesDeltaRCut[0] != tmpListJetIndexDeltaRCut[0] ) and ( listDuplicatesDeltaRCut[0] != tmpListJetIndexDeltaRCut[1] ): 
						numberPartonsSameJet_DeltaRCut.Fill( 1 )
						tmpStopA = ( listP4Jets[ tmpListJetIndexDeltaRCut[0] ] + listP4Jets[ tmpListJetIndexDeltaRCut[1] ] ).M()
						tmpStopC = ( listP4Jets[ listDuplicatesDeltaRCut[0] ] ).M()

						### MERGED
						jetMass_SinglyMerged_DeltaRCut_Merged.Fill( tmpStopC, weight )
						jetPt_SinglyMerged_DeltaRCut_Merged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].Pt(), weight )
						HTvsNPV_SinglyMerged.Fill( HT, events.nvtx, weight )
						jetPtvsMass_SinglyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].Pt(), listP4Jets[ listDuplicatesDeltaRCut[0] ].M(), weight )
						jetPtvsht_SinglyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].Pt(), HT, weight )
						jetMassvsht_SinglyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].M(), HT, weight )
						jetMassvsMET_SinglyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].M(),  events.met, weight )
						jetMassvsNPV_SinglyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].M(),  events.nvtx, weight )

						#### NO MERGED
						jetMass_SinglyMerged_DeltaRCut_NOMerged.Fill( tmpStopA, weight )
						#### NO MERGED 0
						jetPt_SinglyMerged_DeltaRCut_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaRCut[0] ].Pt(), weight )
						##### NO MERGED 1
						jetPt_SinglyMerged_DeltaRCut_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaRCut[1] ].Pt(), weight )

						ht_SinglyMerged_DeltaRCut.Fill( HT, weight )
						ht_SinglyMerged_DeltaRCut_groomed.Fill( HT_groomed, weight )
						HTvsNPV_SinglyMerged_groomed.Fill( HT_groomed, events.nvtx, weight )
						jetPtvsMass_SinglyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].Pt(), listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].M(), weight )
						jetPtvsht_SinglyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].Pt(), HT_groomed, weight )
						jetMassvsht_SinglyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].M(), HT_groomed, weight )
						jetMassvsMET_SinglyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].M(),  events.met, weight )
						jetMassvsNPV_SinglyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].M(),  events.nvtx, weight )

					elif ( listDuplicatesDeltaRCut[0] != tmpListJetIndexDeltaRCut[2] ) and ( listDuplicatesDeltaRCut[0] != tmpListJetIndexDeltaRCut[3] ): 
						numberPartonsSameJet_DeltaRCut.Fill( 1 )
						tmpStopB = ( listP4Jets[ tmpListJetIndexDeltaRCut[2] ] + listP4Jets[ tmpListJetIndexDeltaRCut[3] ] ).M()
						tmpStopC = ( listP4Jets[ listDuplicatesDeltaRCut[0] ] ).M()

						##### MERGED
						jetMass_SinglyMerged_DeltaRCut_Merged.Fill( tmpStopC, weight )
						jetPt_SinglyMerged_DeltaRCut_Merged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].Pt(), weight )
						HTvsNPV_SinglyMerged.Fill( HT, events.nvtx, weight )
						jetPtvsMass_SinglyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].Pt(), listP4Jets[ listDuplicatesDeltaRCut[0] ].M(), weight )
						jetPtvsht_SinglyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].Pt(), HT, weight )
						jetMassvsht_SinglyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].M(), HT, weight )
						jetMassvsMET_SinglyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].M(),  events.met, weight )
						jetMassvsNPV_SinglyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].M(),  events.nvtx, weight )

						##### NO MERGED
						jetMass_SinglyMerged_DeltaRCut_NOMerged.Fill( tmpStopB, weight )
						#### NO MERGED 2
						jetPt_SinglyMerged_DeltaRCut_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaRCut[2] ].Pt(), weight )
						#### NO MERGED 3
						jetPt_SinglyMerged_DeltaRCut_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaRCut[3] ].Pt(), weight )

						ht_SinglyMerged_DeltaRCut.Fill( HT, weight )
						ht_SinglyMerged_DeltaRCut_groomed.Fill( HT_groomed, weight )
						HTvsNPV_SinglyMerged_groomed.Fill( HT_groomed, events.nvtx, weight )
						jetPtvsMass_SinglyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].Pt(), listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].M(), weight )
						jetPtvsht_SinglyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].Pt(), HT_groomed, weight )
						jetMassvsht_SinglyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].M(), HT_groomed, weight )
						jetMassvsMET_SinglyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].M(),  events.met, weight )
						jetMassvsNPV_SinglyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].M(),  events.nvtx, weight )

				######################################## Doubly Merged
				elif ( len( listDuplicatesDeltaRCut ) == 2 ) and ( numUniqueJetsDeltaRCut == 2 ) and ( len( listP4Jets ) == len ( listP4Jets_groomed ) ):
					for jparton, jLists in dictDeltaRCut.iteritems():
						if ( listDuplicatesDeltaRCut[0] == jLists[1][0] ):
							minDeltaRPartonJet_DoublyMerged_DeltaRCut_A.Fill( jLists[0][0], weight )
						if ( listDuplicatesDeltaRCut[1] == jLists[1][0] ):
							minDeltaRPartonJet_DoublyMerged_DeltaRCut_B.Fill( jLists[0][0], weight )

					if ( listDuplicatesDeltaRCut[0] == tmpListJetIndexDeltaRCut[0] ) and ( listDuplicatesDeltaRCut[0] == tmpListJetIndexDeltaRCut[1] ): 
						numberPartonsSameJet_DeltaRCut.Fill( 2 )
						####### STOP A
						tmpStopA = ( listP4Jets[ listDuplicatesDeltaRCut[0] ] ).M()
						jetMass_DoublyMerged_DeltaRCut.Fill( tmpStopA, weight )
						jetPt_DoublyMerged_DeltaRCut.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].Pt(), weight )
						HTvsNPV_DoublyMerged.Fill( HT, events.nvtx, weight )
						jetPtvsMass_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].Pt(), listP4Jets[ listDuplicatesDeltaRCut[0] ].M(), weight )
						jetPtvsht_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].Pt(), HT, weight )
						jetMassvsht_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].M(), HT, weight )
						jetMassvsMET_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].M(),  events.met, weight )
						jetMassvsNPV_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].M(),  events.nvtx, weight )

						#### STOP B
						tmpStopB = ( listP4Jets[ listDuplicatesDeltaRCut[1] ] ).M()
						jetMass_DoublyMerged_DeltaRCut.Fill( tmpStopB, weight )
						jetPt_DoublyMerged_DeltaRCut.Fill( listP4Jets[ listDuplicatesDeltaRCut[1] ].Pt(), weight )
						HTvsNPV_DoublyMerged.Fill( HT, events.nvtx, weight )
						jetPtvsMass_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[1] ].Pt(), listP4Jets[ listDuplicatesDeltaRCut[1] ].M(), weight )
						jetPtvsht_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[1] ].Pt(), HT, weight )
						jetMassvsht_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[1] ].M(), HT, weight )
						jetMassvsMET_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[1] ].M(),  events.met, weight )
						jetMassvsNPV_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[1] ].M(),  events.nvtx, weight )

						ht_DoublyMerged_DeltaRCut.Fill( HT, weight )
						ht_DoublyMerged_DeltaRCut_groomed.Fill( HT_groomed, weight )
						HTvsNPV_DoublyMerged_groomed.Fill( HT_groomed, events.nvtx, weight )
						jetPtvsMass_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].Pt(), listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].M(), weight )
						jetPtvsht_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].Pt(), HT_groomed, weight )
						jetMassvsht_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].M(), HT_groomed, weight )
						jetMassvsMET_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].M(),  events.met, weight )
						jetMassvsNPV_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].M(),  events.nvtx, weight )
						jetPtvsMass_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[1] ].Pt(), listP4Jets_groomed[ listDuplicatesDeltaRCut[1] ].M(), weight )
						jetPtvsht_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[1] ].Pt(), HT_groomed, weight )
						jetMassvsht_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[1] ].M(), HT_groomed, weight )
						jetMassvsMET_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[1] ].M(),  events.met, weight )
						jetMassvsNPV_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[1] ].M(),  events.nvtx, weight )

					elif ( listDuplicatesDeltaRCut[0] == tmpListJetIndexDeltaRCut[2] ) and ( listDuplicatesDeltaRCut[0] == tmpListJetIndexDeltaRCut[3] ): 
						numberPartonsSameJet_DeltaRCut.Fill( 2 )

						##### STOP B
						tmpStopB = ( listP4Jets[ listDuplicatesDeltaRCut[0] ] ).M()
						jetMass_DoublyMerged_DeltaRCut.Fill( tmpStopB, weight )
						jetPt_DoublyMerged_DeltaRCut.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].Pt(), weight )
						HTvsNPV_DoublyMerged.Fill( HT, events.nvtx, weight )
						jetPtvsMass_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].Pt(), listP4Jets[ listDuplicatesDeltaRCut[0] ].M(), weight )
						HTvsNPV_DoublyMerged.Fill( HT, events.nvtx, weight )
						jetPtvsMass_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[1] ].Pt(), listP4Jets[ listDuplicatesDeltaRCut[1] ].M(), weight )
						jetPtvsht_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[1] ].Pt(), HT, weight )
						jetMassvsht_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[1] ].M(), HT, weight )
						jetMassvsMET_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[1] ].M(),  events.met, weight )
						jetMassvsNPV_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[1] ].M(),  events.nvtx, weight )
						jetPtvsht_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].Pt(), HT, weight )
						jetMassvsht_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].M(), HT, weight )
						jetMassvsMET_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].M(),  events.met, weight )
						jetMassvsNPV_DoublyMerged.Fill( listP4Jets[ listDuplicatesDeltaRCut[0] ].M(),  events.nvtx, weight )

						##### STOP A
						tmpStopA = ( listP4Jets[ listDuplicatesDeltaRCut[1] ] ).M()
						jetMass_DoublyMerged_DeltaRCut.Fill( tmpStopA, weight )
						jetPt_DoublyMerged_DeltaRCut.Fill( listP4Jets[ listDuplicatesDeltaRCut[1] ].Pt(), weight )

						ht_DoublyMerged_DeltaRCut.Fill( HT, weight )
						ht_DoublyMerged_DeltaRCut_groomed.Fill( HT_groomed, weight )
						ht_DoublyMerged_DeltaRCut_groomed.Fill( HT_groomed, weight )
						HTvsNPV_DoublyMerged_groomed.Fill( HT_groomed, events.nvtx, weight )
						jetPtvsMass_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].Pt(), listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].M(), weight )
						jetPtvsht_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].Pt(), HT_groomed, weight )
						jetMassvsht_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].M(), HT_groomed, weight )
						jetMassvsMET_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].M(),  events.met, weight )
						jetMassvsNPV_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[0] ].M(),  events.nvtx, weight )
						jetPtvsMass_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[1] ].Pt(), listP4Jets_groomed[ listDuplicatesDeltaRCut[1] ].M(), weight )
						jetPtvsht_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[1] ].Pt(), HT_groomed, weight )
						jetMassvsht_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[1] ].M(), HT_groomed, weight )
						jetMassvsMET_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[1] ].M(),  events.met, weight )
						jetMassvsNPV_DoublyMerged_groomed.Fill( listP4Jets_groomed[ listDuplicatesDeltaRCut[1] ].M(),  events.nvtx, weight )

				##### if one duplicate and 1 different
				elif ( len( listDuplicatesDeltaRCut ) == 1 ) and ( numUniqueJetsDeltaRCut == 2 ):
					numberPartonsSameJet_DeltaRCut.Fill( 3 )


				##### all partons with same jet
				elif ( len( listDuplicatesDeltaRCut ) == 1 ) and ( numUniqueJetsDeltaRCut == 1 ):
					numberPartonsSameJet_DeltaRCut.Fill( 4 )

				##### in case I forgot some category
				else:
					numberPartonsSameJet_DeltaRCut.Fill( 5 )

			###### events without delta cut
			else:
				numberPartonsSameJet_DeltaRCut.Fill( 6 )

	################################################################################################## end event loop

	##### write output file 
	outputFile.cd()
	outputFile.Write()

	##### Closing
	print 'Writing output file: '+ outputFileName
	outputFile.Close()

	###### Extra: send prints to file
	#if couts == False: 
	#	sys.stdout = outfileStdOut
	#	f.close()
	#########################


#################################################################################
if __name__ == '__main__':

	usage = 'usage: %prog [options]'
	
	parser = optparse.OptionParser(usage=usage)
	parser.add_option( '-m', '--mass', action='store', type='int', dest='mass', default=50, help='Mass of the Stop' )
	parser.add_option( '-c', '--cut', action='store', type='float', dest='deltaRcut', default=0.4, help='Delta R cut' )
	parser.add_option( '-j', '--jetAlgo', action='store', type='string', dest='jetAlgo', default='AK5', help='Jet Algorithm' )
	parser.add_option( '-g', '--grooming', action='store', type='string', dest='grooming', default='', help='Jet Algorithm' )
	parser.add_option( '-d', '--debug', action='store_true', dest='couts', default=False, help='True print couts in screen, False print in a file' )
	parser.add_option( '-f', '--final', action='store_true', dest='final', default=False, help='If True, final version' )
	parser.add_option( '-q', '--qcd', action='store',  type='string', dest='QCD', default='250To500', help='Binning of QCD' )
	parser.add_option( '-s', '--sample', action='store',  type='string', dest='samples', default='Signal', help='Type of sample' )
	parser.add_option( '-n', '--nJob', action='store', type='int', dest='nJob', default=0, help='Number of Job' )
	parser.add_option( '-w', '--work', action='store_true', dest='work', default=False, help='True to work on LPC, False Hexfarm' )

	(options, args) = parser.parse_args()

	mass = options.mass
	couts = options.couts
	final = options.final
	jetAlgo = options.jetAlgo
	grooming = options.grooming
	QCD = options.QCD
	samples = options.samples
	Job = options.nJob
	FNAL = options.work
	deltaRcut = options.deltaRcut

	if 'QCD' in samples: 
		sample = 'QCD_HT-'+QCD
		if FNAL:
			#list = os.popen('ls -1 /eos/uscms/store/user/algomez/'+sample+'_8TeV_Summer12_DR53X-PU_S10_START53_V7A-v1/*.root').read().splitlines()
			tmpList = os.popen('ls -1v /eos/uscms/store/user/algomez/'+sample+'_8TeV_Summer12_DR53X-PU_S10_START53_V7A-v1/*.root').read().splitlines()
			outputDir = '/eos/uscms/store/user/algomez/QCD_8TeV/treeResults/'
			#outputDir = '/store/user/algomez/QCD_8TeV/treeResults/'
		else:
			tmpList = os.popen('ls -1v /cms/gomez/Files/QCD_8TeV/PATtuples/'+sample+'_8TeV_Summer12_DR53X-PU_S10_START53_V7A-v1/*.root').read().splitlines()
			outputDir = '/cms/gomez/Files/QCD_8TeV/treeResults/'
		filesPerJob = round(len(tmpList)/30)+1
		iniList = int(filesPerJob*Job)
		finList = int((filesPerJob*(Job+1))-1)
		print filesPerJob, iniList, finList
		list = tmpList[iniList:finList]
		#list = tmpList
		inputList = [i if i.startswith('file') else 'file:' + i for i in list]
		if '250To500' in QCD: weight = 19500*276000/27062078.0
		elif '500To1000' in QCD: weight = 19500*8426/30599292.0
		else: weight = 19500*204/13843863.0
	elif 'Signal' in samples: 
		sample = 'stop_UDD312_'+str(mass)
		if FNAL:
			#list = os.popen('ls -1v /eos/uscms/store/user/algomez/RPVSt100tojj_8TeV_HT500/'+sample+'/PATtuples/*.root').read().splitlines()
			list = os.popen('ls -1v /eos/uscms/store/user/algomez/RPVSttojj_8TeV/'+sample+'/PATtuples/*.root').read().splitlines()
			outputDir = '/eos/uscms/store/user/algomez/RPVSttojj_8TeV/'+sample+'/treeResults/'
			#outputDir = '/uscms_data/d3/algomez/files/RPVSttojj_8TeV/'
		else:
			#list = os.popen('ls -1 /cms/gomez/Substructure/Generation/Simulation/CMSSW_5_3_2_patch4/src/mySimulations/stop_UDD312_50/aodsim/*.root').read().splitlines()
			#list = os.popen('ls -1v /cms/gomez/Stops/st_jj/patTuples/'+sample+'/results/140418/*.root').read().splitlines()
			list = os.popen('ls -1v /cms/gomez/Files/RPVSttojj_8TeV/'+sample+'/PATtuples/*.root').read().splitlines()
			#outputDir = '/cms/gomez/Stops/st_jj/treeResults/'
			outputDir = '/cms/gomez/Files/RPVSttojj_8TeV/treeResults/'
			#list = [ '/cms/gomez/Stops/st_jj/patTuples/stopUDD312_50_tree_test_grom.root' ]
		inputList = [i if i.startswith('file') else 'file:' + i for i in list]
		if mass == 50: weight = 1
		#elif mass == 100: weight = 19500*559.757/100000.0
		elif mass == 100: weight = 1 #9500*559.757/555880845.74
		elif mass == 200: weight = 1 #9500*18.5245/100000.0
	elif 'Data' in samples:
		sample = 'Data_'+QCD
		if FNAL:
			list = os.popen('ls -1v /eos/uscms/store/user/algomez/'+sample+'/*.root').read().splitlines()
			#list = os.popen('ls -1v /uscmst1b_scratch/lpc1/3DayLifetime/algomez/'+sample+'/*.root').read().splitlines()
			outputDir = '/eos/uscms/store/user/algomez/Data/treeResults/'
			#outputDir = '/store/user/algomez/Data/treeResults/'
			#outputDir = '/uscms_data/d3/algomez/files/Data/treeResults/'
		else:
			list = os.popen('ls -1v /cms/gomez/Files/DATA/PATtuples/'+sample+'/*.root').read().splitlines()
			outputDir = '/cms/gomez/Files/DATA/treeResults/'
		inputList = [i if i.startswith('file') else 'file:' + i for i in list]
		weight = 1
	elif 'WJets' in samples:
		sample = 'WJetsFullyHadronic'
		if FNAL:
			#list = os.popen('ls -1v /eos/uscms/store/user/algomez/'+sample+'ToLNu_HT-400ToInf_8TeV-madgraph_v2_Summer12_DR53X-PU_S10_START53_V7A-v1/*.root').read().splitlines()
			list = os.popen('ls -1v /eos/uscms/store/user/algomez/'+sample+'_Ht100_Pt50_Pt30_deta22_Mqq200_8TeV-madgraph_Summer12_DR53X-PU_S10_START53_V7C-v1/*.root').read().splitlines()
			#outputDir = '/uscms_data/d3/algomez/files/WJets/treeResults/'
			outputDir = '/eos/uscms/store/user/algomez/WJets/treeResults/'
		else:
			list = os.popen('ls -1v /cms/gomez/Files/'+sample+'/PATtuples/*.root').read().splitlines()
			outputDir = '/cms/gomez/Files/'+sample+'/treeResults/'
		inputList = [i if i.startswith('file') else 'file:' + i for i in list]
		weight = 19500*0.215/196046.0
	elif 'ZJets' in samples:
		sample = 'ZJets'
		if FNAL:
			list = os.popen('ls -1v /eos/uscms/store/user/algomez/'+sample+'ToNuNu_400_HT_inf_TuneZ2Star_8TeV_madgraph_Summer12_DR53X-PU_S10_START53_V7A-v1/*.root').read().splitlines()
			outputDir = '/eos/uscms/store/user/algomez/ZJets/treeResults/'
		else:
			list = os.popen('ls -1v /cms/gomez/Files/'+sample+'/PATtuples/*.root').read().splitlines()
			outputDir = '/cms/gomez/Files/'+sample+'/treeResults/'
		inputList = [i if i.startswith('file') else 'file:' + i for i in list]
		weight = 19500*0.172/210160.0


	#outputDir = '/eos/uscms/store/user/algomez/'
	print 'InputFiles: ', inputList
	print 'Output_Dir: ', outputDir
	print 'weight: ', weight

	if not final : myTriggerAnalyzer( inputList[:5], outputDir, sample, couts, final, jetAlgo, grooming, weight, Job, FNAL, deltaRcut )
	else: myTriggerAnalyzer( inputList, outputDir, sample, couts, final, jetAlgo, grooming, weight, Job, FNAL, deltaRcut )

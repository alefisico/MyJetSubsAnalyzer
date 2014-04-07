#!/usr/bin/env python

'''
File: myMCTruthJetsMatching.py --mass 50 (optional) --debug -- final --jetAlgo AK5
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: Read genParticles and PFJets info, Matching and count number of events in different categories.
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
def get_info( infile, outputDir, sample, mass, couts, final, jetAlgo, grooming ):

	if not final: 
		outputFile = TFile( outputDir + sample + '_Matching_'+jetAlgo+'_'+grooming+'_Plots_'+dateKey+'.root', 'RECREATE' )
	else:
		if not ( os.path.exists( outputDir + 'rootFiles/' + monthKey ) ): os.makedirs( outputDir + 'rootFiles/' + monthKey )
		outputFile = TFile( outputDir + 'rootFiles/' + monthKey + '/' + sample + '_Matching_'+jetAlgo+'_'+grooming+'_Plots.root', 'RECREATE' )

	######## Extra, send print to file
	#if couts == False :
	#	outfileStdOut = sys.stdout
	#	f = file('tmp_'+sample+'_'+jetAlgo+'_'+dateKey+'.txt', 'w')
	#	sys.stdout = f
	#################################################

	####################################################################################################################################### Histograms
	nBinsDeltaR = 50
	maxDeltaR = 5. 
	maxMass = float(mass)*4. 
	maxJetPt = float(mass)*10
	nBinsMass = int(round( maxMass/5 ))
	nBinsJetPt = int(round( maxMass/10 ))
	nBinsPt = 100
	maxPt = 500.
	nBinsEta = 41
	maxEta = 4.1
	nBinsTau = 40
	maxTau = 1.

	################################################################################################### Event Variables
	ht 		= TH1F('h_ht_'+jetAlgo+'_'+grooming, 	'h_ht_'+jetAlgo, 	100,  	0, 	500.)
	numberPV 	= TH1F('h_numberPV_'+jetAlgo+'_'+grooming, 	'h_numberPV_'+jetAlgo, 	50,  	0., 	50.)
	MET 		= TH1F('h_MET_'+jetAlgo+'_'+grooming, 	'h_MET_'+jetAlgo, 	40,  	0, 	200.)
	numberJets 	= TH1F('h_numberJets_'+jetAlgo+'_'+grooming, 'h_numberJets_'+jetAlgo, 20,  0., 20.)
	numberPartons 	= TH1F('h_numberPartons_'+jetAlgo+'_'+grooming, 'h_numberPartons_'+jetAlgo, 6,  0., 6.)
	jetPt	 	= TH1F('h_jetPt_'+jetAlgo+'_'+grooming, 'h_jetPt_'+jetAlgo, nBinsPt,  0., maxPt)
	jetEta	 	= TH1F('h_jetEta_'+jetAlgo+'_'+grooming, 'h_jetEta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jetPhi	 	= TH1F('h_jetPhi_'+jetAlgo+'_'+grooming, 'h_jetPhi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jetMass	 	= TH1F('h_jetMass_'+jetAlgo+'_'+grooming, 'h_jetMass_'+jetAlgo, nBinsMass,  0., maxMass)
	jetArea 	= TH1F('h_jetArea_'+jetAlgo+'_'+grooming, 'h_jetArea_'+jetAlgo, 80,  0., 2.)
	jetTau1 	= TH1F('h_jetTau1_'+jetAlgo+'_'+grooming, 'h_jetTau1_'+jetAlgo, nBinsTau,  0., maxTau)
	jetTau2 	= TH1F('h_jetTau2_'+jetAlgo+'_'+grooming, 'h_jetTau2_'+jetAlgo, nBinsTau,  0., maxTau)
	jetTau3 	= TH1F('h_jetTau3_'+jetAlgo+'_'+grooming, 'h_jetTau3_'+jetAlgo, nBinsTau,  0., maxTau)
	jetTau21 	= TH1F('h_jetTau21_'+jetAlgo+'_'+grooming, 'h_jetTau21_'+jetAlgo, nBinsTau,  0., maxTau)
	jetTau31 	= TH1F('h_jetTau31_'+jetAlgo+'_'+grooming, 'h_jetTau31_'+jetAlgo, nBinsTau,  0., maxTau)
	jetTau32 	= TH1F('h_jetTau32_'+jetAlgo+'_'+grooming, 'h_jetTau32_'+jetAlgo, nBinsTau,  0., maxTau)


	########################################################################################################### Matching
	jetPt_match		 	= TH1F('h_jetPt_match_'+jetAlgo+'_'+grooming, 'h_jetPt_match_'+jetAlgo, nBinsMass,  0., maxMass)
	numberPartonsSameJet 		= TH1F('h_numberPartonsSameJet_'+jetAlgo+'_'+grooming,	'h_numberPartonsSameJet_'+jetAlgo,	8,   		0.,	8. )
	minDeltaRPartonJet 		= TH1F('h_minDeltaRPartonJet_'+jetAlgo+'_'+grooming,		'h_minDeltaRPartonJet_'+jetAlgo,		nBinsDeltaR, 	0.,	maxDeltaR )
	secMinDeltaRPartonJet		= TH1F('h_secMinDeltaRPartonJet_'+jetAlgo+'_'+grooming, 	'h_secMinDeltaRPartonJet_'+jetAlgo,	nBinsDeltaR, 	0.,	maxDeltaR )
	minvsSecMinDeltaRPartonJet 	= TH2F('h_minDeltaRvsSecMinDeltaR_'+jetAlgo+'_'+grooming,	'h_minDeltaRvsSecMinDeltaR_'+jetAlgo,nBinsDeltaR,0.,maxDeltaR, nBinsDeltaR, 0., maxDeltaR )

	################## No DeltaR cut - No merged
	numberPartonsWithDeltaR0p4_NoMerged = TH1F('h_numberPartonsWithDeltaR0p4_NoMerged_'+jetAlgo+'_'+grooming, 'h_numberPartonsWithDeltaR0p4_NoMerged_'+jetAlgo,	8,  0.,	8. )
	minDeltaRPartonJet_NoMerged 	= TH1F('h_minDeltaRPartonJet_NoMerged_'+jetAlgo+'_'+grooming, 	'h_minDeltaRPartonJet_NoMerged_'+jetAlgo,	nBinsDeltaR, 	0.,	maxDeltaR )
	minDeltaRPartonJet_NoMerged_0 	= TH1F('h_minDeltaRPartonJet_NoMerged_0_'+jetAlgo+'_'+grooming, 	'h_minDeltaRPartonJet_NoMerged_0_'+jetAlgo,	nBinsDeltaR, 	0.,	maxDeltaR )
	minDeltaRPartonJet_NoMerged_1 	= TH1F('h_minDeltaRPartonJet_NoMerged_1_'+jetAlgo+'_'+grooming, 	'h_minDeltaRPartonJet_NoMerged_1_'+jetAlgo,	nBinsDeltaR, 	0.,	maxDeltaR )
	minDeltaRPartonJet_NoMerged_2 	= TH1F('h_minDeltaRPartonJet_NoMerged_2_'+jetAlgo+'_'+grooming, 	'h_minDeltaRPartonJet_NoMerged_2_'+jetAlgo,	nBinsDeltaR, 	0.,	maxDeltaR )
	minDeltaRPartonJet_NoMerged_3 	= TH1F('h_minDeltaRPartonJet_NoMerged_3_'+jetAlgo+'_'+grooming, 	'h_minDeltaRPartonJet_NoMerged_3_'+jetAlgo,	nBinsDeltaR, 	0.,	maxDeltaR )
	invMass_NoMerged 		= TH1F('h_invMass_NoMerged_'+jetAlgo+'_'+grooming, 		'h_invMass_NoMerged_'+jetAlgo, 		nBinsMass, 	0., 	maxMass )
	jetPt_NoMerged		 	= TH1F('h_jetPt_NoMerged_'+jetAlgo+'_'+grooming, 'h_jetPt_NoMerged_'+jetAlgo, nBinsMass,  0., maxMass)

	################## No DeltaR cut - Singly Merged
	minDeltaRPartonJet_SinglyMerged_Merged 	= TH1F('h_minDeltaRPartonJet_SinglyMerged_Merged_'+jetAlgo+'_'+grooming, 		'h_minDeltaRPartonJet_SinglyMerged_Merged_'+jetAlgo,	nBinsDeltaR, 	0., 	maxDeltaR )
	secMinDeltaRPartonJet_SinglyMerged_Merged 	= TH1F('h_secMinDeltaRPartonJet_SinglyMerged_Merged_'+jetAlgo+'_'+grooming,	'h_secMinDeltaRPartonJet_SinglyMerged_Merged_'+jetAlgo, 	nBinsDeltaR, 	0., 	maxDeltaR )
	minDeltaRPartonJet_SinglyMerged_NOMerged 	= TH1F('h_minDeltaRPartonJet_SinglyMerged_NOMerged_'+jetAlgo+'_'+grooming, 		'h_minDeltaRPartonJet_SinglyMerged_NOMerged_'+jetAlgo,	nBinsDeltaR, 	0., 	maxDeltaR )
	secMinDeltaRPartonJet_SinglyMerged_NOMerged 	= TH1F('h_secMinDeltaRPartonJet_SinglyMerged_NOMerged_'+jetAlgo+'_'+grooming,	'h_secMinDeltaRPartonJet_SinglyMerged_NOMerged_'+jetAlgo,	nBinsDeltaR, 	0., 	maxDeltaR )
	minvsSecMinDeltaRPartonJet_SinglyMerged_Merged 	= TH2F('h_minvsSecMinDeltaRPartonJet_SinglyMerged_Merged_'+jetAlgo+'_'+grooming,	'h_minvsSecMinDeltaRPartonJet_SinglyMerged_Merged_'+jetAlgo, 	nBinsDeltaR, 	0., 	maxDeltaR, 	nBinsDeltaR, 	0., 	maxDeltaR )
	minvsSecMinDeltaRPartonJet_SinglyMerged_NOMerged 	= TH2F('h_minvsSecMinDeltaRPartonJet_SinglyMerged_NOMerged_'+jetAlgo+'_'+grooming,	'h_minvsSecMinDeltaRPartonJet_SinglyMerged_NOMerged_'+jetAlgo, 	nBinsDeltaR, 	0., 	maxDeltaR, 	nBinsDeltaR, 	0., 	maxDeltaR )
	invMass_SinglyMerged_NOMerged 	= TH1F('h_invMass_SinglyMerged_NOMerged_'+jetAlgo+'_'+grooming, 	'h_invMass_SinglyMerged_NOMerged_'+jetAlgo, 	nBinsMass, 	0., 	maxMass )
	invMass_SinglyMerged_Merged 		= TH1F('h_invMass_SinglyMerged_Merged_'+jetAlgo+'_'+grooming, 	'h_invMass_SinglyMerged_Merged_'+jetAlgo, 	nBinsMass, 	0., 	maxMass )
	jetPt_SinglyMerged_NOMerged		 	= TH1F('h_jetPt_SinglyMerged_NOMerged_'+jetAlgo+'_'+grooming, 'h_jetPt_SinglyMerged_NOMerged_'+jetAlgo, nBinsMass,  0., maxMass)
	jetPt_SinglyMerged_Merged		 	= TH1F('h_jetPt_SinglyMerged_Merged_'+jetAlgo+'_'+grooming, 'h_jetPt_SinglyMerged_Merged_'+jetAlgo, nBinsJetPt,  0., maxJetPt)

	################## No DeltaR cut - Doubly Merged
	minDeltaRPartonJet_DoublyMerged 		= TH1F('h_minDeltaRPartonJet_DoublyMerged_'+jetAlgo+'_'+grooming, 'h_minDeltaRPartonJet_DoublyMerged_'+jetAlgo, nBinsDeltaR, 0., maxDeltaR )
	secMinDeltaRPartonJet_DoublyMerged 	= TH1F('h_secMinDeltaRPartonJet_DoublyMerged_'+jetAlgo+'_'+grooming,'h_secMinDeltaRPartonJet_DoublyMerged_'+jetAlgo, nBinsDeltaR, 0., maxDeltaR )
	minvsSecMinDeltaRPartonJet_DoublyMerged 	= TH2F('h_minvsSecMinDeltaRPartonJet_DoublyMerged_'+jetAlgo+'_'+grooming,'h_minvsSecMinDeltaRPartonJet_DoublyMerged_'+jetAlgo, nBinsDeltaR, 0., 	maxDeltaR, nBinsDeltaR, 0., maxDeltaR )
	invMass_DoublyMerged_Merged 		= TH1F('h_invMass_DoublyMerged_Merged_'+jetAlgo+'_'+grooming, 	'h_invMass_DoublyMerged_Merged_'+jetAlgo, 	nBinsMass, 0., 	maxMass )
	jetPt_DoublyMerged		 	= TH1F('h_jetPt_DoublyMerged_'+jetAlgo+'_'+grooming, 'h_jetPt_DoublyMerged_'+jetAlgo, nBinsJetPt,  0., maxJetPt)

	################## No DeltaR cut - 3 partons merged
	minDeltaRPartonJet_TriplyMerged 		= TH1F('h_minDeltaRPartonJet_TriplyMerged_'+jetAlgo+'_'+grooming, 	'h_minDeltaRPartonJet_TriplyMerged_'+jetAlgo,	nBinsDeltaR, 0., maxDeltaR)
	secMinDeltaRPartonJet_TriplyMerged 		= TH1F('h_secMinDeltaRPartonJet_TriplyMerged_'+jetAlgo+'_'+grooming,'h_secMinDeltaRPartonJet_TriplyMerged_'+jetAlgo, nBinsDeltaR, 0., maxDeltaR)
	minvsSecMinDeltaRPartonJet_TriplyMerged 	= TH2F('h_minvsSecMinDeltaRPartonJet_TriplyMerged_'+jetAlgo+'_'+grooming,'h_minvsSecMinDeltaRPartonJet_TriplyMerged_'+jetAlgo, nBinsDeltaR, 0., maxDeltaR, nBinsDeltaR, 0., maxDeltaR )
	invMass_TriplyMerged_Merged 			= TH1F('h_invMass_TriplyMerged_Merged_'+jetAlgo+'_'+grooming, 	'h_invMass_TriplyMerged_Merged_'+jetAlgo, 	nBinsMass, 0., 	maxMass )
	jetPt_TriplyMerged_Merged		 	= TH1F('h_jetPt_TriplyMerged_Merged_'+jetAlgo+'_'+grooming, 'h_jetPt_TriplyMerged_Merged_'+jetAlgo, nBinsMass,  0., maxMass)

	################## No DeltaR cut - 4 partons merged
	minDeltaRPartonJet_FourlyMerged = TH1F('h_minDeltaRPartonJet_FourlyMerged_'+jetAlgo+'_'+grooming, 'h_minDeltaRPartonJet_FourlyMerged_'+jetAlgo,	nBinsDeltaR, 0., maxDeltaR)




	######################################################################################### with DeltaR0p4
	nBinsDeltaR0p4 = 20
	maxDeltaR0p4 = 1.
	jetPt_DeltaR0p4			 	= TH1F('h_jetPt_DeltaR0p4_'+jetAlgo+'_'+grooming, 'h_jetPt_DeltaR0p4_'+jetAlgo, nBinsMass,  0., maxMass)
	numberPartonsSameJet_DeltaR0p4 		= TH1F('h_numberPartonsSameJet_DeltaR0p4_'+jetAlgo+'_'+grooming, 	'h_numberPartonsSameJet_DeltaR0p4_'+jetAlgo,	8,  		0.,8. )
	minDeltaRPartonJet_DeltaR0p4 		= TH1F('h_minDeltaRPartonJet_DeltaR0p4_'+jetAlgo+'_'+grooming, 	'h_minDeltaRPartonJet_DeltaR0p4_'+jetAlgo,	nBinsDeltaR0p4,	0.,maxDeltaR0p4 )
	secMinDeltaRPartonJet_DeltaR0p4 	= TH1F('h_secMinDeltaRPartonJet_DeltaR0p4_'+jetAlgo+'_'+grooming,	'h_secMinDeltaRPartonJet_DeltaR0p4_'+jetAlgo,	nBinsDeltaR, 	0.,maxDeltaR)

	################## DeltaR cut - No Merged
	minDeltaRPartonJet_NoMerged_DeltaR0p4 	= TH1F('h_minDeltaRPartonJet_NoMerged_DeltaR0p4_'+jetAlgo+'_'+grooming, 	'h_minDeltaRPartonJet_NoMerged_DeltaR0p4_'+jetAlgo,		nBinsDeltaR0p4,	0.,	maxDeltaR0p4)
	minDeltaRPartonJet_NoMerged_DeltaR0p4_0 	= TH1F('h_minDeltaRPartonJet_NoMerged_DeltaR0p4_0_'+jetAlgo+'_'+grooming, 'h_minDeltaRPartonJet_NoMerged_DeltaR0p4_0_'+jetAlgo,	nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	minDeltaRPartonJet_NoMerged_DeltaR0p4_1 	= TH1F('h_minDeltaRPartonJet_NoMerged_DeltaR0p4_1_'+jetAlgo+'_'+grooming, 'h_minDeltaRPartonJet_NoMerged_DeltaR0p4_1_'+jetAlgo,	nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	minDeltaRPartonJet_NoMerged_DeltaR0p4_2 	= TH1F('h_minDeltaRPartonJet_NoMerged_DeltaR0p4_2_'+jetAlgo+'_'+grooming, 'h_minDeltaRPartonJet_NoMerged_DeltaR0p4_2_'+jetAlgo,	nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	minDeltaRPartonJet_NoMerged_DeltaR0p4_3 	= TH1F('h_minDeltaRPartonJet_NoMerged_DeltaR0p4_3_'+jetAlgo+'_'+grooming, 'h_minDeltaRPartonJet_NoMerged_DeltaR0p4_3_'+jetAlgo,	nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	invMass_NoMerged_DeltaR0p4 		= TH1F('h_invMass_NoMerged_DeltaR0p4_'+jetAlgo+'_'+grooming, 	'h_invMass_NoMerged_DeltaR0p4_'+jetAlgo, 	nBinsMass, 	0., maxMass )
	jetPt_NoMerged_DeltaR0p4		 	= TH1F('h_jetPt_NoMerged_DeltaR0p4_'+jetAlgo+'_'+grooming, 'h_jetPt_NoMerged_DeltaR0p4_'+jetAlgo, nBinsMass,  0., maxMass)

	################## DeltaR cut - singly merged
	minDeltaRPartonJet_SinglyMerged_Merged_DeltaR0p4 	= TH1F('h_minDeltaRPartonJet_SinglyMerged_Merged_DeltaR0p4_'+jetAlgo+'_'+grooming, 'h_minDeltaRPartonJet_SinglyMerged_Merged_DeltaR0p4_'+jetAlgo,	nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	secMinDeltaRPartonJet_SinglyMerged_Merged_DeltaR0p4 = TH1F('h_secMinDeltaRPartonJet_SinglyMerged_Merged_DeltaR0p4_'+jetAlgo+'_'+grooming, 'h_secMinDeltaRPartonJet_SinglyMerged_Merged_DeltaR0p4_'+jetAlgo,nBinsDeltaR, 	0.,	maxDeltaR )
	minDeltaRPartonJet_SinglyMerged_NOMerged_DeltaR0p4 	= TH1F('h_minDeltaRPartonJet_SinglyMerged_NOMerged_DeltaR0p4_'+jetAlgo+'_'+grooming, 'h_minDeltaRPartonJet_SinglyMerged_NOMerged_DeltaR0p4_'+jetAlgo,	nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	secMinDeltaRPartonJet_SinglyMerged_NOMerged_DeltaR0p4 = TH1F('h_secMinDeltaRPartonJet_SinglyMerged_NOMerged_DeltaR0p4_'+jetAlgo+'_'+grooming, 'h_secMinDeltaRPartonJet_SinglyMerged_NOMerged_DeltaR0p4_'+jetAlgo,nBinsDeltaR, 	0.,	maxDeltaR )
	minvsSecMinDeltaRPartonJet_SinglyMerged_Merged_DeltaR0p4 	= TH2F('h_minvsSecMinDeltaRPartonJet_SinglyMerged_Merged_DeltaR0p4_'+jetAlgo+'_'+grooming,	'h_minvsSecMinDeltaRPartonJet_SinglyMerged_Merged_DeltaR0p4_'+jetAlgo, 	nBinsDeltaR, 	0., 	maxDeltaR, 	nBinsDeltaR, 	0., 	maxDeltaR )
	minvsSecMinDeltaRPartonJet_SinglyMerged_NOMerged_DeltaR0p4 	= TH2F('h_minvsSecMinDeltaRPartonJet_SinglyMerged_NOMerged_DeltaR0p4_'+jetAlgo+'_'+grooming,	'h_minvsSecMinDeltaRPartonJet_SinglyMerged_NOMerged_DeltaR0p4_'+jetAlgo, 	nBinsDeltaR, 	0., 	maxDeltaR, 	nBinsDeltaR, 	0., 	maxDeltaR )
	invMass_SinglyMerged_DeltaR0p4_NOMerged 	= TH1F('h_invMass_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo+'_'+grooming, 	'h_invMass_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo, 	nBinsMass, 	0., 	maxMass )
	invMass_SinglyMerged_DeltaR0p4_Merged 	= TH1F('h_invMass_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo+'_'+grooming, 	'h_invMass_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo, 		nBinsMass, 	0., 	maxMass )
	jetPt_SinglyMerged_DeltaR0p4_NOMerged	= TH1F('h_jetPt_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo+'_'+grooming, 'h_jetPt_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo, nBinsMass,  0., maxMass)
	jetPt_SinglyMerged_DeltaR0p4_Merged		= TH1F('h_jetPt_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo+'_'+grooming, 'h_jetPt_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo, nBinsJetPt,  0., maxJetPt)
	jetTau1_SinglyMerged_DeltaR0p4_NOMerged 	= TH1F('h_jetTau1_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo+'_'+grooming, 	'h_jetTau1_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo, 	40,  	0, 	1.)
	jetTau2_SinglyMerged_DeltaR0p4_NOMerged 	= TH1F('h_jetTau2_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo+'_'+grooming, 	'h_jetTau2_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo, 	40,  	0, 	1.)
	jetTau3_SinglyMerged_DeltaR0p4_NOMerged 	= TH1F('h_jetTau3_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo+'_'+grooming, 	'h_jetTau3_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo, 	40,  	0, 	1.)
	jetTau21_SinglyMerged_DeltaR0p4_NOMerged	= TH1F('h_jetTau21_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo+'_'+grooming, 	'h_jetTau21_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo, 	40,  	0, 	1.)
	jetTau31_SinglyMerged_DeltaR0p4_NOMerged	= TH1F('h_jetTau31_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo+'_'+grooming, 	'h_jetTau31_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo, 	40,  	0, 	1.)
	jetTau32_SinglyMerged_DeltaR0p4_NOMerged	= TH1F('h_jetTau32_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo+'_'+grooming, 	'h_jetTau32_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo, 	40,  	0, 	1.)
	jetArea_SinglyMerged_DeltaR0p4_NOMerged 	= TH1F('h_jetArea_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo+'_'+grooming, 	'h_jetArea_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo, 	80,  	0, 	2.)
	jetMass_SinglyMerged_DeltaR0p4_NOMerged 	= TH1F('h_jetMass_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo+'_'+grooming, 	'h_jetMass_SinglyMerged_DeltaR0p4_NOMerged_'+jetAlgo, 	nBinsMass,  	0, 	maxMass)
	jetTau21_SinglyMerged_DeltaR0p4_NOMerged_2D 	= TH2F('h_jetTau21_SinglyMerged_DeltaR0p4_NOMerged_2D_'+jetAlgo+'_'+grooming, 	'h_jetTau21_SinglyMerged_DeltaR0p4_NOMerged_2D_'+jetAlgo, 	40,  	0, 	1., 	40,  	0, 	1.)
	jetTau31_SinglyMerged_DeltaR0p4_NOMerged_2D 	= TH2F('h_jetTau31_SinglyMerged_DeltaR0p4_NOMerged_2D_'+jetAlgo+'_'+grooming, 	'h_jetTau31_SinglyMerged_DeltaR0p4_NOMerged_2D_'+jetAlgo, 	40,  	0, 	1., 	40,  	0, 	1.)
	jetTau32_SinglyMerged_DeltaR0p4_NOMerged_2D 	= TH2F('h_jetTau32_SinglyMerged_DeltaR0p4_NOMerged_2D_'+jetAlgo+'_'+grooming, 	'h_jetTau32_SinglyMerged_DeltaR0p4_NOMerged_2D_'+jetAlgo, 	40,  	0, 	1., 	40,  	0, 	1.)
	jetMassVsPt_SinglyMerged_DeltaR0p4_NOMerged_2D 	= TH2F('h_jetMassVsPt_SinglyMerged_DeltaR0p4_NOMerged_2D_'+jetAlgo+'_'+grooming, 	'h_jetMassVsPt_SinglyMerged_DeltaR0p4_NOMerged_2D_'+jetAlgo, nBinsMass,  0., maxMass, 	nBinsJetPt,  	0, 	maxJetPt)
	jetTau1_SinglyMerged_DeltaR0p4_Merged 	= TH1F('h_jetTau1_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo+'_'+grooming, 	'h_jetTau1_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo, 	40,  	0, 	1.)
	jetTau2_SinglyMerged_DeltaR0p4_Merged 	= TH1F('h_jetTau2_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo+'_'+grooming, 	'h_jetTau2_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo, 	40,  	0, 	1.)
	jetTau3_SinglyMerged_DeltaR0p4_Merged 	= TH1F('h_jetTau3_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo+'_'+grooming, 	'h_jetTau3_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo, 	40,  	0, 	1.)
	jetTau21_SinglyMerged_DeltaR0p4_Merged	= TH1F('h_jetTau21_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo+'_'+grooming, 	'h_jetTau21_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo, 	40,  	0, 	1.)
	jetTau31_SinglyMerged_DeltaR0p4_Merged	= TH1F('h_jetTau31_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo+'_'+grooming, 	'h_jetTau31_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo, 	40,  	0, 	1.)
	jetTau32_SinglyMerged_DeltaR0p4_Merged	= TH1F('h_jetTau32_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo+'_'+grooming, 	'h_jetTau32_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo, 	40,  	0, 	1.)
	jetArea_SinglyMerged_DeltaR0p4_Merged 	= TH1F('h_jetArea_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo+'_'+grooming, 	'h_jetArea_SinglyMerged_DeltaR0p4_Merged_'+jetAlgo, 	80,  	0, 	2.)
	jetTau21_SinglyMerged_DeltaR0p4_Merged_2D 	= TH2F('h_jetTau21_SinglyMerged_DeltaR0p4_Merged_2D_'+jetAlgo+'_'+grooming, 	'h_jetTau21_SinglyMerged_DeltaR0p4_Merged_2D_'+jetAlgo, 	40,  	0, 	1., 	40,  	0, 	1.)
	jetTau31_SinglyMerged_DeltaR0p4_Merged_2D 	= TH2F('h_jetTau31_SinglyMerged_DeltaR0p4_Merged_2D_'+jetAlgo+'_'+grooming, 	'h_jetTau31_SinglyMerged_DeltaR0p4_Merged_2D_'+jetAlgo, 	40,  	0, 	1., 	40,  	0, 	1.)
	jetTau32_SinglyMerged_DeltaR0p4_Merged_2D 	= TH2F('h_jetTau32_SinglyMerged_DeltaR0p4_Merged_2D_'+jetAlgo+'_'+grooming, 	'h_jetTau32_SinglyMerged_DeltaR0p4_Merged_2D_'+jetAlgo, 	40,  	0, 	1., 	40,  	0, 	1.)
	jetMassVsPt_SinglyMerged_DeltaR0p4_Merged_2D 	= TH2F('h_jetMassVsPt_SinglyMerged_DeltaR0p4_Merged_2D_'+jetAlgo+'_'+grooming, 	'h_jetMassVsPt_SinglyMerged_DeltaR0p4_Merged_2D_'+jetAlgo, nBinsMass,  0., maxMass, 	nBinsJetPt,  	0, 	maxJetPt)

	########## Delta cut - Doubly Merged 
	minDeltaRPartonJet_DoublyMerged_DeltaR0p4_A 	= TH1F('h_minDeltaRPartonJet_DoublyMerged_DeltaR0p4_A_'+jetAlgo+'_'+grooming, 	'h_minDeltaRPartonJet_DoublyMerged_DeltaR0p4_A_'+jetAlgo,		nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	secMinDeltaRPartonJet_DoublyMerged_DeltaR0p4_A 	= TH1F('h_secMinDeltaRPartonJet_DoublyMerged_DeltaR0p4_A_'+jetAlgo+'_'+grooming, 'h_secMinDeltaRPartonJet_DoublyMerged_DeltaR0p4_A_'+jetAlgo,	nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	minDeltaRPartonJet_DoublyMerged_DeltaR0p4_B 	= TH1F('h_minDeltaRPartonJet_DoublyMerged_DeltaR0p4_B_'+jetAlgo+'_'+grooming, 	'h_minDeltaRPartonJet_DoublyMerged_DeltaR0p4_B_'+jetAlgo,		nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	secMinDeltaRPartonJet_DoublyMerged_DeltaR0p4_B 	= TH1F('h_secMinDeltaRPartonJet_DoublyMerged_DeltaR0p4_B_'+jetAlgo+'_'+grooming, 'h_secMinDeltaRPartonJet_DoublyMerged_DeltaR0p4_B_'+jetAlgo,	nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	invMass_DoublyMerged_DeltaR0p4 		= TH1F('h_invMass_DoublyMerged_DeltaR0p4_'+jetAlgo+'_'+grooming, 	'h_invMass_DoublyMerged_DeltaR0p4_'+jetAlgo, 		nBinsMass, 	0., 	maxMass )
	jetPt_DoublyMerged_DeltaR0p4		 	= TH1F('h_jetPt_DoublyMerged_DeltaR0p4_'+jetAlgo+'_'+grooming, 'h_jetPt_DoublyMerged_DeltaR0p4_'+jetAlgo, nBinsJetPt,  0., maxJetPt)
	jetTau1_DoublyMerged_DeltaR0p4 	= TH1F('h_jetTau1_DoublyMerged_DeltaR0p4_'+jetAlgo+'_'+grooming, 	'h_jetTau1_DoublyMerged_DeltaR0p4_'+jetAlgo, 	40,  	0, 	1.)
	jetTau2_DoublyMerged_DeltaR0p4 	= TH1F('h_jetTau2_DoublyMerged_DeltaR0p4_'+jetAlgo+'_'+grooming, 	'h_jetTau2_DoublyMerged_DeltaR0p4_'+jetAlgo, 	40,  	0, 	1.)
	jetTau3_DoublyMerged_DeltaR0p4 	= TH1F('h_jetTau3_DoublyMerged_DeltaR0p4_'+jetAlgo+'_'+grooming, 	'h_jetTau3_DoublyMerged_DeltaR0p4_'+jetAlgo, 	40,  	0, 	1.)
	jetTau21_DoublyMerged_DeltaR0p4	= TH1F('h_jetTau21_DoublyMerged_DeltaR0p4_'+jetAlgo+'_'+grooming, 	'h_jetTau21_DoublyMerged_DeltaR0p4_'+jetAlgo, 	40,  	0, 	1.)
	jetTau31_DoublyMerged_DeltaR0p4	= TH1F('h_jetTau31_DoublyMerged_DeltaR0p4_'+jetAlgo+'_'+grooming, 	'h_jetTau31_DoublyMerged_DeltaR0p4_'+jetAlgo, 	40,  	0, 	1.)
	jetTau32_DoublyMerged_DeltaR0p4	= TH1F('h_jetTau32_DoublyMerged_DeltaR0p4_'+jetAlgo+'_'+grooming, 	'h_jetTau32_DoublyMerged_DeltaR0p4_'+jetAlgo, 	40,  	0, 	1.)
	jetArea_DoublyMerged_DeltaR0p4 	= TH1F('h_jetArea_DoublyMerged_DeltaR0p4_'+jetAlgo+'_'+grooming, 	'h_jetArea_DoublyMerged_DeltaR0p4_'+jetAlgo, 	80,  	0, 	2.)
	jetTau21_DoublyMerged_DeltaR0p4_2D 	= TH2F('h_jetTau21_DoublyMerged_DeltaR0p4_2D_'+jetAlgo+'_'+grooming, 	'h_jetTau21_DoublyMerged_DeltaR0p4_2D_'+jetAlgo, 	40,  	0, 	1., 	40,  	0, 	1.)
	jetTau31_DoublyMerged_DeltaR0p4_2D 	= TH2F('h_jetTau31_DoublyMerged_DeltaR0p4_2D_'+jetAlgo+'_'+grooming, 	'h_jetTau31_DoublyMerged_DeltaR0p4_2D_'+jetAlgo, 	40,  	0, 	1., 	40,  	0, 	1.)
	jetTau32_DoublyMerged_DeltaR0p4_2D 	= TH2F('h_jetTau32_DoublyMerged_DeltaR0p4_2D_'+jetAlgo+'_'+grooming, 	'h_jetTau32_DoublyMerged_DeltaR0p4_2D_'+jetAlgo, 	40,  	0, 	1., 	40,  	0, 	1.)
	jetMassVsPt_DoublyMerged_DeltaR0p4_2D 	= TH2F('h_jetMassVsPt_DoublyMerged_DeltaR0p4_2D_'+jetAlgo+'_'+grooming, 	'h_jetMassVsPt_DoublyMerged_DeltaR0p4_2D_'+jetAlgo, nBinsMass,  0., maxMass, 	nBinsJetPt,  	0, 	maxJetPt)

	################## DeltaR cut - 3 partons merged
	minDeltaRPartonJet_TriplyMerged_DeltaR0p4 	= TH1F('h_minDeltaRPartonJet_TriplyMerged_DeltaR0p4_'+jetAlgo+'_'+grooming, 	'h_minDeltaRPartonJet_TriplyMerged_DeltaR0p4_'+jetAlgo,	nBinsDeltaR0p4, 	0.,	maxDeltaR0p4 )
	secMinDeltaRPartonJet_TriplyMerged_DeltaR0p4 	= TH1F('h_secMinDeltaRPartonJet_TriplyMerged_DeltaR0p4_'+jetAlgo+'_'+grooming,	'h_secMinDeltaRPartonJet_TriplyMerged_DeltaR0p4_'+jetAlgo,	nBinsDeltaR, 		0.,	maxDeltaR )
	invMass_TriplyMerged_DeltaR0p4_Merged 	= TH1F('h_invMass_TriplyMerged_DeltaR0p4_Merged_'+jetAlgo+'_'+grooming, 		'h_invMass_TriplyMerged_DeltaR0p4_Merged_'+jetAlgo, 		nBinsMass, 		0., 	maxMass )
	jetPt_TriplyMerged_DeltaR0p4_Merged 	= TH1F('h_jetPt_TriplyMerged_DeltaR0p4_Merged_'+jetAlgo+'_'+grooming, 'h_jetPt_TriplyMerged_DeltaR0p4_Merged_'+jetAlgo, nBinsMass,  0., maxMass)

	################## DeltaR cut - 4 partons merged
	minDeltaRPartonJet_FourlyMerged_DeltaR0p4 = TH1F('h_minDeltaRPartonJet_FourlyMerged_DeltaR0p4_'+jetAlgo+'_'+grooming, 'h_minDeltaRPartonJet_FourlyMerged_DeltaR0p4_'+jetAlgo,	nBinsDeltaR0p4, 0.,	maxDeltaR0p4)

	#h2D = TH2F('h_minDeltaRvsSecMinDeltaR_'+jetAlgo+'_'+grooming,'h_minDeltaRvsSecMinDeltaR_'+jetAlgo, nBinsDeltaR, 0., maxDeltaR, nBinsDeltaR, 0., maxDeltaR )
	#####################################################################################################################################

	###################################### Get GenTree 
	events = TChain( 'PFJet_'+jetAlgo+grooming+'/events' )

	# Loop over the filenames and add to tree.
	for filename in infile:
		print("Adding file: " + filename)
		events.Add(filename)
	#events = inputFile.Get('dijets_'+type+'/events')

	##### read the tree & fill histosgrams -
	numEntries = events.GetEntries()
	
	#print 'Jet Algorithm processing: '+type, '------> Number of events: '+str(numEntries)
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
		numberPartons.Fill( len( listP4PartonsFromStops ) )
		tmpMCStopA = ( listP4PartonsFromStopA[0] + listP4PartonsFromStopA[1] ).M()
		tmpMCStopB = ( listP4PartonsFromStopB[0] + listP4PartonsFromStopB[1] ).M()
		if couts: print tmpMCStopA, tmpMCStopB
		if couts: print listP4PartonsFromStops[0].Pt(), listP4PartonsFromStops[1].Pt(), listP4PartonsFromStops[2].Pt(), listP4PartonsFromStops[3].Pt() 
		#######################################################################################################################################

		###################################################################### Store Jet Info
		listP4Jets = []
		HT = 0
		for j in range( events.nJets ):
			tau1 = -999
			tau2 = -999
			tau3 = -999
			if ( events.jetPt[j] > 20 ) and ( abs( events.jetEta[j] ) < 2.5 ):
				tmpP4 = TLorentzVector()
				tmpP4.SetPtEtaPhiE( events.jetPt[j], events.jetEta[j], events.jetPhi[j], events.jetEnergy[j] )
				if not events.jetTau1[j] == 0: tau1 = events.jetTau1[j]
				if not events.jetTau2[j] == 0: tau2 = events.jetTau2[j]
				if not events.jetTau3[j] == 0: tau3 = events.jetTau3[j]
				tmpListP4Jets = [ tmpP4, tau1, tau2, tau3, events.jetArea[j] ]
				listP4Jets.append( tmpListP4Jets )
				HT += events.jetPt[j]
				jetPt.Fill( events.jetPt[j] )
				jetEta.Fill( events.jetEta[j] )
				jetPhi.Fill( events.jetPhi[j] )
				jetMass.Fill( tmpP4.M() )
				jetArea.Fill( events.jetArea[j] )
				jetTau1.Fill( tau1 )
				jetTau2.Fill( tau2 )
				jetTau3.Fill( tau3 )
				jetTau21.Fill( tau2 / tau1 )
				jetTau31.Fill( tau3 / tau1 )
				jetTau32.Fill( tau3 / tau2 )

		numberJets.Fill( len( listP4Jets ) )
		ht.Fill( HT )
		numberPV.Fill( events.nvtx )
		MET.Fill( events.met )
		#if len( tmplistP4Jets ) > 3 : listP4Jets = tmplistP4Jets
		#if debug: print tmplistP4Jets
		#if debug: print listP4Jets
		#if debug: print len(listP4Jets)
		if couts: 
			for i in range( len( listP4Jets ) ): print i, listP4Jets[i][0].Pt()
		###########################################################################################

		################### Calculate DeltaR between each parton and each jet
		dictDeltaR = {}
		dictDeltaR1 = {}
		dictDeltaR0p4 = {}
		tmpListJetIndex = []
		tmpListJetIndexDeltaR0p4 = []
		for iparton in range( len( listP4PartonsFromStops ) ):
			listDeltaR = []
			#if debug: print '0 ', listP4PartonsFromStops[iparton].Pt()
			for ijet in range( len( listP4Jets ) ):
				deltaR = listP4PartonsFromStops[iparton].DeltaR( listP4Jets[ijet][0] )
				listDeltaR.append( deltaR )
				#if debug: print '1 ', ijet, listP4PartonsFromStops[iparton].Pt(), listP4Jets[ijet].Pt(), deltaR

			#if debug: print '2 ', listDeltaR
			#if debug: print '3 ', sortedListDeltaR
			sortedListDeltaR = sorted( listDeltaR )
			jetIndex = []
			if len( listDeltaR ) > 0:
				for ii in sortedListDeltaR:
					tmpjetIndex = listDeltaR.index( ii )
					jetIndex.append( tmpjetIndex )
					#if debug: print '4 ', ii, tmpjetIndex
				dictDeltaR[ iparton ] = [ sortedListDeltaR, jetIndex ]
				tmpListJetIndex.append( jetIndex[0] )
				if ( sortedListDeltaR[0] < 0.4 ): 
					dictDeltaR0p4[ iparton ] = [ sortedListDeltaR, jetIndex ]
					tmpListJetIndexDeltaR0p4.append( jetIndex[0] )
					#if debug: print '5 ', ii, jetIndex

		#if debug: print '6 ', dictDeltaR
		#dummyList.append( dictDeltaR )
		#if debug: print '6 ', dictDeltaR1
		#if debug: print '7 ', dictDeltaR0p4
		#if len(dictDeltaR0p4) == 0 : dummyList1.append( dictDeltaR0p4 )
		#if len(dictDeltaR0p4) == 1 : dummyList2.append( dictDeltaR0p4 )
		#if len(dictDeltaR0p4) == 2 : dummyList3.append( dictDeltaR0p4 )
		#if len(dictDeltaR0p4) == 3 : dummyList4.append( dictDeltaR0p4 )
		#if len(dictDeltaR0p4) == 4 : dummyList5.append( dictDeltaR0p4 )
		#if len(dictDeltaR0p4) > 4  : dummyList6.append( dictDeltaR0p4 )
		#if debug: print '8 ', tmpListJetIndex
		#if debug: print '9 ', tmpListJetIndexDeltaR0p4
		###############################################################################################################

		######### All jets
		for i,listParton in dictDeltaR.iteritems(): 
			if len( listParton[0] ) > 0: minDeltaRPartonJet.Fill( listParton[0][0] )
			if len( listParton[0] ) > 1: 
				secMinDeltaRPartonJet.Fill( listParton[0][1] )
				minvsSecMinDeltaRPartonJet.Fill( listParton[0][0], listParton[0][1] )
		##########################################################################################

		######### NO CUT in DeltaR
		appearances = defaultdict(int)
		for curr in tmpListJetIndex: appearances[curr] += 1
		listDuplicates = [ i for i, k in appearances.iteritems() if k > 1 ]
		numUniqueJets = len( set( tmpListJetIndex ) )
		#if debug: print '10 ', listDuplicates
		#if debug: print '11 ', numUniqueJets


		if ( len( tmpListJetIndex ) == 4 ) and ( len( listP4Jets ) > 3 ):		
			for z in range( len( listP4Jets ) ): jetPt_match.Fill( listP4Jets[z][0].Pt() )
			##### if no duplicate, i.e. 4 different match jets
			if ( len( listDuplicates ) == 0 ) and ( numUniqueJets == 4 ):
				counterNoMergedMatch = 0
				numberPartonsSameJet.Fill( 0 )
				#if debug: print '4 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				#if debug: print '1', jLists[0], jLists[1]
				#dummyCounter += 1
				for jparton, jLists in dictDeltaR.iteritems():
					if jparton == 0: 
						minDeltaRPartonJet_NoMerged_0.Fill( jLists[0][0] )
						if jLists[0][0] < 0.4 : counterNoMergedMatch += 1
					if jparton == 1: 
						minDeltaRPartonJet_NoMerged_1.Fill( jLists[0][0] )
						if jLists[0][0] < 0.4 : counterNoMergedMatch += 1
					if jparton == 2: 
						minDeltaRPartonJet_NoMerged_2.Fill( jLists[0][0] )
						if jLists[0][0] < 0.4 : counterNoMergedMatch += 1
					if jparton == 3: 
						minDeltaRPartonJet_NoMerged_3.Fill( jLists[0][0] )
						if jLists[0][0] < 0.4 : counterNoMergedMatch += 1
					minDeltaRPartonJet_NoMerged.Fill( jLists[0][0] )
					#if debug: print '12 ', jparton, jLists[0][0]
				numberPartonsWithDeltaR0p4_NoMerged.Fill( counterNoMergedMatch ) 
				tmpA = ( listP4Jets[ tmpListJetIndex[0] ][0] + listP4Jets[ tmpListJetIndex[1] ][0] ).M()
				tmpB = ( listP4Jets[ tmpListJetIndex[2] ][0] + listP4Jets[ tmpListJetIndex[3] ][0] ).M()
				invMass_NoMerged.Fill( tmpA )
				invMass_NoMerged.Fill( tmpB )
				for x in range( len( tmpListJetIndex ) ): jetPt_NoMerged.Fill( listP4Jets[ tmpListJetIndex[x] ][0].Pt() )

			##### if one duplicate and 2 different
			elif ( len( listDuplicates ) == 1 ) and ( numUniqueJets == 3 ):
				numberPartonsSameJet.Fill( 1 )
				#if debug: print '1 duplicate + 2 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				for jparton, jLists in dictDeltaR.iteritems():
					#if debug: print '2', jLists[0], jLists[1]
					if ( listDuplicates[0] == jLists[1][0] ):
						#if debug: print jLists[0][0], jLists[0][1]
						minDeltaRPartonJet_SinglyMerged_Merged.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_SinglyMerged_Merged.Fill( jLists[0][1] )
						minvsSecMinDeltaRPartonJet_SinglyMerged_Merged.Fill( jLists[0][0], jLists[0][1] )
					else:
						minDeltaRPartonJet_SinglyMerged_NOMerged.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_SinglyMerged_NOMerged.Fill( jLists[0][1] )
						minvsSecMinDeltaRPartonJet_SinglyMerged_NOMerged.Fill( jLists[0][0], jLists[0][1] )

				#if couts: print tmpListJetIndex
				if ( listDuplicates[0] != tmpListJetIndex[0] ) and ( listDuplicates[0] != tmpListJetIndex[1] ): 
					tmpStopA = ( listP4Jets[ tmpListJetIndex[0] ][0] + listP4Jets[ tmpListJetIndex[1] ][0] ).M()
					invMass_SinglyMerged_NOMerged.Fill( tmpStopA )
					jetPt_SinglyMerged_NOMerged.Fill( listP4Jets[ tmpListJetIndex[0] ][0].Pt() )
					jetPt_SinglyMerged_NOMerged.Fill( listP4Jets[ tmpListJetIndex[1] ][0].Pt() )
					tmpStopC = ( listP4Jets[ listDuplicates[0] ][0] ).M()
					invMass_SinglyMerged_Merged.Fill( tmpStopC )
					jetPt_SinglyMerged_Merged.Fill( listP4Jets[ listDuplicates[0] ][0].Pt() )
					#if couts: print 'yes1', tmpStopA, tmpStopC
				elif ( listDuplicates[0] != tmpListJetIndex[2] ) and ( listDuplicates[0] != tmpListJetIndex[3] ): 
					tmpStopB = ( listP4Jets[ tmpListJetIndex[2] ][0] + listP4Jets[ tmpListJetIndex[3] ][0] ).M()
					invMass_SinglyMerged_NOMerged.Fill( tmpStopB )
					jetPt_SinglyMerged_NOMerged.Fill( listP4Jets[ tmpListJetIndex[2] ][0].Pt() )
					jetPt_SinglyMerged_NOMerged.Fill( listP4Jets[ tmpListJetIndex[3] ][0].Pt() )
					tmpStopC = ( listP4Jets[ listDuplicates[0] ][0] ).M()
					invMass_SinglyMerged_Merged.Fill( tmpStopC )
					jetPt_SinglyMerged_Merged.Fill( listP4Jets[ listDuplicates[0] ][0].Pt() )
					#if couts: print 'yes2', tmpStopB, tmpStopC

			##### if a pair of two duplicates
			elif ( len( listDuplicates ) == 2 ) and ( numUniqueJets == 2 ):
				numberPartonsSameJet.Fill( 2 )
				#if debug: print '5', jLists[0], jLists[1]
				#if debug: print 'Pair of two duplicate match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				for jparton, jLists in dictDeltaR.iteritems():
					if ( listDuplicates[0] == jLists[1][0] ) or ( listDuplicates[1] == jLists[1][0] ):
						minDeltaRPartonJet_DoublyMerged.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_DoublyMerged.Fill( jLists[0][1] )
						minvsSecMinDeltaRPartonJet_DoublyMerged.Fill( jLists[0][0], jLists[0][1] )
						#if debug: print jLists[1][0], listDuplicates
				tmpStopA = ( listP4Jets[ listDuplicates[0] ][0] ).M()
				invMass_DoublyMerged_Merged.Fill( tmpStopA )
				jetPt_DoublyMerged.Fill( listP4Jets[ listDuplicates[0] ][0].Pt() )
				tmpStopB = ( listP4Jets[ listDuplicates[1] ][0] ).M()
				invMass_DoublyMerged_Merged.Fill( tmpStopB )
				jetPt_DoublyMerged.Fill( listP4Jets[ listDuplicates[1] ][0].Pt() )

			##### if one duplicate and 1 different
			elif ( len( listDuplicates ) == 1 ) and ( numUniqueJets == 2 ):
				numberPartonsSameJet.Fill( 3 )
				#if debug: print '1 duplicate + 1 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				#if debug: print '3', jLists[0], jLists[1]
				for jparton, jLists in dictDeltaR.iteritems():
					if ( listDuplicates[0] == jLists[1][0] ):
						minDeltaRPartonJet_TriplyMerged.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_TriplyMerged.Fill( jLists[0][1] )
						minvsSecMinDeltaRPartonJet_TriplyMerged.Fill( jLists[0][0], jLists[0][1] )
						#if debug: print jLists[1][0], listDuplicates
				tmpMass = ( listP4Jets[ listDuplicates[0] ][0] ).M()
				invMass_TriplyMerged_Merged.Fill( tmpMass )
				jetPt_TriplyMerged_Merged.Fill( listP4Jets[ listDuplicates[0] ][0].Pt() )

			##### all partons with same jet
			elif ( len( listDuplicates ) == 1 ) and ( numUniqueJets == 1 ):
				numberPartonsSameJet.Fill( 4 )
				#if debug: print '1 duplicate + 0 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				#if debug: print '4', jLists[0], jLists[1]
				for jparton, jLists in dictDeltaR.iteritems():
					if ( listDuplicates[0] == jLists[1][0] ):
						minDeltaRPartonJet_FourlyMerged.Fill( jLists[0][0] )
						#if debug: print jLists[1][0], listDuplicates

		##### less than 4 jets
		else:
			#if debug: print 'less than 4 jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
			#if debug: print '6', jLists[0], jLists[1]
			numberPartonsSameJet.Fill( 6 )
			#if debug: print tmpListJetIndex, listDuplicates, numUniqueJets
		##################################################################################################################################


		########################################################################################## DeltaR < 0.4
		#### check if cut is applied:
		for i,listParton in dictDeltaR0p4.iteritems(): 
			if len( listParton[0] ) > 0: minDeltaRPartonJet_DeltaR0p4.Fill( listParton[0][0] )
			if len( listParton[0] ) > 1: secMinDeltaRPartonJet_DeltaR0p4.Fill( listParton[0][1] )

		#### check number of repetitions
		appearancesDeltaR0p4 = defaultdict(int)
		for curr in tmpListJetIndexDeltaR0p4: appearancesDeltaR0p4[curr] += 1
		listDuplicatesDeltaR0p4 = [ i for i, k in appearancesDeltaR0p4.iteritems() if k > 1 ]
		numUniqueJetsDeltaR0p4 = len( set( tmpListJetIndexDeltaR0p4 ) )
		#if debug: print tmpListJetIndexDeltaR0p4
		#if debug: print '13 ', listDuplicatesDeltaR0p4
		#if debug: print '14 ', numUniqueJetsDeltaR0p4

		#################### if 4 jets after delta cut
		if len( tmpListJetIndexDeltaR0p4 ) == 4:		
			for z in range( len( listP4Jets ) ): jetPt_DeltaR0p4.Fill( listP4Jets[z][0].Pt() )

			################### No Merged
			if ( len( listDuplicatesDeltaR0p4 ) == 0 ) and ( numUniqueJetsDeltaR0p4 == 4 ):
				#if debug: print '1', jLists[0], jLists[1]
				#if debug: print '4 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				#dummyCounter2 += 1
				numberPartonsSameJet_DeltaR0p4.Fill( 0 )
				for jparton, jLists in dictDeltaR0p4.iteritems():
					#if debug: print '15 ', jparton, jLists[0][0]
					#if debug: print jLists[1][0], listDuplicates
					if jparton == 0: minDeltaRPartonJet_NoMerged_DeltaR0p4_0.Fill( jLists[0][0] )
					if jparton == 1: minDeltaRPartonJet_NoMerged_DeltaR0p4_1.Fill( jLists[0][0] )
					if jparton == 2: minDeltaRPartonJet_NoMerged_DeltaR0p4_2.Fill( jLists[0][0] )
					if jparton == 3: minDeltaRPartonJet_NoMerged_DeltaR0p4_3.Fill( jLists[0][0] )
					minDeltaRPartonJet_NoMerged_DeltaR0p4.Fill( jLists[0][0] )

				tmpStopA = ( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][0] + listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][0] ).M()
				tmpStopB = ( listP4Jets[ tmpListJetIndexDeltaR0p4[2] ][0] + listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][0] ).M()
				invMass_NoMerged_DeltaR0p4.Fill( tmpStopA )
				invMass_NoMerged_DeltaR0p4.Fill( tmpStopB )
				for x in range( len( tmpListJetIndexDeltaR0p4 ) ): jetPt_NoMerged_DeltaR0p4.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[x] ][0].Pt() )
				#if debug: print tmpStopA, tmpStopB

			######################### Singly Merged
			elif ( len( listDuplicatesDeltaR0p4 ) == 1 ) and ( numUniqueJetsDeltaR0p4 == 3 ):
				#if debug: print '2', jLists[0], jLists[1]
				for jparton, jLists in dictDeltaR0p4.iteritems():
					#if debug: print jLists[1][0], listDuplicates
					if ( listDuplicatesDeltaR0p4[0] == jLists[1][0] ):
						minDeltaRPartonJet_SinglyMerged_Merged_DeltaR0p4.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_SinglyMerged_Merged_DeltaR0p4.Fill( jLists[0][1] )
						minvsSecMinDeltaRPartonJet_SinglyMerged_Merged_DeltaR0p4.Fill( jLists[0][0], jLists[0][1] )
					else:
						minDeltaRPartonJet_SinglyMerged_NOMerged_DeltaR0p4.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_SinglyMerged_NOMerged_DeltaR0p4.Fill( jLists[0][1] )
						minvsSecMinDeltaRPartonJet_SinglyMerged_NOMerged_DeltaR0p4.Fill( jLists[0][0], jLists[0][1] )

				if ( listDuplicatesDeltaR0p4[0] != tmpListJetIndexDeltaR0p4[0] ) and ( listDuplicatesDeltaR0p4[0] != tmpListJetIndexDeltaR0p4[1] ): 
					numberPartonsSameJet_DeltaR0p4.Fill( 1 )
					tmpStopA = ( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][0] + listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][0] ).M()
					tmpStopC = ( listP4Jets[ listDuplicatesDeltaR0p4[0] ][0] ).M()

					### MERGED
					invMass_SinglyMerged_DeltaR0p4_Merged.Fill( tmpStopC )
					jetPt_SinglyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][0].Pt() )

					jetArea_SinglyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][4] )
					jetTau1_SinglyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] )
					jetTau2_SinglyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] )
					jetTau3_SinglyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] )
					jetTau21_SinglyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] / listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] )
					jetTau32_SinglyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] / listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] )
					jetTau31_SinglyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] / listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] )
					jetTau21_SinglyMerged_DeltaR0p4_Merged_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] , listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] )
					jetTau31_SinglyMerged_DeltaR0p4_Merged_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] , listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] )
					jetTau32_SinglyMerged_DeltaR0p4_Merged_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] , listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] )
					jetMassVsPt_SinglyMerged_DeltaR0p4_Merged_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][0].M(), listP4Jets[ listDuplicatesDeltaR0p4[0] ][0].Pt() )

					#### NO MERGED
					invMass_SinglyMerged_DeltaR0p4_NOMerged.Fill( tmpStopA )
					#### NO MERGED 0
					jetPt_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][0].Pt() )
					jetArea_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][4] )
					jetMass_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][0].M() )
					jetTau1_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][1] )
					jetTau2_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][2] )
					jetTau3_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][3] )
					jetTau21_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][2] / listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][1] )
					jetTau32_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][3] / listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][2] )
					jetTau31_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][3] / listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][1] )
					jetTau21_SinglyMerged_DeltaR0p4_NOMerged_2D.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][1] , listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][2] )
					jetTau31_SinglyMerged_DeltaR0p4_NOMerged_2D.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][1] , listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][3] )
					jetTau32_SinglyMerged_DeltaR0p4_NOMerged_2D.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][2] , listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][3] )
					jetMassVsPt_SinglyMerged_DeltaR0p4_NOMerged_2D.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][0].M(), listP4Jets[ tmpListJetIndexDeltaR0p4[0] ][0].Pt() )
					##### NO MERGED 1
					jetPt_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][0].Pt() )
					jetArea_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][4] )
					jetMass_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][0].M() )
					jetTau1_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][1] )
					jetTau2_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][2] )
					jetTau3_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][3] )
					jetTau21_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][2] / listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][1] )
					jetTau32_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][3] / listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][2] )
					jetTau31_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][3] / listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][1] )
					jetTau21_SinglyMerged_DeltaR0p4_NOMerged_2D.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][1] , listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][2] )
					jetTau31_SinglyMerged_DeltaR0p4_NOMerged_2D.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][1] , listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][3] )
					jetTau32_SinglyMerged_DeltaR0p4_NOMerged_2D.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][2] , listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][3] )
					jetMassVsPt_SinglyMerged_DeltaR0p4_NOMerged_2D.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][0].M(), listP4Jets[ tmpListJetIndexDeltaR0p4[1] ][0].Pt() )

					#if debug: print '1 jet merged + 2 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
					#if debug: print 'jetMass ', tmpStopC
					#if debug: print 'stopA ', tmpStopA
				elif ( listDuplicatesDeltaR0p4[0] != tmpListJetIndexDeltaR0p4[2] ) and ( listDuplicatesDeltaR0p4[0] != tmpListJetIndexDeltaR0p4[3] ): 
					numberPartonsSameJet_DeltaR0p4.Fill( 1 )
					tmpStopB = ( listP4Jets[ tmpListJetIndexDeltaR0p4[2] ][0] + listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][0] ).M()
					tmpStopC = ( listP4Jets[ listDuplicatesDeltaR0p4[0] ][0] ).M()

					##### MERGED
					invMass_SinglyMerged_DeltaR0p4_Merged.Fill( tmpStopC )
					jetPt_SinglyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][0].Pt() )

					jetArea_SinglyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][4] )
					jetTau1_SinglyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] )
					jetTau2_SinglyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] )
					jetTau3_SinglyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] )
					jetTau21_SinglyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] / listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] )
					jetTau32_SinglyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] / listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] )
					jetTau31_SinglyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] / listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] )
					jetTau21_SinglyMerged_DeltaR0p4_Merged_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] , listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] )
					jetTau31_SinglyMerged_DeltaR0p4_Merged_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] , listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] )
					jetTau32_SinglyMerged_DeltaR0p4_Merged_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] , listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] )
					jetMassVsPt_SinglyMerged_DeltaR0p4_Merged_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][0].M(), listP4Jets[ listDuplicatesDeltaR0p4[0] ][0].Pt() )

					##### NO MERGED
					invMass_SinglyMerged_DeltaR0p4_NOMerged.Fill( tmpStopB )
					#### NO MERGED 2
					jetPt_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[2] ][0].Pt() )
					jetArea_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[2] ][4] )
					jetTau1_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[2] ][1] )
					jetTau2_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[2] ][2] )
					jetTau3_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[2] ][3] )
					jetTau21_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[2] ][2] / listP4Jets[ tmpListJetIndexDeltaR0p4[2] ][1] )
					jetTau32_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[2] ][3] / listP4Jets[ tmpListJetIndexDeltaR0p4[2] ][2] )
					jetTau31_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[2] ][3] / listP4Jets[ tmpListJetIndexDeltaR0p4[2] ][1] )
					jetMassVsPt_SinglyMerged_DeltaR0p4_NOMerged_2D.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[2] ][0].M(), listP4Jets[ tmpListJetIndexDeltaR0p4[2] ][0].Pt() )
					#### NO MERGED 3
					jetPt_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][0].Pt() )
					jetArea_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][4] )
					jetTau1_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][1] )
					jetTau2_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][2] )
					jetTau3_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][3] )
					jetTau21_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][2] / listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][1] )
					jetTau32_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][3] / listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][2] )
					jetTau31_SinglyMerged_DeltaR0p4_NOMerged.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][3] / listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][1] )
					jetTau21_SinglyMerged_DeltaR0p4_NOMerged_2D.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][1] , listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][2] )
					jetTau31_SinglyMerged_DeltaR0p4_NOMerged_2D.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][1] , listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][3] )
					jetTau32_SinglyMerged_DeltaR0p4_NOMerged_2D.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][2] , listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][3] )
					jetMassVsPt_SinglyMerged_DeltaR0p4_NOMerged_2D.Fill( listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][0].M(), listP4Jets[ tmpListJetIndexDeltaR0p4[3] ][0].Pt() )
					#if debug: print '1 jet merged + 2 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
					#if debug: print ' jetMass ', tmpStopC
					#if debug: print 'stopB ', tmpStopB

			######################################## Doubly Merged
			elif ( len( listDuplicatesDeltaR0p4 ) == 2 ) and ( numUniqueJetsDeltaR0p4 == 2 ):
				#if debug: print '5', jLists[0], jLists[1]
				for jparton, jLists in dictDeltaR0p4.iteritems():
					#if debug: print jLists[1][0], listDuplicates
					if ( listDuplicatesDeltaR0p4[0] == jLists[1][0] ):
						minDeltaRPartonJet_DoublyMerged_DeltaR0p4_A.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_DoublyMerged_DeltaR0p4_A.Fill( jLists[0][1] )
					if ( listDuplicatesDeltaR0p4[1] == jLists[1][0] ):
						minDeltaRPartonJet_DoublyMerged_DeltaR0p4_B.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_DoublyMerged_DeltaR0p4_B.Fill( jLists[0][1] )

				if ( listDuplicatesDeltaR0p4[0] == tmpListJetIndexDeltaR0p4[0] ) and ( listDuplicatesDeltaR0p4[0] == tmpListJetIndexDeltaR0p4[1] ): 
					numberPartonsSameJet_DeltaR0p4.Fill( 2 )
					####### STOP A
					tmpStopA = ( listP4Jets[ listDuplicatesDeltaR0p4[0] ][0] ).M()
					invMass_DoublyMerged_DeltaR0p4.Fill( tmpStopA )
					jetPt_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][0].Pt() )

					jetArea_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][4] )
					jetTau1_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] )
					jetTau2_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] )
					jetTau3_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] )
					jetTau21_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] / listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] )
					jetTau32_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] / listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] )
					jetTau31_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] / listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] )
					jetTau21_DoublyMerged_DeltaR0p4_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] , listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] )
					jetTau31_DoublyMerged_DeltaR0p4_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] , listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] )
					jetTau32_DoublyMerged_DeltaR0p4_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] , listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] )
					jetMassVsPt_DoublyMerged_DeltaR0p4_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][0].M(), listP4Jets[ listDuplicatesDeltaR0p4[0] ][0].Pt() )

					#### STOP B
					tmpStopB = ( listP4Jets[ listDuplicatesDeltaR0p4[1] ][0] ).M()
					invMass_DoublyMerged_DeltaR0p4.Fill( tmpStopB )
					jetPt_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][0].Pt() )
					jetArea_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][4] )
					jetTau1_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][1] )
					jetTau2_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][2] )
					jetTau3_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][3] )
					jetTau21_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][2] / listP4Jets[ listDuplicatesDeltaR0p4[1] ][1] )
					jetTau32_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][3] / listP4Jets[ listDuplicatesDeltaR0p4[1] ][2] )
					jetTau31_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][3] / listP4Jets[ listDuplicatesDeltaR0p4[1] ][1] )
					jetTau21_DoublyMerged_DeltaR0p4_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][1] , listP4Jets[ listDuplicatesDeltaR0p4[1] ][2] )
					jetTau31_DoublyMerged_DeltaR0p4_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][1] , listP4Jets[ listDuplicatesDeltaR0p4[1] ][3] )
					jetTau32_DoublyMerged_DeltaR0p4_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][2] , listP4Jets[ listDuplicatesDeltaR0p4[1] ][3] )
					jetMassVsPt_DoublyMerged_DeltaR0p4_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][0].M(), listP4Jets[ listDuplicatesDeltaR0p4[1] ][0].Pt() )
					#if couts: print tmpStopA, tmpStopB, tmpListJetIndexDeltaR0p4

				elif ( listDuplicatesDeltaR0p4[0] == tmpListJetIndexDeltaR0p4[2] ) and ( listDuplicatesDeltaR0p4[0] == tmpListJetIndexDeltaR0p4[3] ): 
					numberPartonsSameJet_DeltaR0p4.Fill( 2 )

					##### STOP B
					tmpStopB = ( listP4Jets[ listDuplicatesDeltaR0p4[0] ][0] ).M()
					invMass_DoublyMerged_DeltaR0p4.Fill( tmpStopB )
					jetPt_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][0].Pt() )
					jetArea_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][4] )
					jetTau1_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] )
					jetTau2_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] )
					jetTau3_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] )
					jetTau21_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] / listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] )
					jetTau32_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] / listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] )
					jetTau31_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] / listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] )
					jetTau21_DoublyMerged_DeltaR0p4_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] , listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] )
					jetTau31_DoublyMerged_DeltaR0p4_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][1] , listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] )
					jetTau32_DoublyMerged_DeltaR0p4_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][2] , listP4Jets[ listDuplicatesDeltaR0p4[0] ][3] )
					jetMassVsPt_DoublyMerged_DeltaR0p4_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][0].M(), listP4Jets[ listDuplicatesDeltaR0p4[0] ][0].Pt() )

					##### STOP A
					tmpStopA = ( listP4Jets[ listDuplicatesDeltaR0p4[1] ][0] ).M()
					invMass_DoublyMerged_DeltaR0p4.Fill( tmpStopA )
					jetPt_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][0].Pt() )
					jetArea_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][4] )
					jetTau1_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][1] )
					jetTau2_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][2] )
					jetTau3_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][3] )
					jetTau21_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][2] / listP4Jets[ listDuplicatesDeltaR0p4[1] ][1] )
					jetTau32_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][3] / listP4Jets[ listDuplicatesDeltaR0p4[1] ][2] )
					jetTau31_DoublyMerged_DeltaR0p4.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][3] / listP4Jets[ listDuplicatesDeltaR0p4[1] ][1] )
					jetTau21_DoublyMerged_DeltaR0p4_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][1] , listP4Jets[ listDuplicatesDeltaR0p4[1] ][2] )
					jetTau31_DoublyMerged_DeltaR0p4_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][1] , listP4Jets[ listDuplicatesDeltaR0p4[1] ][3] )
					jetTau32_DoublyMerged_DeltaR0p4_2D.Fill( listP4Jets[ listDuplicatesDeltaR0p4[1] ][2] , listP4Jets[ listDuplicatesDeltaR0p4[1] ][3] )
					#if couts: print tmpStopA, tmpStopB, tmpListJetIndexDeltaR0p4
				#if debug: print 'Pair 2 jet merged : ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				#if debug: print 'stopA ', tmpStopA
				#if debug: print 'stopB ', tmpStopB

			##### if one duplicate and 1 different
			elif ( len( listDuplicatesDeltaR0p4 ) == 1 ) and ( numUniqueJetsDeltaR0p4 == 2 ):
				numberPartonsSameJet_DeltaR0p4.Fill( 3 )
				#if debug: print '3', jLists[0], jLists[1]
				#if debug: print '3 jet merged + 1 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				for jparton, jLists in dictDeltaR0p4.iteritems():
					#if debug: print jLists[1][0], listDuplicates
					if ( listDuplicatesDeltaR0p4[0] == jLists[1][0] ):
						minDeltaRPartonJet_TriplyMerged_DeltaR0p4.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_TriplyMerged_DeltaR0p4.Fill( jLists[0][1] )
				tmpMass = ( listP4Jets[ listDuplicatesDeltaR0p4[0] ][0] ).M()
				invMass_TriplyMerged_DeltaR0p4_Merged.Fill( tmpMass )
				jetPt_TriplyMerged_DeltaR0p4_Merged.Fill( listP4Jets[ listDuplicatesDeltaR0p4[0] ][0].Pt() )


			##### all partons with same jet
			elif ( len( listDuplicatesDeltaR0p4 ) == 1 ) and ( numUniqueJetsDeltaR0p4 == 1 ):
				#if debug: print '4', jLists[0], jLists[1]
				#if debug: print '4 jet merged : ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				numberPartonsSameJet_DeltaR0p4.Fill( 4 )
				for jparton, jLists in dictDeltaR0p4.iteritems():
					#if debug: print jLists[1][0], listDuplicates
					if ( listDuplicatesDeltaR0p4[0] == jLists[1][0] ):
						minDeltaRPartonJet_FourlyMerged_DeltaR0p4.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_FourlyMerged_DeltaR0p4.Fill( jLists[0][1] )


			##### in case I forgot some category
			else:
				#if debug: print '6', jLists[0], jLists[1]
				numberPartonsSameJet_DeltaR0p4.Fill( 5 )

		###### events without delta cut
		else:
			#if debug: print '15', jLists[0], jLists[1]
			numberPartonsSameJet_DeltaR0p4.Fill( 6 )

	################################################################################################## end event loop

	#if debug: print 'd1 ', dummyCounter
	#if debug: print 'd2 ', dummyCounter2
	#if debug: print 'd3', len(dummyList)
	#if debug: print 'd4', len(dummyList1)
	#if debug: print 'd5', len(dummyList2)
	#if debug: print 'd6', len(dummyList3)
	#if debug: print 'd7', len(dummyList4)
	#if debug: print 'd8', len(dummyList5)
	#if debug: print 'd9', len(dummyList6)
	##### write output file 
	outputFile.cd()
	outputFile.Write()

	##### Closing
	print 'Writing output file: '+ outputDir + sample + '_Matching_'+jetAlgo+'_'+grooming+'_Plots_'+dateKey+'.root'
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
	parser.add_option( '-j', '--jetAlgo', action='store', type='string', dest='jetAlgo', default='AK5', help='Jet Algorithm' )
	parser.add_option( '-g', '--grooming', action='store', type='string', dest='grooming', default='', help='Jet Algorithm' )
	parser.add_option( '-d', '--debug', action='store_true', dest='couts', default=False, help='True print couts in screen, False print in a file' )
	parser.add_option( '-f', '--final', action='store_true', dest='final', default=False, help='If True, final version' )

	(options, args) = parser.parse_args()

	mass = options.mass
	couts = options.couts
	final = options.final
	jetAlgo = options.jetAlgo
	grooming = options.grooming

	sample = 'stopUDD312_'+str(mass)
	#list = os.popen('ls -1 /cms/gomez/Substructure/Generation/Simulation/CMSSW_5_3_2_patch4/src/mySimulations/stop_UDD312_50/aodsim/*.root').read().splitlines()
	list = os.popen('ls -1 /cms/gomez/Stops/st_jj/patTuples/'+sample+'/results/140402/*.root').read().splitlines()
	#list = [ '/cms/gomez/Stops/st_jj/patTuples/stopUDD312_50_tree_test_grom.root' ]
	inputList = [i if i.startswith('file') else 'file:' + i for i in list]

	outputDir = '/cms/gomez/Stops/st_jj/treeResults/'

	if not final : get_info( inputList[:2], outputDir, sample, mass, couts, final, jetAlgo, grooming )
	else: get_info( inputList, outputDir, sample, mass, couts, final, jetAlgo, grooming )

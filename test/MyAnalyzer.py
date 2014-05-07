#!/usr/bin/env python

'''
File: MyAnalyzer.py --mass 50 (optional) --debug -- final --jetAlgo AK5
Author: Alejandro Gomez Es5.nosa
Email: gomez@physics.rutgers.edu
Description: 
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
def myAnalyzer( infile, outputDir, sample, couts, final, jetAlgo, grooming, weight, Job ):

	####### for hexfarm
	#if not final: 
	#	outputFile = TFile( outputDir + sample + '_'+jetAlgo+'_'+grooming+'_Plots_'+dateKey+'.root', 'RECREATE' )
	#else:
	#	if not ( os.path.exists( outputDir + 'rootFiles/' + monthKey ) ): os.makedirs( outputDir + 'rootFiles/' + monthKey )
	#	outputFile = TFile( outputDir + 'rootFiles/' + monthKey + '/' + sample + '_'+jetAlgo+'_'+grooming+'_Plots.root', 'RECREATE' )

	####### for LPC
	if final:
		if not ( os.path.exists( outputDir + sample + '_rootFiles/' ) ): os.makedirs( outputDir + sample +'_rootFiles/' )
		if 'QCD' in sample:
			outputFileName = outputDir + sample + '_rootFiles/' + sample + '_'+jetAlgo+'_'+grooming+'_'+str(Job)+'_Plots.root'
		elif 'Data' in sample:
			outputFileName = outputDir + sample + '_rootFiles/' + sample + '_'+jetAlgo+'_'+grooming+'_'+str(Job)+'_Plots.root'
		else:
			outputFileName = outputDir + sample + '/rootFiles/' + sample + '_'+jetAlgo+'_'+grooming+'_Plots.root'
	else:
		outputFileName = sample + '_'+jetAlgo+'_'+grooming+'_Plots_TEST.root'


	outputFile = TFile( outputFileName , 'RECREATE' )

	######## Extra, send print to file
	#if couts == False :
	#	outfileStdOut = sys.stdout
	#	f = file('tmp_'+sample+'_'+jetAlgo+'_'+dateKey+'.txt', 'w')
	#	sys.stdout = f
	#################################################

	####################################################################################################################################### Histograms
	nBinsDeltaR = 50
	maxDeltaR = 5. 
	maxMass = 500
	maxPt = 1000
	nBinsMass = 100  #int(round( maxMass/5 ))
	nBinsPt = 200  #int(round( maxPt/5 ))
	nBinsEta = 41
	maxEta = 4.1
	nBinsTau = 40
	maxTau = 1.
	nBinsHT = 150
	maxHT = 1500.

	#####################################################
	#### Only kinematic cuts - (pt > 30, |eta| < 2.5 )
	################################################################################################### Event Variables
	ht 		= TH1F('h_ht_'+jetAlgo+'_'+grooming, 	'h_ht_'+jetAlgo, 	nBinsHT,  	0, 	maxHT)
	numberPV 	= TH1F('h_numberPV_'+jetAlgo+'_'+grooming, 	'h_numberPV_'+jetAlgo, 	50,  	0., 	50.)
	MET 		= TH1F('h_MET_'+jetAlgo+'_'+grooming, 	'h_MET_'+jetAlgo, 	24,  	0, 	120.)
	numberJets 	= TH1F('h_numberJets_'+jetAlgo+'_'+grooming, 'h_numberJets_'+jetAlgo, 15,  0., 15.)
	jetPt	 	= TH1F('h_jetPt_'+jetAlgo+'_'+grooming, 'h_jetPt_'+jetAlgo, nBinsPt,  0., maxPt)
	jetEta	 	= TH1F('h_jetEta_'+jetAlgo+'_'+grooming, 'h_jetEta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jetPhi	 	= TH1F('h_jetPhi_'+jetAlgo+'_'+grooming, 'h_jetPhi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jetMass	 	= TH1F('h_jetMass_'+jetAlgo+'_'+grooming, 'h_jetMass_'+jetAlgo, nBinsMass,  0., maxMass)
	jetPtvsMass	= TH2F('h_jetPtvsMass_'+jetAlgo+'_'+grooming, 'h_jetPtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	jetArea 	= TH1F('h_jetArea_'+jetAlgo+'_'+grooming, 'h_jetArea_'+jetAlgo, 50,  0., 5.)
	jetTau1 	= TH1F('h_jetTau1_'+jetAlgo+'_'+grooming, 'h_jetTau1_'+jetAlgo, nBinsTau,  0., maxTau)
	jetTau2 	= TH1F('h_jetTau2_'+jetAlgo+'_'+grooming, 'h_jetTau2_'+jetAlgo, nBinsTau,  0., maxTau)
	jetTau3 	= TH1F('h_jetTau3_'+jetAlgo+'_'+grooming, 'h_jetTau3_'+jetAlgo, nBinsTau,  0., maxTau)
	jetTau21 	= TH1F('h_jetTau21_'+jetAlgo+'_'+grooming, 'h_jetTau21_'+jetAlgo, nBinsTau,  0., maxTau)
	jetTau31 	= TH1F('h_jetTau31_'+jetAlgo+'_'+grooming, 'h_jetTau31_'+jetAlgo, nBinsTau,  0., maxTau)
	jetTau32 	= TH1F('h_jetTau32_'+jetAlgo+'_'+grooming, 'h_jetTau32_'+jetAlgo, nBinsTau,  0., maxTau)
	jetTau2vsTau1 	= TH2F('h_jetTau2vsTau1_'+jetAlgo+'_'+grooming, 'h_jetTau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jetTau3vsTau1 	= TH2F('h_jetTau3vsTau1_'+jetAlgo+'_'+grooming, 'h_jetTau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jetTau3vsTau2 	= TH2F('h_jetTau3vsTau2_'+jetAlgo+'_'+grooming, 'h_jetTau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)

	############################################################ Leading Jet 
	jet1Pt	 	= TH1F('h_jet1Pt_'+jetAlgo+'_'+grooming, 'h_jet1Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	jet1Mass 	= TH1F('h_jet1Mass_'+jetAlgo+'_'+grooming, 'h_jet1Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	jet1Eta	 	= TH1F('h_jet1Eta_'+jetAlgo+'_'+grooming, 'h_jet1Eta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jet1Phi	 	= TH1F('h_jet1Phi_'+jetAlgo+'_'+grooming, 'h_jet1Phi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jet1PtvsMass	= TH2F('h_jet1PtvsMass_'+jetAlgo+'_'+grooming, 'h_jet1PtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	jet1Area 	= TH1F('h_jet1Area_'+jetAlgo+'_'+grooming, 'h_jet1Area_'+jetAlgo, 50,  0., 5.)
	jet1Tau1 	= TH1F('h_jet1Tau1_'+jetAlgo+'_'+grooming, 'h_jet1Tau1_'+jetAlgo, nBinsTau,  0., maxTau)
	jet1Tau2 	= TH1F('h_jet1Tau2_'+jetAlgo+'_'+grooming, 'h_jet1Tau2_'+jetAlgo, nBinsTau,  0., maxTau)
	jet1Tau3 	= TH1F('h_jet1Tau3_'+jetAlgo+'_'+grooming, 'h_jet1Tau3_'+jetAlgo, nBinsTau,  0., maxTau)
	jet1Tau21 	= TH1F('h_jet1Tau21_'+jetAlgo+'_'+grooming, 'h_jet1Tau21_'+jetAlgo, nBinsTau,  0., maxTau)
	jet1Tau31 	= TH1F('h_jet1Tau31_'+jetAlgo+'_'+grooming, 'h_jet1Tau31_'+jetAlgo, nBinsTau,  0., maxTau)
	jet1Tau32 	= TH1F('h_jet1Tau32_'+jetAlgo+'_'+grooming, 'h_jet1Tau32_'+jetAlgo, nBinsTau,  0., maxTau)
	jet1Tau2vsTau1 	= TH2F('h_jet1Tau2vsTau1_'+jetAlgo+'_'+grooming, 'h_jet1Tau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet1Tau3vsTau1 	= TH2F('h_jet1Tau3vsTau1_'+jetAlgo+'_'+grooming, 'h_jet1Tau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet1Tau3vsTau2 	= TH2F('h_jet1Tau3vsTau2_'+jetAlgo+'_'+grooming, 'h_jet1Tau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet1Ptvsht 	= TH2F('h_jet1Ptvsht_'+jetAlgo+'_'+grooming, 'h_jet1Ptvsht_'+jetAlgo, nBinsPt,  0., maxPt, nBinsHT,  	0, 	maxHT)
	jet1Massvsht 	= TH2F('h_jet1Massvsht_'+jetAlgo+'_'+grooming, 'h_jet1Massvsht_'+jetAlgo, nBinsMass,  0., maxMass, nBinsHT,  	0, 	maxHT)
	jet1MassvsTau21 	= TH2F('h_jet1MassvsTau21_'+jetAlgo+'_'+grooming, 'h_jet1MassvsTau21_'+jetAlgo, nBinsMass,  0., maxMass, nBinsTau,  0., maxTau)

	############################################################ 2nd Leading Jet 
	jet2Pt	 	= TH1F('h_jet2Pt_'+jetAlgo+'_'+grooming, 'h_jet2Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	jet2Mass 	= TH1F('h_jet2Mass_'+jetAlgo+'_'+grooming, 'h_jet2Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	jet2Eta	 	= TH1F('h_jet2Eta_'+jetAlgo+'_'+grooming, 'h_jet2Eta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jet2Phi	 	= TH1F('h_jet2Phi_'+jetAlgo+'_'+grooming, 'h_jet2Phi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jet2PtvsMass	= TH2F('h_jet2PtvsMass_'+jetAlgo+'_'+grooming, 'h_jet2PtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	jet2Area 	= TH1F('h_jet2Area_'+jetAlgo+'_'+grooming, 'h_jet2Area_'+jetAlgo, 50,  0., 5.)
	jet2Tau1 	= TH1F('h_jet2Tau1_'+jetAlgo+'_'+grooming, 'h_jet2Tau1_'+jetAlgo, nBinsTau,  0., maxTau)
	jet2Tau2 	= TH1F('h_jet2Tau2_'+jetAlgo+'_'+grooming, 'h_jet2Tau2_'+jetAlgo, nBinsTau,  0., maxTau)
	jet2Tau3 	= TH1F('h_jet2Tau3_'+jetAlgo+'_'+grooming, 'h_jet2Tau3_'+jetAlgo, nBinsTau,  0., maxTau)
	jet2Tau21 	= TH1F('h_jet2Tau21_'+jetAlgo+'_'+grooming, 'h_jet2Tau21_'+jetAlgo, nBinsTau,  0., maxTau)
	jet2Tau31 	= TH1F('h_jet2Tau31_'+jetAlgo+'_'+grooming, 'h_jet2Tau31_'+jetAlgo, nBinsTau,  0., maxTau)
	jet2Tau32 	= TH1F('h_jet2Tau32_'+jetAlgo+'_'+grooming, 'h_jet2Tau32_'+jetAlgo, nBinsTau,  0., maxTau)
	jet2Tau2vsTau1 	= TH2F('h_jet2Tau2vsTau1_'+jetAlgo+'_'+grooming, 'h_jet2Tau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet2Tau3vsTau1 	= TH2F('h_jet2Tau3vsTau1_'+jetAlgo+'_'+grooming, 'h_jet2Tau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet2Tau3vsTau2 	= TH2F('h_jet2Tau3vsTau2_'+jetAlgo+'_'+grooming, 'h_jet2Tau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet2Ptvsht 	= TH2F('h_jet2Ptvsht_'+jetAlgo+'_'+grooming, 'h_jet2Ptvsht_'+jetAlgo, nBinsPt,  0., maxPt, nBinsHT,  	0, 	maxHT)
	jet2Massvsht 	= TH2F('h_jet2Massvsht_'+jetAlgo+'_'+grooming, 'h_jet2Massvsht_'+jetAlgo, nBinsMass,  0., maxMass, nBinsHT,  	0, 	maxHT)
	jet2MassvsTau21 	= TH2F('h_jet2MassvsTau21_'+jetAlgo+'_'+grooming, 'h_jet2MassvsTau21_'+jetAlgo, nBinsMass,  0., maxMass, nBinsTau,  0., maxTau)

	########################################################### Leading and 2nd Leading Jet
	jet1vsjet2Mass 	= TH2F('h_jet1vsjet2Mass_'+jetAlgo+'_'+grooming, 'h_jet1vsjet2Mass_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMass,  0., maxMass)
	jet1vsjet2Tau21 	= TH2F('h_jet1vsjet2Tau21_'+jetAlgo+'_'+grooming, 'h_jet1vsjet2Tau21_'+jetAlgo,   nBinsTau,  0., maxTau,   nBinsTau,  0., maxTau)

	############################################################ 3rd Leading Jet 
	jet3Pt	 	= TH1F('h_jet3Pt_'+jetAlgo+'_'+grooming, 'h_jet3Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	jet3Mass 	= TH1F('h_jet3Mass_'+jetAlgo+'_'+grooming, 'h_jet3Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	jet3Eta	 	= TH1F('h_jet3Eta_'+jetAlgo+'_'+grooming, 'h_jet3Eta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jet3Phi	 	= TH1F('h_jet3Phi_'+jetAlgo+'_'+grooming, 'h_jet3Phi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jet3PtvsMass	= TH2F('h_jet3PtvsMass_'+jetAlgo+'_'+grooming, 'h_jet3PtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	jet3Area 	= TH1F('h_jet3Area_'+jetAlgo+'_'+grooming, 'h_jet3Area_'+jetAlgo, 50,  0., 5.)
	jet3Tau1 	= TH1F('h_jet3Tau1_'+jetAlgo+'_'+grooming, 'h_jet3Tau1_'+jetAlgo, nBinsTau,  0., maxTau)
	jet3Tau2 	= TH1F('h_jet3Tau2_'+jetAlgo+'_'+grooming, 'h_jet3Tau2_'+jetAlgo, nBinsTau,  0., maxTau)
	jet3Tau3 	= TH1F('h_jet3Tau3_'+jetAlgo+'_'+grooming, 'h_jet3Tau3_'+jetAlgo, nBinsTau,  0., maxTau)
	jet3Tau21 	= TH1F('h_jet3Tau21_'+jetAlgo+'_'+grooming, 'h_jet3Tau21_'+jetAlgo, nBinsTau,  0., maxTau)
	jet3Tau31 	= TH1F('h_jet3Tau31_'+jetAlgo+'_'+grooming, 'h_jet3Tau31_'+jetAlgo, nBinsTau,  0., maxTau)
	jet3Tau32 	= TH1F('h_jet3Tau32_'+jetAlgo+'_'+grooming, 'h_jet3Tau32_'+jetAlgo, nBinsTau,  0., maxTau)
	jet3Tau2vsTau1 	= TH2F('h_jet3Tau2vsTau1_'+jetAlgo+'_'+grooming, 'h_jet3Tau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet3Tau3vsTau1 	= TH2F('h_jet3Tau3vsTau1_'+jetAlgo+'_'+grooming, 'h_jet3Tau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet3Tau3vsTau2 	= TH2F('h_jet3Tau3vsTau2_'+jetAlgo+'_'+grooming, 'h_jet3Tau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet3Ptvsht 	= TH2F('h_jet3Ptvsht_'+jetAlgo+'_'+grooming, 'h_jet3Ptvsht_'+jetAlgo, nBinsPt,  0., maxPt, nBinsHT,  	0, 	maxHT)
	jet3Massvsht 	= TH2F('h_jet3Massvsht_'+jetAlgo+'_'+grooming, 'h_jet3Massvsht_'+jetAlgo, nBinsMass,  0., maxMass, nBinsHT,  	0, 	maxHT)

	############################################################ 4th Leading Jet 
	jet4Pt	 	= TH1F('h_jet4Pt_'+jetAlgo+'_'+grooming, 'h_jet4Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	jet4Mass 	= TH1F('h_jet4Mass_'+jetAlgo+'_'+grooming, 'h_jet4Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	jet4Eta	 	= TH1F('h_jet4Eta_'+jetAlgo+'_'+grooming, 'h_jet4Eta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jet4Phi	 	= TH1F('h_jet4Phi_'+jetAlgo+'_'+grooming, 'h_jet4Phi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jet4PtvsMass	= TH2F('h_jet4PtvsMass_'+jetAlgo+'_'+grooming, 'h_jet4PtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	jet4Area 	= TH1F('h_jet4Area_'+jetAlgo+'_'+grooming, 'h_jet4Area_'+jetAlgo, 50,  0., 5.)
	jet4Tau1 	= TH1F('h_jet4Tau1_'+jetAlgo+'_'+grooming, 'h_jet4Tau1_'+jetAlgo, nBinsTau,  0., maxTau)
	jet4Tau2 	= TH1F('h_jet4Tau2_'+jetAlgo+'_'+grooming, 'h_jet4Tau2_'+jetAlgo, nBinsTau,  0., maxTau)
	jet4Tau3 	= TH1F('h_jet4Tau3_'+jetAlgo+'_'+grooming, 'h_jet4Tau3_'+jetAlgo, nBinsTau,  0., maxTau)
	jet4Tau21 	= TH1F('h_jet4Tau21_'+jetAlgo+'_'+grooming, 'h_jet4Tau21_'+jetAlgo, nBinsTau,  0., maxTau)
	jet4Tau31 	= TH1F('h_jet4Tau31_'+jetAlgo+'_'+grooming, 'h_jet4Tau31_'+jetAlgo, nBinsTau,  0., maxTau)
	jet4Tau32 	= TH1F('h_jet4Tau32_'+jetAlgo+'_'+grooming, 'h_jet4Tau32_'+jetAlgo, nBinsTau,  0., maxTau)
	jet4Tau2vsTau1 	= TH2F('h_jet4Tau2vsTau1_'+jetAlgo+'_'+grooming, 'h_jet4Tau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet4Tau3vsTau1 	= TH2F('h_jet4Tau3vsTau1_'+jetAlgo+'_'+grooming, 'h_jet4Tau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet4Tau3vsTau2 	= TH2F('h_jet4Tau3vsTau2_'+jetAlgo+'_'+grooming, 'h_jet4Tau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet4Ptvsht 	= TH2F('h_jet4Ptvsht_'+jetAlgo+'_'+grooming, 'h_jet4Ptvsht_'+jetAlgo, nBinsPt,  0., maxPt, nBinsHT,  	0, 	maxHT)
	jet4Massvsht 	= TH2F('h_jet4Massvsht_'+jetAlgo+'_'+grooming, 'h_jet4Massvsht_'+jetAlgo, nBinsMass,  0., maxMass, nBinsHT,  	0, 	maxHT)


	#####################################################
	#### kinematic cuts plus other
	################################################################################################### Event Variables
	cut_ht 		= TH1F('h_cut_ht_'+jetAlgo+'_'+grooming, 	'h_cut_ht_'+jetAlgo, 	nBinsHT,  	0, 	maxHT)
	cut_numberJets 	= TH1F('h_cut_numberJets_'+jetAlgo+'_'+grooming, 'h_cut_numberJets_'+jetAlgo, 15,  0., 15.)
#	cut_numberPV 	= TH1F('h_cut_numberPV_'+jetAlgo+'_'+grooming, 	'h_cut_numberPV_'+jetAlgo, 	50,  	0., 	50.)
#	cut_MET 		= TH1F('h_cut_MET_'+jetAlgo+'_'+grooming, 	'h_cut_MET_'+jetAlgo, 	24,  	0, 	120.)
#	cut_jetPt	 	= TH1F('h_cut_jetPt_'+jetAlgo+'_'+grooming, 'h_cut_jetPt_'+jetAlgo, nBinsPt,  0., maxPt)
#	cut_jetEta	 	= TH1F('h_cut_jetEta_'+jetAlgo+'_'+grooming, 'h_cut_jetEta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
#	cut_jetPhi	 	= TH1F('h_cut_jetPhi_'+jetAlgo+'_'+grooming, 'h_cut_jetPhi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
#	cut_jetMass	 	= TH1F('h_cut_jetMass_'+jetAlgo+'_'+grooming, 'h_cut_jetMass_'+jetAlgo, nBinsMass,  0., maxMass)
#	cut_jetPtvsMass	= TH2F('h_cut_jetPtvsMass_'+jetAlgo+'_'+grooming, 'h_cut_jetPtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
#	cut_jetArea 	= TH1F('h_cut_jetArea_'+jetAlgo+'_'+grooming, 'h_cut_jetArea_'+jetAlgo, 50,  0., 5.)
#	cut_jetTau1 	= TH1F('h_cut_jetTau1_'+jetAlgo+'_'+grooming, 'h_cut_jetTau1_'+jetAlgo, nBinsTau,  0., maxTau)
#	cut_jetTau2 	= TH1F('h_cut_jetTau2_'+jetAlgo+'_'+grooming, 'h_cut_jetTau2_'+jetAlgo, nBinsTau,  0., maxTau)
#	cut_jetTau3 	= TH1F('h_cut_jetTau3_'+jetAlgo+'_'+grooming, 'h_cut_jetTau3_'+jetAlgo, nBinsTau,  0., maxTau)
#	cut_jetTau21 	= TH1F('h_cut_jetTau21_'+jetAlgo+'_'+grooming, 'h_cut_jetTau21_'+jetAlgo, nBinsTau,  0., maxTau)
#	cut_jetTau31 	= TH1F('h_cut_jetTau31_'+jetAlgo+'_'+grooming, 'h_cut_jetTau31_'+jetAlgo, nBinsTau,  0., maxTau)
#	cut_jetTau32 	= TH1F('h_cut_jetTau32_'+jetAlgo+'_'+grooming, 'h_cut_jetTau32_'+jetAlgo, nBinsTau,  0., maxTau)
#	cut_jetTau2vsTau1 	= TH2F('h_cut_jetTau2vsTau1_'+jetAlgo+'_'+grooming, 'h_cut_jetTau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
#	cut_jetTau3vsTau1 	= TH2F('h_cut_jetTau3vsTau1_'+jetAlgo+'_'+grooming, 'h_cut_jetTau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
#	cut_jetTau3vsTau2 	= TH2F('h_cut_jetTau3vsTau2_'+jetAlgo+'_'+grooming, 'h_cut_jetTau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)

	############################################################ Leading Jet 
	cut_jet1Pt	 	= TH1F('h_cut_jet1Pt_'+jetAlgo+'_'+grooming, 'h_cut_jet1Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	cut_jet1Mass 	= TH1F('h_cut_jet1Mass_'+jetAlgo+'_'+grooming, 'h_cut_jet1Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	cut_jet1Eta	 	= TH1F('h_cut_jet1Eta_'+jetAlgo+'_'+grooming, 'h_cut_jet1Eta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	cut_jet1Phi	 	= TH1F('h_cut_jet1Phi_'+jetAlgo+'_'+grooming, 'h_cut_jet1Phi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	cut_jet1PtvsMass	= TH2F('h_cut_jet1PtvsMass_'+jetAlgo+'_'+grooming, 'h_cut_jet1PtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	cut_jet1Area 	= TH1F('h_cut_jet1Area_'+jetAlgo+'_'+grooming, 'h_cut_jet1Area_'+jetAlgo, 50,  0., 5.)
	cut_jet1Tau1 	= TH1F('h_cut_jet1Tau1_'+jetAlgo+'_'+grooming, 'h_cut_jet1Tau1_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet1Tau2 	= TH1F('h_cut_jet1Tau2_'+jetAlgo+'_'+grooming, 'h_cut_jet1Tau2_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet1Tau3 	= TH1F('h_cut_jet1Tau3_'+jetAlgo+'_'+grooming, 'h_cut_jet1Tau3_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet1Tau21 	= TH1F('h_cut_jet1Tau21_'+jetAlgo+'_'+grooming, 'h_cut_jet1Tau21_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet1Tau31 	= TH1F('h_cut_jet1Tau31_'+jetAlgo+'_'+grooming, 'h_cut_jet1Tau31_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet1Tau32 	= TH1F('h_cut_jet1Tau32_'+jetAlgo+'_'+grooming, 'h_cut_jet1Tau32_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet1Tau2vsTau1 	= TH2F('h_cut_jet1Tau2vsTau1_'+jetAlgo+'_'+grooming, 'h_cut_jet1Tau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cut_jet1Tau3vsTau1 	= TH2F('h_cut_jet1Tau3vsTau1_'+jetAlgo+'_'+grooming, 'h_cut_jet1Tau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cut_jet1Tau3vsTau2 	= TH2F('h_cut_jet1Tau3vsTau2_'+jetAlgo+'_'+grooming, 'h_cut_jet1Tau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cut_jet1Ptvsht 	= TH2F('h_cut_jet1Ptvsht_'+jetAlgo+'_'+grooming, 'h_cut_jet1Ptvsht_'+jetAlgo, nBinsPt,  0., maxPt, nBinsHT,  	0, 	maxHT)
	cut_jet1Massvsht 	= TH2F('h_cut_jet1Massvsht_'+jetAlgo+'_'+grooming, 'h_cut_jet1Massvsht_'+jetAlgo, nBinsMass,  0., maxMass, nBinsHT,  	0, 	maxHT)
	cut_jet1MassvsTau21 	= TH2F('h_cut_jet1MassvsTau21_'+jetAlgo+'_'+grooming, 'h_cut_jet1MassvsTau21_'+jetAlgo, nBinsMass,  0., maxMass, nBinsTau,  0., maxTau)

	############################################################ 2nd Leading Jet 
	cut_jet2Pt	 	= TH1F('h_cut_jet2Pt_'+jetAlgo+'_'+grooming, 'h_cut_jet2Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	cut_jet2Mass 	= TH1F('h_cut_jet2Mass_'+jetAlgo+'_'+grooming, 'h_cut_jet2Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	cut_jet2Eta	 	= TH1F('h_cut_jet2Eta_'+jetAlgo+'_'+grooming, 'h_cut_jet2Eta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	cut_jet2Phi	 	= TH1F('h_cut_jet2Phi_'+jetAlgo+'_'+grooming, 'h_cut_jet2Phi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	cut_jet2PtvsMass	= TH2F('h_cut_jet2PtvsMass_'+jetAlgo+'_'+grooming, 'h_cut_jet2PtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	cut_jet2Area 	= TH1F('h_cut_jet2Area_'+jetAlgo+'_'+grooming, 'h_cut_jet2Area_'+jetAlgo, 50,  0., 5.)
	cut_jet2Tau1 	= TH1F('h_cut_jet2Tau1_'+jetAlgo+'_'+grooming, 'h_cut_jet2Tau1_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet2Tau2 	= TH1F('h_cut_jet2Tau2_'+jetAlgo+'_'+grooming, 'h_cut_jet2Tau2_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet2Tau3 	= TH1F('h_cut_jet2Tau3_'+jetAlgo+'_'+grooming, 'h_cut_jet2Tau3_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet2Tau21 	= TH1F('h_cut_jet2Tau21_'+jetAlgo+'_'+grooming, 'h_cut_jet2Tau21_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet2Tau31 	= TH1F('h_cut_jet2Tau31_'+jetAlgo+'_'+grooming, 'h_cut_jet2Tau31_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet2Tau32 	= TH1F('h_cut_jet2Tau32_'+jetAlgo+'_'+grooming, 'h_cut_jet2Tau32_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet2Tau2vsTau1 	= TH2F('h_cut_jet2Tau2vsTau1_'+jetAlgo+'_'+grooming, 'h_cut_jet2Tau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cut_jet2Tau3vsTau1 	= TH2F('h_cut_jet2Tau3vsTau1_'+jetAlgo+'_'+grooming, 'h_cut_jet2Tau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cut_jet2Tau3vsTau2 	= TH2F('h_cut_jet2Tau3vsTau2_'+jetAlgo+'_'+grooming, 'h_cut_jet2Tau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cut_jet2Ptvsht 	= TH2F('h_cut_jet2Ptvsht_'+jetAlgo+'_'+grooming, 'h_cut_jet2Ptvsht_'+jetAlgo, nBinsPt,  0., maxPt, nBinsHT,  	0, 	maxHT)
	cut_jet2Massvsht 	= TH2F('h_cut_jet2Massvsht_'+jetAlgo+'_'+grooming, 'h_cut_jet2Massvsht_'+jetAlgo, nBinsMass,  0., maxMass, nBinsHT,  	0, 	maxHT)
	cut_jet2MassvsTau21 	= TH2F('h_cut_jet2MassvsTau21_'+jetAlgo+'_'+grooming, 'h_cut_jet2MassvsTau21_'+jetAlgo, nBinsMass,  0., maxMass,  nBinsTau,  0., maxTau)

	########################################################### Leading and 2nd Leading Jet
	cut_jet1vsjet2Mass 	= TH2F('h_cut_jet1vsjet2Mass_'+jetAlgo+'_'+grooming, 'h_cut_jet1vsjet2Mass_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMass,  0., maxMass)
	cut_jet1vsjet2Tau21 	= TH2F('h_cut_jet1vsjet2Tau21_'+jetAlgo+'_'+grooming, 'h_cut_jet1vsjet2Tau21_'+jetAlgo,   nBinsTau,  0., maxTau,   nBinsTau,  0., maxTau)


	############################################################ 3rd Leading Jet 
	cut_jet3Pt	 	= TH1F('h_cut_jet3Pt_'+jetAlgo+'_'+grooming, 'h_cut_jet3Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	cut_jet3Mass 	= TH1F('h_cut_jet3Mass_'+jetAlgo+'_'+grooming, 'h_cut_jet3Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	cut_jet3Eta	 	= TH1F('h_cut_jet3Eta_'+jetAlgo+'_'+grooming, 'h_cut_jet3Eta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	cut_jet3Phi	 	= TH1F('h_cut_jet3Phi_'+jetAlgo+'_'+grooming, 'h_cut_jet3Phi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	cut_jet3PtvsMass	= TH2F('h_cut_jet3PtvsMass_'+jetAlgo+'_'+grooming, 'h_cut_jet3PtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	cut_jet3Area 	= TH1F('h_cut_jet3Area_'+jetAlgo+'_'+grooming, 'h_cut_jet3Area_'+jetAlgo, 50,  0., 5.)
	cut_jet3Tau1 	= TH1F('h_cut_jet3Tau1_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau1_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet3Tau2 	= TH1F('h_cut_jet3Tau2_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau2_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet3Tau3 	= TH1F('h_cut_jet3Tau3_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau3_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet3Tau21 	= TH1F('h_cut_jet3Tau21_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau21_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet3Tau31 	= TH1F('h_cut_jet3Tau31_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau31_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet3Tau32 	= TH1F('h_cut_jet3Tau32_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau32_'+jetAlgo, nBinsTau,  0., maxTau)
	cut_jet3Tau2vsTau1 	= TH2F('h_cut_jet3Tau2vsTau1_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cut_jet3Tau3vsTau1 	= TH2F('h_cut_jet3Tau3vsTau1_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cut_jet3Tau3vsTau2 	= TH2F('h_cut_jet3Tau3vsTau2_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	#####################################################################################################################################

	###################################### Get Trigger Histos
	#TriggerNames = TH1F( 'h_TriggerNames', 'h_TriggerNames', 16, 0, 16 )
	#TriggerPass = TH1F( 'h_TriggerPass', 'h_TriggerPass', 16, 0, 16 )

	###################################### Get GenTree 
	events = TChain( 'PFJet_'+jetAlgo+grooming+'/events' )

	# Loop over the filenames and add to tree.
	for filename in infile:
		print("Adding file: " + filename)
		events.Add(filename)
		#f1 = TFile(filename)
		#tmpTN = f1.Get( 'PFJet_'+jetAlgo+grooming+'/TriggerNames') 
		#tmpTP = f1.Get( 'PFJet_'+jetAlgo+grooming+'/TriggerPass') 
		#tmpTriggerNames.Add( tmpTN )
		#tmpTriggerPass.Add( tmpTP )

	##### read the tree & fill histosgrams -
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

		###################################################################### Trigger Info
		###### Just for reference order of triggers in 
		###### QCD and Signal: 'HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750'
		###### Data: 'HT250','HT300','HT350','HT400','HT450','HT500','HT550','HT650','HT750','PFHT350','PFHT650','PFHT700','PFHT750', 'PFNoPUHT350', 'PFNoPUHT650', 'PFNoPUHT700', 'PFNoPUHT750'
		###### events.triggerResult is False/True
		#for i in range( len( events.triggerResult ) ):
		#	print 'trigger ', i, events.triggerResult[i]

		###################################################################### Cuts
		HT = 0			### sanity clear
		for ijet in range( events.nJets ):
			cut_simpleKinematic =  events.jetPt[ijet] > 30 and abs( events.jetEta[ijet] ) < 2.5 
			HT += events.jetPt[ijet]
		cut_minTwoJets = events.nJets > 1
		cut_jet1pt = events.jetPt[0] > 200
		cut_HT = HT > 850


		###################################################################### Filling Histograms
		if cut_simpleKinematic and cut_minTwoJets:

			############  Event Variables
			for k in range( events.nJets ):
				jetPt.Fill( events.jetPt[k], weight )
				jetEta.Fill( events.jetEta[k], weight )
				jetPhi.Fill( events.jetPhi[k], weight )
				jetMass.Fill( events.jetMass[k], weight )
				jetPtvsMass.Fill( events.jetPt[k], events.jetMass[k], weight )
				jetArea.Fill( events.jetArea[k], weight )
				jetTau1.Fill( events.jetTau1[k], weight ) 
				jetTau2.Fill( events.jetTau2[k], weight ) 
				jetTau3.Fill( events.jetTau3[k], weight ) 
				jetTau21.Fill( events.jetTau2[k] / events.jetTau1[k] ) 
				jetTau31.Fill( events.jetTau3[k] / events.jetTau1[k] ) 
				jetTau32.Fill( events.jetTau3[k] / events.jetTau2[k] ) 
				jetTau2vsTau1.Fill( events.jetTau1[k], events.jetTau2[k] )  
				jetTau3vsTau1.Fill( events.jetTau1[k], events.jetTau3[k] )
				jetTau3vsTau2.Fill( events.jetTau2[k], events.jetTau3[k] ) 

			numberJets.Fill( events.nJets, weight )
			ht.Fill( HT, weight )
			numberPV.Fill( events.nvtx, weight )
			MET.Fill( events.met, weight )

			############ Leading Jet
			jet1Pt.Fill( events.jetPt[0], weight )
			jet1Eta.Fill( events.jetEta[0], weight )
			jet1Phi.Fill( events.jetPhi[0], weight )
			jet1Mass.Fill( events.jetMass[0], weight )
			jet1PtvsMass.Fill( events.jetPt[0], events.jetMass[0] )
			jet1Area.Fill( events.jetArea[0], weight )
			jet1Tau1.Fill( events.jetTau1[0], weight )
			jet1Tau2.Fill( events.jetTau2[0], weight )
			jet1Tau3.Fill( events.jetTau3[0], weight )
			jet1Tau21.Fill( events.jetTau2[0] / events.jetTau1[0] )
			jet1Tau31.Fill( events.jetTau3[0] / events.jetTau1[0] )
			jet1Tau32.Fill( events.jetTau3[0] / events.jetTau2[0] )
			jet1Tau2vsTau1.Fill( events.jetTau1[0], events.jetTau2[0] )
			jet1Tau3vsTau1.Fill( events.jetTau1[0], events.jetTau3[0] )
			jet1Tau3vsTau2.Fill( events.jetTau2[0], events.jetTau3[0] )
			jet1Ptvsht.Fill( events.jetPt[0], HT )
			jet1Massvsht.Fill( events.jetPt[0], HT )
			jet1MassvsTau21.Fill( events.jetPt[0], events.jetTau2[0] / events.jetTau1[0] )

#			####### 2nd Leading Jet
			jet2Pt.Fill( events.jetPt[1], weight )
			jet2Eta.Fill( events.jetEta[1], weight )
			jet2Phi.Fill( events.jetPhi[1], weight )
			jet2Mass.Fill( events.jetMass[1], weight )
			jet2PtvsMass.Fill( events.jetPt[1], events.jetMass[1] )
			jet2Area.Fill( events.jetArea[1], weight )
			jet2Tau1.Fill( events.jetTau1[1], weight )
			jet2Tau2.Fill( events.jetTau2[1], weight )
			jet2Tau3.Fill( events.jetTau3[1], weight )
			jet2Tau21.Fill( events.jetTau2[1] / events.jetTau1[1] )
			jet2Tau31.Fill( events.jetTau3[1] / events.jetTau1[1] )
			jet2Tau32.Fill( events.jetTau3[1] / events.jetTau2[1] )
			jet2Tau2vsTau1.Fill( events.jetTau1[1], events.jetTau2[1] )
			jet2Tau3vsTau1.Fill( events.jetTau1[1], events.jetTau3[1] )
			jet2Tau3vsTau2.Fill( events.jetTau2[1], events.jetTau3[1] )
			jet2Ptvsht.Fill( events.jetPt[1], HT )
			jet2Massvsht.Fill( events.jetPt[1], HT )
			jet2MassvsTau21.Fill( events.jetPt[1], events.jetTau2[1] / events.jetTau1[1] )

			####### Leading and Second Leading
			jet1vsjet2Mass.Fill( events.jetMass[0], events.jetMass[1] )
			jet1vsjet2Tau21.Fill(  events.jetTau2[0] / events.jetTau1[0], events.jetTau2[1] / events.jetTau1[1] )

			####### 3rd Leading Jet
			if events.nJets > 2:
				jet3Pt.Fill( events.jetPt[2], weight )
				jet3Eta.Fill( events.jetEta[2], weight )
				jet3Phi.Fill( events.jetPhi[2], weight )
				jet3Mass.Fill( events.jetMass[2], weight )
				jet3PtvsMass.Fill( events.jetPt[2], events.jetMass[2] )
				jet3Area.Fill( events.jetArea[2], weight )
				jet3Tau1.Fill( events.jetTau1[2], weight )
				jet3Tau2.Fill( events.jetTau2[2], weight )
				jet3Tau3.Fill( events.jetTau3[2], weight )
				jet3Tau21.Fill( events.jetTau2[2] / events.jetTau1[2] )
				jet3Tau31.Fill( events.jetTau3[2] / events.jetTau1[2] )
				jet3Tau32.Fill( events.jetTau3[2] / events.jetTau2[2] )
				jet3Tau2vsTau1.Fill( events.jetTau1[2], events.jetTau2[2] )
				jet3Tau3vsTau1.Fill( events.jetTau1[2], events.jetTau3[2] )
				jet3Tau3vsTau2.Fill( events.jetTau2[2], events.jetTau3[2] )
				jet3Ptvsht.Fill( events.jetPt[2], HT )
				jet3Massvsht.Fill( events.jetPt[2], HT )

			####### 4th Leading Jet
			if events.nJets > 3:
				jet4Pt.Fill( events.jetPt[3], weight )
				jet4Eta.Fill( events.jetEta[3], weight )
				jet4Phi.Fill( events.jetPhi[3], weight )
				jet4Mass.Fill( events.jetMass[3], weight )
				jet4PtvsMass.Fill( events.jetPt[3], events.jetMass[3] )
				jet4Area.Fill( events.jetArea[3], weight )
				jet4Tau1.Fill( events.jetTau1[3], weight )
				jet4Tau2.Fill( events.jetTau2[3], weight )
				jet4Tau3.Fill( events.jetTau3[3], weight )
				jet4Tau21.Fill( events.jetTau2[3] / events.jetTau1[3] )
				jet4Tau31.Fill( events.jetTau3[3] / events.jetTau1[3] )
				jet4Tau32.Fill( events.jetTau3[3] / events.jetTau2[3] )
				jet4Tau2vsTau1.Fill( events.jetTau1[3], events.jetTau2[3] )
				jet4Tau3vsTau1.Fill( events.jetTau1[3], events.jetTau3[3] )
				jet4Tau3vsTau2.Fill( events.jetTau2[3], events.jetTau3[3] )
				jet4Ptvsht.Fill( events.jetPt[3], HT )
				jet4Massvsht.Fill( events.jetPt[3], HT )

			if cut_jet1pt and cut_HT:

				############  Event Variables
				cut_numberJets.Fill( events.nJets, weight )
				cut_ht.Fill( HT, weight )

				############ Leading Jet
				cut_jet1Pt.Fill( events.jetPt[0], weight )
				cut_jet1Eta.Fill( events.jetEta[0], weight )
				cut_jet1Phi.Fill( events.jetPhi[0], weight )
				cut_jet1Mass.Fill( events.jetMass[0], weight )
				cut_jet1PtvsMass.Fill( events.jetPt[0], events.jetMass[0] )
				cut_jet1Area.Fill( events.jetArea[0], weight )
				cut_jet1Tau1.Fill( events.jetTau1[0], weight )
				cut_jet1Tau2.Fill( events.jetTau2[0], weight )
				cut_jet1Tau3.Fill( events.jetTau3[0], weight )
				cut_jet1Tau21.Fill( events.jetTau2[0] / events.jetTau1[0] )
				cut_jet1Tau31.Fill( events.jetTau3[0] / events.jetTau1[0] )
				cut_jet1Tau32.Fill( events.jetTau3[0] / events.jetTau2[0] )
				cut_jet1Tau2vsTau1.Fill( events.jetTau1[0], events.jetTau2[0] )
				cut_jet1Tau3vsTau1.Fill( events.jetTau1[0], events.jetTau3[0] )
				cut_jet1Tau3vsTau2.Fill( events.jetTau2[0], events.jetTau3[0] )
				cut_jet1Ptvsht.Fill( events.jetPt[0], HT )
				cut_jet1Massvsht.Fill( events.jetPt[0], HT )
				cut_jet1MassvsTau21.Fill( events.jetPt[0], events.jetTau2[0] / events.jetTau1[0] )

	#			####### 2nd Leading Jet
				cut_jet2Pt.Fill( events.jetPt[1], weight )
				cut_jet2Eta.Fill( events.jetEta[1], weight )
				cut_jet2Phi.Fill( events.jetPhi[1], weight )
				cut_jet2Mass.Fill( events.jetMass[1], weight )
				cut_jet2PtvsMass.Fill( events.jetPt[1], events.jetMass[1] )
				cut_jet2Area.Fill( events.jetArea[1], weight )
				cut_jet2Tau1.Fill( events.jetTau1[1], weight )
				cut_jet2Tau2.Fill( events.jetTau2[1], weight )
				cut_jet2Tau3.Fill( events.jetTau3[1], weight )
				cut_jet2Tau21.Fill( events.jetTau2[1] / events.jetTau1[1] )
				cut_jet2Tau31.Fill( events.jetTau3[1] / events.jetTau1[1] )
				cut_jet2Tau32.Fill( events.jetTau3[1] / events.jetTau2[1] )
				cut_jet2Tau2vsTau1.Fill( events.jetTau1[1], events.jetTau2[1] )
				cut_jet2Tau3vsTau1.Fill( events.jetTau1[1], events.jetTau3[1] )
				cut_jet2Tau3vsTau2.Fill( events.jetTau2[1], events.jetTau3[1] )
				cut_jet2Ptvsht.Fill( events.jetPt[1], HT )
				cut_jet2Massvsht.Fill( events.jetPt[1], HT )
				cut_jet2MassvsTau21.Fill( events.jetPt[1], events.jetTau2[1] / events.jetTau1[1] )

				####### Leading and Second Leading
				cut_jet1vsjet2Mass.Fill( events.jetMass[0], events.jetMass[1] )
				cut_jet1vsjet2Tau21.Fill(  events.jetTau2[0] / events.jetTau1[0], events.jetTau2[1] / events.jetTau1[1] )




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
	parser.add_option( '-j', '--jetAlgo', action='store', type='string', dest='jetAlgo', default='AK5', help='Jet Algorithm' )
	parser.add_option( '-g', '--grooming', action='store', type='string', dest='grooming', default='', help='Jet Algorithm' )
	parser.add_option( '-d', '--debug', action='store_true', dest='couts', default=False, help='True print couts in screen, False print in a file' )
	parser.add_option( '-f', '--final', action='store_true', dest='final', default=False, help='If True, final version' )
	parser.add_option( '-q', '--qcd', action='store',  type='string', dest='QCD', default='250To500', help='Binning of QCD' )
	parser.add_option( '-s', '--sample', action='store',  type='string', dest='samples', default='Signal', help='Type of sample' )
	parser.add_option( '-n', '--nJob', action='store', type='int', dest='nJob', default=0, help='Number of Job' )

	(options, args) = parser.parse_args()

	mass = options.mass
	couts = options.couts
	final = options.final
	jetAlgo = options.jetAlgo
	grooming = options.grooming
	QCD = options.QCD
	samples = options.samples
	Job = options.nJob

	if 'QCD' in samples: 
		sample = 'QCD_HT-'+QCD
		#list = os.popen('ls -1 /eos/uscms/store/user/algomez/'+sample+'_8TeV_Summer12_DR53X-PU_S10_START53_V7A-v1/*.root').read().splitlines()
		tmpList = os.popen('ls -1v /eos/uscms/store/user/algomez/'+sample+'_8TeV_Summer12_DR53X-PU_S10_START53_V7A-v1/*.root').read().splitlines()
		filesPerJob = round(len(tmpList)/25)+1
		iniList = int(filesPerJob*Job)
		finList = int(filesPerJob*(Job+1)-1)
		print filesPerJob, iniList, finList
		#list = tmpList[iniList:finList]
		list = tmpList[0:2]
		inputList = [i if i.startswith('file') else 'file:' + i for i in list]
		if '250To500' in QCD: weight = 19500*276000/27062078.0
		elif '500To1000' in QCD: weight = 19500*8426/30599292.0
		else: weight = 19500*204/13843863.0
	elif 'Signal' in samples: 
		sample = 'stopUDD312_'+str(mass)
		#list = os.popen('ls -1 /cms/gomez/Substructure/Generation/Simulation/CMSSW_5_3_2_patch4/src/mySimulations/stop_UDD312_50/aodsim/*.root').read().splitlines()
		list = os.popen('ls -1v /cms/gomez/Stops/st_jj/patTuples/'+sample+'/results/140417/*.root').read().splitlines()
		#list = [ '/cms/gomez/Stops/st_jj/patTuples/stopUDD312_50_tree_test_grom.root' ]
		inputList = [i if i.startswith('file') else 'file:' + i for i in list]
		if mass == 50: weight = 1
		elif mass == 100: weight = 19500*559.757/100000.0
		elif mass == 200: weight = 19500*18.5245/100000.0
	elif 'Data' in samples:
		sample = 'Data_'+QCD
		list = os.popen('ls -1v /eos/uscms/store/user/algomez/'+sample+'/*.root').read().splitlines()
		#filesPerJob = round(len(tmpList)/25)+1
		#iniList = int(filesPerJob*Job)
		#finList = int(filesPerJob*(Job+1)-1)
		#print filesPerJob, iniList, finList
		#list = tmpList[iniList:finList]
		#list = tmpList[0:2]
		inputList = [i if i.startswith('file') else 'file:' + i for i in list]
		weight = 1


	outputDir = '/uscms_data/d3/algomez/files/Data/treeResults/'
	#outputDir = '/uscms_data/d3/algomez/files/QCD_8TeV/treeResults/'
	#outputDir = '/eos/uscms/store/user/algomez/'
	#outputDir = '/cms/gomez/Stops/st_jj/treeResults/'
	print inputList
	print weight

	if not final : myAnalyzer( inputList[:2], outputDir, sample, couts, final, jetAlgo, grooming, weight, Job )
	else: myAnalyzer( inputList, outputDir, sample, couts, final, jetAlgo, grooming, weight, Job )

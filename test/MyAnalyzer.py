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
def myAnalyzer( infile, outputDir, sample, couts, final, jetAlgo, grooming, weight, Job, FNAL ):

	if FNAL:
		if final:
			if not ( os.path.exists( outputDir ) ): os.makedirs( outputDir )
			#if not ( os.path.exists( '/eos/uscms/'+outputDir ) ): os.makedirs( '/eos/uscms/'+outputDir )
			if 'QCD' in sample:
				outputFileName = outputDir + sample + '_'+jetAlgo+'_'+grooming+'_'+str(Job)+'_Plots.root'
			else:
				outputFileName = outputDir + sample + '_'+jetAlgo+'_'+grooming+'_Plots.root'
		else:
			outputFileName = sample + '_'+jetAlgo+'_'+grooming+'_Plots_TEST.root'

	else:
		if not final: 
			outputFileName = sample + '_'+jetAlgo+'_'+grooming+'_Plots_TEST.root'
		else:
			if not ( os.path.exists( outputDir + 'rootFiles/' + monthKey ) ): os.makedirs( outputDir + 'rootFiles/' + monthKey )
			if 'QCD' in sample:
				outputFileName = outputDir + 'rootFiles/' + monthKey + '/' + sample + '_'+jetAlgo+'_'+grooming+'_'+str(Job)+'_Plots.root'
			else:
				outputFileName = outputDir + 'rootFiles/' + monthKey + '/' + sample + '_'+jetAlgo+'_'+grooming+'_Plots.root'


	outputFile = TFile( outputFileName , 'RECREATE' )
	#outputFile = TFile( 'root://xrootd.unl.edu/'+outputFileName , 'RECREATE' )
	#outputFile = TFile( 'root://cmssrv32.fnal.gov/'+outputFileName , 'RECREATE' )

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
	ht 		= TH1F('h_ht_'+jetAlgo+'_'+grooming, 	'h_ht_'+jetAlgo, 	nBinsHT,  	0, 	maxHT)
	numberPV 	= TH1F('h_numberPV_'+jetAlgo+'_'+grooming, 	'h_numberPV_'+jetAlgo, 	50,  	0., 	50.)
	MET 		= TH1F('h_MET_'+jetAlgo+'_'+grooming, 	'h_MET_'+jetAlgo, 	nBinsMET,  	0, 	maxMET)
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
	HTvsNPV 	= TH2F('h_HTvsNPV_'+jetAlgo+'_'+grooming, 'h_HTvsNPV_'+jetAlgo, nBinsHT,  0., maxHT, 50,  0., 50.)

	############################################################ Leading Jet 
	jet1Pt	 	= TH1F('h_jet1Pt_'+jetAlgo+'_'+grooming, 'h_jet1Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	jet1Mass 	= TH1F('h_jet1Mass_'+jetAlgo+'_'+grooming, 'h_jet1Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	jet1MassOverPt 	= TH1F('h_jet1MassOverPt_'+jetAlgo+'_'+grooming, 'h_jet1MassOverPt_'+jetAlgo, 20,  0., 2)
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
	jet1MassvsMET 	= TH2F('h_jet1MassvsMET_'+jetAlgo+'_'+grooming, 'h_jet1MassvsMET_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMET,  	0, 	maxMET)
	jet1MassvsNPV 	= TH2F('h_jet1MassvsNPV_'+jetAlgo+'_'+grooming, 'h_jet1MassvsNPV_'+jetAlgo, nBinsMass,  0., maxMass, 50,  	0, 	50)

	############################################################ 2nd Leading Jet 
	jet2Pt	 	= TH1F('h_jet2Pt_'+jetAlgo+'_'+grooming, 'h_jet2Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	jet2Mass 	= TH1F('h_jet2Mass_'+jetAlgo+'_'+grooming, 'h_jet2Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	jet2MassOverPt 	= TH1F('h_jet2MassOverPt_'+jetAlgo+'_'+grooming, 'h_jet2MassOverPt_'+jetAlgo, 20,  0., 2)
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
	jet2MassvsMET 	= TH2F('h_jet2MassvsMET_'+jetAlgo+'_'+grooming, 'h_jet2MassvsMET_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMET,  	0, 	maxMET)
	jet2MassvsNPV 	= TH2F('h_jet2MassvsNPV_'+jetAlgo+'_'+grooming, 'h_jet2MassvsNPV_'+jetAlgo, nBinsMass,  0., maxMass, 50,  	0, 	50)

	########################################################### Leading and 2nd Leading Jet
	jet1vsjet2Mass 	= TH2F('h_jet1vsjet2Mass_'+jetAlgo+'_'+grooming, 'h_jet1vsjet2Mass_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMass,  0., maxMass)
	jet1vsjet2Tau21 	= TH2F('h_jet1vsjet2Tau21_'+jetAlgo+'_'+grooming, 'h_jet1vsjet2Tau21_'+jetAlgo,   nBinsTau,  0., maxTau,   nBinsTau,  0., maxTau)
	jet2CosThetaStar = TH1F('h_jet2CosThetaStar_'+jetAlgo+'_'+grooming, 'h_jet2CosThetaStar_'+jetAlgo, 20,  -1., 1.)
	jet1CosThetaStar = TH1F('h_jet1CosThetaStar_'+jetAlgo+'_'+grooming, 'h_jet1CosThetaStar_'+jetAlgo, 20,  -1., 1.)

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
	cut_HTvsNPV 	= TH2F('h_cut_HTvsNPV_'+jetAlgo+'_'+grooming, 'h_cut_HTvsNPV_'+jetAlgo, nBinsHT,  0., maxHT, 50,  0., 50.)
	cut_numberPV 	= TH1F('h_cut_numberPV_'+jetAlgo+'_'+grooming, 	'h_cut_numberPV_'+jetAlgo, 	50,  	0., 	50.)
	cut_MET 		= TH1F('h_cut_MET_'+jetAlgo+'_'+grooming, 	'h_cut_MET_'+jetAlgo, 	24,  	0, 	120.)
	#cut_jetPt	 	= TH1F('h_cut_jetPt_'+jetAlgo+'_'+grooming, 'h_cut_jetPt_'+jetAlgo, nBinsPt,  0., maxPt)
	#cut_jetEta	 	= TH1F('h_cut_jetEta_'+jetAlgo+'_'+grooming, 'h_cut_jetEta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	#cut_jetPhi	 	= TH1F('h_cut_jetPhi_'+jetAlgo+'_'+grooming, 'h_cut_jetPhi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	#cut_jetMass	 	= TH1F('h_cut_jetMass_'+jetAlgo+'_'+grooming, 'h_cut_jetMass_'+jetAlgo, nBinsMass,  0., maxMass)
	#cut_jetPtvsMass	= TH2F('h_cut_jetPtvsMass_'+jetAlgo+'_'+grooming, 'h_cut_jetPtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	#cut_jetArea 	= TH1F('h_cut_jetArea_'+jetAlgo+'_'+grooming, 'h_cut_jetArea_'+jetAlgo, 50,  0., 5.)
	#cut_jetTau1 	= TH1F('h_cut_jetTau1_'+jetAlgo+'_'+grooming, 'h_cut_jetTau1_'+jetAlgo, nBinsTau,  0., maxTau)
	#cut_jetTau2 	= TH1F('h_cut_jetTau2_'+jetAlgo+'_'+grooming, 'h_cut_jetTau2_'+jetAlgo, nBinsTau,  0., maxTau)
	#cut_jetTau3 	= TH1F('h_cut_jetTau3_'+jetAlgo+'_'+grooming, 'h_cut_jetTau3_'+jetAlgo, nBinsTau,  0., maxTau)
	#cut_jetTau21 	= TH1F('h_cut_jetTau21_'+jetAlgo+'_'+grooming, 'h_cut_jetTau21_'+jetAlgo, nBinsTau,  0., maxTau)
	#cut_jetTau31 	= TH1F('h_cut_jetTau31_'+jetAlgo+'_'+grooming, 'h_cut_jetTau31_'+jetAlgo, nBinsTau,  0., maxTau)
	#cut_jetTau32 	= TH1F('h_cut_jetTau32_'+jetAlgo+'_'+grooming, 'h_cut_jetTau32_'+jetAlgo, nBinsTau,  0., maxTau)
	#cut_jetTau2vsTau1 	= TH2F('h_cut_jetTau2vsTau1_'+jetAlgo+'_'+grooming, 'h_cut_jetTau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	#cut_jetTau3vsTau1 	= TH2F('h_cut_jetTau3vsTau1_'+jetAlgo+'_'+grooming, 'h_cut_jetTau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	#cut_jetTau3vsTau2 	= TH2F('h_cut_jetTau3vsTau2_'+jetAlgo+'_'+grooming, 'h_cut_jetTau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)

	############################################################ Leading Jet 
	cut_jet1Pt	 	= TH1F('h_cut_jet1Pt_'+jetAlgo+'_'+grooming, 'h_cut_jet1Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	cut_jet1Mass 	= TH1F('h_cut_jet1Mass_'+jetAlgo+'_'+grooming, 'h_cut_jet1Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	cut_jet1MassOverPt 	= TH1F('h_cut_jet1MassOverPt_'+jetAlgo+'_'+grooming, 'h_cut_jet1MassOverPt_'+jetAlgo, 20,  0., 2)
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
	cut_jet1MassvsMET 	= TH2F('h_cut_jet1MassvsMET_'+jetAlgo+'_'+grooming, 'h_cut_jet1MassvsMET_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMET, 	0, 	maxMET)
	cut_jet1MassvsNPV 	= TH2F('h_cut_jet1MassvsNPV_'+jetAlgo+'_'+grooming, 'h_cut_jet1MassvsNPV_'+jetAlgo, nBinsMass,  0., maxMass, 50,  	0, 	50)

	############################################################ 2nd Leading Jet 
	cut_jet2Pt	 	= TH1F('h_cut_jet2Pt_'+jetAlgo+'_'+grooming, 'h_cut_jet2Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	cut_jet2Mass 	= TH1F('h_cut_jet2Mass_'+jetAlgo+'_'+grooming, 'h_cut_jet2Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	cut_jet2MassOverPt 	= TH1F('h_cut_jet2MassOverPt_'+jetAlgo+'_'+grooming, 'h_cut_jet2MassOverPt_'+jetAlgo, 20,  0., 2)
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
	cut_jet2MassvsMET 	= TH2F('h_cut_jet2MassvsMET_'+jetAlgo+'_'+grooming, 'h_cut_jet2MassvsMET_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMET, 	0, 	maxMET)
	cut_jet2MassvsNPV 	= TH2F('h_cut_jet2MassvsNPV_'+jetAlgo+'_'+grooming, 'h_cut_jet2MassvsNPV_'+jetAlgo, nBinsMass,  0., maxMass, 50,  	0, 	50)

	########################################################### Leading and 2nd Leading Jet
	cut_jet1vsjet2Mass 	= TH2F('h_cut_jet1vsjet2Mass_'+jetAlgo+'_'+grooming, 'h_cut_jet1vsjet2Mass_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMass,  0., maxMass)
	cut_jet1vsjet2Tau21 	= TH2F('h_cut_jet1vsjet2Tau21_'+jetAlgo+'_'+grooming, 'h_cut_jet1vsjet2Tau21_'+jetAlgo,   nBinsTau,  0., maxTau,   nBinsTau,  0., maxTau)
	cut_jet2CosThetaStar 	= TH1F('h_cut_jet2CosThetaStar_'+jetAlgo+'_'+grooming, 'h_cut_jet2CosThetaStar_'+jetAlgo, 20,  -1., 1.)
	cut_jet1CosThetaStar 	= TH1F('h_cut_jet1CosThetaStar_'+jetAlgo+'_'+grooming, 'h_cut_jet1CosThetaStar_'+jetAlgo, 20,  -1., 1.)


	############################################################ 3rd Leading Jet 
	#cut_jet3Pt	 	= TH1F('h_cut_jet3Pt_'+jetAlgo+'_'+grooming, 'h_cut_jet3Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	#cut_jet3Mass 	= TH1F('h_cut_jet3Mass_'+jetAlgo+'_'+grooming, 'h_cut_jet3Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	#cut_jet3Eta	 	= TH1F('h_cut_jet3Eta_'+jetAlgo+'_'+grooming, 'h_cut_jet3Eta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	#cut_jet3Phi	 	= TH1F('h_cut_jet3Phi_'+jetAlgo+'_'+grooming, 'h_cut_jet3Phi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	#cut_jet3PtvsMass	= TH2F('h_cut_jet3PtvsMass_'+jetAlgo+'_'+grooming, 'h_cut_jet3PtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	#cut_jet3Area 	= TH1F('h_cut_jet3Area_'+jetAlgo+'_'+grooming, 'h_cut_jet3Area_'+jetAlgo, 50,  0., 5.)
	#cut_jet3Tau1 	= TH1F('h_cut_jet3Tau1_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau1_'+jetAlgo, nBinsTau,  0., maxTau)
	#cut_jet3Tau2 	= TH1F('h_cut_jet3Tau2_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau2_'+jetAlgo, nBinsTau,  0., maxTau)
	#cut_jet3Tau3 	= TH1F('h_cut_jet3Tau3_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau3_'+jetAlgo, nBinsTau,  0., maxTau)
	#cut_jet3Tau21 	= TH1F('h_cut_jet3Tau21_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau21_'+jetAlgo, nBinsTau,  0., maxTau)
	#cut_jet3Tau31 	= TH1F('h_cut_jet3Tau31_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau31_'+jetAlgo, nBinsTau,  0., maxTau)
	#cut_jet3Tau32 	= TH1F('h_cut_jet3Tau32_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau32_'+jetAlgo, nBinsTau,  0., maxTau)
	#cut_jet3Tau2vsTau1 	= TH2F('h_cut_jet3Tau2vsTau1_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	#cut_jet3Tau3vsTau1 	= TH2F('h_cut_jet3Tau3vsTau1_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	#cut_jet3Tau3vsTau2 	= TH2F('h_cut_jet3Tau3vsTau2_'+jetAlgo+'_'+grooming, 'h_cut_jet3Tau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	#####################################################################################################################################


	#####################################################
	#### kinematic cuts plus others and ONLY 2 jets
	################################################################################################### Event Variables
	cut2Jets_ht 		= TH1F('h_cut2Jets_ht_'+jetAlgo+'_'+grooming, 	'h_cut2Jets_ht_'+jetAlgo, 	nBinsHT,  	0, 	maxHT)
	cut2Jets_numberJets 	= TH1F('h_cut2Jets_numberJets_'+jetAlgo+'_'+grooming, 'h_cut2Jets_numberJets_'+jetAlgo, 15,  0., 15.)
	cut2Jets_HTvsNPV 	= TH2F('h_cut2Jets_HTvsNPV_'+jetAlgo+'_'+grooming, 'h_cut2Jets_HTvsNPV_'+jetAlgo, nBinsHT,  0., maxHT, 50,  0., 50.)
	cut2Jets_numberPV 	= TH1F('h_cut2Jets_numberPV_'+jetAlgo+'_'+grooming, 	'h_cut2Jets_numberPV_'+jetAlgo, 	50,  	0., 	50.)
	cut2Jets_MET 		= TH1F('h_cut2Jets_MET_'+jetAlgo+'_'+grooming, 	'h_cut2Jets_MET_'+jetAlgo, 	24,  	0, 	120.)

	############################################################ Leading Jet 
	cut2Jets_jet1Pt	 	= TH1F('h_cut2Jets_jet1Pt_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	cut2Jets_jet1Mass 	= TH1F('h_cut2Jets_jet1Mass_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	cut2Jets_jet1MassOverPt 	= TH1F('h_cut2Jets_jet1MassOverPt_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1MassOverPt_'+jetAlgo, 20,  0., 2)
	cut2Jets_jet1Eta	 	= TH1F('h_cut2Jets_jet1Eta_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1Eta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	cut2Jets_jet1Phi	 	= TH1F('h_cut2Jets_jet1Phi_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1Phi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	cut2Jets_jet1PtvsMass	= TH2F('h_cut2Jets_jet1PtvsMass_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1PtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	cut2Jets_jet1Area 	= TH1F('h_cut2Jets_jet1Area_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1Area_'+jetAlgo, 50,  0., 5.)
	cut2Jets_jet1Tau1 	= TH1F('h_cut2Jets_jet1Tau1_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1Tau1_'+jetAlgo, nBinsTau,  0., maxTau)
	cut2Jets_jet1Tau2 	= TH1F('h_cut2Jets_jet1Tau2_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1Tau2_'+jetAlgo, nBinsTau,  0., maxTau)
	cut2Jets_jet1Tau3 	= TH1F('h_cut2Jets_jet1Tau3_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1Tau3_'+jetAlgo, nBinsTau,  0., maxTau)
	cut2Jets_jet1Tau21 	= TH1F('h_cut2Jets_jet1Tau21_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1Tau21_'+jetAlgo, nBinsTau,  0., maxTau)
	cut2Jets_jet1Tau31 	= TH1F('h_cut2Jets_jet1Tau31_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1Tau31_'+jetAlgo, nBinsTau,  0., maxTau)
	cut2Jets_jet1Tau32 	= TH1F('h_cut2Jets_jet1Tau32_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1Tau32_'+jetAlgo, nBinsTau,  0., maxTau)
	cut2Jets_jet1Tau2vsTau1 	= TH2F('h_cut2Jets_jet1Tau2vsTau1_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1Tau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cut2Jets_jet1Tau3vsTau1 	= TH2F('h_cut2Jets_jet1Tau3vsTau1_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1Tau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cut2Jets_jet1Tau3vsTau2 	= TH2F('h_cut2Jets_jet1Tau3vsTau2_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1Tau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cut2Jets_jet1Ptvsht 	= TH2F('h_cut2Jets_jet1Ptvsht_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1Ptvsht_'+jetAlgo, nBinsPt,  0., maxPt, nBinsHT,  	0, 	maxHT)
	cut2Jets_jet1Massvsht 	= TH2F('h_cut2Jets_jet1Massvsht_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1Massvsht_'+jetAlgo, nBinsMass,  0., maxMass, nBinsHT,  	0, 	maxHT)
	cut2Jets_jet1MassvsTau21 	= TH2F('h_cut2Jets_jet1MassvsTau21_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1MassvsTau21_'+jetAlgo, nBinsMass,  0., maxMass, nBinsTau,  0., maxTau)
	cut2Jets_jet1MassvsMET 	= TH2F('h_cut2Jets_jet1MassvsMET_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1MassvsMET_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMET, 	0, 	maxMET)
	cut2Jets_jet1MassvsNPV 	= TH2F('h_cut2Jets_jet1MassvsNPV_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1MassvsNPV_'+jetAlgo, nBinsMass,  0., maxMass, 50,  	0, 	50)

	############################################################ 2nd Leading Jet 
	cut2Jets_jet2Pt	 	= TH1F('h_cut2Jets_jet2Pt_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	cut2Jets_jet2Mass 	= TH1F('h_cut2Jets_jet2Mass_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	cut2Jets_jet2MassOverPt 	= TH1F('h_cut2Jets_jet2MassOverPt_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2MassOverPt_'+jetAlgo, 20,  0., 2)
	cut2Jets_jet2Eta	 	= TH1F('h_cut2Jets_jet2Eta_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2Eta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	cut2Jets_jet2Phi	 	= TH1F('h_cut2Jets_jet2Phi_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2Phi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	cut2Jets_jet2PtvsMass	= TH2F('h_cut2Jets_jet2PtvsMass_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2PtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	cut2Jets_jet2Area 	= TH1F('h_cut2Jets_jet2Area_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2Area_'+jetAlgo, 50,  0., 5.)
	cut2Jets_jet2Tau1 	= TH1F('h_cut2Jets_jet2Tau1_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2Tau1_'+jetAlgo, nBinsTau,  0., maxTau)
	cut2Jets_jet2Tau2 	= TH1F('h_cut2Jets_jet2Tau2_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2Tau2_'+jetAlgo, nBinsTau,  0., maxTau)
	cut2Jets_jet2Tau3 	= TH1F('h_cut2Jets_jet2Tau3_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2Tau3_'+jetAlgo, nBinsTau,  0., maxTau)
	cut2Jets_jet2Tau21 	= TH1F('h_cut2Jets_jet2Tau21_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2Tau21_'+jetAlgo, nBinsTau,  0., maxTau)
	cut2Jets_jet2Tau31 	= TH1F('h_cut2Jets_jet2Tau31_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2Tau31_'+jetAlgo, nBinsTau,  0., maxTau)
	cut2Jets_jet2Tau32 	= TH1F('h_cut2Jets_jet2Tau32_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2Tau32_'+jetAlgo, nBinsTau,  0., maxTau)
	cut2Jets_jet2Tau2vsTau1 	= TH2F('h_cut2Jets_jet2Tau2vsTau1_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2Tau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cut2Jets_jet2Tau3vsTau1 	= TH2F('h_cut2Jets_jet2Tau3vsTau1_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2Tau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cut2Jets_jet2Tau3vsTau2 	= TH2F('h_cut2Jets_jet2Tau3vsTau2_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2Tau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cut2Jets_jet2Ptvsht 	= TH2F('h_cut2Jets_jet2Ptvsht_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2Ptvsht_'+jetAlgo, nBinsPt,  0., maxPt, nBinsHT,  	0, 	maxHT)
	cut2Jets_jet2Massvsht 	= TH2F('h_cut2Jets_jet2Massvsht_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2Massvsht_'+jetAlgo, nBinsMass,  0., maxMass, nBinsHT,  	0, 	maxHT)
	cut2Jets_jet2MassvsTau21 	= TH2F('h_cut2Jets_jet2MassvsTau21_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2MassvsTau21_'+jetAlgo, nBinsMass,  0., maxMass,  nBinsTau,  0., maxTau)
	cut2Jets_jet2MassvsMET 	= TH2F('h_cut2Jets_jet2MassvsMET_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2MassvsMET_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMET, 	0, 	maxMET)
	cut2Jets_jet2MassvsNPV 	= TH2F('h_cut2Jets_jet2MassvsNPV_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2MassvsNPV_'+jetAlgo, nBinsMass,  0., maxMass, 50,  	0, 	50)

	########################################################### Leading and 2nd Leading Jet
	cut2Jets_jet1vsjet2Mass 	= TH2F('h_cut2Jets_jet1vsjet2Mass_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1vsjet2Mass_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMass,  0., maxMass)
	cut2Jets_jet1vsjet2Tau21 	= TH2F('h_cut2Jets_jet1vsjet2Tau21_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1vsjet2Tau21_'+jetAlgo,   nBinsTau,  0., maxTau,   nBinsTau,  0., maxTau)
	cut2Jets_jet2CosThetaStar 	= TH1F('h_cut2Jets_jet2CosThetaStar_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet2CosThetaStar_'+jetAlgo, 20,  -1., 1.)
	cut2Jets_jet1CosThetaStar 	= TH1F('h_cut2Jets_jet1CosThetaStar_'+jetAlgo+'_'+grooming, 'h_cut2Jets_jet1CosThetaStar_'+jetAlgo, 20,  -1., 1.)


	#####################################################
	#### kinematic cuts plus other, remove lead pt cut
	################################################################################################### Event Variables
	cutWO1jetpt_ht 		= TH1F('h_cutWO1jetpt_ht_'+jetAlgo+'_'+grooming, 	'h_cutWO1jetpt_ht_'+jetAlgo, 	nBinsHT,  	0, 	maxHT)
	cutWO1jetpt_numberJets 	= TH1F('h_cutWO1jetpt_numberJets_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_numberJets_'+jetAlgo, 15,  0., 15.)
	cutWO1jetpt_HTvsNPV 	= TH2F('h_cutWO1jetpt_HTvsNPV_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_HTvsNPV_'+jetAlgo, nBinsHT,  0., maxHT, 50,  0., 50.)
	cutWO1jetpt_numberPV 	= TH1F('h_cutWO1jetpt_numberPV_'+jetAlgo+'_'+grooming, 	'h_cutWO1jetpt_numberPV_'+jetAlgo, 	50,  	0., 	50.)
	cutWO1jetpt_MET 		= TH1F('h_cutWO1jetpt_MET_'+jetAlgo+'_'+grooming, 	'h_cutWO1jetpt_MET_'+jetAlgo, 	24,  	0, 	120.)

	############################################################ Leading Jet 
	cutWO1jetpt_jet1Pt	 	= TH1F('h_cutWO1jetpt_jet1Pt_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	cutWO1jetpt_jet1Mass 	= TH1F('h_cutWO1jetpt_jet1Mass_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	cutWO1jetpt_jet1MassOverPt 	= TH1F('h_cutWO1jetpt_jet1MassOverPt_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1MassOverPt_'+jetAlgo, 20,  0., 2)
	cutWO1jetpt_jet1Eta	 	= TH1F('h_cutWO1jetpt_jet1Eta_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1Eta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	cutWO1jetpt_jet1Phi	 	= TH1F('h_cutWO1jetpt_jet1Phi_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1Phi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	cutWO1jetpt_jet1PtvsMass	= TH2F('h_cutWO1jetpt_jet1PtvsMass_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1PtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	cutWO1jetpt_jet1Area 	= TH1F('h_cutWO1jetpt_jet1Area_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1Area_'+jetAlgo, 50,  0., 5.)
	cutWO1jetpt_jet1Tau1 	= TH1F('h_cutWO1jetpt_jet1Tau1_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1Tau1_'+jetAlgo, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet1Tau2 	= TH1F('h_cutWO1jetpt_jet1Tau2_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1Tau2_'+jetAlgo, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet1Tau3 	= TH1F('h_cutWO1jetpt_jet1Tau3_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1Tau3_'+jetAlgo, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet1Tau21 	= TH1F('h_cutWO1jetpt_jet1Tau21_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1Tau21_'+jetAlgo, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet1Tau31 	= TH1F('h_cutWO1jetpt_jet1Tau31_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1Tau31_'+jetAlgo, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet1Tau32 	= TH1F('h_cutWO1jetpt_jet1Tau32_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1Tau32_'+jetAlgo, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet1Tau2vsTau1 	= TH2F('h_cutWO1jetpt_jet1Tau2vsTau1_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1Tau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet1Tau3vsTau1 	= TH2F('h_cutWO1jetpt_jet1Tau3vsTau1_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1Tau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet1Tau3vsTau2 	= TH2F('h_cutWO1jetpt_jet1Tau3vsTau2_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1Tau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet1Ptvsht 	= TH2F('h_cutWO1jetpt_jet1Ptvsht_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1Ptvsht_'+jetAlgo, nBinsPt,  0., maxPt, nBinsHT,  	0, 	maxHT)
	cutWO1jetpt_jet1Massvsht 	= TH2F('h_cutWO1jetpt_jet1Massvsht_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1Massvsht_'+jetAlgo, nBinsMass,  0., maxMass, nBinsHT,  	0, 	maxHT)
	cutWO1jetpt_jet1MassvsTau21 	= TH2F('h_cutWO1jetpt_jet1MassvsTau21_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1MassvsTau21_'+jetAlgo, nBinsMass,  0., maxMass, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet1MassvsMET 	= TH2F('h_cutWO1jetpt_jet1MassvsMET_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1MassvsMET_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMET, 	0, 	maxMET)
	cutWO1jetpt_jet1MassvsNPV 	= TH2F('h_cutWO1jetpt_jet1MassvsNPV_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1MassvsNPV_'+jetAlgo, nBinsMass,  0., maxMass, 50,  	0, 	50)

	############################################################ 2nd Leading Jet 
	cutWO1jetpt_jet2Pt	 	= TH1F('h_cutWO1jetpt_jet2Pt_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	cutWO1jetpt_jet2Mass 	= TH1F('h_cutWO1jetpt_jet2Mass_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	cutWO1jetpt_jet2MassOverPt 	= TH1F('h_cutWO1jetpt_jet2MassOverPt_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2MassOverPt_'+jetAlgo, 20,  0., 2)
	cutWO1jetpt_jet2Eta	 	= TH1F('h_cutWO1jetpt_jet2Eta_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2Eta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	cutWO1jetpt_jet2Phi	 	= TH1F('h_cutWO1jetpt_jet2Phi_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2Phi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	cutWO1jetpt_jet2PtvsMass	= TH2F('h_cutWO1jetpt_jet2PtvsMass_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2PtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	cutWO1jetpt_jet2Area 	= TH1F('h_cutWO1jetpt_jet2Area_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2Area_'+jetAlgo, 50,  0., 5.)
	cutWO1jetpt_jet2Tau1 	= TH1F('h_cutWO1jetpt_jet2Tau1_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2Tau1_'+jetAlgo, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet2Tau2 	= TH1F('h_cutWO1jetpt_jet2Tau2_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2Tau2_'+jetAlgo, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet2Tau3 	= TH1F('h_cutWO1jetpt_jet2Tau3_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2Tau3_'+jetAlgo, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet2Tau21 	= TH1F('h_cutWO1jetpt_jet2Tau21_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2Tau21_'+jetAlgo, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet2Tau31 	= TH1F('h_cutWO1jetpt_jet2Tau31_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2Tau31_'+jetAlgo, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet2Tau32 	= TH1F('h_cutWO1jetpt_jet2Tau32_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2Tau32_'+jetAlgo, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet2Tau2vsTau1 	= TH2F('h_cutWO1jetpt_jet2Tau2vsTau1_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2Tau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet2Tau3vsTau1 	= TH2F('h_cutWO1jetpt_jet2Tau3vsTau1_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2Tau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet2Tau3vsTau2 	= TH2F('h_cutWO1jetpt_jet2Tau3vsTau2_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2Tau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	cutWO1jetpt_jet2Ptvsht 	= TH2F('h_cutWO1jetpt_jet2Ptvsht_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2Ptvsht_'+jetAlgo, nBinsPt,  0., maxPt, nBinsHT,  	0, 	maxHT)
	cutWO1jetpt_jet2Massvsht 	= TH2F('h_cutWO1jetpt_jet2Massvsht_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2Massvsht_'+jetAlgo, nBinsMass,  0., maxMass, nBinsHT,  	0, 	maxHT)
	cutWO1jetpt_jet2MassvsTau21 	= TH2F('h_cutWO1jetpt_jet2MassvsTau21_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2MassvsTau21_'+jetAlgo, nBinsMass,  0., maxMass,  nBinsTau,  0., maxTau)
	cutWO1jetpt_jet2MassvsMET 	= TH2F('h_cutWO1jetpt_jet2MassvsMET_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2MassvsMET_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMET, 	0, 	maxMET)
	cutWO1jetpt_jet2MassvsNPV 	= TH2F('h_cutWO1jetpt_jet2MassvsNPV_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2MassvsNPV_'+jetAlgo, nBinsMass,  0., maxMass, 50,  	0, 	50)

	########################################################### Leading and 2nd Leading Jet
	cutWO1jetpt_jet1vsjet2Mass 	= TH2F('h_cutWO1jetpt_jet1vsjet2Mass_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1vsjet2Mass_'+jetAlgo, nBinsMass,  0., maxMass, nBinsMass,  0., maxMass)
	cutWO1jetpt_jet1vsjet2Tau21 	= TH2F('h_cutWO1jetpt_jet1vsjet2Tau21_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1vsjet2Tau21_'+jetAlgo,   nBinsTau,  0., maxTau,   nBinsTau,  0., maxTau)
	cutWO1jetpt_jet2CosThetaStar 	= TH1F('h_cutWO1jetpt_jet2CosThetaStar_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet2CosThetaStar_'+jetAlgo, 20,  -1., 1.)
	cutWO1jetpt_jet1CosThetaStar 	= TH1F('h_cutWO1jetpt_jet1CosThetaStar_'+jetAlgo+'_'+grooming, 'h_cutWO1jetpt_jet1CosThetaStar_'+jetAlgo, 20,  -1., 1.)


	###################################### Get GenTree 
	#events = TChain( 'PFJet_'+jetAlgo+grooming+'/events' )
	events = TChain( 'PFJet_'+jetAlgo+'/events' )

	# Loop over the filenames and add to tree.
	for filename in infile:
		print("Adding file: " + filename)
		events.Add(filename)
		#f1 = TFile(filename)
		#tmpTN = f1.Get( 'PFJet_'+jetAlgo+'/TriggerNames') 
		#tmpTP = f1.Get( 'PFJet_'+jetAlgo+'/TriggerPass') 
		#TriggerNames.Add( tmpTN )
		#TriggerPass.Add( tmpTP )

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

		###################################################################### Cuts
		HT = 0			### sanity clear
		for ijet in range( getattr( events, 'nJets'+grooming ) ):
			cut_simpleKinematic =  getattr( events, 'jet'+grooming+'Pt')[ijet] > 30 and abs( getattr( events, 'jet'+grooming+'Eta')[ijet] ) < 2.5 
			HT += getattr( events, 'jet'+grooming+'Pt')[ijet]
		cut_minTwoJets = getattr( events, 'nJets'+grooming ) > 1
		cut_TwoJets = getattr( events, 'nJets'+grooming ) == 2
		cut_jet1pt = getattr( events, 'nJets'+grooming ) > 0 and getattr( events, 'jet'+grooming+'Pt')[0] > 200 
		cut_HT = HT > 850


		###################################################################### Filling Histograms
		if cut_simpleKinematic:

			############# Trigger Info
			###### Just for reference order of triggers in 
			###### Data, QCD, and Signal: HT350, HT750, PFHT350, PFHT650
			###### TriggerPass PFHT650, PFHT350, HT750, HT350
			###### There is a weird behavior in CRAB, that is why I am splitting this into categories

			if 'RPV' in sample:
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

			############  Event Variables
			for k in range( getattr( events, 'nJets'+grooming ) ):
				jetPt.Fill( getattr( events, 'jet'+grooming+'Pt')[k], weight )
				jetEta.Fill( getattr( events, 'jet'+grooming+'Eta')[k], weight )
				jetPhi.Fill( getattr( events, 'jet'+grooming+'Phi')[k], weight )
				jetMass.Fill( getattr( events, 'jet'+grooming+'Mass')[k], weight )
				jetArea.Fill( getattr( events, 'jet'+grooming+'Area')[k], weight )
				jetTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[k], weight ) 
				jetTau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[k], weight ) 
				jetTau3.Fill( getattr( events, 'jet'+grooming+'Tau3')[k], weight ) 
				#jetTau21.Fill( events.jetTau2[k] / events.jetTau1[k] ) 
				#jetTau31.Fill( events.jetTau3[k] / events.jetTau1[k] ) 
				#jetTau32.Fill( events.jetTau3[k] / events.jetTau2[k] ) 
				jetTau2vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[k], getattr( events, 'jet'+grooming+'Tau2')[k] )  
				jetTau3vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[k], getattr( events, 'jet'+grooming+'Tau3')[k] )
				jetTau3vsTau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[k], getattr( events, 'jet'+grooming+'Tau3')[k] ) 
				jetPtvsMass.Fill( getattr( events, 'jet'+grooming+'Pt')[k], getattr( events, 'jet'+grooming+'Mass')[k] )

			numberJets.Fill( getattr( events, 'nJets'+grooming ), weight )
			ht.Fill( HT, weight )
			HTvsNPV.Fill( HT, events.nvtx )
			numberPV.Fill( events.nvtx, weight )
			MET.Fill( events.met, weight )

			############ Leading Jet
			if getattr( events, 'nJets'+grooming ) > 0:
				jet1Pt.Fill( getattr( events, 'jet'+grooming+'Pt')[0], weight )
				jet1Eta.Fill( getattr( events, 'jet'+grooming+'Eta')[0], weight )
				jet1Phi.Fill( getattr( events, 'jet'+grooming+'Phi')[0], weight )
				jet1Mass.Fill( getattr( events, 'jet'+grooming+'Mass')[0], weight )
				jet1MassOverPt.Fill( ( getattr( events, 'jet'+grooming+'Mass')[0] ) / ( getattr( events, 'jet'+grooming+'Pt')[0] ) , weight )
				jet1Area.Fill( getattr( events, 'jet'+grooming+'Area')[0], weight )
				jet1Tau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[0], weight )
				jet1Tau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[0], weight )
				jet1Tau3.Fill( getattr( events, 'jet'+grooming+'Tau3')[0], weight )
				jet1Tau2vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[0], getattr( events, 'jet'+grooming+'Tau2')[0] )
				jet1Tau3vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[0], getattr( events, 'jet'+grooming+'Tau3')[0] )
				jet1Tau3vsTau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[0], getattr( events, 'jet'+grooming+'Tau3')[0] )
				jet1PtvsMass.Fill( getattr( events, 'jet'+grooming+'Pt')[0], getattr( events, 'jet'+grooming+'Mass')[0] )
				jet1Ptvsht.Fill( getattr( events, 'jet'+grooming+'Pt')[0], HT )
				jet1Massvsht.Fill( getattr( events, 'jet'+grooming+'Mass')[0], HT )
				jet1MassvsMET.Fill( getattr( events, 'jet'+grooming+'Mass')[0], events.met )
				jet1MassvsNPV.Fill( getattr( events, 'jet'+grooming+'Mass')[0], events.nvtx )
				
				try: 
					valJet1Tau21 = getattr( events, 'jet'+grooming+'Tau2')[0] / getattr( events, 'jet'+grooming+'Tau1')[0]
				except ZeroDivisionError: 
					valJet1Tau21 = 0
				try: 
					valJet1Tau31 = getattr( events, 'jet'+grooming+'Tau3')[0] / getattr( events, 'jet'+grooming+'Tau1')[0]
				except ZeroDivisionError: 
					valJet1Tau31 = 0
				try: 
					valJet1Tau32 = getattr( events, 'jet'+grooming+'Tau3')[0] / getattr( events, 'jet'+grooming+'Tau2')[0]
				except ZeroDivisionError: 
					valJet1Tau32 = 0

				jet1Tau21.Fill( valJet1Tau21 )
				jet1Tau31.Fill( valJet1Tau31 )
				jet1MassvsTau21.Fill( getattr( events, 'jet'+grooming+'Mass')[0], valJet1Tau21 )
				jet1Tau32.Fill( valJet1Tau32 )

			####### 2nd Leading Jet
			if getattr( events, 'nJets'+grooming ) > 1:
				jet2Pt.Fill( getattr( events, 'jet'+grooming+'Pt')[1], weight )
				jet2Eta.Fill( getattr( events, 'jet'+grooming+'Eta')[1], weight )
				jet2Phi.Fill( getattr( events, 'jet'+grooming+'Phi')[1], weight )
				jet2Mass.Fill( getattr( events, 'jet'+grooming+'Mass')[1], weight )
				jet2MassOverPt.Fill( ( getattr( events, 'jet'+grooming+'Mass')[1] ) / ( getattr( events, 'jet'+grooming+'Pt')[1] ) , weight )
				jet2Area.Fill( getattr( events, 'jet'+grooming+'Area')[1], weight )
				jet2Tau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[1], weight )
				jet2Tau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[1], weight )
				jet2Tau3.Fill( getattr( events, 'jet'+grooming+'Tau3')[1], weight )
				jet2Tau2vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[1], getattr( events, 'jet'+grooming+'Tau2')[1] )
				jet2Tau3vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[1], getattr( events, 'jet'+grooming+'Tau3')[1] )
				jet2Tau3vsTau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[1], getattr( events, 'jet'+grooming+'Tau3')[1] )
				jet2PtvsMass.Fill( getattr( events, 'jet'+grooming+'Pt')[1], getattr( events, 'jet'+grooming+'Mass')[1] )
				jet2Ptvsht.Fill( getattr( events, 'jet'+grooming+'Pt')[1], HT )
				jet2Massvsht.Fill( getattr( events, 'jet'+grooming+'Mass')[1], HT )
				jet2MassvsMET.Fill( getattr( events, 'jet'+grooming+'Mass')[1], events.met )
				jet2MassvsNPV.Fill( getattr( events, 'jet'+grooming+'Mass')[1], events.nvtx )

				try: 
					valJet2Tau21 = getattr( events, 'jet'+grooming+'Tau2')[1] / getattr( events, 'jet'+grooming+'Tau1')[1]
				except ZeroDivisionError: 
					valJet2Tau21 = 0
				try: 
					valJet2Tau31 = getattr( events, 'jet'+grooming+'Tau3')[1] / getattr( events, 'jet'+grooming+'Tau1')[1]
				except ZeroDivisionError: 
					valJet2Tau31 = 0
				try: 
					valJet2Tau32 = getattr( events, 'jet'+grooming+'Tau3')[1] / getattr( events, 'jet'+grooming+'Tau2')[1]
				except ZeroDivisionError: 
					valJet2Tau32 = 0

				jet2Tau21.Fill( valJet2Tau21 )
				jet2Tau31.Fill( valJet2Tau31 )
				jet2MassvsTau21.Fill( getattr( events, 'jet'+grooming+'Mass')[1], valJet2Tau21 )
				jet2Tau32.Fill( valJet2Tau32 )

				########## Leading and Second Leading
				jet1vsjet2Mass.Fill( getattr( events, 'jet'+grooming+'Mass')[0], getattr( events, 'jet'+grooming+'Mass')[1] )
				jet1vsjet2Tau21.Fill( valJet1Tau21, valJet2Tau21 )

				### To calculate the direction of the second jet in the leading jet rest frame
				jet1P4 = TLorentzVector()
				jet2P4 = TLorentzVector()
				jet1P4.SetPtEtaPhiE( getattr( events, 'jet'+grooming+'Pt')[0], getattr( events, 'jet'+grooming+'Eta')[0], getattr( events, 'jet'+grooming+'Phi')[0], getattr( events, 'jet'+grooming+'Energy')[0] ) 
				jet2P4.SetPtEtaPhiE( getattr( events, 'jet'+grooming+'Pt')[1], getattr( events, 'jet'+grooming+'Eta')[1], getattr( events, 'jet'+grooming+'Phi')[1], getattr( events, 'jet'+grooming+'Energy')[1] ) 
				#print 'jet1 Pt', getattr( events, 'jet'+grooming+'Pt')[0], jet1P4.Pt(), jet1P4.Theta()
				#print 'jet2 Pt', getattr( events, 'jet'+grooming+'Pt')[1], jet2P4.Pt(), jet2P4.Theta()
				boost = TVector3()
				boost = jet1P4.BoostVector()
				#boost.SetXYZ( 0, 0, 0 )
				jet2P4.Boost( boost )
				#jet1P4.Boost( boost )
				#jet1P4.RotateY( -jet1P4.Theta() )
				#cosThetaStarjet1 = jet1P4.CosTheta()
				cosThetaStar = jet2P4.CosTheta()
				#print 'jet2 Pt Boosted', getattr( events, 'jet'+grooming+'Pt')[1], jet2P4.Pt(), jet2P4.Theta()
				#print 'jet1 Pt Boosted', getattr( events, 'jet'+grooming+'Pt')[0], jet1P4.Pt(), jet1P4.Theta()
				#jet2CosThetaStar.Fill( cosThetaStarjet1, weight )
				jet2CosThetaStar.Fill( cosThetaStar, weight )
				DeltaEta = abs( jet1P4.Eta() - jet2P4.Eta() )
				tmpCosThetaStar = TMath.TanH( DeltaEta / 2.0  )
				jet1CosThetaStar.Fill( tmpCosThetaStar, weight )


			####### 3rd Leading Jet
			if getattr( events, 'nJets'+grooming ) > 2:
				jet3Pt.Fill( getattr( events, 'jet'+grooming+'Pt')[2], weight )
				jet3Eta.Fill( getattr( events, 'jet'+grooming+'Eta')[2], weight )
				jet3Phi.Fill( getattr( events, 'jet'+grooming+'Phi')[2], weight )
				jet3Mass.Fill( getattr( events, 'jet'+grooming+'Mass')[2], weight )
				jet3Area.Fill( getattr( events, 'jet'+grooming+'Area')[2], weight )
				jet3Tau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[2], weight )
				jet3Tau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[2], weight )
				jet3Tau3.Fill( getattr( events, 'jet'+grooming+'Tau3')[2], weight )
				jet3Tau2vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[2], getattr( events, 'jet'+grooming+'Tau2')[2] )
				jet3Tau3vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[2], getattr( events, 'jet'+grooming+'Tau3')[2] )
				jet3Tau3vsTau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[2], getattr( events, 'jet'+grooming+'Tau3')[2] )
				jet3PtvsMass.Fill( getattr( events, 'jet'+grooming+'Pt')[2], getattr( events, 'jet'+grooming+'Mass')[2] )
				jet3Ptvsht.Fill( getattr( events, 'jet'+grooming+'Pt')[2], HT )
				jet3Massvsht.Fill( getattr( events, 'jet'+grooming+'Mass')[2], HT )
				#jet3Tau21.Fill( getattr( events, 'jet'+grooming+'Tau2')[2] / getattr( events, 'jet'+grooming+'Tau1')[2] )
				#jet3Tau31.Fill( getattr( events, 'jet'+grooming+'Tau3')[2] / getattr( events, 'jet'+grooming+'Tau1')[2] )
				#jet3Tau32.Fill( getattr( events, 'jet'+grooming+'Tau3')[2] / getattr( events, 'jet'+grooming+'Tau2')[2] )

			####### 4th Leading Jet
			if getattr( events, 'nJets'+grooming ) > 3:
				jet4Pt.Fill( getattr( events, 'jet'+grooming+'Pt')[3], weight )
				jet4Eta.Fill( getattr( events, 'jet'+grooming+'Eta')[3], weight )
				jet4Phi.Fill( getattr( events, 'jet'+grooming+'Phi')[3], weight )
				jet4Mass.Fill( getattr( events, 'jet'+grooming+'Mass')[3], weight )
				jet4Area.Fill( getattr( events, 'jet'+grooming+'Area')[3], weight )
				jet4Tau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[3], weight )
				jet4Tau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[3], weight )
				jet4Tau3.Fill( getattr( events, 'jet'+grooming+'Tau3')[3], weight )
				jet4Tau2vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[3], getattr( events, 'jet'+grooming+'Tau2')[3] )
				jet4Tau3vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[3], getattr( events, 'jet'+grooming+'Tau3')[3] )
				jet4Tau3vsTau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[3], getattr( events, 'jet'+grooming+'Tau3')[3] )
				jet4PtvsMass.Fill( getattr( events, 'jet'+grooming+'Pt')[3], getattr( events, 'jet'+grooming+'Mass')[3] )
				jet4Ptvsht.Fill( getattr( events, 'jet'+grooming+'Pt')[3], HT )
				jet4Massvsht.Fill( getattr( events, 'jet'+grooming+'Mass')[3], HT )
				#jet4Tau21.Fill( getattr( events, 'jet'+grooming+'Tau2')[3] / getattr( events, 'jet'+grooming+'Tau1')[3] )
				#jet4Tau31.Fill( getattr( events, 'jet'+grooming+'Tau3')[3] / getattr( events, 'jet'+grooming+'Tau1')[3] )
				#jet4Tau32.Fill( getattr( events, 'jet'+grooming+'Tau3')[3] / getattr( events, 'jet'+grooming+'Tau2')[3] )

			if cut_minTwoJets and cut_jet1pt and cut_HT:

				############  Event Variables
				cut_numberJets.Fill( getattr( events, 'nJets'+grooming ), weight )
				cut_numberPV.Fill( events.nvtx, weight )
				cut_ht.Fill( HT, weight )
				cut_HTvsNPV.Fill( HT, events.nvtx )
				cut_MET.Fill( events.met, weight )

				############ Leading Jet
				cut_jet1Pt.Fill( getattr( events, 'jet'+grooming+'Pt')[0], weight )
				cut_jet1Eta.Fill( getattr( events, 'jet'+grooming+'Eta')[0], weight )
				cut_jet1Phi.Fill( getattr( events, 'jet'+grooming+'Phi')[0], weight )
				cut_jet1Mass.Fill( getattr( events, 'jet'+grooming+'Mass')[0], weight )
				cut_jet1MassOverPt.Fill( ( getattr( events, 'jet'+grooming+'Mass')[0] ) / ( getattr( events, 'jet'+grooming+'Pt')[0] ) , weight )
				cut_jet1Area.Fill( getattr( events, 'jet'+grooming+'Area')[0], weight )
				cut_jet1Tau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[0], weight )
				cut_jet1Tau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[0], weight )
				cut_jet1Tau3.Fill( getattr( events, 'jet'+grooming+'Tau3')[0], weight )
				cut_jet1Tau2vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[0], getattr( events, 'jet'+grooming+'Tau2')[0] )
				cut_jet1Tau3vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[0], getattr( events, 'jet'+grooming+'Tau3')[0] )
				cut_jet1Tau3vsTau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[0], getattr( events, 'jet'+grooming+'Tau3')[0] )
				cut_jet1PtvsMass.Fill( getattr( events, 'jet'+grooming+'Pt')[0], getattr( events, 'jet'+grooming+'Mass')[0] )
				cut_jet1Ptvsht.Fill( getattr( events, 'jet'+grooming+'Pt')[0], HT )
				cut_jet1Massvsht.Fill( getattr( events, 'jet'+grooming+'Mass')[0], HT )
				cut_jet1MassvsMET.Fill( getattr( events, 'jet'+grooming+'Mass')[0], events.met )
				cut_jet1MassvsNPV.Fill( getattr( events, 'jet'+grooming+'Mass')[0], events.nvtx )
				cut_jet1Tau21.Fill( valJet1Tau21 )
				cut_jet1Tau31.Fill( valJet1Tau31 )
				cut_jet1MassvsTau21.Fill( getattr( events, 'jet'+grooming+'Mass')[0], valJet1Tau21 )
				cut_jet1Tau32.Fill( valJet1Tau32 )

				####### 2nd Leading Jet
				cut_jet2Pt.Fill( getattr( events, 'jet'+grooming+'Pt')[1], weight )
				cut_jet2Eta.Fill( getattr( events, 'jet'+grooming+'Eta')[1], weight )
				cut_jet2Phi.Fill( getattr( events, 'jet'+grooming+'Phi')[1], weight )
				cut_jet2Mass.Fill( getattr( events, 'jet'+grooming+'Mass')[1], weight )
				cut_jet2MassOverPt.Fill( ( getattr( events, 'jet'+grooming+'Mass')[1] ) / ( getattr( events, 'jet'+grooming+'Pt')[1] ) , weight )
				cut_jet2Area.Fill( getattr( events, 'jet'+grooming+'Area')[1], weight )
				cut_jet2Tau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[1], weight )
				cut_jet2Tau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[1], weight )
				cut_jet2Tau3.Fill( getattr( events, 'jet'+grooming+'Tau3')[1], weight )
				cut_jet2Tau2vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[1], getattr( events, 'jet'+grooming+'Tau2')[1] )
				cut_jet2Tau3vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[1], getattr( events, 'jet'+grooming+'Tau3')[1] )
				cut_jet2Tau3vsTau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[1], getattr( events, 'jet'+grooming+'Tau3')[1] )
				cut_jet2PtvsMass.Fill( getattr( events, 'jet'+grooming+'Pt')[1], getattr( events, 'jet'+grooming+'Mass')[1] )
				cut_jet2Ptvsht.Fill( getattr( events, 'jet'+grooming+'Pt')[1], HT )
				cut_jet2Massvsht.Fill( getattr( events, 'jet'+grooming+'Mass')[1], HT )
				cut_jet2MassvsMET.Fill( getattr( events, 'jet'+grooming+'Mass')[1], events.met )
				cut_jet2MassvsNPV.Fill( getattr( events, 'jet'+grooming+'Mass')[1], events.nvtx )
				cut_jet2Tau21.Fill( valJet2Tau21 )
				cut_jet2Tau31.Fill( valJet2Tau31 )
				cut_jet2MassvsTau21.Fill( getattr( events, 'jet'+grooming+'Mass')[1], valJet2Tau21 )
				cut_jet2Tau32.Fill( valJet2Tau32 )

				####### Leading and Second Leading
				cut_jet1vsjet2Mass.Fill( getattr( events, 'jet'+grooming+'Mass')[0], getattr( events, 'jet'+grooming+'Mass')[1] )
				cut_jet1vsjet2Tau21.Fill(  valJet1Tau21, valJet2Tau21 )
				cut_jet2CosThetaStar.Fill( cosThetaStar, weight )
				cut_jet1CosThetaStar.Fill( tmpCosThetaStar, weight )

			if cut_TwoJets and cut_jet1pt and cut_HT:

				############  Event Variables
				cut2Jets_numberJets.Fill( getattr( events, 'nJets'+grooming ), weight )
				cut2Jets_numberPV.Fill( events.nvtx, weight )
				cut2Jets_ht.Fill( HT, weight )
				cut2Jets_HTvsNPV.Fill( HT, events.nvtx )
				cut2Jets_MET.Fill( events.met, weight )

				############ Leading Jet
				cut2Jets_jet1Pt.Fill( getattr( events, 'jet'+grooming+'Pt')[0], weight )
				cut2Jets_jet1Eta.Fill( getattr( events, 'jet'+grooming+'Eta')[0], weight )
				cut2Jets_jet1Phi.Fill( getattr( events, 'jet'+grooming+'Phi')[0], weight )
				cut2Jets_jet1Mass.Fill( getattr( events, 'jet'+grooming+'Mass')[0], weight )
				cut2Jets_jet1MassOverPt.Fill( ( getattr( events, 'jet'+grooming+'Mass')[0] ) / ( getattr( events, 'jet'+grooming+'Pt')[0] ) , weight )
				cut2Jets_jet1Area.Fill( getattr( events, 'jet'+grooming+'Area')[0], weight )
				cut2Jets_jet1Tau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[0], weight )
				cut2Jets_jet1Tau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[0], weight )
				cut2Jets_jet1Tau3.Fill( getattr( events, 'jet'+grooming+'Tau3')[0], weight )
				cut2Jets_jet1Tau2vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[0], getattr( events, 'jet'+grooming+'Tau2')[0] )
				cut2Jets_jet1Tau3vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[0], getattr( events, 'jet'+grooming+'Tau3')[0] )
				cut2Jets_jet1Tau3vsTau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[0], getattr( events, 'jet'+grooming+'Tau3')[0] )
				cut2Jets_jet1PtvsMass.Fill( getattr( events, 'jet'+grooming+'Pt')[0], getattr( events, 'jet'+grooming+'Mass')[0] )
				cut2Jets_jet1Ptvsht.Fill( getattr( events, 'jet'+grooming+'Pt')[0], HT )
				cut2Jets_jet1Massvsht.Fill( getattr( events, 'jet'+grooming+'Mass')[0], HT )
				cut2Jets_jet1MassvsMET.Fill( getattr( events, 'jet'+grooming+'Mass')[0], events.met )
				cut2Jets_jet1MassvsNPV.Fill( getattr( events, 'jet'+grooming+'Mass')[0], events.nvtx )
				cut2Jets_jet1Tau21.Fill( valJet1Tau21 )
				cut2Jets_jet1Tau31.Fill( valJet1Tau31 )
				cut2Jets_jet1MassvsTau21.Fill( getattr( events, 'jet'+grooming+'Mass')[0], valJet1Tau21 )
				cut2Jets_jet1Tau32.Fill( valJet1Tau32 )

				####### 2nd Leading Jet
				cut2Jets_jet2Pt.Fill( getattr( events, 'jet'+grooming+'Pt')[1], weight )
				cut2Jets_jet2Eta.Fill( getattr( events, 'jet'+grooming+'Eta')[1], weight )
				cut2Jets_jet2Phi.Fill( getattr( events, 'jet'+grooming+'Phi')[1], weight )
				cut2Jets_jet2Mass.Fill( getattr( events, 'jet'+grooming+'Mass')[1], weight )
				cut2Jets_jet2MassOverPt.Fill( ( getattr( events, 'jet'+grooming+'Mass')[1] ) / ( getattr( events, 'jet'+grooming+'Pt')[1] ) , weight )
				cut2Jets_jet2Area.Fill( getattr( events, 'jet'+grooming+'Area')[1], weight )
				cut2Jets_jet2Tau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[1], weight )
				cut2Jets_jet2Tau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[1], weight )
				cut2Jets_jet2Tau3.Fill( getattr( events, 'jet'+grooming+'Tau3')[1], weight )
				cut2Jets_jet2Tau2vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[1], getattr( events, 'jet'+grooming+'Tau2')[1] )
				cut2Jets_jet2Tau3vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[1], getattr( events, 'jet'+grooming+'Tau3')[1] )
				cut2Jets_jet2Tau3vsTau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[1], getattr( events, 'jet'+grooming+'Tau3')[1] )
				cut2Jets_jet2PtvsMass.Fill( getattr( events, 'jet'+grooming+'Pt')[1], getattr( events, 'jet'+grooming+'Mass')[1] )
				cut2Jets_jet2Ptvsht.Fill( getattr( events, 'jet'+grooming+'Pt')[1], HT )
				cut2Jets_jet2Massvsht.Fill( getattr( events, 'jet'+grooming+'Mass')[1], HT )
				cut2Jets_jet2MassvsMET.Fill( getattr( events, 'jet'+grooming+'Mass')[1], events.met )
				cut2Jets_jet2MassvsNPV.Fill( getattr( events, 'jet'+grooming+'Mass')[1], events.nvtx )
				cut2Jets_jet2Tau21.Fill( valJet2Tau21 )
				cut2Jets_jet2Tau31.Fill( valJet2Tau31 )
				cut2Jets_jet2MassvsTau21.Fill( getattr( events, 'jet'+grooming+'Mass')[1], valJet2Tau21 )
				cut2Jets_jet2Tau32.Fill( valJet2Tau32 )

				####### Leading and Second Leading
				cut2Jets_jet1vsjet2Mass.Fill( getattr( events, 'jet'+grooming+'Mass')[0], getattr( events, 'jet'+grooming+'Mass')[1] )
				cut2Jets_jet1vsjet2Tau21.Fill(  valJet1Tau21, valJet2Tau21 )
				cut2Jets_jet2CosThetaStar.Fill( cosThetaStar, weight )
				cut2Jets_jet1CosThetaStar.Fill( tmpCosThetaStar, weight )

			if cut_minTwoJets and cut_HT:

				############  Event Variables
				cutWO1jetpt_numberJets.Fill( getattr( events, 'nJets'+grooming ), weight )
				cutWO1jetpt_numberPV.Fill( events.nvtx, weight )
				cutWO1jetpt_ht.Fill( HT, weight )
				cutWO1jetpt_HTvsNPV.Fill( HT, events.nvtx )
				cutWO1jetpt_MET.Fill( events.met, weight )

				############ Leading Jet
				cutWO1jetpt_jet1Pt.Fill( getattr( events, 'jet'+grooming+'Pt')[0], weight )
				cutWO1jetpt_jet1Eta.Fill( getattr( events, 'jet'+grooming+'Eta')[0], weight )
				cutWO1jetpt_jet1Phi.Fill( getattr( events, 'jet'+grooming+'Phi')[0], weight )
				cutWO1jetpt_jet1Mass.Fill( getattr( events, 'jet'+grooming+'Mass')[0], weight )
				cutWO1jetpt_jet1MassOverPt.Fill( ( getattr( events, 'jet'+grooming+'Mass')[0] ) / ( getattr( events, 'jet'+grooming+'Pt')[0] ) , weight )
				cutWO1jetpt_jet1Area.Fill( getattr( events, 'jet'+grooming+'Area')[0], weight )
				cutWO1jetpt_jet1Tau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[0], weight )
				cutWO1jetpt_jet1Tau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[0], weight )
				cutWO1jetpt_jet1Tau3.Fill( getattr( events, 'jet'+grooming+'Tau3')[0], weight )
				cutWO1jetpt_jet1Tau2vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[0], getattr( events, 'jet'+grooming+'Tau2')[0] )
				cutWO1jetpt_jet1Tau3vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[0], getattr( events, 'jet'+grooming+'Tau3')[0] )
				cutWO1jetpt_jet1Tau3vsTau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[0], getattr( events, 'jet'+grooming+'Tau3')[0] )
				cutWO1jetpt_jet1PtvsMass.Fill( getattr( events, 'jet'+grooming+'Pt')[0], getattr( events, 'jet'+grooming+'Mass')[0] )
				cutWO1jetpt_jet1Ptvsht.Fill( getattr( events, 'jet'+grooming+'Pt')[0], HT )
				cutWO1jetpt_jet1Massvsht.Fill( getattr( events, 'jet'+grooming+'Mass')[0], HT )
				cutWO1jetpt_jet1MassvsMET.Fill( getattr( events, 'jet'+grooming+'Mass')[0], events.met )
				cutWO1jetpt_jet1MassvsNPV.Fill( getattr( events, 'jet'+grooming+'Mass')[0], events.nvtx )
				cutWO1jetpt_jet1Tau21.Fill( valJet1Tau21 )
				cutWO1jetpt_jet1Tau31.Fill( valJet1Tau31 )
				cutWO1jetpt_jet1MassvsTau21.Fill( getattr( events, 'jet'+grooming+'Mass')[0], valJet1Tau21 )
				cutWO1jetpt_jet1Tau32.Fill( valJet1Tau32 )

				####### 2nd Leading Jet
				cutWO1jetpt_jet2Pt.Fill( getattr( events, 'jet'+grooming+'Pt')[1], weight )
				cutWO1jetpt_jet2Eta.Fill( getattr( events, 'jet'+grooming+'Eta')[1], weight )
				cutWO1jetpt_jet2Phi.Fill( getattr( events, 'jet'+grooming+'Phi')[1], weight )
				cutWO1jetpt_jet2Mass.Fill( getattr( events, 'jet'+grooming+'Mass')[1], weight )
				cutWO1jetpt_jet2MassOverPt.Fill( ( getattr( events, 'jet'+grooming+'Mass')[1] ) / ( getattr( events, 'jet'+grooming+'Pt')[1] ) , weight )
				cutWO1jetpt_jet2Area.Fill( getattr( events, 'jet'+grooming+'Area')[1], weight )
				cutWO1jetpt_jet2Tau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[1], weight )
				cutWO1jetpt_jet2Tau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[1], weight )
				cutWO1jetpt_jet2Tau3.Fill( getattr( events, 'jet'+grooming+'Tau3')[1], weight )
				cutWO1jetpt_jet2Tau2vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[1], getattr( events, 'jet'+grooming+'Tau2')[1] )
				cutWO1jetpt_jet2Tau3vsTau1.Fill( getattr( events, 'jet'+grooming+'Tau1')[1], getattr( events, 'jet'+grooming+'Tau3')[1] )
				cutWO1jetpt_jet2Tau3vsTau2.Fill( getattr( events, 'jet'+grooming+'Tau2')[1], getattr( events, 'jet'+grooming+'Tau3')[1] )
				cutWO1jetpt_jet2PtvsMass.Fill( getattr( events, 'jet'+grooming+'Pt')[1], getattr( events, 'jet'+grooming+'Mass')[1] )
				cutWO1jetpt_jet2Ptvsht.Fill( getattr( events, 'jet'+grooming+'Pt')[1], HT )
				cutWO1jetpt_jet2Massvsht.Fill( getattr( events, 'jet'+grooming+'Mass')[1], HT )
				cutWO1jetpt_jet2MassvsMET.Fill( getattr( events, 'jet'+grooming+'Mass')[1], events.met )
				cutWO1jetpt_jet2MassvsNPV.Fill( getattr( events, 'jet'+grooming+'Mass')[1], events.nvtx )
				cutWO1jetpt_jet2Tau21.Fill( valJet2Tau21 )
				cutWO1jetpt_jet2Tau31.Fill( valJet2Tau31 )
				cutWO1jetpt_jet2MassvsTau21.Fill( getattr( events, 'jet'+grooming+'Mass')[1], valJet2Tau21 )
				cutWO1jetpt_jet2Tau32.Fill( valJet2Tau32 )

				####### Leading and Second Leading
				cutWO1jetpt_jet1vsjet2Mass.Fill( getattr( events, 'jet'+grooming+'Mass')[0], getattr( events, 'jet'+grooming+'Mass')[1] )
				cutWO1jetpt_jet1vsjet2Tau21.Fill(  valJet1Tau21, valJet2Tau21 )
				cutWO1jetpt_jet2CosThetaStar.Fill( cosThetaStar, weight )
				cutWO1jetpt_jet1CosThetaStar.Fill( tmpCosThetaStar, weight )

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

	if 'QCD' in samples: 
		sample = 'QCD_HT-'+QCD
		if FNAL:
			#list = os.popen('ls -1 /eos/uscms/store/user/algomez/'+sample+'_8TeV_Summer12_DR53X-PU_S10_START53_V7A-v1/*.root').read().splitlines()
			tmpList = os.popen('ls -1v /eos/uscms/store/user/algomez/'+sample+'_8TeV_Summer12_DR53X-PU_S10_START53_V7A-v1/*.root').read().splitlines()
			#outputDir = '/eos/uscms/store/user/algomez/QCD_8TeV/treeResults/'
			outputDir = '/store/user/algomez/QCD_8TeV/treeResults/'
		else:
			tmpList = os.popen('ls -1v /cms/gomez/Files/QCD_8TeV/PATtuples/'+sample+'_8TeV_Summer12_DR53X-PU_S10_START53_V7A-v1/*.root').read().splitlines()
			outputDir = '/cms/gomez/Files/QCD_8TeV/treeResults/'
		filesPerJob = round(len(tmpList)/30)+1
		iniList = int(filesPerJob*Job)
		finList = int((filesPerJob*(Job+1))-1)
		print filesPerJob, iniList, finList
		list = tmpList[iniList:finList]
		#list = tmpList[0:2]
		inputList = [i if i.startswith('file') else 'file:' + i for i in list]
		if '250To500' in QCD: weight = 19500*276000/27062078.0
		elif '500To1000' in QCD: weight = 19500*8426/30599292.0
		else: weight = 19500*204/13843863.0
	elif 'Signal' in samples: 
		sample = 'RPVSt'+str(mass)+'tojj_8TeV_HT500_'+str(Job)
		if FNAL:
			list = os.popen('ls -1v /eos/uscms/store/user/algomez/RPVSt100tojj_8TeV_HT500/'+sample+'/PATtuples/*.root').read().splitlines()
			outputDir = '/eos/uscms/store/user/algomez/RPVSt100tojj_8TeV_HT500/'+sample+'/treeResults/'
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
		elif mass == 100: weight = 19500*559.757/555880845.74
		elif mass == 200: weight = 19500*18.5245/100000.0
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

	if not final : myAnalyzer( inputList[:10], outputDir, sample, couts, final, jetAlgo, grooming, weight, Job, FNAL )
	else: myAnalyzer( inputList, outputDir, sample, couts, final, jetAlgo, grooming, weight, Job, FNAL )

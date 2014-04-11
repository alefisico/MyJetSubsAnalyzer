#!/usr/bin/env python

'''
File: MyAnalyzer.py --mass 50 (optional) --debug -- final --jetAlgo AK5
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: 
'''

import sys,os,time
from math import pi
import optparse
from collections import defaultdict
from ROOT import *
from DataFormats.FWLite import Events, Handle

gROOT.SetBatch()

###### Trick for add date or month to plots
dateKey   = time.strftime("%y%m%d%H%M")
monthKey   = time.strftime("%y%m%d")

######################################
def myAnalyzer( infile, outputDir, sample, couts, final, jetAlgo, grooming ):

	if not final: 
		outputFile = TFile( outputDir + sample + '_'+jetAlgo+'_'+grooming+'_Plots_'+dateKey+'.root', 'RECREATE' )
	else:
		if not ( os.path.exists( outputDir + 'rootFiles/' + monthKey ) ): os.makedirs( outputDir + 'rootFiles/' + monthKey )
		outputFile = TFile( outputDir + 'rootFiles/' + monthKey + '/' + sample + '_'+jetAlgo+'_'+grooming+'_Plots.root', 'RECREATE' )

	######## Extra, send print to file
	#if couts == False :
	#	outfileStdOut = sys.stdout
	#	f = file('tmp_'+sample+'_'+jetAlgo+'_'+dateKey+'.txt', 'w')
	#	sys.stdout = f
	#################################################

	####################################################################################################################################### Histograms
	nBinsDeltaR = 50
	maxDeltaR = 5. 
	maxMass = 300
	maxPt = 500
	nBinsMass = 60  #int(round( maxMass/5 ))
	nBinsPt = 100  #int(round( maxPt/5 ))
	nBinsEta = 41
	maxEta = 4.1
	nBinsTau = 40
	maxTau = 1.

	################################################################################################### Event Variables
	ht 		= TH1F('h_ht_'+jetAlgo+'_'+grooming, 	'h_ht_'+jetAlgo, 	60,  	0, 	600.)
	numberPV 	= TH1F('h_numberPV_'+jetAlgo+'_'+grooming, 	'h_numberPV_'+jetAlgo, 	50,  	0., 	50.)
	MET 		= TH1F('h_MET_'+jetAlgo+'_'+grooming, 	'h_MET_'+jetAlgo, 	24,  	0, 	120.)
	numberJets 	= TH1F('h_numberJets_'+jetAlgo+'_'+grooming, 'h_numberJets_'+jetAlgo, 15,  0., 15.)
	jetPt	 	= TH1F('h_jetPt_'+jetAlgo+'_'+grooming, 'h_jetPt_'+jetAlgo, nBinsPt,  0., maxPt)
	jetEta	 	= TH1F('h_jetEta_'+jetAlgo+'_'+grooming, 'h_jetEta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jetPhi	 	= TH1F('h_jetPhi_'+jetAlgo+'_'+grooming, 'h_jetPhi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jetMass	 	= TH1F('h_jetMass_'+jetAlgo+'_'+grooming, 'h_jetMass_'+jetAlgo, nBinsMass,  0., maxMass)
	jetPtvsMass	= TH2F('h_jetPtvsMass_'+jetAlgo+'_'+grooming, 'h_jetPtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	jetArea 	= TH1F('h_jetArea_'+jetAlgo+'_'+grooming, 'h_jetArea_'+jetAlgo, 40,  0., pi/2)
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
	jet1Area 	= TH1F('h_jet1Area_'+jetAlgo+'_'+grooming, 'h_jet1Area_'+jetAlgo, 40,  0., pi/2)
	jet1Tau1 	= TH1F('h_jet1Tau1_'+jetAlgo+'_'+grooming, 'h_jet1Tau1_'+jetAlgo, nBinsTau,  0., maxTau)
	jet1Tau2 	= TH1F('h_jet1Tau2_'+jetAlgo+'_'+grooming, 'h_jet1Tau2_'+jetAlgo, nBinsTau,  0., maxTau)
	jet1Tau3 	= TH1F('h_jet1Tau3_'+jetAlgo+'_'+grooming, 'h_jet1Tau3_'+jetAlgo, nBinsTau,  0., maxTau)
	jet1Tau21 	= TH1F('h_jet1Tau21_'+jetAlgo+'_'+grooming, 'h_jet1Tau21_'+jetAlgo, nBinsTau,  0., maxTau)
	jet1Tau31 	= TH1F('h_jet1Tau31_'+jetAlgo+'_'+grooming, 'h_jet1Tau31_'+jetAlgo, nBinsTau,  0., maxTau)
	jet1Tau32 	= TH1F('h_jet1Tau32_'+jetAlgo+'_'+grooming, 'h_jet1Tau32_'+jetAlgo, nBinsTau,  0., maxTau)
	jet1Tau2vsTau1 	= TH2F('h_jet1Tau2vsTau1_'+jetAlgo+'_'+grooming, 'h_jet1Tau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet1Tau3vsTau1 	= TH2F('h_jet1Tau3vsTau1_'+jetAlgo+'_'+grooming, 'h_jet1Tau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet1Tau3vsTau2 	= TH2F('h_jet1Tau3vsTau2_'+jetAlgo+'_'+grooming, 'h_jet1Tau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)

	############################################################ 2nd Leading Jet 
	jet2Pt	 	= TH1F('h_jet2Pt_'+jetAlgo+'_'+grooming, 'h_jet2Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	jet2Mass 	= TH1F('h_jet2Mass_'+jetAlgo+'_'+grooming, 'h_jet2Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	jet2Eta	 	= TH1F('h_jet2Eta_'+jetAlgo+'_'+grooming, 'h_jet2Eta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jet2Phi	 	= TH1F('h_jet2Phi_'+jetAlgo+'_'+grooming, 'h_jet2Phi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jet2PtvsMass	= TH2F('h_jet2PtvsMass_'+jetAlgo+'_'+grooming, 'h_jet2PtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	jet2Area 	= TH1F('h_jet2Area_'+jetAlgo+'_'+grooming, 'h_jet2Area_'+jetAlgo, 40,  0., pi/2)
	jet2Tau1 	= TH1F('h_jet2Tau1_'+jetAlgo+'_'+grooming, 'h_jet2Tau1_'+jetAlgo, nBinsTau,  0., maxTau)
	jet2Tau2 	= TH1F('h_jet2Tau2_'+jetAlgo+'_'+grooming, 'h_jet2Tau2_'+jetAlgo, nBinsTau,  0., maxTau)
	jet2Tau3 	= TH1F('h_jet2Tau3_'+jetAlgo+'_'+grooming, 'h_jet2Tau3_'+jetAlgo, nBinsTau,  0., maxTau)
	jet2Tau21 	= TH1F('h_jet2Tau21_'+jetAlgo+'_'+grooming, 'h_jet2Tau21_'+jetAlgo, nBinsTau,  0., maxTau)
	jet2Tau31 	= TH1F('h_jet2Tau31_'+jetAlgo+'_'+grooming, 'h_jet2Tau31_'+jetAlgo, nBinsTau,  0., maxTau)
	jet2Tau32 	= TH1F('h_jet2Tau32_'+jetAlgo+'_'+grooming, 'h_jet2Tau32_'+jetAlgo, nBinsTau,  0., maxTau)
	jet2Tau2vsTau1 	= TH2F('h_jet2Tau2vsTau1_'+jetAlgo+'_'+grooming, 'h_jet2Tau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet2Tau3vsTau1 	= TH2F('h_jet2Tau3vsTau1_'+jetAlgo+'_'+grooming, 'h_jet2Tau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet2Tau3vsTau2 	= TH2F('h_jet2Tau3vsTau2_'+jetAlgo+'_'+grooming, 'h_jet2Tau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)

	############################################################ 3rd Leading Jet 
	jet3Pt	 	= TH1F('h_jet3Pt_'+jetAlgo+'_'+grooming, 'h_jet3Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	jet3Mass 	= TH1F('h_jet3Mass_'+jetAlgo+'_'+grooming, 'h_jet3Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	jet3Eta	 	= TH1F('h_jet3Eta_'+jetAlgo+'_'+grooming, 'h_jet3Eta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jet3Phi	 	= TH1F('h_jet3Phi_'+jetAlgo+'_'+grooming, 'h_jet3Phi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jet3PtvsMass	= TH2F('h_jet3PtvsMass_'+jetAlgo+'_'+grooming, 'h_jet3PtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	jet3Area 	= TH1F('h_jet3Area_'+jetAlgo+'_'+grooming, 'h_jet3Area_'+jetAlgo, 40,  0., pi/2)
	jet3Tau1 	= TH1F('h_jet3Tau1_'+jetAlgo+'_'+grooming, 'h_jet3Tau1_'+jetAlgo, nBinsTau,  0., maxTau)
	jet3Tau2 	= TH1F('h_jet3Tau2_'+jetAlgo+'_'+grooming, 'h_jet3Tau2_'+jetAlgo, nBinsTau,  0., maxTau)
	jet3Tau3 	= TH1F('h_jet3Tau3_'+jetAlgo+'_'+grooming, 'h_jet3Tau3_'+jetAlgo, nBinsTau,  0., maxTau)
	jet3Tau21 	= TH1F('h_jet3Tau21_'+jetAlgo+'_'+grooming, 'h_jet3Tau21_'+jetAlgo, nBinsTau,  0., maxTau)
	jet3Tau31 	= TH1F('h_jet3Tau31_'+jetAlgo+'_'+grooming, 'h_jet3Tau31_'+jetAlgo, nBinsTau,  0., maxTau)
	jet3Tau32 	= TH1F('h_jet3Tau32_'+jetAlgo+'_'+grooming, 'h_jet3Tau32_'+jetAlgo, nBinsTau,  0., maxTau)
	jet3Tau2vsTau1 	= TH2F('h_jet3Tau2vsTau1_'+jetAlgo+'_'+grooming, 'h_jet3Tau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet3Tau3vsTau1 	= TH2F('h_jet3Tau3vsTau1_'+jetAlgo+'_'+grooming, 'h_jet3Tau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet3Tau3vsTau2 	= TH2F('h_jet3Tau3vsTau2_'+jetAlgo+'_'+grooming, 'h_jet3Tau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)

	############################################################ 4th Leading Jet 
	jet4Pt	 	= TH1F('h_jet4Pt_'+jetAlgo+'_'+grooming, 'h_jet4Pt_'+jetAlgo, nBinsPt,  0., maxPt)
	jet4Mass 	= TH1F('h_jet4Mass_'+jetAlgo+'_'+grooming, 'h_jet4Mass_'+jetAlgo, nBinsMass,  0., maxMass)
	jet4Eta	 	= TH1F('h_jet4Eta_'+jetAlgo+'_'+grooming, 'h_jet4Eta_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jet4Phi	 	= TH1F('h_jet4Phi_'+jetAlgo+'_'+grooming, 'h_jet4Phi_'+jetAlgo, nBinsEta,  -maxEta, maxEta)
	jet4PtvsMass	= TH2F('h_jet4PtvsMass_'+jetAlgo+'_'+grooming, 'h_jet4PtvsMass_'+jetAlgo, nBinsPt,  0., maxPt, nBinsMass,  0., maxMass)
	jet4Area 	= TH1F('h_jet4Area_'+jetAlgo+'_'+grooming, 'h_jet4Area_'+jetAlgo, 40,  0., pi/2)
	jet4Tau1 	= TH1F('h_jet4Tau1_'+jetAlgo+'_'+grooming, 'h_jet4Tau1_'+jetAlgo, nBinsTau,  0., maxTau)
	jet4Tau2 	= TH1F('h_jet4Tau2_'+jetAlgo+'_'+grooming, 'h_jet4Tau2_'+jetAlgo, nBinsTau,  0., maxTau)
	jet4Tau3 	= TH1F('h_jet4Tau3_'+jetAlgo+'_'+grooming, 'h_jet4Tau3_'+jetAlgo, nBinsTau,  0., maxTau)
	jet4Tau21 	= TH1F('h_jet4Tau21_'+jetAlgo+'_'+grooming, 'h_jet4Tau21_'+jetAlgo, nBinsTau,  0., maxTau)
	jet4Tau31 	= TH1F('h_jet4Tau31_'+jetAlgo+'_'+grooming, 'h_jet4Tau31_'+jetAlgo, nBinsTau,  0., maxTau)
	jet4Tau32 	= TH1F('h_jet4Tau32_'+jetAlgo+'_'+grooming, 'h_jet4Tau32_'+jetAlgo, nBinsTau,  0., maxTau)
	jet4Tau2vsTau1 	= TH2F('h_jet4Tau2vsTau1_'+jetAlgo+'_'+grooming, 'h_jet4Tau2vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet4Tau3vsTau1 	= TH2F('h_jet4Tau3vsTau1_'+jetAlgo+'_'+grooming, 'h_jet4Tau3vsTau1_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)
	jet4Tau3vsTau2 	= TH2F('h_jet4Tau3vsTau2_'+jetAlgo+'_'+grooming, 'h_jet4Tau3vsTau2_'+jetAlgo, nBinsTau,  0., maxTau, nBinsTau,  0., maxTau)


	#####################################################################################################################################

	###################################### Get GenTree 
	events = TChain( 'PFJet_'+jetAlgo+grooming+'/events' )

	# Loop over the filenames and add to tree.
	for filename in infile:
		print("Adding file: " + filename)
		events.Add(filename)

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

		###################################################################### Store Jet Info
		listP4Jets = []
		HT = 0
		for j in range( events.nJets ):
			tau1 = -999
			tau2 = -999
			tau3 = -999
			if ( events.jetPt[j] > 30 ) and ( abs( events.jetEta[j] ) < 2.5 ):
					tmpP4 = TLorentzVector()
					tmpP4.SetPtEtaPhiE( events.jetPt[j], events.jetEta[j], events.jetPhi[j], events.jetEnergy[j] )
					if not events.jetTau1[j] == 0: tau1 = events.jetTau1[j]
					if not events.jetTau2[j] == 0: tau2 = events.jetTau2[j]
					if not events.jetTau3[j] == 0: tau3 = events.jetTau3[j]
					tmpListP4Jets = [ tmpP4, tau1, tau2, tau3, events.jetArea[j] ]
					listP4Jets.append( tmpListP4Jets )
		if couts: 
			for i in range( len( listP4Jets ) ): print i, listP4Jets[i][0].Pt()

		if ( len( listP4Jets ) > 1 ):
			for k in range( len( listP4Jets ) ):
				HT += listP4Jets[k][0].Pt()
				jetPt.Fill( listP4Jets[k][0].Pt() )
				jetEta.Fill( listP4Jets[k][0].Eta() )
				jetPhi.Fill( listP4Jets[k][0].Phi() )
				jetMass.Fill( listP4Jets[k][0].M() )
				jetPtvsMass.Fill( listP4Jets[k][0].Pt(), listP4Jets[k][0].M() )
				jetArea.Fill( listP4Jets[k][4] )
				jetTau1.Fill( listP4Jets[k][1] ) 
				jetTau2.Fill( listP4Jets[k][2] ) 
				jetTau3.Fill( listP4Jets[k][3] ) 
				jetTau21.Fill( listP4Jets[k][2] / listP4Jets[k][1] ) 
				jetTau31.Fill( listP4Jets[k][3] / listP4Jets[k][1] ) 
				jetTau32.Fill( listP4Jets[k][3] / listP4Jets[k][2] ) 
				jetTau2vsTau1.Fill( listP4Jets[k][1], listP4Jets[k][2] )  
				jetTau3vsTau1.Fill( listP4Jets[k][1], listP4Jets[k][3] )
				jetTau3vsTau2.Fill( listP4Jets[k][2], listP4Jets[k][3] ) 

			numberJets.Fill( len( listP4Jets ) )
			ht.Fill( HT )
			numberPV.Fill( events.nvtx )
			MET.Fill( events.met )
		###########################################################################################

		####### Leading Jet
		if len( listP4Jets ) > 0 :
			jet1Pt.Fill( listP4Jets[0][0].Pt() )
			jet1Eta.Fill( listP4Jets[0][0].Eta() )
			jet1Phi.Fill( listP4Jets[0][0].Phi() )
			jet1Mass.Fill( listP4Jets[0][0].M() )
			jet1PtvsMass.Fill( listP4Jets[0][0].Pt(), listP4Jets[0][0].M() )
			jet1Area.Fill( listP4Jets[0][4] )
			jet1Tau1.Fill( listP4Jets[0][1] )
			jet1Tau2.Fill( listP4Jets[0][2] )
			jet1Tau3.Fill( listP4Jets[0][3] )
			jet1Tau21.Fill( listP4Jets[0][2] / listP4Jets[0][1] )
			jet1Tau31.Fill( listP4Jets[0][3] / listP4Jets[0][1] )
			jet1Tau32.Fill( listP4Jets[0][3] / listP4Jets[0][2] )
			jet1Tau2vsTau1.Fill( listP4Jets[0][1], listP4Jets[0][2] )
			jet1Tau3vsTau1.Fill( listP4Jets[0][1], listP4Jets[0][3] )
			jet1Tau3vsTau2.Fill( listP4Jets[0][2], listP4Jets[0][3] )

		####### 2nd Leading Jet
		if len( listP4Jets ) > 1 :
			jet2Pt.Fill( listP4Jets[1][0].Pt() )
			jet2Eta.Fill( listP4Jets[1][0].Eta() )
			jet2Phi.Fill( listP4Jets[1][0].Phi() )
			jet2Mass.Fill( listP4Jets[1][0].M() )
			jet2PtvsMass.Fill( listP4Jets[1][0].Pt(), listP4Jets[1][0].M() )
			jet2Area.Fill( listP4Jets[1][4] )
			jet2Tau1.Fill( listP4Jets[1][1] )
			jet2Tau2.Fill( listP4Jets[1][2] )
			jet2Tau3.Fill( listP4Jets[1][3] )
			jet2Tau21.Fill( listP4Jets[1][2] / listP4Jets[1][1] )
			jet2Tau31.Fill( listP4Jets[1][3] / listP4Jets[1][1] )
			jet2Tau32.Fill( listP4Jets[1][3] / listP4Jets[1][2] )
			jet2Tau2vsTau1.Fill( listP4Jets[1][1], listP4Jets[1][2] )
			jet2Tau3vsTau1.Fill( listP4Jets[1][1], listP4Jets[1][3] )
			jet2Tau3vsTau2.Fill( listP4Jets[1][2], listP4Jets[1][3] )

		####### 3rd Leading Jet
		if len( listP4Jets ) > 2 :
			jet3Pt.Fill( listP4Jets[2][0].Pt() )
			jet3Eta.Fill( listP4Jets[2][0].Eta() )
			jet3Phi.Fill( listP4Jets[2][0].Phi() )
			jet3Mass.Fill( listP4Jets[2][0].M() )
			jet3PtvsMass.Fill( listP4Jets[2][0].Pt(), listP4Jets[2][0].M() )
			jet3Area.Fill( listP4Jets[2][4] )
			jet3Tau1.Fill( listP4Jets[2][1] )
			jet3Tau2.Fill( listP4Jets[2][2] )
			jet3Tau3.Fill( listP4Jets[2][3] )
			jet3Tau21.Fill( listP4Jets[2][2] / listP4Jets[2][1] )
			jet3Tau31.Fill( listP4Jets[2][3] / listP4Jets[2][1] )
			jet3Tau32.Fill( listP4Jets[2][3] / listP4Jets[2][2] )
			jet3Tau2vsTau1.Fill( listP4Jets[2][1], listP4Jets[2][2] )
			jet3Tau3vsTau1.Fill( listP4Jets[2][1], listP4Jets[2][3] )
			jet3Tau3vsTau2.Fill( listP4Jets[2][2], listP4Jets[2][3] )

		####### 4th Leading Jet
		if len( listP4Jets ) > 3 :
			jet1Pt.Fill( listP4Jets[3][0].Pt() )
			jet1Eta.Fill( listP4Jets[3][0].Eta() )
			jet1Phi.Fill( listP4Jets[3][0].Phi() )
			jet1Mass.Fill( listP4Jets[3][0].M() )
			jet1PtvsMass.Fill( listP4Jets[3][0].Pt(), listP4Jets[3][0].M() )
			jet1Area.Fill( listP4Jets[3][4] )
			jet1Tau1.Fill( listP4Jets[3][1] )
			jet1Tau2.Fill( listP4Jets[3][2] )
			jet1Tau3.Fill( listP4Jets[3][3] )
			jet1Tau21.Fill( listP4Jets[3][2] / listP4Jets[3][1] )
			jet1Tau31.Fill( listP4Jets[3][3] / listP4Jets[3][1] )
			jet1Tau32.Fill( listP4Jets[3][3] / listP4Jets[3][2] )
			jet1Tau2vsTau1.Fill( listP4Jets[3][1], listP4Jets[3][2] )
			jet1Tau3vsTau1.Fill( listP4Jets[3][1], listP4Jets[3][3] )
			jet1Tau3vsTau2.Fill( listP4Jets[3][2], listP4Jets[3][3] )


	################################################################################################## end event loop

	##### write output file 
	outputFile.cd()
	outputFile.Write()

	##### Closing
	print 'Writing output file: '+ outputDir + sample + '_'+jetAlgo+'_'+grooming+'_Plots_'+dateKey+'.root'
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
	parser.add_option( '-q', '--qcd', action='store_true', dest='QCD', default=False, help='If True, QCD' )

	(options, args) = parser.parse_args()

	mass = options.mass
	couts = options.couts
	final = options.final
	jetAlgo = options.jetAlgo
	grooming = options.grooming
	QCD = options.QCD

	if QCD : 
		sample = 'QCD'
		list = os.popen('ls -1 /cms/gomez/Stops/st_jj/patTuples/'+sample+'/results/140410/*.root').read().splitlines()
	else: 
		sample = 'stopUDD312_'+str(mass)
		#list = os.popen('ls -1 /cms/gomez/Substructure/Generation/Simulation/CMSSW_5_3_2_patch4/src/mySimulations/stop_UDD312_50/aodsim/*.root').read().splitlines()
		list = os.popen('ls -1 /cms/gomez/Stops/st_jj/patTuples/'+sample+'/results/140402/*.root').read().splitlines()
		#list = [ '/cms/gomez/Stops/st_jj/patTuples/stopUDD312_50_tree_test_grom.root' ]
	inputList = [i if i.startswith('file') else 'file:' + i for i in list]

	outputDir = '/cms/gomez/Stops/st_jj/treeResults/'

	if not final : myAnalyzer( inputList[:2], outputDir, sample, couts, final, jetAlgo, grooming )
	else: myAnalyzer( inputList, outputDir, sample, couts, final, jetAlgo, grooming )

#!/usr/bin/env python

'''
File: myMCTruthJetsMatching.py --mass 50 (optional) --debug -- final
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: Read genParticles and AK5PFJets info, Matching and count number of events in different categories.
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
def get_info( infile, outputDir, sample, mass, couts, final ):

	if not final: 
		outputFile = TFile( outputDir + sample + '_Matching_Plots_'+dateKey+'.root', 'RECREATE' )
	else:
		if not ( os.path.exists( outputDir + 'rootFiles/' + monthKey ) ): os.makedirs( outputDir + 'rootFiles/' + monthKey )
		outputFile = TFile( outputDir + 'rootFiles/' + monthKey + '/' + sample + '_Matching_Plots.root', 'RECREATE' )

	######## Extra, send print to file
	if couts == False :
		outfileStdOut = sys.stdout
		f = file('tmp_'+sample+'_'+dateKey+'.txt', 'w')
		sys.stdout = f
	#################################################

	######### Histograms
	nBinsDeltaR = 50
	maxDeltaR = 5. 
	maxMass = float(mass)*3. 
	nBinsMass = int(round( maxMass/5 ))

	numberJets 	= TH1F('h_numberJets', 'h_numberJets', 20,  0., 20.)
	numberPartons 	= TH1F('h_numberPartons', 'h_numberPartons', 6,  0., 6.)

	numberPartonsSameJet 		= TH1F('h_numberPartonsSameJet',	'h_numberPartonsSameJet',	8,   		0.,	8. )
	minDeltaRPartonJet 		= TH1F('h_minDeltaRPartonJet',		'h_minDeltaRPartonJet',		nBinsDeltaR, 	0.,	maxDeltaR )
	secMinDeltaRPartonJet		= TH1F('h_secMinDeltaRPartonJet', 	'h_secMinDeltaRPartonJet',	nBinsDeltaR, 	0.,	maxDeltaR )
	minvsSecMinDeltaRPartonJet 	= TH2F('h_minDeltaRvsSecMinDeltaR',	'h_minDeltaRvsSecMinDeltaR',nBinsDeltaR,0.,maxDeltaR, nBinsDeltaR, 0., maxDeltaR )

	numberPartonsWithDeltaR0p4_4Matched = TH1F('h_numberPartonsWithDeltaR0p4_4Matched', 'h_numberPartonsWithDeltaR0p4_4Matched',	8,  0.,	8. )
	minDeltaRPartonJet_4Matched 	= TH1F('h_minDeltaRPartonJet_4Matched', 	'h_minDeltaRPartonJet_4Matched',	nBinsDeltaR, 	0.,	maxDeltaR )
	minDeltaRPartonJet_4Matched_0 	= TH1F('h_minDeltaRPartonJet_4Matched_0', 	'h_minDeltaRPartonJet_4Matched_0',	nBinsDeltaR, 	0.,	maxDeltaR )
	minDeltaRPartonJet_4Matched_1 	= TH1F('h_minDeltaRPartonJet_4Matched_1', 	'h_minDeltaRPartonJet_4Matched_1',	nBinsDeltaR, 	0.,	maxDeltaR )
	minDeltaRPartonJet_4Matched_2 	= TH1F('h_minDeltaRPartonJet_4Matched_2', 	'h_minDeltaRPartonJet_4Matched_2',	nBinsDeltaR, 	0.,	maxDeltaR )
	minDeltaRPartonJet_4Matched_3 	= TH1F('h_minDeltaRPartonJet_4Matched_3', 	'h_minDeltaRPartonJet_4Matched_3',	nBinsDeltaR, 	0.,	maxDeltaR )
	invMass_4Matched 			= TH1F('h_invMass_4Matched', 		'h_invMass_4Matched', 		nBinsMass, 	0., 	maxMass )

	minDeltaRPartonJet_2Merged2Matched_Merged 	= TH1F('h_minDeltaRPartonJet_2Merged2Matched_Merged', 		'h_minDeltaRPartonJet_2Merged2Matched_Merged'		,nBinsDeltaR, 	0., 	maxDeltaR )
	secMinDeltaRPartonJet_2Merged2Matched_Merged 	= TH1F('h_secMinDeltaRPartonJet_2Merged2Matched_Merged',	'h_secMinDeltaRPartonJet_2Merged2Matched_Merged'	,nBinsDeltaR, 	0., 	maxDeltaR )
	minDeltaRPartonJet_2Merged2Matched_NOMerged 	= TH1F('h_minDeltaRPartonJet_2Merged2Matched_NOMerged', 		'h_minDeltaRPartonJet_2Merged2Matched_NOMerged'		,nBinsDeltaR, 	0., 	maxDeltaR )
	secMinDeltaRPartonJet_2Merged2Matched_NOMerged 	= TH1F('h_secMinDeltaRPartonJet_2Merged2Matched_NOMerged',	'h_secMinDeltaRPartonJet_2Merged2Matched_NOMerged'	,nBinsDeltaR, 	0., 	maxDeltaR )
	minvsSecMinDeltaRPartonJet_2Merged2Matched_Merged 	= TH2F('h_minvsSecMinDeltaRPartonJet_2Merged2Matched_Merged',	'h_minvsSecMinDeltaRPartonJet_2Merged2Matched_Merged', 	nBinsDeltaR, 	0., 	maxDeltaR, 	nBinsDeltaR, 	0., 	maxDeltaR )
	minvsSecMinDeltaRPartonJet_2Merged2Matched_NOMerged 	= TH2F('h_minvsSecMinDeltaRPartonJet_2Merged2Matched_NOMerged',	'h_minvsSecMinDeltaRPartonJet_2Merged2Matched_NOMerged', 	nBinsDeltaR, 	0., 	maxDeltaR, 	nBinsDeltaR, 	0., 	maxDeltaR )
	invMass_2Merged2Matched_NOMerged 	= TH1F('h_invMass_2Merged2Matched_NOMerged', 	'h_invMass_2Merged2Matched_NOMerged', 	nBinsMass, 	0., 	maxMass )
	invMass_2Merged2Matched_Merged 		= TH1F('h_invMass_2Merged2Matched_Merged', 	'h_invMass_2Merged2Matched_Merged', 	nBinsMass, 	0., 	maxMass )

	minDeltaRPartonJet_Pair2Merged 		= TH1F('h_minDeltaRPartonJet_Pair2Merged', 'h_minDeltaRPartonJet_Pair2Merged', nBinsDeltaR, 0., maxDeltaR )
	secMinDeltaRPartonJet_Pair2Merged 	= TH1F('h_secMinDeltaRPartonJet_Pair2Merged','h_secMinDeltaRPartonJet_Pair2Merged', nBinsDeltaR, 0., maxDeltaR )
	minvsSecMinDeltaRPartonJet_Pair2Merged 	= TH2F('h_minvsSecMinDeltaRPartonJet_Pair2Merged','h_minvsSecMinDeltaRPartonJet_Pair2Merged', nBinsDeltaR, 0., 	maxDeltaR, nBinsDeltaR, 0., maxDeltaR )
	invMass_Pair2Merged_Merged 		= TH1F('h_invMass_Pair2Merged_Merged', 	'h_invMass_Pair2Merged_Merged', 	nBinsMass, 0., 	maxMass )

	minDeltaRPartonJet_3Merged1Match 		= TH1F('h_minDeltaRPartonJet_3Merged1Match', 	'h_minDeltaRPartonJet_3Merged1Match',	nBinsDeltaR, 0., maxDeltaR)
	secMinDeltaRPartonJet_3Merged1Match 		= TH1F('h_secMinDeltaRPartonJet_3Merged1Match','h_secMinDeltaRPartonJet_3Merged1Match', nBinsDeltaR, 0., maxDeltaR)
	minvsSecMinDeltaRPartonJet_3Merged1Match 	= TH2F('h_minvsSecMinDeltaRPartonJet_3Merged1Match','h_minvsSecMinDeltaRPartonJet_3Merged1Match', nBinsDeltaR, 0., maxDeltaR, nBinsDeltaR, 0., maxDeltaR )
	invMass_3Merged1Match_Merged 			= TH1F('h_invMass_3Merged1Match_Merged', 	'h_invMass_3Merged1Match_Merged', 	nBinsMass, 0., 	maxMass )

	minDeltaRPartonJet_4Merged = TH1F('h_minDeltaRPartonJet_4Merged', 'h_minDeltaRPartonJet_4Merged',	nBinsDeltaR, 0., maxDeltaR)

	#### with DeltaR0p4
	nBinsDeltaR0p4 = 20
	maxDeltaR0p4 = 1.
	numberPartonsSameJet_DeltaR0p4 		= TH1F('h_numberPartonsSameJet_DeltaR0p4', 	'h_numberPartonsSameJet_DeltaR0p4',	8,  		0.,8. )
	minDeltaRPartonJet_DeltaR0p4 		= TH1F('h_minDeltaRPartonJet_DeltaR0p4', 	'h_minDeltaRPartonJet_DeltaR0p4',	nBinsDeltaR0p4,	0.,maxDeltaR0p4 )
	secMinDeltaRPartonJet_DeltaR0p4 	= TH1F('h_secMinDeltaRPartonJet_DeltaR0p4',	'h_secMinDeltaRPartonJet_DeltaR0p4',	nBinsDeltaR, 	0.,maxDeltaR)

	minDeltaRPartonJet_4Matched_DeltaR0p4 	= TH1F('h_minDeltaRPartonJet_4Matched_DeltaR0p4', 	'h_minDeltaRPartonJet_4Matched_DeltaR0p4',		nBinsDeltaR0p4,	0.,	maxDeltaR0p4)
	minDeltaRPartonJet_4Matched_DeltaR0p4_0 	= TH1F('h_minDeltaRPartonJet_4Matched_DeltaR0p4_0', 'h_minDeltaRPartonJet_4Matched_DeltaR0p4_0',	nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	minDeltaRPartonJet_4Matched_DeltaR0p4_1 	= TH1F('h_minDeltaRPartonJet_4Matched_DeltaR0p4_1', 'h_minDeltaRPartonJet_4Matched_DeltaR0p4_1',	nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	minDeltaRPartonJet_4Matched_DeltaR0p4_2 	= TH1F('h_minDeltaRPartonJet_4Matched_DeltaR0p4_2', 'h_minDeltaRPartonJet_4Matched_DeltaR0p4_2',	nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	minDeltaRPartonJet_4Matched_DeltaR0p4_3 	= TH1F('h_minDeltaRPartonJet_4Matched_DeltaR0p4_3', 'h_minDeltaRPartonJet_4Matched_DeltaR0p4_3',	nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	invMass_4Matched_DeltaR0p4 		= TH1F('h_invMass_4Matched_DeltaR0p4', 	'h_invMass_4Matched_DeltaR0p4', 	nBinsMass, 	0., maxMass )

	minDeltaRPartonJet_2Merged2Matched_Merged_DeltaR0p4 	= TH1F('h_minDeltaRPartonJet_2Merged2Matched_Merged_DeltaR0p4', 'h_minDeltaRPartonJet_2Merged2Matched_Merged_DeltaR0p4',	nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	secMinDeltaRPartonJet_2Merged2Matched_Merged_DeltaR0p4 = TH1F('h_secMinDeltaRPartonJet_2Merged2Matched_Merged_DeltaR0p4', 'h_secMinDeltaRPartonJet_2Merged2Matched_Merged_DeltaR0p4',nBinsDeltaR, 	0.,	maxDeltaR )
	minDeltaRPartonJet_2Merged2Matched_NOMerged_DeltaR0p4 	= TH1F('h_minDeltaRPartonJet_2Merged2Matched_NOMerged_DeltaR0p4', 'h_minDeltaRPartonJet_2Merged2Matched_NOMerged_DeltaR0p4',	nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	secMinDeltaRPartonJet_2Merged2Matched_NOMerged_DeltaR0p4 = TH1F('h_secMinDeltaRPartonJet_2Merged2Matched_NOMerged_DeltaR0p4', 'h_secMinDeltaRPartonJet_2Merged2Matched_NOMerged_DeltaR0p4',nBinsDeltaR, 	0.,	maxDeltaR )
	minvsSecMinDeltaRPartonJet_2Merged2Matched_Merged_DeltaR0p4 	= TH2F('h_minvsSecMinDeltaRPartonJet_2Merged2Matched_Merged_DeltaR0p4',	'h_minvsSecMinDeltaRPartonJet_2Merged2Matched_Merged_DeltaR0p4', 	nBinsDeltaR, 	0., 	maxDeltaR, 	nBinsDeltaR, 	0., 	maxDeltaR )
	minvsSecMinDeltaRPartonJet_2Merged2Matched_NOMerged_DeltaR0p4 	= TH2F('h_minvsSecMinDeltaRPartonJet_2Merged2Matched_NOMerged_DeltaR0p4',	'h_minvsSecMinDeltaRPartonJet_2Merged2Matched_NOMerged_DeltaR0p4', 	nBinsDeltaR, 	0., 	maxDeltaR, 	nBinsDeltaR, 	0., 	maxDeltaR )
	invMass_2Merged2Matched_DeltaR0p4_NOMerged 	= TH1F('h_invMass_2Merged2Matched_DeltaR0p4_NOMerged', 	'h_invMass_2Merged2Matched_DeltaR0p4_NOMerged', 	nBinsMass, 	0., 	maxMass )
	invMass_2Merged2Matched_DeltaR0p4_Merged 	= TH1F('h_invMass_2Merged2Matched_DeltaR0p4_Merged', 	'h_invMass_2Merged2Matched_DeltaR0p4_Merged', 		nBinsMass, 	0., 	maxMass )

	minDeltaRPartonJet_Pair2Merged_DeltaR0p4_A 	= TH1F('h_minDeltaRPartonJet_Pair2Merged_DeltaR0p4_A', 	'h_minDeltaRPartonJet_Pair2Merged_DeltaR0p4_A',		nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	secMinDeltaRPartonJet_Pair2Merged_DeltaR0p4_A 	= TH1F('h_secMinDeltaRPartonJet_Pair2Merged_DeltaR0p4_A', 'h_secMinDeltaRPartonJet_Pair2Merged_DeltaR0p4_A',	nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	minDeltaRPartonJet_Pair2Merged_DeltaR0p4_B 	= TH1F('h_minDeltaRPartonJet_Pair2Merged_DeltaR0p4_B', 	'h_minDeltaRPartonJet_Pair2Merged_DeltaR0p4_B',		nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	secMinDeltaRPartonJet_Pair2Merged_DeltaR0p4_B 	= TH1F('h_secMinDeltaRPartonJet_Pair2Merged_DeltaR0p4_B', 'h_secMinDeltaRPartonJet_Pair2Merged_DeltaR0p4_B',	nBinsDeltaR0p4, 0.,	maxDeltaR0p4 )
	invMass_Pair2Merged_DeltaR0p4_Merged 		= TH1F('h_invMass_Pair2Merged_DeltaR0p4_Merged', 	'h_invMass_Pair2Merged_DeltaR0p4_Merged', 		nBinsMass, 	0., 	maxMass )

	minDeltaRPartonJet_3Merged1Match_DeltaR0p4 	= TH1F('h_minDeltaRPartonJet_3Merged1Match_DeltaR0p4', 	'h_minDeltaRPartonJet_3Merged1Match_DeltaR0p4',	nBinsDeltaR0p4, 	0.,	maxDeltaR0p4 )
	secMinDeltaRPartonJet_3Merged1Match_DeltaR0p4 	= TH1F('h_secMinDeltaRPartonJet_3Merged1Match_DeltaR0p4',	'h_secMinDeltaRPartonJet_3Merged1Match_DeltaR0p4',	nBinsDeltaR, 		0.,	maxDeltaR )
	invMass_3Merged1Match_DeltaR0p4_Merged 	= TH1F('h_invMass_3Merged1Match_DeltaR0p4_Merged', 		'h_invMass_3Merged1Match_DeltaR0p4_Merged', 		nBinsMass, 		0., 	maxMass )

	minDeltaRPartonJet_4Merged_DeltaR0p4 = TH1F('h_minDeltaRPartonJet_4Merged_DeltaR0p4', 'h_minDeltaRPartonJet_4Merged_DeltaR0p4',	nBinsDeltaR0p4, 0.,	maxDeltaR0p4)

	#h2D = TH2F('h_minDeltaRvsSecMinDeltaR','h_minDeltaRvsSecMinDeltaR', nBinsDeltaR, 0., maxDeltaR, nBinsDeltaR, 0., maxDeltaR )

	#####################################################################################################################################

	########### Read Events
	events = Events (infile)
	handleGen = Handle ("vector<reco::GenParticle>")
	labelGen = "genParticles"
	handleReco = Handle ("vector<reco::PFJet>")
	labelReco = "ak5PFJets"

	entry = 0
	print 'Reading: ', infile[ entry ]

	#dummyCounter = 0
	#dummyCounter2 = 0
	#dummyList = []
	#dummyList1 = []
	#dummyList2 = []
	#dummyList3 = []
	#dummyList4 = []
	#dummyList5 = []
	#dummyList6 = []
	for event in events:
		#---- progress of the reading --------
		entry += 1
		Run      = event.eventAuxiliary().run()
		Lumi     = event.eventAuxiliary().luminosityBlock()
		NumEvent = event.eventAuxiliary().event()
		
		if ( entry % 1000 == 0 ): print '------> Number of events: '+str(entry)
		if couts: print 'Entry ', Run, ':', Lumi, ':', NumEvent

		event.getByLabel(labelGen, handleGen)
		event.getByLabel(labelReco, handleReco)
		gens = handleGen.product()
		reco = handleReco.product()
		#if debug: print len(gens), len(reco)

		############# Store Parton information in list
		listP4PartonsFromStopA = []
		listP4PartonsFromStopB = []
		for parton in gens:
			if ( parton.status() == 3 ) and ( parton.mother() ):
				#if debug: print parton.pdgId()

				if '50' in sample: stopPdgId = 1000002
				else: stopPdgId = 1000006

				if parton.mother().pdgId() == stopPdgId:
					#if debug: print parton.pdgId()
					tmpP4 = TLorentzVector()
					tmpP4.SetPtEtaPhiE( parton.pt(), parton.eta(), parton.phi(), parton.energy()  )
					listP4PartonsFromStopA.append( tmpP4 )

				if parton.mother().pdgId() == -stopPdgId:
					#if debug: print parton.pdgId()
					tmpP4 = TLorentzVector()
					tmpP4.SetPtEtaPhiE( parton.pt(), parton.eta(), parton.phi(), parton.energy()  )
					listP4PartonsFromStopB.append( tmpP4 )

		listP4PartonsFromStops = listP4PartonsFromStopA + listP4PartonsFromStopB
		numberPartons.Fill( len( listP4PartonsFromStops ) )
		#tmpMCStopA = ( listP4PartonsFromStopA[0] + listP4PartonsFromStopA[1] ).M()
		#tmpMCStopB = ( listP4PartonsFromStopB[0] + listP4PartonsFromStopB[1] ).M()
		#if debug: print tmpMCStopA, tmpMCStopB
		#if debug: print listP4PartonsFromStops[0].Pt(), listP4PartonsFromStops[1].Pt(), listP4PartonsFromStops[2].Pt(), listP4PartonsFromStops[3].Pt() 
		#######################################################################################################################################

		#################### Store Jet Info
		#tmplistP4Jets = []
		listP4Jets = []
		for jet in reco:
			if ( jet.pt() > 20 ) and ( abs( jet.eta() ) < 2.5 ):
				tmpP4 = TLorentzVector()
				tmpP4.SetPtEtaPhiE( jet.pt(), jet.eta(), jet.phi(), jet.energy() )
				#tmplistP4Jets.append( tmpP4 )
				listP4Jets.append( tmpP4 )

		numberJets.Fill( len( listP4Jets ) )
		#if len( tmplistP4Jets ) > 3 : listP4Jets = tmplistP4Jets
		#if debug: print tmplistP4Jets
		#if debug: print listP4Jets
		#if debug: print len(listP4Jets)
		#for i in range( len( listP4Jets ) ): print i, listP4Jets[i].Pt()
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
				deltaR = listP4PartonsFromStops[iparton].DeltaR( listP4Jets[ijet] )
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
			##### if no duplicate, i.e. 4 different match jets
			if ( len( listDuplicates ) == 0 ) and ( numUniqueJets == 4 ):
				counter4MatchedMatch = 0
				numberPartonsSameJet.Fill( 0 )
				#if debug: print '4 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				#if debug: print '1', jLists[0], jLists[1]
				#dummyCounter += 1
				for jparton, jLists in dictDeltaR.iteritems():
					if jparton == 0: 
						minDeltaRPartonJet_4Matched_0.Fill( jLists[0][0] )
						if jLists[0][0] < 0.4 : counter4MatchedMatch += 1
					if jparton == 1: 
						minDeltaRPartonJet_4Matched_1.Fill( jLists[0][0] )
						if jLists[0][0] < 0.4 : counter4MatchedMatch += 1
					if jparton == 2: 
						minDeltaRPartonJet_4Matched_2.Fill( jLists[0][0] )
						if jLists[0][0] < 0.4 : counter4MatchedMatch += 1
					if jparton == 3: 
						minDeltaRPartonJet_4Matched_3.Fill( jLists[0][0] )
						if jLists[0][0] < 0.4 : counter4MatchedMatch += 1
					minDeltaRPartonJet_4Matched.Fill( jLists[0][0] )
					#if debug: print '12 ', jparton, jLists[0][0]
				numberPartonsWithDeltaR0p4_4Matched.Fill( counter4MatchedMatch ) 
				tmpA = ( listP4Jets[ tmpListJetIndex[0] ] + listP4Jets[ tmpListJetIndex[1] ] ).M()
				tmpB = ( listP4Jets[ tmpListJetIndex[2] ] + listP4Jets[ tmpListJetIndex[3] ] ).M()
				invMass_4Matched.Fill( tmpA )
				invMass_4Matched.Fill( tmpB )

			##### if one duplicate and 2 different
			elif ( len( listDuplicates ) == 1 ) and ( numUniqueJets == 3 ):
				numberPartonsSameJet.Fill( 1 )
				#if debug: print '1 duplicate + 2 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				for jparton, jLists in dictDeltaR.iteritems():
					#if debug: print '2', jLists[0], jLists[1]
					if ( listDuplicates[0] == jLists[1][0] ):
						#if debug: print jLists[0][0], jLists[0][1]
						minDeltaRPartonJet_2Merged2Matched_Merged.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_2Merged2Matched_Merged.Fill( jLists[0][1] )
						minvsSecMinDeltaRPartonJet_2Merged2Matched_Merged.Fill( jLists[0][0], jLists[0][1] )
					else:
						minDeltaRPartonJet_2Merged2Matched_NOMerged.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_2Merged2Matched_NOMerged.Fill( jLists[0][1] )
						minvsSecMinDeltaRPartonJet_2Merged2Matched_NOMerged.Fill( jLists[0][0], jLists[0][1] )

				#if couts: print tmpListJetIndex
				if ( listDuplicates[0] != tmpListJetIndex[0] ) and ( listDuplicates[0] != tmpListJetIndex[1] ): 
					tmpStopA = ( listP4Jets[ tmpListJetIndex[0] ] + listP4Jets[ tmpListJetIndex[1] ] ).M()
					invMass_2Merged2Matched_NOMerged.Fill( tmpStopA )
					tmpStopC = ( listP4Jets[ listDuplicates[0] ] ).M()
					invMass_2Merged2Matched_Merged.Fill( tmpStopC )
					#if couts: print 'yes1', tmpStopA, tmpStopC
				elif ( listDuplicates[0] != tmpListJetIndex[2] ) and ( listDuplicates[0] != tmpListJetIndex[3] ): 
					tmpStopB = ( listP4Jets[ tmpListJetIndex[2] ] + listP4Jets[ tmpListJetIndex[3] ] ).M()
					invMass_2Merged2Matched_NOMerged.Fill( tmpStopB )
					tmpStopC = ( listP4Jets[ listDuplicates[0] ] ).M()
					invMass_2Merged2Matched_Merged.Fill( tmpStopC )
					#if couts: print 'yes2', tmpStopB, tmpStopC

			##### if a pair of two duplicates
			elif ( len( listDuplicates ) == 2 ) and ( numUniqueJets == 2 ):
				numberPartonsSameJet.Fill( 2 )
				#if debug: print '5', jLists[0], jLists[1]
				#if debug: print 'Pair of two duplicate match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				for jparton, jLists in dictDeltaR.iteritems():
					if ( listDuplicates[0] == jLists[1][0] ) or ( listDuplicates[1] == jLists[1][0] ):
						minDeltaRPartonJet_Pair2Merged.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_Pair2Merged.Fill( jLists[0][1] )
						minvsSecMinDeltaRPartonJet_Pair2Merged.Fill( jLists[0][0], jLists[0][1] )
						#if debug: print jLists[1][0], listDuplicates
				tmpStopA = ( listP4Jets[ listDuplicates[0] ] ).M()
				invMass_Pair2Merged_Merged.Fill( tmpStopA )
				tmpStopB = ( listP4Jets[ listDuplicates[1] ] ).M()
				invMass_Pair2Merged_Merged.Fill( tmpStopB )

			##### if one duplicate and 1 different
			elif ( len( listDuplicates ) == 1 ) and ( numUniqueJets == 2 ):
				numberPartonsSameJet.Fill( 3 )
				#if debug: print '1 duplicate + 1 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				#if debug: print '3', jLists[0], jLists[1]
				for jparton, jLists in dictDeltaR.iteritems():
					if ( listDuplicates[0] == jLists[1][0] ):
						minDeltaRPartonJet_3Merged1Match.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_3Merged1Match.Fill( jLists[0][1] )
						minvsSecMinDeltaRPartonJet_3Merged1Match.Fill( jLists[0][0], jLists[0][1] )
						#if debug: print jLists[1][0], listDuplicates
				tmpMass = ( listP4Jets[ listDuplicates[0] ] ).M()
				invMass_3Merged1Match_Merged.Fill( tmpMass )

			##### all partons with same jet
			elif ( len( listDuplicates ) == 1 ) and ( numUniqueJets == 1 ):
				numberPartonsSameJet.Fill( 4 )
				#if debug: print '1 duplicate + 0 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				#if debug: print '4', jLists[0], jLists[1]
				for jparton, jLists in dictDeltaR.iteritems():
					if ( listDuplicates[0] == jLists[1][0] ):
						minDeltaRPartonJet_4Merged.Fill( jLists[0][0] )
						#if debug: print jLists[1][0], listDuplicates

		##### less than 4 jets
		else:
			#if debug: print 'less than 4 jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
			#if debug: print '6', jLists[0], jLists[1]
			numberPartonsSameJet.Fill( 6 )
			#if debug: print tmpListJetIndex, listDuplicates, numUniqueJets
		###########################################################################################################

		########################## DeltaR < 0.4
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

		##### if 4 jets after delta cut
		if len( tmpListJetIndexDeltaR0p4 ) == 4:		
			##### if no duplicate, i.e. 4 different match jets
			if ( len( listDuplicatesDeltaR0p4 ) == 0 ) and ( numUniqueJetsDeltaR0p4 == 4 ):
				#if debug: print '1', jLists[0], jLists[1]
				#if debug: print '4 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				#dummyCounter2 += 1
				numberPartonsSameJet_DeltaR0p4.Fill( 0 )
				for jparton, jLists in dictDeltaR0p4.iteritems():
					#if debug: print '15 ', jparton, jLists[0][0]
					#if debug: print jLists[1][0], listDuplicates
					if jparton == 0: minDeltaRPartonJet_4Matched_DeltaR0p4_0.Fill( jLists[0][0] )
					if jparton == 1: minDeltaRPartonJet_4Matched_DeltaR0p4_1.Fill( jLists[0][0] )
					if jparton == 2: minDeltaRPartonJet_4Matched_DeltaR0p4_2.Fill( jLists[0][0] )
					if jparton == 3: minDeltaRPartonJet_4Matched_DeltaR0p4_3.Fill( jLists[0][0] )
					minDeltaRPartonJet_4Matched_DeltaR0p4.Fill( jLists[0][0] )

				tmpStopA = ( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ] + listP4Jets[ tmpListJetIndexDeltaR0p4[1] ] ).M()
				tmpStopB = ( listP4Jets[ tmpListJetIndexDeltaR0p4[2] ] + listP4Jets[ tmpListJetIndexDeltaR0p4[3] ] ).M()
				invMass_4Matched_DeltaR0p4.Fill( tmpStopA )
				invMass_4Matched_DeltaR0p4.Fill( tmpStopB )
				#if debug: print tmpStopA, tmpStopB

			##### if one duplicate and 2 different
			elif ( len( listDuplicatesDeltaR0p4 ) == 1 ) and ( numUniqueJetsDeltaR0p4 == 3 ):
				#if debug: print '2', jLists[0], jLists[1]
				numberPartonsSameJet_DeltaR0p4.Fill( 1 )
				for jparton, jLists in dictDeltaR0p4.iteritems():
					#if debug: print jLists[1][0], listDuplicates
					if ( listDuplicatesDeltaR0p4[0] == jLists[1][0] ):
						minDeltaRPartonJet_2Merged2Matched_Merged_DeltaR0p4.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_2Merged2Matched_Merged_DeltaR0p4.Fill( jLists[0][1] )
						minvsSecMinDeltaRPartonJet_2Merged2Matched_Merged_DeltaR0p4.Fill( jLists[0][0], jLists[0][1] )
					else:
						minDeltaRPartonJet_2Merged2Matched_NOMerged_DeltaR0p4.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_2Merged2Matched_NOMerged_DeltaR0p4.Fill( jLists[0][1] )
						minvsSecMinDeltaRPartonJet_2Merged2Matched_NOMerged_DeltaR0p4.Fill( jLists[0][0], jLists[0][1] )

				if ( listDuplicatesDeltaR0p4[0] != tmpListJetIndexDeltaR0p4[0] ) and ( listDuplicatesDeltaR0p4[0] != tmpListJetIndexDeltaR0p4[1] ): 
					tmpStopA = ( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ] + listP4Jets[ tmpListJetIndexDeltaR0p4[1] ] ).M()
					tmpStopC = ( listP4Jets[ listDuplicatesDeltaR0p4[0] ] ).M()
					invMass_2Merged2Matched_DeltaR0p4_NOMerged.Fill( tmpStopA )
					invMass_2Merged2Matched_DeltaR0p4_Merged.Fill( tmpStopC )
					#if debug: print '1 jet merged + 2 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
					#if debug: print 'jetMass ', tmpStopC
					#if debug: print 'stopA ', tmpStopA
				elif ( listDuplicatesDeltaR0p4[0] != tmpListJetIndexDeltaR0p4[2] ) and ( listDuplicatesDeltaR0p4[0] != tmpListJetIndexDeltaR0p4[3] ): 
					tmpStopB = ( listP4Jets[ tmpListJetIndexDeltaR0p4[2] ] + listP4Jets[ tmpListJetIndexDeltaR0p4[3] ] ).M()
					tmpStopC = ( listP4Jets[ listDuplicatesDeltaR0p4[0] ] ).M()
					invMass_2Merged2Matched_DeltaR0p4_NOMerged.Fill( tmpStopB )
					invMass_2Merged2Matched_DeltaR0p4_Merged.Fill( tmpStopC )
					#if debug: print '1 jet merged + 2 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
					#if debug: print ' jetMass ', tmpStopC
					#if debug: print 'stopB ', tmpStopB

			##### if a pair of two duplicates
			elif ( len( listDuplicatesDeltaR0p4 ) == 2 ) and ( numUniqueJetsDeltaR0p4 == 2 ):
				#if debug: print '5', jLists[0], jLists[1]
				numberPartonsSameJet_DeltaR0p4.Fill( 2 )
				for jparton, jLists in dictDeltaR0p4.iteritems():
					#if debug: print jLists[1][0], listDuplicates
					if ( listDuplicatesDeltaR0p4[0] == jLists[1][0] ):
						minDeltaRPartonJet_Pair2Merged_DeltaR0p4_A.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_Pair2Merged_DeltaR0p4_A.Fill( jLists[0][1] )
					if ( listDuplicatesDeltaR0p4[1] == jLists[1][0] ):
						minDeltaRPartonJet_Pair2Merged_DeltaR0p4_B.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_Pair2Merged_DeltaR0p4_B.Fill( jLists[0][1] )

				if ( listDuplicatesDeltaR0p4[0] == tmpListJetIndexDeltaR0p4[0] ) and ( listDuplicatesDeltaR0p4[0] == tmpListJetIndexDeltaR0p4[1] ): 
					tmpStopA = ( listP4Jets[ listDuplicatesDeltaR0p4[0] ] ).M()
					invMass_Pair2Merged_DeltaR0p4_Merged.Fill( tmpStopA )
					tmpStopB = ( listP4Jets[ listDuplicatesDeltaR0p4[1] ] ).M()
					invMass_Pair2Merged_DeltaR0p4_Merged.Fill( tmpStopB )
					if couts: print tmpStopA, tmpStopB, tmpListJetIndexDeltaR0p4
				elif ( listDuplicatesDeltaR0p4[0] == tmpListJetIndexDeltaR0p4[2] ) and ( listDuplicatesDeltaR0p4[0] == tmpListJetIndexDeltaR0p4[3] ): 
					tmpStopA = ( listP4Jets[ listDuplicatesDeltaR0p4[1] ] ).M()
					invMass_Pair2Merged_DeltaR0p4_Merged.Fill( tmpStopA )
					tmpStopB = ( listP4Jets[ listDuplicatesDeltaR0p4[0] ] ).M()
					invMass_Pair2Merged_DeltaR0p4_Merged.Fill( tmpStopB )
					if couts: print tmpStopA, tmpStopB, tmpListJetIndexDeltaR0p4
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
						minDeltaRPartonJet_3Merged1Match_DeltaR0p4.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_3Merged1Match_DeltaR0p4.Fill( jLists[0][1] )
				tmpMass = ( listP4[ listDuplicatesDeltaR0p4[0] ] ).M()
				invMass_3Merged1Match_DeltaR0p4_Merged.Fill( tmpMass )


			##### all partons with same jet
			elif ( len( listDuplicatesDeltaR0p4 ) == 1 ) and ( numUniqueJetsDeltaR0p4 == 1 ):
				#if debug: print '4', jLists[0], jLists[1]
				#if debug: print '4 jet merged : ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				numberPartonsSameJet_DeltaR0p4.Fill( 4 )
				for jparton, jLists in dictDeltaR0p4.iteritems():
					#if debug: print jLists[1][0], listDuplicates
					if ( listDuplicatesDeltaR0p4[0] == jLists[1][0] ):
						minDeltaRPartonJet_4Merged_DeltaR0p4.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_4Merged_DeltaR0p4.Fill( jLists[0][1] )


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
	print 'Writing output file: '+sample + '_Matching_Plots.root'
	outputFile.Close()

	###### Extra: send prints to file
	if couts == False: 
		sys.stdout = outfileStdOut
		f.close()
	#########################


#################################################################################
if __name__ == '__main__':

	usage = 'usage: %prog [options]'
	
	parser = optparse.OptionParser(usage=usage)
	parser.add_option( '-m', '--mass', action='store', type='int', dest='mass', default=50, help='Mass of the Stop' )
	parser.add_option( '-d', '--debug', action='store_true', dest='couts', default=False, help='True print couts in screen, False print in a file' )
	parser.add_option( '-f', '--final', action='store_true', dest='final', default=False, help='If True, final version' )

	(options, args) = parser.parse_args()

	mass = options.mass
	couts = options.couts
	final = options.final

	sample = 'stop_UDD312_'+str(mass)
	#list = os.popen('ls -1 /cms/gomez/Substructure/Generation/Simulation/CMSSW_5_3_2_patch4/src/mySimulations/stop_UDD312_50/aodsim/*.root').read().splitlines()
	list = os.popen('ls -1 /cms/gomez/Stops/st_jj/AOD/'+sample+'/*.root').read().splitlines()
	outputList = [i if i.startswith('file') else 'file:' + i for i in list]
	outputDir = '/cms/gomez/Stops/st_jj/MCTruth/'

	if not final : get_info( outputList[:2], outputDir, sample, mass, couts, final )
	else: get_info( outputList, outputDir, sample, mass, couts, final )

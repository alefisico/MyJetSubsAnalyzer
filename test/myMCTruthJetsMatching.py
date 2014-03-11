#!/usr/bin/env python

import sys,os,time
import operator
from collections import defaultdict
from ROOT import *
from DataFormats.FWLite import Events, Handle

gROOT.SetBatch()

###### Trick for add date or month to plots
dateKey   = time.strftime("%y%m%d%H%M")

######################################
def get_info( infile, outputDir, sample ):

	outputFile = TFile( outputDir + sample + '_Matching_Plots_'+dateKey+'.root', 'RECREATE' )

	######## Extra, send print to file
	outfileStdOut = sys.stdout
	f = file('tmp_'+sample+'_'+dateKey+'.txt', 'w')
	sys.stdout = f
	#################################################

	######### Histograms
	numberPartonsSameJet = TH1F('h_numberPartonsSameJet', 'h_numberPartonsSameJet',	7,  0.,	7.)
	minDeltaRPartonJet = TH1F('h_minDeltaRPartonJet', 'h_minDeltaRPartonJet',	50, 0.,	5.)
	secMinDeltaRPartonJet = TH1F('h_secMinDeltaRPartonJet',	'h_secMinDeltaRPartonJet',	50, 0.,	5.)
	minvsSecMinDeltaRPartonJet = TH2F('h_minDeltaRvsSecMinDeltaR','h_minDeltaRvsSecMinDeltaR', 50, 0., 5., 50, 0., 5. )

	minDeltaRPartonJet_4Diff = TH1F('h_minDeltaRPartonJet_4Diff', 'h_minDeltaRPartonJet_4Diff',	50, 0.,	5.)
	minDeltaRPartonJet_2PartonSameJetPlus2Diff = TH1F('h_minDeltaRPartonJet_2PartonSameJetPlus2Diff', 'h_minDeltaRPartonJet_2PartonSameJetPlus2Diff',	50, 0.,	5.)
	secMinDeltaRPartonJet_2PartonSameJetPlus2Diff = TH1F('h_secMinDeltaRPartonJet_2PartonSameJetPlus2Diff',	'h_secMinDeltaRPartonJet_2PartonSameJetPlus2Diff',	50, 0.,	5.)
	minvsSecMinDeltaRPartonJet_2PartonSameJetPlus2Diff = TH2F('h_minvsSecMinDeltaRPartonJet_2PartonSameJetPlus2Diff','h_minvsSecMinDeltaRPartonJet_2PartonSameJetPlus2Diff', 50, 0., 5., 50, 0., 5. )
	minDeltaRPartonJet_Pair2PartonSameJet = TH1F('h_minDeltaRPartonJet_Pair2PartonSameJet', 'h_minDeltaRPartonJet_Pair2PartonSameJet',	50, 0.,	5.)
	secMinDeltaRPartonJet_Pair2PartonSameJet = TH1F('h_secMinDeltaRPartonJet_Pair2PartonSameJet',	'h_secMinDeltaRPartonJet_Pair2PartonSameJet',	50, 0.,	5.)
	minvsSecMinDeltaRPartonJet_Pair2PartonSameJet = TH2F('h_minvsSecMinDeltaRPartonJet_Pair2PartonSameJet','h_minvsSecMinDeltaRPartonJet_Pair2PartonSameJet', 50, 0., 5., 50, 0., 5. )
	minDeltaRPartonJet_3PartonSameJet = TH1F('h_minDeltaRPartonJet_3PartonSameJet', 'h_minDeltaRPartonJet_3PartonSameJet',	50, 0.,	5.)
	secMinDeltaRPartonJet_3PartonSameJet = TH1F('h_secMinDeltaRPartonJet_3PartonSameJet',	'h_secMinDeltaRPartonJet_3PartonSameJet',	50, 0.,	5.)
	minvsSecMinDeltaRPartonJet_3PartonSameJet = TH2F('h_minvsSecMinDeltaRPartonJet_3PartonSameJet','h_minvsSecMinDeltaRPartonJet_3PartonSameJet', 50, 0., 5., 50, 0., 5. )
	minDeltaRPartonJet_4PartonSameJet = TH1F('h_minDeltaRPartonJet_4PartonSameJet', 'h_minDeltaRPartonJet_4PartonSameJet',	50, 0.,	5.)

	#### with DeltaR0p4
	numberPartonsSameJet_DeltaR0p4 = TH1F('h_numberPartonsSameJet_DeltaR0p4', 'h_numberPartonsSameJet_DeltaR0p4',	16,  0.,	16.)
	minDeltaRPartonJet_DeltaR0p4 = TH1F('h_minDeltaRPartonJet_DeltaR0p4', 'h_minDeltaRPartonJet_DeltaR0p4',	20, 0.,	1.)
	secMinDeltaRPartonJet_DeltaR0p4 = TH1F('h_secMinDeltaRPartonJet_DeltaR0p4',	'h_secMinDeltaRPartonJet_DeltaR0p4',	50, 0.,	5.)

	minDeltaRPartonJet_4Diff_DeltaR0p4 = TH1F('h_minDeltaRPartonJet_4Diff_DeltaR0p4', 'h_minDeltaRPartonJet_4Diff_DeltaR0p4',	20, 0.,	1.)
	invMass_4Diff_DeltaR0p4 = TH1F('h_invMass_4Diff_DeltaR0p4', 'h_invMass_4Diff_DeltaR0p4', 100, 0., 1000. )
	minDeltaRPartonJet_2PartonSameJetPlus2Diff_DeltaR0p4 = TH1F('h_minDeltaRPartonJet_2PartonSameJetPlus2Diff_DeltaR0p4', 'h_minDeltaRPartonJet_2PartonSameJetPlus2Diff_DeltaR0p4',	20, 0.,	1.)
	secMinDeltaRPartonJet_2PartonSameJetPlus2Diff_DeltaR0p4 = TH1F('h_secMinDeltaRPartonJet_2PartonSameJetPlus2Diff_DeltaR0p4',	'h_secMinDeltaRPartonJet_2PartonSameJetPlus2Diff_DeltaR0p4',	50, 0.,	5.)
	invMass_2PartonSameJetPlus2Diff_DeltaR0p4_NOMerged = TH1F('h_invMass_2PartonSameJetPlus2Diff_DeltaR0p4_NOMerged', 'h_invMass_2PartonSameJetPlus2Diff_DeltaR0p4_NOMerged', 100, 0., 1000. )
	invMass_2PartonSameJetPlus2Diff_DeltaR0p4_Merged = TH1F('h_invMass_2PartonSameJetPlus2Diff_DeltaR0p4_Merged', 'h_invMass_2PartonSameJetPlus2Diff_DeltaR0p4_Merged', 100, 0., 1000. )

	minDeltaRPartonJet_3PartonSameJet_DeltaR0p4 = TH1F('h_minDeltaRPartonJet_3PartonSameJet_DeltaR0p4', 'h_minDeltaRPartonJet_3PartonSameJet_DeltaR0p4',	20, 0.,	1.)
	secMinDeltaRPartonJet_3PartonSameJet_DeltaR0p4 = TH1F('h_secMinDeltaRPartonJet_3PartonSameJet_DeltaR0p4',	'h_secMinDeltaRPartonJet_3PartonSameJet_DeltaR0p4',	50, 0.,	5.)

	minDeltaRPartonJet_4PartonSameJet_DeltaR0p4 = TH1F('h_minDeltaRPartonJet_4PartonSameJet_DeltaR0p4', 'h_minDeltaRPartonJet_4PartonSameJet_DeltaR0p4',	20, 0.,	1.)

	minDeltaRPartonJet_Pair2PartonSameJet_DeltaR0p4_A = TH1F('h_minDeltaRPartonJet_Pair2PartonSameJet_DeltaR0p4_A', 'h_minDeltaRPartonJet_Pair2PartonSameJet_DeltaR0p4_A',	20, 0.,	1.)
	secMinDeltaRPartonJet_Pair2PartonSameJet_DeltaR0p4_A = TH1F('h_secMinDeltaRPartonJet_Pair2PartonSameJet_DeltaR0p4_A', 'h_secMinDeltaRPartonJet_Pair2PartonSameJet_DeltaR0p4_A',	20, 0.,	1.)
	minDeltaRPartonJet_Pair2PartonSameJet_DeltaR0p4_B = TH1F('h_minDeltaRPartonJet_Pair2PartonSameJet_DeltaR0p4_B', 'h_minDeltaRPartonJet_Pair2PartonSameJet_DeltaR0p4_B',	20, 0.,	1.)
	secMinDeltaRPartonJet_Pair2PartonSameJet_DeltaR0p4_B = TH1F('h_secMinDeltaRPartonJet_Pair2PartonSameJet_DeltaR0p4_B', 'h_secMinDeltaRPartonJet_Pair2PartonSameJet_DeltaR0p4_B',	20, 0.,	1.)
	invMass_Pair2PartonSameJet_DeltaR0p4_Merged = TH1F('h_invMass_Pair2PartonSameJet_DeltaR0p4_Merged', 'h_invMass_Pair2PartonSameJet_DeltaR0p4_Merged', 100, 0., 1000. )
	#h2D = TH2F('h_minDeltaRvsSecMinDeltaR','h_minDeltaRvsSecMinDeltaR', 50, 0., 5., 50, 0., 5. )

	#####################################################################################################################################

	########### Read Events
	events = Events (infile)
	handleGen = Handle ("vector<reco::GenParticle>")
	labelGen = "genParticles"
	handleReco = Handle ("vector<reco::PFJet>")
	labelReco = "ak5PFJets"

	entry = 0
	print 'Reading: ', infile[ entry ]

	for event in events:
		#---- progress of the reading --------
		entry += 1
		if ( entry % 1000 == 0 ): print '------> Number of events: '+str(entry)

		event.getByLabel(labelGen, handleGen)
		event.getByLabel(labelReco, handleReco)
		gens = handleGen.product()
		reco = handleReco.product()
		#print len(gens), len(reco)
		Run      = event.eventAuxiliary().run()
		Lumi     = event.eventAuxiliary().luminosityBlock()
		NumEvent = event.eventAuxiliary().event()
		

		############# Store Parton information in list
		listP4PartonsFromStopA = []
		listP4PartonsFromStopB = []
		for parton in gens:
			if ( parton.status() == 3 ) and ( parton.mother() ):
				#print parton.pdgId()

				if '50' in sample: stopPdgId = 1000002
				else: stopPdgId = 1000006

				if parton.mother().pdgId() == stopPdgId:
					#print parton.pdgId()
					tmpP4 = TLorentzVector()
					tmpP4.SetPtEtaPhiE( parton.pt(), parton.eta(), parton.phi(), parton.energy()  )
					listP4PartonsFromStopA.append( tmpP4 )

				if parton.mother().pdgId() == -stopPdgId:
					#print parton.pdgId()
					tmpP4 = TLorentzVector()
					tmpP4.SetPtEtaPhiE( parton.pt(), parton.eta(), parton.phi(), parton.energy()  )
					listP4PartonsFromStopB.append( tmpP4 )

		listP4PartonsFromStops = listP4PartonsFromStopA + listP4PartonsFromStopB
		#tmpMCStopA = ( listP4PartonsFromStopA[0] + listP4PartonsFromStopA[1] ).M()
		#tmpMCStopB = ( listP4PartonsFromStopB[0] + listP4PartonsFromStopB[1] ).M()
		#print tmpMCStopA, tmpMCStopB
		#print listP4PartonsFromStops[0].Pt(), listP4PartonsFromStops[1].Pt(), listP4PartonsFromStops[2].Pt(), listP4PartonsFromStops[3].Pt() 
		#######################################################################################################################################

		#################### Store Jet Info
		listP4Jets = []
		for jet in reco:
			if ( jet.pt() > 20 ) and ( abs( jet.eta() ) < 2.5 ):
				tmpP4 = TLorentzVector()
				tmpP4.SetPtEtaPhiE( jet.pt(), jet.eta(), jet.phi(), jet.energy() )
				listP4Jets.append( tmpP4 )
		#print len(listP4Jets)
		#for i in range( len( listP4Jets ) ): print i, listP4Jets[i].Pt()
		###########################################################################################

		################### Calculate DeltaR between each parton and each jet
		dictDeltaR = {}
		dictDeltaR0p4 = {}
		tmpListJetIndex = []
		tmpListJetIndexDeltaR0p4 = []
		for iparton in range( len( listP4PartonsFromStops ) ):
			listDeltaR = []
			for ijet in range( len( listP4Jets ) ):
				deltaR = listP4PartonsFromStops[iparton].DeltaR( listP4Jets[ijet] )
				listDeltaR.append( deltaR )

			sortedListDeltaR = sorted( listDeltaR )
			jetIndex = []
			#print listDeltaR, sortedListDeltaR
			if len( listDeltaR ) > 0:
				for i in sortedListDeltaR:
					tmpjetIndex = listDeltaR.index( i )
					jetIndex.append( tmpjetIndex )
				dictDeltaR[ iparton ] = [ sortedListDeltaR, jetIndex ]
				tmpListJetIndex.append( jetIndex[0] )
				if ( sortedListDeltaR[0] < 0.4 ): 
					dictDeltaR0p4[ iparton ] = [ sortedListDeltaR, jetIndex ]
					tmpListJetIndexDeltaR0p4.append( jetIndex[0] )

		#print dictDeltaR
		#print dictDeltaR0p4
		#print tmpListJetIndex
		#print tmpListJetIndexDeltaR0p4
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

		if len( tmpListJetIndex ) == 4:		
			##### if no duplicate, i.e. 4 different match jets
			if ( len( listDuplicates ) == 0 ) and ( numUniqueJets == 4 ):
				#print '4 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				#print '1', jLists[0], jLists[1]
				numberPartonsSameJet.Fill( 0 )
				for jparton, jLists in dictDeltaR.iteritems():
					minDeltaRPartonJet_4Diff.Fill( jLists[0][0] )

			##### if one duplicate and 2 different
			elif ( len( listDuplicates ) == 1 ) and ( numUniqueJets == 3 ):
				#print '1 duplicate + 2 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				numberPartonsSameJet.Fill( 1 )
				for jparton, jLists in dictDeltaR.iteritems():
					#print '2', jLists[0], jLists[1]
					if ( listDuplicates[0] == jLists[1][0] ):
						#print jLists[0][0], jLists[0][1]
						minDeltaRPartonJet_2PartonSameJetPlus2Diff.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_2PartonSameJetPlus2Diff.Fill( jLists[0][1] )
						minvsSecMinDeltaRPartonJet_2PartonSameJetPlus2Diff.Fill( jLists[0][0], jLists[0][1] )

			##### if a pair of two duplicates
			elif ( len( listDuplicates ) == 2 ) and ( numUniqueJets == 2 ):
				#print '5', jLists[0], jLists[1]
				#print 'Pair of two duplicate match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				numberPartonsSameJet.Fill( 2 )
				for jparton, jLists in dictDeltaR.iteritems():
					if ( listDuplicates[0] == jLists[1][0] ) or ( listDuplicates[1] == jLists[1][0] ):
						#print jLists[1][0], listDuplicates
						minDeltaRPartonJet_Pair2PartonSameJet.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_Pair2PartonSameJet.Fill( jLists[0][1] )
						minvsSecMinDeltaRPartonJet_Pair2PartonSameJet.Fill( jLists[0][0], jLists[0][1] )

			##### if one duplicate and 1 different
			elif ( len( listDuplicates ) == 1 ) and ( numUniqueJets == 2 ):
				#print '1 duplicate + 1 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				#print '3', jLists[0], jLists[1]
				numberPartonsSameJet.Fill( 3 )
				for jparton, jLists in dictDeltaR.iteritems():
					if ( listDuplicates[0] == jLists[1][0] ):
						#print jLists[1][0], listDuplicates
						minDeltaRPartonJet_3PartonSameJet.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_3PartonSameJet.Fill( jLists[0][1] )
						minvsSecMinDeltaRPartonJet_3PartonSameJet.Fill( jLists[0][0], jLists[0][1] )

			##### all partons with same jet
			elif ( len( listDuplicates ) == 1 ) and ( numUniqueJets == 1 ):
				#print '1 duplicate + 0 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				#print '4', jLists[0], jLists[1]
				numberPartonsSameJet.Fill( 4 )
				for jparton, jLists in dictDeltaR.iteritems():
					if ( listDuplicates[0] == jLists[1][0] ):
						#print jLists[1][0], listDuplicates
						minDeltaRPartonJet_4PartonSameJet.Fill( jLists[0][0] )

		##### less than 4 jets
		else:
			#print 'less than 4 jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
			#print '6', jLists[0], jLists[1]
			numberPartonsSameJet.Fill( 6 )
			#print tmpListJetIndex, listDuplicates, numUniqueJets

##########################################################################
#		appearances = defaultdict(int)
#		for curr in tmpListJetIndex: appearances[curr] += 1
#		#for i, k in appearances.iteritems(): print i, k #appearances
#
#		if len(appearances) == 1 : 			###### 4 partons with same jet
#			numberPartonsSameJet.Fill( 4 )
#			for i,listParton in dictDeltaR.iteritems(): 
#				minDeltaRPartonJet_4PartonSameJet.Fill( listParton[1][0] )
#		elif len(appearances) == 2 : 
#			for i, k in appearances.iteritems():
#				if k == 2: 			###### 2 partons with same jet
#					numberPartonsSameJet.Fill( 2 )
#					#print dictDeltaR
#					#print '2 partons with same jet: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
#					for i,listParton in dictDeltaR.iteritems(): 
#						minDeltaRPartonJet_2PartonSameJet.Fill( listParton[1][0] )
#						secMinDeltaRPartonJet_2PartonSameJet.Fill( listParton[1][1] )
#					break
#				else: 				###### 3 partons with same jet
#					numberPartonsSameJet.Fill( 3 )
#					#print '3 partons with same jet: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
#					for i,listParton in dictDeltaR.iteritems(): 
#						minDeltaRPartonJet_3PartonSameJet.Fill( listParton[1][0] )
#						secMinDeltaRPartonJet_3PartonSameJet.Fill( listParton[1][1] )
#					break
#		elif len(appearances) == 3: 			###### 2 partons with same jet + 2 diff
#			numberPartonsSameJet.Fill( 1 )
#			#print '2 partons with same jet + 2 diff: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
#			for i,listParton in dictDeltaR.iteritems(): 
#				minDeltaRPartonJet_2PartonSameJetPlus2Diff.Fill( listParton[1][0] )
#				secMinDeltaRPartonJet_2PartonSameJetPlus2Diff.Fill( listParton[1][1] )
#		elif len(appearances) == 4: 			###### 4 diff jets
#			numberPartonsSameJet.Fill( 0 )
#			#print '4 diff: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
#			for i,listParton in dictDeltaR.iteritems(): 
#				minDeltaRPartonJet_4Diff.Fill( listParton[1][0] )
#		else:						###### something wrong (like no jets)
#			numberPartonsSameJet.Fill( 6 )
#		#print tmpListJetIndex, listP4Jets
#########################################################################################################
		
		###### DeltaR < 0.4
		#### check if cut is applied:
		for i,listParton in dictDeltaR0p4.iteritems(): 
			if len( listParton[0] ) > 0: minDeltaRPartonJet_DeltaR0p4.Fill( listParton[0][0] )
			if len( listParton[0] ) > 1: secMinDeltaRPartonJet_DeltaR0p4.Fill( listParton[0][1] )

		#### check number of repetitions
		appearancesDeltaR0p4 = defaultdict(int)
		for curr in tmpListJetIndexDeltaR0p4: appearancesDeltaR0p4[curr] += 1
		listDuplicatesDeltaR0p4 = [ i for i, k in appearancesDeltaR0p4.iteritems() if k > 1 ]
		numUniqueJetsDeltaR0p4 = len( set( tmpListJetIndexDeltaR0p4 ) )
		#print tmpListJetIndexDeltaR0p4
		#print listDuplicatesDeltaR0p4
		#print numUniqueJetsDeltaR0p4

		##### if 4 jets after delta cut
		if len( tmpListJetIndexDeltaR0p4 ) == 4:		
			##### if no duplicate, i.e. 4 different match jets
			if ( len( listDuplicatesDeltaR0p4 ) == 0 ) and ( numUniqueJetsDeltaR0p4 == 4 ):
				#print '1', jLists[0], jLists[1]
				#print '4 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				numberPartonsSameJet_DeltaR0p4.Fill( 0 )
				for jparton, jLists in dictDeltaR0p4.iteritems():
					#print jLists[1][0], listDuplicates
					minDeltaRPartonJet_4Diff_DeltaR0p4.Fill( jLists[0][0] )

				tmpStopA = ( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ] + listP4Jets[ tmpListJetIndexDeltaR0p4[1] ] ).M()
				tmpStopB = ( listP4Jets[ tmpListJetIndexDeltaR0p4[2] ] + listP4Jets[ tmpListJetIndexDeltaR0p4[3] ] ).M()
				invMass_4Diff_DeltaR0p4.Fill( tmpStopA )
				invMass_4Diff_DeltaR0p4.Fill( tmpStopB )
				#print tmpStopA, tmpStopB

			##### if one duplicate and 2 different
			elif ( len( listDuplicatesDeltaR0p4 ) == 1 ) and ( numUniqueJetsDeltaR0p4 == 3 ):
				#print '2', jLists[0], jLists[1]
				numberPartonsSameJet_DeltaR0p4.Fill( 1 )
				for jparton, jLists in dictDeltaR0p4.iteritems():
					#print jLists[1][0], listDuplicates
					if ( listDuplicatesDeltaR0p4[0] == jLists[1][0] ):
						minDeltaRPartonJet_2PartonSameJetPlus2Diff_DeltaR0p4.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_2PartonSameJetPlus2Diff_DeltaR0p4.Fill( jLists[0][1] )

				if ( listDuplicatesDeltaR0p4[0] != tmpListJetIndexDeltaR0p4[0] ) and ( listDuplicatesDeltaR0p4[0] != tmpListJetIndexDeltaR0p4[1] ): 
					tmpStopA = ( listP4Jets[ tmpListJetIndexDeltaR0p4[0] ] + listP4Jets[ tmpListJetIndexDeltaR0p4[1] ] ).M()
					tmpStopC = ( listP4Jets[ listDuplicatesDeltaR0p4[0] ] ).M()
					invMass_2PartonSameJetPlus2Diff_DeltaR0p4_NOMerged.Fill( tmpStopA )
					invMass_2PartonSameJetPlus2Diff_DeltaR0p4_Merged.Fill( tmpStopC )
					#print '1 jet merged + 2 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
					#print 'jetMass ', tmpStopC
					#print 'stopA ', tmpStopA
				elif ( listDuplicatesDeltaR0p4[0] != tmpListJetIndexDeltaR0p4[2] ) and ( listDuplicatesDeltaR0p4[0] != tmpListJetIndexDeltaR0p4[3] ): 
					tmpStopB = ( listP4Jets[ tmpListJetIndexDeltaR0p4[2] ] + listP4Jets[ tmpListJetIndexDeltaR0p4[3] ] ).M()
					tmpStopC = ( listP4Jets[ listDuplicatesDeltaR0p4[0] ] ).M()
					invMass_2PartonSameJetPlus2Diff_DeltaR0p4_NOMerged.Fill( tmpStopB )
					invMass_2PartonSameJetPlus2Diff_DeltaR0p4_Merged.Fill( tmpStopC )
					#print '1 jet merged + 2 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
					#print ' jetMass ', tmpStopC
					#print 'stopB ', tmpStopB

			##### if one duplicate and 1 different
			elif ( len( listDuplicatesDeltaR0p4 ) == 1 ) and ( numUniqueJetsDeltaR0p4 == 2 ):
				#print '3', jLists[0], jLists[1]
				#print '3 jet merged + 1 diff match jets: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				numberPartonsSameJet_DeltaR0p4.Fill( 2 )
				for jparton, jLists in dictDeltaR0p4.iteritems():
					#print jLists[1][0], listDuplicates
					if ( listDuplicatesDeltaR0p4[0] == jLists[1][0] ):
						minDeltaRPartonJet_3PartonSameJet_DeltaR0p4.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_3PartonSameJet_DeltaR0p4.Fill( jLists[0][1] )

			##### all partons with same jet
			elif ( len( listDuplicatesDeltaR0p4 ) == 1 ) and ( numUniqueJetsDeltaR0p4 == 1 ):
				#print '4', jLists[0], jLists[1]
				#print '4 jet merged : ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				numberPartonsSameJet_DeltaR0p4.Fill( 3 )
				for jparton, jLists in dictDeltaR0p4.iteritems():
					#print jLists[1][0], listDuplicates
					if ( listDuplicatesDeltaR0p4[0] == jLists[1][0] ):
						minDeltaRPartonJet_4PartonSameJet_DeltaR0p4.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_4PartonSameJet_DeltaR0p4.Fill( jLists[0][1] )

			##### if a pair of two duplicates
			elif ( len( listDuplicatesDeltaR0p4 ) == 2 ) and ( numUniqueJetsDeltaR0p4 == 2 ):
				#print '5', jLists[0], jLists[1]
				numberPartonsSameJet_DeltaR0p4.Fill( 4 )
				for jparton, jLists in dictDeltaR0p4.iteritems():
					#print jLists[1][0], listDuplicates
					if ( listDuplicatesDeltaR0p4[0] == jLists[1][0] ):
						minDeltaRPartonJet_Pair2PartonSameJet_DeltaR0p4_A.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_Pair2PartonSameJet_DeltaR0p4_A.Fill( jLists[0][1] )
					if ( listDuplicatesDeltaR0p4[1] == jLists[1][0] ):
						minDeltaRPartonJet_Pair2PartonSameJet_DeltaR0p4_B.Fill( jLists[0][0] )
						secMinDeltaRPartonJet_Pair2PartonSameJet_DeltaR0p4_B.Fill( jLists[0][1] )

				tmpStopA = ( listP4Jets[ listDuplicatesDeltaR0p4[0] ] ).M()
				invMass_Pair2PartonSameJet_DeltaR0p4_Merged.Fill( tmpStopA )
				tmpStopB = ( listP4Jets[ listDuplicatesDeltaR0p4[1] ] ).M()
				invMass_Pair2PartonSameJet_DeltaR0p4_Merged.Fill( tmpStopB )
				#print 'Pair 2 jet merged : ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
				#print 'stopA ', tmpStopA
				#print 'stopB ', tmpStopB

			##### in case I forgot some category
			else:
				#print '6', jLists[0], jLists[1]
				numberPartonsSameJet_DeltaR0p4.Fill( 5 )

		##### if 3 jets after delta cut
		elif len( tmpListJetIndexDeltaR0p4 ) == 3:		
			##### if no duplicates
			if ( len( listDuplicatesDeltaR0p4 ) == 0 ) and ( numUniqueJetsDeltaR0p4 == 3 ):
				#print '7', jLists[0], jLists[1]
				numberPartonsSameJet_DeltaR0p4.Fill( 6 )

			##### if one duplicate and 1 different
			elif ( len( listDuplicatesDeltaR0p4 ) == 1 ) and ( numUniqueJetsDeltaR0p4 == 2 ):
				#print '8', jLists[0], jLists[1]
				numberPartonsSameJet_DeltaR0p4.Fill( 7 )

			##### if one duplicate and 1 different
			elif ( len( listDuplicatesDeltaR0p4 ) == 1 ) and ( numUniqueJetsDeltaR0p4 == 1 ):
				#print '9', jLists[0], jLists[1]
				numberPartonsSameJet_DeltaR0p4.Fill( 8 )

			##### in case I forgot some category
			else:
				#print '10', jLists[0], jLists[1]
				numberPartonsSameJet_DeltaR0p4.Fill( 9 )

		##### if 2 jets after delta cut
		elif len( tmpListJetIndexDeltaR0p4 ) == 2:		
			##### if no duplicates
			if ( len( listDuplicatesDeltaR0p4 ) == 0 ) and ( numUniqueJetsDeltaR0p4 == 2 ):
				#print '11', jLists[0], jLists[1]
				numberPartonsSameJet_DeltaR0p4.Fill( 10 )

			##### if one duplicate and 1 different
			elif ( len( listDuplicatesDeltaR0p4 ) == 1 ) and ( numUniqueJetsDeltaR0p4 == 1 ):
				#print '12', jLists[0], jLists[1]
				numberPartonsSameJet_DeltaR0p4.Fill( 11 )

			##### in case I forgot some category
			else:
				#print '13', jLists[0], jLists[1]
				numberPartonsSameJet_DeltaR0p4.Fill( 12 )

		##### if 1 jets after delta cut
		elif len( tmpListJetIndexDeltaR0p4 ) == 1:		
			#print '14', jLists[0], jLists[1]
			numberPartonsSameJet_DeltaR0p4.Fill( 13 )

		###### no jets after delta cut
		else:
			#print '15', jLists[0], jLists[1]
			numberPartonsSameJet_DeltaR0p4.Fill( 15 )


################################################################# Other way to categorize
#		if 2 in listRepDeltaR0p4: 								##### if at least two index are repeated 
#			if len( listRepDeltaR0p4 ) == 1: 							##### 2 partons in the only match jet identified
#				print '1', tmpListJetIndexDeltaR0p4, listRepDeltaR0p4
#				numberPartonsSameJet_DeltaR0p4.Fill( 1 )
#				for i,listParton in dictDeltaR0p4.iteritems(): 
#					minDeltaRPartonJet_2PartonSameJet_DeltaR0p4.Fill( listParton[1][0] )
#					secMinDeltaRPartonJet_2PartonSameJet_DeltaR0p4.Fill( listParton[1][1] )
#
#			elif ( len( listRepDeltaR0p4 ) == 2 ) and ( len(tmpListJetIndexDeltaR0p4) == 3): 	##### 2 partons in one match jet and 1 extra match jet
#				print '2', tmpListJetIndexDeltaR0p4, listRepDeltaR0p4
#				numberPartonsSameJet_DeltaR0p4.Fill( 2 )
#			elif ( len( listRepDeltaR0p4 ) == 2 ) and ( len(tmpListJetIndexDeltaR0p4) == 4):	##### a pair of 2 partons in one match jet
#				print '3', tmpListJetIndexDeltaR0p4, listRepDeltaR0p4
#				numberPartonsSameJet_DeltaR0p4.Fill( 3 )
#			elif ( len( listRepDeltaR0p4 ) == 3 ):							##### 2 partons in one match jet and 2 extra match jet
#				print '4', tmpListJetIndexDeltaR0p4, listRepDeltaR0p4
#				numberPartonsSameJet_DeltaR0p4.Fill( 4 )
#		elif ( len( listRepDeltaR0p4 ) == 0 ): 							##### if there are no match jets
#			print '6', tmpListJetIndexDeltaR0p4, listRepDeltaR0p4
#			numberPartonsSameJet_DeltaR0p4.Fill( 6 )
#		else: 											###### no repeated index
#			print '5', tmpListJetIndexDeltaR0p4, listRepDeltaR0p4
#			numberPartonsSameJet_DeltaR0p4.Fill( 0 )
##############################################################################################################







#		if len(appearancesDeltaR0p4) == 1 : 			###### 4 partons with same jet
#			numberPartonsSameJet_DeltaR0p4.Fill( 4 )
#			#print '4 partons with same jet: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
#			for i,listParton in dictDeltaR0p4.iteritems(): 
#				minDeltaRPartonJet_4PartonSameJet_DeltaR0p4.Fill( listParton[1][0] )
#		elif len(appearancesDeltaR0p4) == 2 : 
#			for i, k in appearancesDeltaR0p4.iteritems():
#				if k == 2: 			###### 2 partons with same jet
#					numberPartonsSameJet_DeltaR0p4.Fill( 2 )
#					#print dictDeltaR0p4
#					#print '2 partons with same jet: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
#					for i,listParton in dictDeltaR0p4.iteritems(): 
#						minDeltaRPartonJet_2PartonSameJet_DeltaR0p4.Fill( listParton[1][0] )
#						secMinDeltaRPartonJet_2PartonSameJet_DeltaR0p4.Fill( listParton[1][1] )
#					break
#				else: 				###### 3 partons with same jet
#					numberPartonsSameJet_DeltaR0p4.Fill( 3 )
#					#print '3 partons with same jet: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
#					for i,listParton in dictDeltaR0p4.iteritems(): 
#						minDeltaRPartonJet_3PartonSameJet_DeltaR0p4.Fill( listParton[1][0] )
#						secMinDeltaRPartonJet_3PartonSameJet_DeltaR0p4.Fill( listParton[1][1] )
#					break
#		elif len(appearancesDeltaR0p4) == 3: 			###### 2 partons with same jet + 2 diff
#			numberPartonsSameJet_DeltaR0p4.Fill( 1 )
#			#print '2 partons with same jet + 2 diff: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
#			for i,listParton in dictDeltaR0p4.iteritems(): 
#				minDeltaRPartonJet_2PartonSameJetPlus2Diff_DeltaR0p4.Fill( listParton[1][0] )
#				secMinDeltaRPartonJet_2PartonSameJetPlus2Diff_DeltaR0p4.Fill( listParton[1][1] )
#		elif len(appearancesDeltaR0p4) == 4: 			###### 4 diff jets
#			numberPartonsSameJet_DeltaR0p4.Fill( 0 )
#			#print '4 diff: ', str(Run)+':'+str(Lumi)+':'+str(NumEvent)
#			for i,listParton in dictDeltaR0p4.iteritems(): 
#				minDeltaRPartonJet_4Diff_DeltaR0p4.Fill( listParton[1][0] )
#		else:						###### something wrong (like no jets)
#			numberPartonsSameJet_DeltaR0p4.Fill( 6 )

		#listJetIndex = [ listMatching[2] for q, listMatching in dictDeltaR.iteritems() if ( len(listMatching) > 1 )]
		#print listJetIndex, len( listJetIndex )









		#####################################################
#		listMatchJets = []
#		if ( len(listJetIndex) > 1 ) and ( len( listJetIndex ) == len( set( listJetIndex ) ) ) : 	#### check for duplicates
#			for t in listJetIndex:
#				listMatchJets.append( listP4Jets[t]  )
#				#print t, listP4Jets[t].Pt()
#			massStopA = (listMatchJets[0] + listMatchJets[1]).M()
#			massStopB = (listMatchJets[2] + listMatchJets[3]).M()
#			print massStopA, massStopB
#
#		else:
#			print 'NOOOOOOOOOOOOOOOOO'
#		for z in range( len( listMatchJets ) ) : print z, listMatchJets[z].Pt()



		#print listMatchJets
			#numMatchJets = len( set( listJetIndex ))
		#print numMatchJets
	################################################################################################## end event loop

	##### write output file 
	outputFile.cd()
	outputFile.Write()

	##### Closing
	print 'Writing output file: '+sample + '_Matching_Plots.root'
	outputFile.Close()


	###### Extra: send prints to file
	sys.stdout = outfileStdOut
	f.close()
	#########################


#################################################################################
if __name__ == '__main__':

	mass = sys.argv[1]
	sample = 'stop_UDD312_'+str(mass)
	#list = os.popen('ls -1 /cms/gomez/Substructure/Generation/Simulation/CMSSW_5_3_2_patch4/src/mySimulations/stop_UDD312_50/aodsim/*.root').read().splitlines()
	list = os.popen('ls -1 /cms/gomez/Stops/st_jj/AOD/'+sample+'/*.root').read().splitlines()
	outputList = [i if i.startswith('file') else 'file:' + i for i in list]
	outputDir = '/cms/gomez/Stops/st_jj/MCTruth/Plots/'
	#print outputList[:10]

	get_info( outputList, outputDir, sample )

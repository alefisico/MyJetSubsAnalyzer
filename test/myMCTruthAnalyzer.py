#!/usr/bin/env python

from ROOT import * 
from math import *
from array import array
from numpy import mean
import optparse, os

gROOT.Reset()

###############################################################
### My Analyzer                                           #####
###############################################################
def myMCTruthAnalyzer( inputF, outputDir, outputDileName ):
	"""take tree from inputDir and fill histograms"""

	######## Variables for MyAnalyzer
	dictHistos = {}
	#dictHistos[ 'dummyNum' ] = [ 'nameVariable',  Minimum,  Maximum, nBins ]
	dictHistos[ 0 ]  = [ 'numberStops',		0.,	5.,	5]
	dictHistos[ 1 ]  = [ 'numberPartonStopA',	0.,	5.,	5]
	dictHistos[ 2 ]  = [ 'numberPartonStopB',	0.,	5.,	5]
	dictHistos[ 3 ]  = [ 'numberPartonsFromStop',	0.,	6.,	6]

	dictStopsHistos = {}
	dictStopsHistos[ 0 ]  = [ 'ptStops',	      	0.,	200.,	40]
	dictStopsHistos[ 1 ]  = [ 'etaStops',	   	-5.,	5.,	40]
	dictStopsHistos[ 2 ]  = [ 'massStops',	     	0.,	100.,	100]
	dictStopsHistos[ 3 ]  = [ 'phiStops',	   	-3.14,	3.14,	35] 
	dictStopsHistos[ 4 ]  = [ 'invMassPartonsFromStop',   	0.,	100.,	100]

	dictStopAHistos = {}
	dictStopAHistos[ 0 ]  = [ 'ptPartonsFromStopA',     	0.,	200.,	40]
	dictStopAHistos[ 1 ]  = [ 'etaPartonsFromStopA',  	-5.,	5.,	40]
	dictStopAHistos[ 2 ]  = [ 'phiPartonsFromStopA',  	-3.14, 	3.14,	35]
	dictStopAHistos[ 3 ]  = [ 'massPartonsFromStopA',    	0.,	100.,	100]

	dictStopBHistos = {}
	dictStopBHistos[ 0 ] = [ 'ptPartonsFromStopB',     	0.,	200.,	40]
	dictStopBHistos[ 1 ] = [ 'etaPartonsFromStopB',  	-5.,	5.,	40]
	dictStopBHistos[ 2 ] = [ 'phiPartonsFromStopB',  	-3.14, 	3.14,	35]
	dictStopBHistos[ 3 ] = [ 'massPartonsFromStopB',    	0.,	100.,	100]

	dictPartonsStopHistos = {}
	dictPartonsStopHistos[ 0 ] = [ 'ptTotalPartonsFromStop',     	0.,	200.,	40]
	dictPartonsStopHistos[ 1 ] = [ 'etaTotalPartonsFromStop',  	-5.,	5.,	40]
	dictPartonsStopHistos[ 2 ] = [ 'phiTotalPartonsFromStop',  	-3.14, 	3.14,	35]
	dictPartonsStopHistos[ 3 ] = [ 'massTotalPartonsFromStop',    	0.,	100.,	100]

	sorted( dictHistos.keys() )

	inputFile = TFile.Open( inputF )
	print 'Reading the input file: '+inputFile.GetName()
	##### create the output file 
	outputFile = TFile( outputDir + sample + '_plots.root', 'RECREATE' )


	##### create the histograms
	histosVar      = []
	histosStopsVar = []
	histosStopAVar = []
	histosStopBVar = []
	histosPartonsStopVar = []

	for i,listEvent in dictHistos.iteritems():
		h = TH1F('h_'+listEvent[0],'h_'+listEvent[0], listEvent[3], listEvent[1], listEvent[2] )
		h.Sumw2()
		histosVar.append(h)

	for i,listEvent in dictStopsHistos.iteritems():
		h = TH1F('h_'+listEvent[0],'h_'+listEvent[0], listEvent[3], listEvent[1], listEvent[2] )
		h.Sumw2()
		histosStopsVar.append(h)

	for i,listEvent in dictStopAHistos.iteritems():
		h = TH1F('h_'+listEvent[0],'h_'+listEvent[0], listEvent[3], listEvent[1], listEvent[2] )
		h.Sumw2()
		histosStopAVar.append(h)

	for i,listEvent in dictStopBHistos.iteritems():
		h = TH1F('h_'+listEvent[0],'h_'+listEvent[0], listEvent[3], listEvent[1], listEvent[2] )
		h.Sumw2()
		histosStopBVar.append(h)

	for i,listEvent in dictPartonsStopHistos.iteritems():
		h = TH1F('h_'+listEvent[0],'h_'+listEvent[0], listEvent[3], listEvent[1], listEvent[2] )
		h.Sumw2()
		histosPartonsStopVar.append(h)

	##### get the tree 
	events = inputFile.Get('MCTruthAna/mcTruthTree')

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

		dictHistosVar = {}
		dictHistosVar[0] = events.numStops
		dictHistosVar[1] = events.numPartonsStopA
		dictHistosVar[2] = events.numPartonsStopB
		dictHistosVar[3] = events.numPartonsStopB + events.numPartonsStopA

		#### Storing jets in TL
		partonStopAP4 = []
		for k in range( events.numPartonsStopA ):
			tmpTL = TLorentzVector()
			tmpTL.SetPtEtaPhiE( events.stopAPt[k], events.stopAEta[k], events.stopAPhi[k], events.stopAEnergy[k] ) 
			partonStopAP4.append( tmpTL )

		partonStopBP4 = []
		for k in range( events.numPartonsStopB ):
			tmpTL = TLorentzVector()
			tmpTL.SetPtEtaPhiE( events.stopBPt[k], events.stopBEta[k], events.stopBPhi[k], events.stopBEnergy[k] ) 
			partonStopBP4.append( tmpTL )

		totalPartonsStopsP4 = partonStopAP4 + partonStopBP4

		invMass = [ ( totalPartonsStopsP4[0] + totalPartonsStopsP4[1] ).M() , ( totalPartonsStopsP4[2] + totalPartonsStopsP4[3] ).M() ]
		for j in range( events.numStops ):
			dictStopsHistosVar = {}
			dictStopsHistosVar[0] = events.stopsPt[j] 
			dictStopsHistosVar[1] = events.stopsEta[j]
			dictStopsHistosVar[2] = events.stopsMass[j]
			dictStopsHistosVar[3] = events.stopsPhi[j]
			dictStopsHistosVar[4] = invMass[j]

			sorted( dictStopsHistosVar.keys() )
			for k, var in dictStopsHistosVar.iteritems():
				histosStopsVar[k].Fill( var )
			#print i, events.stopsPt[i], events.stopsMass[i]

		####### Filling Histos
		for q in range( len( partonStopAP4 ) ):
			dictStopAHistosVar = {}
			dictStopAHistosVar[0]  = partonStopAP4[q].Pt()
			dictStopAHistosVar[1]  = partonStopAP4[q].Eta()
			dictStopAHistosVar[2] = partonStopAP4[q].Phi()
			dictStopAHistosVar[3] = partonStopAP4[q].M()

			sorted( dictStopAHistosVar.keys() )
			for k, var in dictStopAHistosVar.iteritems():
				histosStopAVar[k].Fill( var )

		for w in range( len( partonStopBP4 ) ):
			dictStopBHistosVar = {}
			dictStopBHistosVar[0] = partonStopBP4[w].Pt()
			dictStopBHistosVar[1] = partonStopBP4[w].Eta()
			dictStopBHistosVar[2] = partonStopBP4[w].Phi()
			dictStopBHistosVar[3] = partonStopBP4[w].M()

			sorted( dictStopBHistosVar.keys() )
			for k, var in dictStopBHistosVar.iteritems():
				histosStopBVar[k].Fill( var )

		for z in range( len( totalPartonsStopsP4 ) ):
			dictPartonsStopHistosVar = {}
			dictPartonsStopHistosVar[0] = totalPartonsStopsP4[z].Pt()
			dictPartonsStopHistosVar[1] = totalPartonsStopsP4[z].Eta()
			dictPartonsStopHistosVar[2] = totalPartonsStopsP4[z].Phi()
			dictPartonsStopHistosVar[3] = totalPartonsStopsP4[z].M()

			sorted( dictPartonsStopHistosVar.keys() )
			for k, var in dictPartonsStopHistosVar.iteritems():
				histosPartonsStopVar[k].Fill( var )


		sorted( dictHistosVar.keys() )
		for k, var in dictHistosVar.iteritems():
			histosVar[k].Fill( var )

	##### write output file 
	outputFile.cd()
	outputFile.Write()

	##### Closing
	print 'Writing output file: '+outputFile.GetName()
	outputFile.Close()
  
#########################################################################################
if __name__ == '__main__':

	listSamples = [ 'stopUDD312_50' ]

	outputDir = '/cms/gomez/Stops/st_jj/MCTruth/Plots/'

	for sample in listSamples: 

		inputDir = '/cms/gomez/Stops/st_jj/MCTruth/rootFiles/'
		inputName = sample+'_MCTruth_plots.root'
		inputFile = inputDir + inputName

		myMCTruthAnalyzer( inputFile, outputDir, sample )


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
def myAnalyzer( inputList, outputDir, outputDileName, typeJet ):
	"""take tree from inputDir and fill histograms"""

	########################## for my records
	#*Br   22 :jetChf    : vector<float>                                          *
	#*Br   23 :jetNhf    : vector<float>                                          *
	#*Br   24 :jetPhf    : vector<float>                                          *
	#*Br   25 :jetMuf    : vector<float>                                          *
	#*Br   26 :jetElf    : vector<float>                                          *
	#######################################################################

	######## Variables for MyAnalyzer
	dictEvent = {}
	#dictEvent[ 'dummyNum' ] = [ 'nameVariable',  Minimum,  Maximum, nBins ]
	dictEvent[ 0 ]  = [ 'ht',  		0.,  	500.,   100]
	dictEvent[ 1 ]  = [ 'mjj',		0.,	500.,	100]
	dictEvent[ 2 ]  = [ 'dEtajj',		0.,	5.,	100]
	dictEvent[ 3 ]  = [ 'dPhijj',		0.,	pi,	100]
	dictEvent[ 4 ]  = [ 'metOvSumEt',	0.,	0.2,	40]
	dictEvent[ 5 ]  = [ 'numJets',		0.,	10.,	10]
	dictEvent[ 6 ]  = [ 'numPV',		0.,	50.,	50]
	dictEvent[ 7 ]  = [ 'MET',		0.,	200.,	40]
	dictEvent[ 8 ]  = [ 'jet1Tau1', 	0.,	1.,	40]
	dictEvent[ 9 ]  = [ 'jet2Tau1',		0.,	1.,	40]
	dictEvent[ 10 ] = [ 'jet1Tau2',		0.,	1.,	40]
	dictEvent[ 11 ] = [ 'jet2Tau2',		0.,	1.,	40]
	dictEvent[ 12 ] = [ 'jet1Tau3',		0.,	1.,	40]
	dictEvent[ 13 ] = [ 'jet2Tau3',		0.,	1.,	40]
	dictEvent[ 14 ] = [ 'jet1Area',		0.,	1.5,	60]
	dictEvent[ 15 ] = [ 'jet2Area',		0.,	1.5,	60]
	dictEvent[ 16 ] = [ 'jet1numConst',	0.,	50.,	50]
	dictEvent[ 17 ] = [ 'jet2numConst',	0.,	50.,	50]
	dictEvent[ 18 ] = [ 'jet1Tau21',	0.,	1.,	100]
	dictEvent[ 19 ] = [ 'jet1Tau32',	0.,	1.,	100]
	dictEvent[ 20 ] = [ 'jet1Tau31',	0.,	1.,	100]
	dictEvent[ 21 ] = [ 'jet2Tau21',	0.,	1.,	100]
	dictEvent[ 22 ] = [ 'jet2Tau32',	0.,	1.,	100]
	dictEvent[ 23 ] = [ 'jet2Tau31',	0.,	1.,	100]
	dictEvent[ 24 ] = [ 'jet1Mass',		0.,	100.,	50]
	dictEvent[ 25 ] = [ 'jet2Mass',		0.,	100.,	50]
	dictEvent[ 26 ] = [ 'jet1MassPruned',	0.,	100.,	50]
	dictEvent[ 27 ] = [ 'jet2MassPruned',	0.,	100.,	50]
	dictEvent[ 28 ] = [ 'avgJetPt',      	0.,	200.,	40]

	dictJet = {}
	dictJet[ 0 ]  = ['jetPt', 		0.,	500.,	100]
	dictJet[ 1 ]  = ['jetEta',		-5.,	5.,	100]
	dictJet[ 2 ]  = ['jetPhi',		-pi,	pi,	100]
	dictJet[ 3 ]  = ['jetMass',		0.,	100.,	50]
	dictJet[ 4 ]  = ['jetMassPruned',	0.,	100.,	50]
	dictJet[ 5 ]  = ['jetArea',		0.,	1.5,	30]
	dictJet[ 6 ]  = ['jetTau1',		0.,	1.,	100]
	dictJet[ 7 ]  = ['jetTau2',		0.,	1.,	100]
	dictJet[ 8 ]  = ['jetTau3',		0.,	1.,	100]
	dictJet[ 9 ]  = ['jetTau21',		0.,	1.,	100]
	dictJet[ 10 ] = ['jetTau31',		0.,	1.,	100]
	dictJet[ 11 ] = ['jetTau32',		0.,	1.,	100]

	sorted( dictEvent.keys() )
	sorted( dictJet.keys() )

	#inputFile = TFile.Open( inputDir + inputFileName )
	#print 'Reading the input file: '+inputFile.GetName()
	##### create the output file 
	outputFile = TFile( outputDir + sample + '_plots.root', 'RECREATE' )

	###### Loop over different Jet algorithms
	for type in typeJet:

		##### create the histograms
		histEventVar    = []
		histJetVar      = []
		histEventVarSub = []
		histJetVarSub   = []

		for i,listEvent in dictEvent.iteritems():
			h = TH1F('h_'+listEvent[0]+'_'+type,'h_'+listEvent[0]+'_'+type, listEvent[3], listEvent[1], listEvent[2] )
			h.Sumw2()
			histEventVar.append(h)
			#hSub = TH1F('h_sub_'+i,'h_sub_'+i,eventVarBins[k],eventVarMin[k],eventVarMax[k]) 
			#hSub.Sumw2()
			#histEventVarSub.append(hSub)

		for i,listJet in dictJet.iteritems():
			h = TH1F('h_'+listJet[0]+'_'+type,'h_'+listJet[0]+'_'+type, listJet[3], listJet[1], listJet[2] )
			h.Sumw2()
			histJetVar.append(h)
			#hSub = TH1F('h_sub_'+i,'h_sub_'+i,jetVarBins[k],jetVarMin[k],jetVarMax[k]) 
			#hSub.Sumw2()
			#histJetVarSub.append(hSub)

		##### get the tree 
		events = TChain( 'dijets_'+type+'/events' )
		# Loop over the filenames and add to tree.
		for filename in inputList:
			print("Adding file: " + filename)
			events.Add(filename)
		#events = inputFile.Get('dijets_'+type+'/events')

		##### read the tree & fill histosgrams -
		numEntries = events.GetEntries()
		print 'Jet Algorithm processing: '+type, '------> Number of events: '+str(numEntries)
		d = 0

		for i in xrange(numEntries):
			events.GetEntry(i)

			#---- progress of the reading --------
			fraction = 10.*i/(1.*numEntries)
			if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
			d = TMath.FloorNint(fraction)

		#	######################################################################################
		#	###### From the Jet Substructure exercise... 
		#	cut_trigger      = True 
		#	cut_mass         = True
		#	cut_dEtajj       = events.dEtajj < 1.3
		#	cut_leptonVeto   = events.jetElf[0]<0.7 and events.jetElf[1]<0.7 and events.jetMuf[0]<0.7 and events.jetMuf[1]<0.7
		#	cut_eta          = fabs(events.jetEta[0])<2.5 and fabs(events.jetEta[1])<2.5
		#	cut_pt           = events.jetPt[1]>40
		#	cut_substructure = (
		#			events.jetMassPruned[0] > 60 and 
		#			events.jetMassPruned[0] < 100 and 
		#			events.jetMassPruned[1] > 60 and 
		#			events.jetMassPruned[1] < 100 and 
		#			events.jetTau2[0]/events.jetTau1[0] < 0.5 and 
		#			events.jetTau2[1]/events.jetTau1[1] < 0.5)
		#
		#	if (cut_dEtajj and cut_mass and cut_leptonVeto and cut_eta and cut_pt):
		#		#---- set the event variables ----
		#		eventVar = [events.ht,events.mjj,events.dEtajj,events.dPhijj,events.metSig]
		#		for k in xrange(len(histEventVar)):
		#			histEventVar[k].Fill(eventVar[k])
		#			if cut_substructure:
		#				histEventVarSub[k].Fill(eventVar[k])
		#		for j in xrange(2):
		#			#---- set the jet variables ----
		#			jetVar = [events.jetTau2[j]/events.jetTau1[j],events.jetPt[j],events.jetEta[j],events.jetPhi[j],events.jetMass[j],events.jetMassPruned[j]]
		#			for k in xrange(len(histJetVar)):
		#				histJetVar[k].Fill(jetVar[k])
		#				if cut_substructure:
		#					histJetVarSub[k].Fill(jetVar[k])
		#	##########################################################################################

			#### Storing jets in TL
			jetP4 = [ TLorentzVector( events.jetPt[i], events.jetEta[i], events.jetPhi[i], events.jetEnergy[i] ) for i in range( events.nJets ) ]
			for nJet in range( events.nJets ):
				cut_pt  = events.jetPt[nJet] > 40 
				cut_eta = abs( events.jetEta[nJet] ) < 2.5

			#if ( cut_pt and cut_eta ):

			#---- set the event variables ----
			dictEventVar = {}
			dictEventVar[ 4 ]  = events.metSig
			dictEventVar[ 5 ]  = events.nJets
			dictEventVar[ 6 ]  = events.nvtx
			dictEventVar[ 7 ]  = events.met

			if events.nJets > 0:
				dictEventVar[ 0 ]  = sum( [ events.jetPt[i] for i in range( events.nJets ) ] )
				dictEventVar[ 8 ]  = events.jetTau1[0]
				dictEventVar[ 10 ] = events.jetTau2[0]
				dictEventVar[ 12 ] = events.jetTau3[0]
				dictEventVar[ 14 ] = events.jetArea[0]
				dictEventVar[ 16 ] = events.numJetConstituent[0]
				if events.jetTau1[0] != 0 : dictEventVar[ 18 ] = events.jetTau2[0]/events.jetTau1[0]
				if events.jetTau2[0] != 0 : dictEventVar[ 19 ] = events.jetTau3[0]/events.jetTau2[0]
				if events.jetTau1[0] != 0 : dictEventVar[ 20 ] = events.jetTau3[0]/events.jetTau1[0]
				dictEventVar[ 24 ] = events.jetMass[0]
				dictEventVar[ 26 ] = events.jetMassPruned[0]
				dictEventVar[ 28 ] = mean( [ events.jetPt[i] for i in range( events.nJets ) ] )
			else:
				dictEventVar[ 0 ]  = -999
				dictEventVar[ 8 ]  = -999
				dictEventVar[ 10 ] = -999
				dictEventVar[ 12 ] = -999
				dictEventVar[ 14 ] = -999
				dictEventVar[ 16 ] = -999
				dictEventVar[ 18 ] = -999
				dictEventVar[ 19 ] = -999
				dictEventVar[ 20 ] = -999
				dictEventVar[ 24 ] = -999
				dictEventVar[ 26 ] = -999
				dictEventVar[ 28 ] = -999

			if events.nJets > 1 :
				dictEventVar[ 1 ]  = ( jetP4[0] + jetP4[1] ).M()
				dictEventVar[ 2 ]  = abs( jetP4[0].Eta() - jetP4[1].Eta() )
				dictEventVar[ 3 ]  = abs( jetP4[0].DeltaPhi( jetP4[1] ) )
				dictEventVar[ 9 ]  = events.jetTau1[1]
				dictEventVar[ 11 ] = events.jetTau2[1]
				dictEventVar[ 13 ] = events.jetTau3[1]
				dictEventVar[ 15 ] = events.jetArea[1]
				dictEventVar[ 17 ] = events.numJetConstituent[1]
				if events.jetTau1[1] != 0 : dictEventVar[ 21 ] = events.jetTau2[1]/events.jetTau1[1]
				if events.jetTau2[1] != 0 : dictEventVar[ 22 ] = events.jetTau3[1]/events.jetTau2[1]
				if events.jetTau1[1] != 0 : dictEventVar[ 23 ] = events.jetTau3[1]/events.jetTau1[1]
				dictEventVar[ 25 ] = events.jetMass[1]
				dictEventVar[ 27 ] = events.jetMassPruned[1]
			else:
				dictEventVar[ 1 ]  = -999
				dictEventVar[ 2 ]  = -999
				dictEventVar[ 3 ]  = -999
				dictEventVar[ 9 ]  = -999
				dictEventVar[ 11 ] = -999
				dictEventVar[ 13 ] = -999
				dictEventVar[ 15 ] = -999
				dictEventVar[ 17 ] = -999
				dictEventVar[ 21 ] = -999
				dictEventVar[ 22 ] = -999
				dictEventVar[ 23 ] = -999
				dictEventVar[ 25 ] = -999
				dictEventVar[ 27 ] = -999

			sorted( dictEventVar.keys() )
			for k, var in dictEventVar.iteritems():
				histEventVar[k].Fill( var )


			for j in range( events.nJets ):
				#---- set the jet variables ----
				dictJetVar = {}
				dictJetVar[ 0 ]  = events.jetPt[j]
				dictJetVar[ 1 ]  = events.jetEta[j]
				dictJetVar[ 2 ]  = events.jetPhi[j]
				dictJetVar[ 3 ]  = events.jetMass[j]
				dictJetVar[ 4 ]  = events.jetMassPruned[j]
				dictJetVar[ 5 ]  = events.jetArea[j]
				dictJetVar[ 6 ]  = events.jetTau1[j]
				dictJetVar[ 7 ]  = events.jetTau2[j]
				dictJetVar[ 8 ]  = events.jetTau3[j]
				if events.jetTau1[j] != 0 : dictJetVar[ 9 ]  = events.jetTau2[j]/events.jetTau1[j]
				if events.jetTau1[j] != 0 : dictJetVar[ 10 ] = events.jetTau3[j]/events.jetTau1[j]
				if events.jetTau2[j] !=0 : dictJetVar[ 11 ] = events.jetTau3[j]/events.jetTau2[j]

				sorted( dictJetVar.keys() )
				for k, var in dictJetVar.iteritems():
					histJetVar[k].Fill( var )
					#if cut_substructure:
					#	histJetVarSub[k].Fill(jetVar[k])
					#print histJetVar[k]

		##### write output file 
		outputFile.cd()
		outputFile.Write()

	##### Closing
	print 'Writing output file: '+outputFile.GetName()
	outputFile.Close()
  
#########################################################################################
if __name__ == '__main__':

	#inputDir = '/cms/gomez/Stops/st_jj/patTuples/'
	listSamples = [ 'stopUDD312_50' ]
	### Directory in tree root file
	#typeJet = [ 'AK4', 'AK5', 'AK7', 'AK1p1' ] 
	typeJet = [ 'AK4', 'AK5', 'AK7', 'AK1p1', 'CA4', 'CA8', 'CA1p2', 'KT4' ] 

	outputDir = '/cms/gomez/Stops/st_jj/treeResults/'

	for sample in listSamples: 

		inputDir = '/cms/gomez/Stops/st_jj/patTuples/'+sample+'/results/'
		inputList = os.popen('ls -1v '+inputDir+'*.root').read().splitlines()
		#inputFileName = 'stopUDD312_ISR_upto2j_50_tree_test.root'
		#inputFileName = 'stopUDD312_50_0_tree.root'

		myAnalyzer( inputList, outputDir, sample, typeJet )

#	usage = "usage: %prog [options]"
#	parser = optparse.OptionParser(usage)
#	parser.add_option("--sample",action="store",type="string",dest="sample",default='RS2000')
#	parser.add_option("--trigger",action="store",type="string",dest="trigger",default='signal')
#	
#	(options, args) = parser.parse_args()
#	sample = options.sample
#	trigger = options.trigger
#	
#	trigger_options = ['signal','ref','refSig']
#	if trigger not in trigger_options:
#		print 'WARNING: the requested trigger option ('+trigger+') does not exist !!!'
#		print 'Available trigger options are: '+str(trigger_options)
#		print 'Forcing the default option: \"signal\"'
#		trigger = 'signal'

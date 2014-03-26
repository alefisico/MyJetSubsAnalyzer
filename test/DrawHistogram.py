#!/usr/bin/env python
'''
File: DrawHistogram.py
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Draw histograms. Check for options at the end.
'''

#from ROOT import TFile, TH1F, THStack, TCanvas, TMath, gROOT, gPad
from ROOT import *
from setTDRStyle import setTDRStyle, setSelectionTitle, setTitle
import time, os, math, sys
import tarfile
import optparse

gROOT.Reset()
gROOT.SetBatch()
setTDRStyle()
gROOT.ForceStyle()
gROOT.SetStyle('tdrStyle')

###### Trick for add date or month to plots
monthKey  =  time.strftime("%y%m")
dateKey   = time.strftime("%y%m%d")

###############################################################
###  Draw Histograms from final Tree (after selection)    #####
###############################################################
def analysisPlots():
	"""create Plots from Final selection"""

	Sample = 'stopUDD312_50'
	inputDir = '/cms/gomez/Stops/st_jj/treeResults/'
	outputDir = '/cms/gomez/Stops/st_jj/treeResults/Plots/'
	jetAlgoList = [ 'CA8', 'AK4' ]

	targetDir = outputDir + dateKey + '/'
	print 'Output directory: ', targetDir
	if not ( os.path.exists( targetDir ) ): os.makedirs( targetDir )
	tarFile = dateKey+"files.tar.gz"
	tar = tarfile.open( targetDir + tarFile, "w:gz")

	outputList = [] ### for format

	#---- open the files --------------------
	inputFile = TFile.Open( inputDir+Sample+'_plots.root' )
	print 'Drawing Histograms from: ', inputFile.GetName()

	for jetAlgo in jetAlgoList:
		for i, varList in dictHisto.iteritems():
		
			outputFileName = dateKey+'_'+varList[0]+'_'+jetAlgo+'.png'  
			print 'Processing.......', outputFileName
			outputFile = targetDir + outputFileName
			outputList.append( outputFileName )
			h = inputFile.Get('h_'+varList[0]+'_'+jetAlgo)
			#h.Scale(wt)
			#h.Rebin(rebin)
			#h.SetDirectory(0)
			#h.SetFillColor(colorF[i_f])
			#h.SetLineColor(colorL[i_f])
			#h.SetMarkerColor(colorL[i_f])
			#hist.append(h)
		   

		#NQCD = hist[0].Integral()+hist[1].Integral()
		#NDAT = hist[3].Integral()
		#kFactor = NDAT/NQCD
		#print kFactor
		#
		#hist[0].Scale(kFactor)
		#hist[1].Scale(kFactor)
		#
		#histQCD = hist[0].Clone('histQCD')
		#histQCD.Add(hist[1])
		#
		#hsQCD = THStack('QCD','QCD')
		#
		#hsQCD.Add(hist[0])
		#hsQCD.Add(hist[1])

			#----- Drawing -----------------------
			h.GetXaxis().SetTitle( varList[4] )
			h.GetYaxis().SetTitle( varList[5] )

			can = TCanvas('can_'+str(i),'can_'+str(i),800,500)
			h.Draw('HISTE')
			setSelectionTitle( Sample )
			can.SaveAs( outputFile )
			del can
		
			tar.add( outputFile, dateKey+'_'+varList[0]+'_'+jetAlgo+'.png' )

	tar.close()
	print 'Creating tar file with all plots named: ',  tarFile
	printHTML( outputList  )

			#if logy: gPad.SetLogy()
			#hAux = hist[3].Clone('aux')
			#hAux.Reset()
			#hAux.GetXaxis().SetRangeUser(xmin,xmax)
			#hAux.GetXaxis().SetTitle(xtitle)
			#hAux.SetMaximum(1.2*TMath.Max(hist[3].GetBinContent(hist[3].GetMaximumBin()),histQCD.GetBinContent(histQCD.GetMaximumBin())))
			#hAux.SetMinimum(0.01)
			#hAux.Draw()
			#hsQCD.Draw('same hist')
			#hist[3].Draw('same E')
			#hist[2].Draw('same hist')
			#gPad.RedrawAxis()
		    

##########################################################################
### Draw Histograms from List, create tar file and HTML code    #####
##########################################################################
def Draw( Sample, inputName, inputDir, outputName, outputDir, listHistos):
	"""create Plots from MCTruth"""

	targetDir = outputDir + dateKey + '/'
	print 'Output directory: ', targetDir
	if not ( os.path.exists( targetDir ) ): os.makedirs( targetDir )
	tarFile = dateKey+"files.tar.gz"
	tar = tarfile.open( targetDir + tarFile, "w:gz")

	outputList = [] ### for format
	#---- open the files --------------------
	inputFile = TFile.Open( inputDir+inputName+'.root' )
	print 'Drawing Histograms from: ', inputFile.GetName()

	for histoInfo in listHistos:
	
		outputFileName = dateKey+'_'+histoInfo[0]+'_'+outputName+'.png'  
		print 'Processing.......', outputFileName
		outputFile = targetDir + outputFileName
		outputList.append( outputFileName )
		h = inputFile.Get('h_'+histoInfo[0])
		#----- Drawing -----------------------
		h.GetXaxis().SetTitle( histoInfo[4] )
		h.GetYaxis().SetTitle( histoInfo[5] )
		if ( 'numberPartonsSameJet' in histoInfo[0] ):
			h.GetXaxis().SetBinLabel( 1 , '4Matched' )
			h.GetXaxis().SetBinLabel( 2 , '2Merged+2Match' )
			h.GetXaxis().SetBinLabel( 3 , 'Pair2Merged' )
			h.GetXaxis().SetBinLabel( 4 , '3Merged+1Match' )
			h.GetXaxis().SetBinLabel( 5 , '4Merged' )
			h.GetXaxis().SetBinLabel( 6 , '' )
			h.GetXaxis().SetBinLabel( 7 , 'less 4 Jets' )

		can = TCanvas('can_'+histoInfo[0],'can_'+histoInfo[0],800,500)
		h.Draw('HISTE')
		setTitle( Sample )
		can.SaveAs( outputFile )
		del can
	
		tar.add( outputFile, dateKey+'_'+histoInfo[0]+'_'+outputName+'.png' )

	tar.close()
	print 'Creating tar file with all plots named: ',  tarFile
	printHTML( outputList  )

##########################################################################
### Draw Histograms from List, create tar file and HTML code    #####
##########################################################################
def DrawCmp( Sample, inputDir, outputName, outputDir, listHistos, Algo1, Algo2):
	"""create Plots from MCTruth"""

	gStyle.SetOptStat(0)
	targetDir = outputDir + dateKey + '/'
	print 'Output directory: ', targetDir
	if not ( os.path.exists( targetDir ) ): os.makedirs( targetDir )
	tarFile = dateKey+"files_"+Sample+"_"+Algo1+"_"+Algo2+".tar.gz"
	tar = tarfile.open( targetDir + tarFile, "w:gz")

	outputList = [] ### for format
	#---- open the files --------------------
	inputFile1 = TFile.Open( inputDir+Sample+'_Matching_'+Algo1+'_Plots.root' )
	inputFile2 = TFile.Open( inputDir+Sample+'_Matching_'+Algo2+'_Plots.root' )
	print 'Drawing Histograms from: ', inputFile1.GetName(), 'and ', inputFile2.GetName()

	for histoInfo in listHistos:
	
		outputFileName = dateKey+'_'+histoInfo[0]+'_'+outputName+'_'+Algo1+'vs'+Algo2+'.png'  
		print 'Processing.......', outputFileName
		outputFile = targetDir + outputFileName
		outputList.append( outputFileName )
		print histoInfo[0]
		h1 = inputFile1.Get('h_'+histoInfo[0]+'_'+Algo1)
		h2 = inputFile2.Get('h_'+histoInfo[0]+'_'+Algo2)
		#----- Drawing -----------------------
		h1.GetXaxis().SetTitle( histoInfo[1] )
		binWidth = h1.GetBinWidth(1)
		h1.GetYaxis().SetTitle( histoInfo[2]+str(binWidth) )
		h1.SetLineColor(1)
		h2.SetLineColor(4)
		h1.SetMaximum(1.2*TMath.Max(h1.GetBinContent(h1.GetMaximumBin()),h2.GetBinContent(h2.GetMaximumBin())))

		legend=TLegend(0.75,0.70,0.90,0.85)
		#legend.SetFillColor(0);
		legend.AddEntry(h1, Algo1, "l")
		legend.AddEntry(h2, Algo2, "l")

		if ( 'numberPartonsSameJet' in histoInfo[0] ):
			h1.GetXaxis().SetBinLabel( 1 , '4Matched' )
			h1.GetXaxis().SetBinLabel( 2 , '2Merged+2Match' )
			h1.GetXaxis().SetBinLabel( 3 , 'Pair2Merged' )
			h1.GetXaxis().SetBinLabel( 4 , '3Merged+1Match' )
			h1.GetXaxis().SetBinLabel( 5 , '4Merged' )
			h1.GetXaxis().SetBinLabel( 6 , '' )
			h1.GetXaxis().SetBinLabel( 7 , 'less 4 Jets' )

		can = TCanvas('can_'+histoInfo[0],'can_'+histoInfo[0],800,500)
		if ( 'numberPartonsSameJet' in histoInfo[0] ): can.SetLogy()
		h1.Draw('histe ')
		h2.Draw('same histe')
		legend.Draw()
		setTitle( Sample )
		can.SaveAs( outputFile )
		del can
	
		tar.add( outputFile, outputFileName )

	tar.close()
	print 'Creating tar file with all plots named: ',  tarFile
	printHTML( outputList  )
	printLatex( outputList  )


###############################################################
###  Print histo name in HTML format                      #####
###############################################################
def printHTML( list ):

	print '#######################################################'
	print '#### HTML code (for easy upload)                  #####'
	print '#######################################################'
	print "<ul>"
	for histo in list: print "<li>", '<p><img src="%s"><br>' % histo
	print "</ul>"

###############################################################
###  Print histo name in latex format                     #####
###############################################################
def printLatex( list ):
	print '#######################################################'
	print '#### Latex code (for easy upload)                 #####'
	print '#######################################################'
	for histo in list: 
		print '\\begin{frame}{}'
		print '\\centerline{\includegraphics[scale=0.40]{%s}}' % histo
		print '\\end{frame}'
		print ''



########################################################
if __name__ == '__main__':

	usage = 'usage: %prog [options]'
	
	parser = optparse.OptionParser(usage=usage)
	parser.add_option( '-p', '--proc', action='store', type='string', dest='process', default='jetAlgoCmp', help='Type of plot' )
	parser.add_option( '-m', '--mass', action='store', type='string', dest='mass', default='50', help='Mass of the Stop' )
	parser.add_option( '-1', '--jetAlgo1', action='store', type='string', dest='jetAlgo1', default='AK5', help='Jet Algorithm 1' )
	parser.add_option( '-2', '--jetAlgo2', action='store', type='string', dest='jetAlgo2', default='AK7', help='Jet Algorithm 2' )

	(options, args) = parser.parse_args()

	mass = options.mass
	jetAlgo1 = options.jetAlgo1
	jetAlgo2 = options.jetAlgo2
	process = options.process

	dictHisto = {}
	dictHisto[ 0 ]  = ['jetPt', 		0.,	500.,	100,	'p_{T} [GeV]', 			'Jets / 5 [GeV]']
	dictHisto[ 1 ]  = ['jetEta',		-5.,	5.,	100,	'jet #eta',			'Jets / 0.1']
	dictHisto[ 2 ]  = ['jetPhi',		-3.14,	3.14,	100, 	'jet #phi',			'Jets / 0.03']
	dictHisto[ 3 ]  = ['jetMass',		0.,	100.,	50,	'jet Invariant Mass [Gev]',	'Jets / 2 [GeV]']
	dictHisto[ 4 ]  = ['jetMassPruned',	0.,	100.,	50, 	'jet Invariant Mass [Gev]',	'Jets / 2 [GeV]']
	dictHisto[ 5 ]  = ['jetArea',		0.,	5., 	50,	'jet Area',			'Jets / 0.1']
	dictHisto[ 6 ]  = ['jetTau1',		0.,	1.,	100,	'jet #tau_{1}',			'Jets / 0.01']
	dictHisto[ 7 ]  = ['jetTau2',		0.,	1.,	100,	'jet #tau_{2}',			'Jets / 0.01']
	dictHisto[ 8 ]  = ['jetTau3',		0.,	1.,	100,	'jet #tau_{3}',			'Jets / 0.01']
	dictHisto[ 9 ]  = ['jetTau21',		0.,	1.,	100,	'jet #tau_{2} / #tau_{1}',	'Jets / 0.01']
	dictHisto[ 10 ] = ['jetTau31',		0.,	1.,	100,	'jet #tau_{3} / #tau_{1}',	'Jets / 0.01']
	dictHisto[ 11 ] = ['jetTau32',		0.,	1.,	100,	'jet #tau_{3} / #tau_{2}',	'Jets / 0.01']
	dictHisto[ 12 ] = [ 'ht',  		0.,  	500.,   100, 	'HT [GeV]',			'Events / 5 [GeV]']
	dictHisto[ 13 ] = [ 'mjj',		0.,	500.,	100,	'Dijet (1j,2j) Invariant Mass [GeV]', 'Events / 5 [GeV]']
	dictHisto[ 14 ] = [ 'dEtajj',		0.,	5.,	100,	'#Delta #eta (1j,2j)',		'Events / 0.05']
	dictHisto[ 15 ] = [ 'dPhijj',		0.,	3.14,	100,	'#Delta #phi (1j,2j)',		'Events / 0.03']
	dictHisto[ 16 ] = [ 'metOvSumEt',	0.,	0.2,	40, 	'MET / #sum Et',		'Events / 0.005']
	dictHisto[ 17 ] = [ 'numJets',		0.,	10.,	10, 	'Number of jets',		'Events / 1']
	dictHisto[ 18 ] = [ 'numPV',		0.,	50.,	50,	'Number of Primary Vertex',	'Events / 1']
	dictHisto[ 19 ] = [ 'MET',		0.,	200.,	40,	'MET [GeV]',			'Events / 5 [GeV]']
	dictHisto[ 20 ] = [ 'jet1Tau1', 	0.,	1.,	40,	'Leading Jet #tau_1',		'Events / 0.025']
	dictHisto[ 21 ] = [ 'jet2Tau1',		0.,	1.,	40,	'2nd Leading Jet #tau_1',	'Events / 0.025']
	dictHisto[ 22 ] = [ 'jet1Tau2',		0.,	1.,	40,	'Leading Jet #tau_2',		'Events / 0.025']
	dictHisto[ 23 ] = [ 'jet2Tau2',		0.,	1.,	40,	'2nd Leading Jet #tau_2',	'Events / 0.025']
	dictHisto[ 24 ] = [ 'jet1Tau3',		0.,	1.,	40,	'Leading Jet #tau_3',		'Events / 0.025']
	dictHisto[ 25 ] = [ 'jet2Tau3',		0.,	1.,	40,	'2nd Leading Jet #tau_3',	'Events / 0.025']
	dictHisto[ 26 ] = [ 'jet1Area',		0.,	5., 	50,	'Leading Jet Area',		'Events / 0.1']
	dictHisto[ 27 ] = [ 'jet2Area',		0.,	5., 	50,	'2nd Leading Jet Area',		'Events / 0.1']
	dictHisto[ 28 ] = [ 'jet1numConst',	0.,	50.,	50, 	'Number of Constituents Leading Jet',	'Events / 1']
	dictHisto[ 29 ] = [ 'jet2numConst',	0.,	50.,	50, 	'Number of Constituents 2nd Leading Jet','Events / 1']
	dictHisto[ 30 ] = [ 'jet1Tau21',	0.,	1.,	100,	'Leading Jet #tau_{2} / #tau_{1}',	'Events / 0.01']
	dictHisto[ 31 ] = [ 'jet1Tau32',	0.,	1.,	100,	'Leading Jet #tau_{3} / #tau_{2}',	'Events / 0.01']
	dictHisto[ 32 ] = [ 'jet1Tau31',	0.,	1.,	100,	'Leading Jet #tau_{3} / #tau_{1}',	'Events / 0.01']
	dictHisto[ 33 ] = [ 'jet2Tau21',	0.,	1.,	100,	'2nd Leading Jet #tau_{2} / #tau_{1}',	'Events / 0.01']
	dictHisto[ 34 ] = [ 'jet2Tau32',	0.,	1.,	100,	'2nd Leading Jet #tau_{3} / #tau_{2}',	'Events / 0.01']
	dictHisto[ 35 ] = [ 'jet2Tau31',	0.,	1.,	100,	'2nd Leading Jet #tau_{3} / #tau_{1}',	'Events / 0.01']
	dictHisto[ 36 ] = [ 'jet1Mass',		0.,	100.,	50,	'Leading Jet Invariant Mass [Gev]',	'Events / 2 [GeV]']
	dictHisto[ 37 ] = [ 'jet2Mass',		0.,	100.,	50,	'2nd Leading Jet Invariant Mass [Gev]',	'Events / 2 [GeV]']
	dictHisto[ 38 ] = [ 'jet1MassPruned',	0.,	100.,	50,	'Leading Jet Pruned Invariant Mass [Gev]',	'Events / 2 [GeV]']
	dictHisto[ 39 ] = [ 'jet2MassPruned',	0.,	100.,	50,	'2nd Leading Jet Pruned Invariant Mass [Gev]',	'Events / 2 [GeV]']
	dictHisto[ 40 ] = [ 'avgJetPt',      	0.,	200.,	40,	'p_{T}^{AVG} [GeV]',		'Events / 5 [GeV]']
	if ('analysis' in process ): analysisPlots()

	dictMCHistos = {}
	dictMCHistos[0]  = [ 'numberStops',		0.,	5.,	5, 	'Number of Stops (MCTruth)',		'Events / 1']
	dictMCHistos[1]  = [ 'numberPartonStopA',	0.,	5.,	5, 	'Number of partons in StopA (MCTruth)',		'Events / 1']
	dictMCHistos[2]  = [ 'numberPartonStopB',	0.,	5.,	5, 	'Number of partons in StopB (MCTruth)',		'Events / 1']
	dictMCHistos[3]  = [ 'numberPartonsFromStop',	0.,	5.,	5, 	'Number of partons in Stops (MCTruth)',		'Events / 1']
	dictMCHistos[4]  = [ 'ptStops', 		0.,	500.,	100,	'MCTruth Stops p_{T} [GeV]', 			'Stops / 5 [GeV]']
	dictMCHistos[5]  = [ 'etaStops',		-5.,	5.,	100,	'MCTruth Stops #eta',			'Stops / 0.1']
	dictMCHistos[6]  = [ 'phiStops',		-3.14,	3.14,	100, 	'MCTruth Stops #phi',			'Stops / 0.03']
	dictMCHistos[7]  = [ 'massStops',		0.,	100.,	50,	'MCTruth Stops Invariant Mass [Gev]',	'Stops / 2 [GeV]']
	dictMCHistos[8]  = [ 'invMassPartonsFromStop',		0.,	100.,	50,	'MCTruth Stops Reconstruct Invariant Mass [Gev]',	'Stops / 2 [GeV]']
	dictMCHistos[9]  = [ 'ptPartonsFromStopA', 		0.,	500.,	100,	'MCTruth Partons from StopA p_{T} [GeV]',		'Stops / 5 [GeV]']
	dictMCHistos[10] = [ 'etaPartonsFromStopA',		-5.,	5.,	100,	'MCTruth Partons from StopA #eta',			'Stops / 0.1']
	dictMCHistos[11] = [ 'phiPartonsFromStopA',		-3.14,	3.14,	100, 	'MCTruth Partons from StopA #phi',			'Stops / 0.03']
	dictMCHistos[12] = [ 'massPartonsFromStopA',		0.,	100.,	50,	'MCTruth Partons from StopA Invariant Mass [Gev]',	'Stops / 2 [GeV]']
	dictMCHistos[13] = [ 'ptPartonsFromStopB', 		0.,	500.,	100,	'MCTruth Partons from StopB p_{T} [GeV]',		'Stops / 5 [GeV]']
	dictMCHistos[14] = [ 'etaPartonsFromStopB',		-5.,	5.,	100,	'MCTruth Partons from StopB #eta',			'Stops / 0.1']
	dictMCHistos[15] = [ 'phiPartonsFromStopB',		-3.14,	3.14,	100, 	'MCTruth Partons from StopB #phi',			'Stops / 0.03']
	dictMCHistos[16] = [ 'massPartonsFromStopB',		0.,	100.,	50,	'MCTruth Partons from StopB Invariant Mass [Gev]',	'Stops / 2 [GeV]']
	dictMCHistos[17] = [ 'ptTotalPartonsFromStop', 		0.,	500.,	100,	'MCTruth Partons from Stops p_{T} [GeV]',		'Stops / 5 [GeV]']
	dictMCHistos[18] = [ 'etaTotalPartonsFromStop',		-5.,	5.,	100,	'MCTruth Partons from Stops #eta',			'Stops / 0.1']
	dictMCHistos[19] = [ 'phiTotalPartonsFromStop',		-3.14,	3.14,	100, 	'MCTruth Partons from Stops #phi',			'Stops / 0.03']
	dictMCHistos[20] = [ 'massTotalPartonsFromStop',	0.,	100.,	50,	'MCTruth Partons from Stops Invariant Mass [Gev]',	'Stops / 2 [GeV]']

	if ('MCTruth' in process): Draw( 'stopUDD312_50', 'stopUDD312_50_plots', '/cms/gomez/Stops/st_jj/MCTruth/Plots/', 'stopUDD312_50', '/cms/gomez/Stops/st_jj/MCTruth/Plots/', dictMCHistos )

	listMatchingHistos = [
		[ 'numberJets', 'Number of Jets', 'Events / '], 
		[ 'numberPartons', 'Number of Partons from Stop', 'Events / ' ],
		[ 'jetPt', 'Jets p_{T} ', 'Jets per Events / ' ],

		[ 'numberPartonsSameJet', 'Number of Partons with Same Jet', 'Events / ' ],
		[ 'minDeltaRPartonJet', 'min #DeltaR(parton, jet) (All Jets)', 'Parton per Event / ' ],
		[ 'secMinDeltaRPartonJet', '2nd min #DeltaR(parton, jet) (All Jets)', 'Parton per Event / '  ],
		#[ 'minvsSecMinDeltaRPartonJet 	= TH2F('h_minDeltaRvsSecMinDeltaR',	'h_minDeltaRvsSecMinDeltaR',   maxDeltaR ],

		[ 'numberPartonsWithDeltaR0p4_4Matched', 'Number of Match Partons (4Matched)', 'Events / ' ],
		[ 'minDeltaRPartonJet_4Matched','min #DeltaR(parton, jet) (4Matched)', 'Event / ' ],
		[ 'minDeltaRPartonJet_4Matched_0','min #DeltaR(parton, jet) (4Matched)', 'Event / ' ],
		[ 'minDeltaRPartonJet_4Matched_1','min #DeltaR(parton, jet) (4Matched)', 'Event / ' ],
		[ 'minDeltaRPartonJet_4Matched_2','min #DeltaR(parton, jet) (4Matched)', 'Event / ' ],
		[ 'minDeltaRPartonJet_4Matched_3','min #DeltaR(parton, jet) (4Matched)', 'Event / ' ],
		[ 'invMass_4Matched', 'Invariant Mass of Match Jets (4Matched) from Stop [GeV]', 'Event / ' ],
		[ 'jetPt_4Matched', 'Jets p_{T}  (4Matched)', 'Jets per Events / ' ],
		
		['minDeltaRPartonJet_2Merged2Matched_Merged','min #DeltaR(parton, jet) Merged (2Merged+2Match)', 'Parton per Event / ' ],
		['secMinDeltaRPartonJet_2Merged2Matched_Merged', '2nd min #DeltaR(parton, jet) Merged (2Merged+2Match)', 'Parton per Event / ' ],
		['minDeltaRPartonJet_2Merged2Matched_NOMerged', 'min #DeltaR(parton, jet) Match (2Merged+2Match)', 'Parton per Event / ' ],
		['secMinDeltaRPartonJet_2Merged2Matched_NOMerged', '2nd min #DeltaR(parton, jet) Match (2Merged+2Match)', 'Parton per Event / ' ],
		#[ 'minvsSecMinDeltaRPartonJet_2Merged2Matched_Merged 	= TH2F('h_minvsSecMinDeltaRPartonJet_2Merged2Matched_Merged',	'h_minvsSecMinDeltaRPartonJet_2Merged2Matched_Merged', 	 maxDeltaR ],
		#[ 'minvsSecMinDeltaRPartonJet_2Merged2Matched_NOMerged 	= TH2F('h_minvsSecMinDeltaRPartonJet_2Merged2Matched_NOMerged',	'h_minvsSecMinDeltaRPartonJet_2Merged2Matched_NOMerged',maxDeltaR ],
		['invMass_2Merged2Matched_NOMerged', 'Invariant Mass of Match Jets (2Merged+2Match) from Stop [GeV]', 'Event / '  ],
		['invMass_2Merged2Matched_Merged', 'Invariant Mass of Merged Jets (2Merged+2Match) from Stop [GeV]', 'Event / '  ],
		[ 'jetPt_2Merged2Matched_NOMerged', 'Matched Jets p_{T}  (2Merged2Matched)', 'Jets per Events / ' ],
		[ 'jetPt_2Merged2Matched_Merged', 'Merged Jets p_{T}  (2Merged2Matched)', 'Jets per Events / ' ],

		['minDeltaRPartonJet_Pair2Merged', 'min #DeltaR(parton, jet) (2Merged)', 'Parton per Event / ' ],
		['secMinDeltaRPartonJet_Pair2Merged', '2nd min #DeltaR(parton, jet) (2Merged)', 'Parton per Event / ' ],
		#['minvsSecMinDeltaRPartonJet_Pair2Merged',   	   maxDeltaR ],
		['invMass_Pair2Merged_Merged', 	'Invariant Mass of Merged Jets (2Merged) from Stop [GeV]', 'Event / '  ],
		[ 'jetPt_Pair2Merged', 'Merged Jets p_{T}  (Pair2Merged)', 'Jets per Events / ' ],

		['minDeltaRPartonJet_3Merged1Match','min #DeltaR(parton, jet) (3Merged+1Match)', 'Parton per Event / '],
		['secMinDeltaRPartonJet_3Merged1Match', '2nd min #DeltaR(parton, jet) (3Merged+1Match)', 'Parton per Event / '],
		#[ 'minvsSecMinDeltaRPartonJet_3Merged1Match 	= TH2F('h_minvsSecMinDeltaRPartonJet_3Merged1Match','h_minvsSecMinDeltaRPartonJet_3Merged1Match',maxDeltaR ],
		['invMass_3Merged1Match_Merged', 'Invariant Mass of Merged Jets (3Merged+1Match) from Stop [GeV]', 'Event / '  ],
		[ 'jetPt_3Merged1Match_Merged', 'Merged Jets p_{T}  (3Merged1Match)', 'Jets per Events / ' ],

		['minDeltaRPartonJet_4Merged',	   'min #DeltaR(parton, jet) (4Merged)', 'Parton per Event / '],

		#### with DeltaR0p4,
		['numberPartonsSameJet_DeltaR0p4','Number of Partons with Same Jet Matched', 'Events / ' ],
		[ 'jetPt_DeltaR0p4', 'Matched Jets p_{T} ', 'Jets per Events / ' ],
		['minDeltaRPartonJet_DeltaR0p4','min #DeltaR(parton, jet) (All Jets Matched)', 'Parton per Event / ' ],
		['secMinDeltaRPartonJet_DeltaR0p4','2nd min #DeltaR(parton, jet) (All Jets Matched)', 'Parton per Event / ' ],
		
		['minDeltaRPartonJet_4Matched_DeltaR0p4','min #DeltaR(parton, jet) (All Jets Matched)', 'Parton per Event / ' ],
		['minDeltaRPartonJet_4Matched_DeltaR0p4_0','min #DeltaR(parton, jet) (All Jets Matched)', 'Parton per Event / '  ],
		['minDeltaRPartonJet_4Matched_DeltaR0p4_1','min #DeltaR(parton, jet) (All Jets Matched)', 'Parton per Event / '  ],
		['minDeltaRPartonJet_4Matched_DeltaR0p4_2','min #DeltaR(parton, jet) (All Jets Matched)', 'Parton per Event / '  ],
		['minDeltaRPartonJet_4Matched_DeltaR0p4_3','min #DeltaR(parton, jet) (All Jets Matched)', 'Parton per Event / '  ],
		['invMass_4Matched_DeltaR0p4', 	'Invariant Mass of Match Jets (4Matched) from Stop [GeV]', 'Event / '  ],
		[ 'jetPt_4Matched_DeltaR0p4', 'Matched Jets p_{T}  (4Matched)', 'Jets per Events / ' ],

		['minDeltaRPartonJet_2Merged2Matched_Merged_DeltaR0p4',	'min #DeltaR(parton, jet) Merged (2Merged+2Matched)', 'Parton per Event / '  ],
		['secMinDeltaRPartonJet_2Merged2Matched_Merged_DeltaR0p4', '2nd min #DeltaR(parton, jet) Merged (2Merged+2Matched)', 'Parton per Event / '  ],
		['minDeltaRPartonJet_2Merged2Matched_NOMerged_DeltaR0p4','min #DeltaR(parton, jet) Matched (2Merged+2Matched)', 'Parton per Event / '  ],
		['secMinDeltaRPartonJet_2Merged2Matched_NOMerged_DeltaR0p4', '2nd min #DeltaR(parton, jet) Matched (2Merged+2Matched)', 'Parton per Event / '  ],
		#['minvsSecMinDeltaRPartonJet_2Merged2Matched_Merged_DeltaR0p4', 	 	 	 	 	 	maxDeltaR ],
		#['minvsSecMinDeltaRPartonJet_2Merged2Matched_NOMerged_DeltaR0p4', 	 	 	 	 	 	maxDeltaR ],
		['invMass_2Merged2Matched_DeltaR0p4_NOMerged', 'Invariant Mass of Match Jets Matched (2Merged+2Matched) from Stop [GeV]', 'Event / '  ],
		['invMass_2Merged2Matched_DeltaR0p4_Merged', 'Invariant Mass of Match Jets Merged (2Merged+2Matched) from Stop [GeV]', 'Event / '  ],
		[ 'jetPt_2Merged2Matched_DeltaR0p4_NOMerged', 'Matched Jets p_{T}  (2Merged2Matched)', 'Jets per Events / ' ],
		[ 'jetPt_2Merged2Matched_DeltaR0p4_Merged', 'Merged Jets p_{T}  (2Merged2Matched)', 'Jets per Events / ' ],

		['minDeltaRPartonJet_Pair2Merged_DeltaR0p4_A',	'min #DeltaR(parton, jet) MergedA (Pair2Merged)', 'Parton per Event / '  ],
		['secMinDeltaRPartonJet_Pair2Merged_DeltaR0p4_A','2nd min #DeltaR(parton, jet) MergedA (Pair2Merged)', 'Parton per Event / '  ],
		['minDeltaRPartonJet_Pair2Merged_DeltaR0p4_B',	'min #DeltaR(parton, jet) MergedB (Pair2Merged)', 'Parton per Event / '  ],
		['secMinDeltaRPartonJet_Pair2Merged_DeltaR0p4_B','2nd min #DeltaR(parton, jet) MergedB (Pair2Merged)', 'Parton per Event / '  ],
		['invMass_Pair2Merged_DeltaR0p4_Merged', 'Invariant Mass of Merged Jets (Pair2Merged) from Stop [GeV]', 'Event / '  ],
		[ 'jetPt_Pair2Merged_DeltaR0p4', 'Merged Jets p_{T} (Pair2Merged)', 'Jets per Events / ' ],

		['minDeltaRPartonJet_3Merged1Match_DeltaR0p4',	'min #DeltaR(parton, jet) (3Merged1Matched)', 'Parton per Event / '  ],
		['secMinDeltaRPartonJet_3Merged1Match_DeltaR0p4','2nd min #DeltaR(parton, jet) (3Merged1Matched)', 'Parton per Event / '  ],
		['invMass_3Merged1Match_DeltaR0p4_Merged', 'Invariant Mass of Match Jets (3Matched1Match) from Stop [GeV]', 'Event / '  ],
		[ 'jetPt_3Merged1Match_DeltaR0p4_Merged', 'Merged Jets p_{T}  (3Merged1Match)', 'Jets per Events / ' ],

		['minDeltaRPartonJet_4Merged_DeltaR0p4','min #DeltaR(parton, jet) (4Merged)', 'Parton per Event / ' ]
	]

	#if ('Matching' in sys.argv): Draw( 'stopUDD312_50', 'stop_UDD312_50_Matching_Plots', '/cms/gomez/Stops/st_jj/MCTruth/rootFiles/140314/', 'stopUDD312_50_Matching', '/cms/gomez/Stops/st_jj/MCTruth/Plots/', listMatchingHistos )

	if ('jetAlgoCmp' in process): DrawCmp( 'stopUDD312_'+mass, '/cms/gomez/Stops/st_jj/treeResults/rootFiles/140325/', 'stopUDD312_'+mass+'_Matching', '/cms/gomez/Stops/st_jj/treeResults/Plots/', listMatchingHistos, jetAlgo1, jetAlgo2 )



#!/usr/bin/env python
#import ROOT
from ROOT import * #TFile, TH1F, THStack, TCanvas, TMath, gROOT, gPad
from setTDRStyle import setTDRStyle, setSelectionTitle, setTitle
import time, os, math
import tarfile
#import optparse

gROOT.Reset()
gROOT.SetBatch()
setTDRStyle()
gROOT.ForceStyle()
gROOT.SetStyle('tdrStyle')

###############################################################
### Dictionary with Histogram features                    #####
###############################################################
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
		    
###############################################################
###  Draw Histograms from final Tree (after selection)    #####
###############################################################
def MCTruthAnalysis():
	"""create Plots from MCTruth"""

	Sample = 'stopUDD312_50'
	inputDir = '/cms/gomez/Stops/st_jj/MCTruth/Plots/'
	outputDir = '/cms/gomez/Stops/st_jj/MCTruth/Plots/'

	targetDir = outputDir + dateKey + '/'
	print 'Output directory: ', targetDir
	if not ( os.path.exists( targetDir ) ): os.makedirs( targetDir )
	tarFile = dateKey+"files.tar.gz"
	tar = tarfile.open( targetDir + tarFile, "w:gz")

	outputList = [] ### for format

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
	dictMCHistos[9]  = [ 'ptPartonsFromStopB', 		0.,	500.,	100,	'MCTruth Partons from StopB p_{T} [GeV]',		'Stops / 5 [GeV]']
	dictMCHistos[10] = [ 'etaPartonsFromStopB',		-5.,	5.,	100,	'MCTruth Partons from StopB #eta',			'Stops / 0.1']
	dictMCHistos[11] = [ 'phiPartonsFromStopB',		-3.14,	3.14,	100, 	'MCTruth Partons from StopB #phi',			'Stops / 0.03']
	dictMCHistos[12] = [ 'massPartonsFromStopB',		0.,	100.,	50,	'MCTruth Partons from StopB Invariant Mass [Gev]',	'Stops / 2 [GeV]']
	dictMCHistos[9]  = [ 'ptTotalPartonsFromStop', 		0.,	500.,	100,	'MCTruth Partons from Stops p_{T} [GeV]',		'Stops / 5 [GeV]']
	dictMCHistos[10] = [ 'etaTotalPartonsFromStop',		-5.,	5.,	100,	'MCTruth Partons from Stops #eta',			'Stops / 0.1']
	dictMCHistos[11] = [ 'phiTotalPartonsFromStop',		-3.14,	3.14,	100, 	'MCTruth Partons from Stops #phi',			'Stops / 0.03']
	dictMCHistos[12] = [ 'massTotalPartonsFromStop',	0.,	100.,	50,	'MCTruth Partons from Stops Invariant Mass [Gev]',	'Stops / 2 [GeV]']
	#print dictMCHistos

	#---- open the files --------------------
	inputFile = TFile.Open( inputDir+Sample+'_plots.root' )
	print 'Drawing Histograms from: ', inputFile.GetName()

	for i, varList in dictMCHistos.iteritems():
	
		outputFileName = dateKey+'_'+varList[0]+'_'+Sample+'.png'  
		print 'Processing.......', outputFileName
		outputFile = targetDir + outputFileName
		outputList.append( outputFileName )
		h = inputFile.Get('h_'+varList[0])
		#----- Drawing -----------------------
		h.GetXaxis().SetTitle( varList[4] )
		h.GetYaxis().SetTitle( varList[5] )

		can = TCanvas('can_'+str(i),'can_'+str(i),800,500)
		h.Draw('HISTE')
		setTitle( Sample )
		can.SaveAs( outputFile )
		del can
	
		tar.add( outputFile, dateKey+'_'+varList[0]+'_'+Sample+'.png' )

	tar.close()
	print 'Creating tar file with all plots named: ',  tarFile
	printHTML( outputList  )

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

########################################################
if __name__ == '__main__':

	#analysisPlots()
	MCTruthAnalysis()

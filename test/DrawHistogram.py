#!/usr/bin/env python
#import ROOT
from ROOT import * #TFile, TH1F, THStack, TCanvas, TMath, gROOT, gPad
from setTDRStyle import setTDRStyle, setSelectionTitle
import time, os, math
import tarfile
#import optparse

gROOT.Reset()
gROOT.SetBatch()
setTDRStyle()
gROOT.ForceStyle()
gROOT.SetStyle('tdrStyle')

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

#fileNames = ['QCD500','QCD1000','RS2000','data']
#xsections = [8426.,204.,4.083e-3,1.]
#colorF    = [ROOT.kBlue-9,ROOT.kBlue-8,ROOT.kWhite,ROOT.kBlack]
#colorL    = [ROOT.kBlack,ROOT.kBlack,ROOT.kRed,ROOT.kBlack]
hist      = []
#LUMI      = 19800.

inputDir = '/cms/gomez/Stops/st_jj/treeResults/'
outputDir = '/cms/gomez/Stops/st_jj/treeResults/Plots/'
Sample = 'stopUDD312_50'
jetAlgoList = [ 'CA8', 'AK4' ]

monthKey  =  time.strftime("%y%m")
dateKey   = time.strftime("%y%m%d")
targetDir = outputDir + dateKey + '/'
tar = tarfile.open( targetDir+dateKey+"files.tar.gz", "w:gz")
if not ( os.path.exists( targetDir ) ):
	os.makedirs( targetDir )

#---- open the files --------------------
#for f in fileNames:
inputFile = TFile.Open( inputDir+Sample+'_plots.root' )
print inputFile.GetName()

for jetAlgo in jetAlgoList:
	for i, varList in dictHisto.iteritems():
	
		outputFile = targetDir+dateKey+'_'+varList[0]+'_'+jetAlgo+'.png'  
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
	    
	#----- keep the GUI alive ------------
	#if __name__ == '__main__':
	#  rep = ''
	#  while not rep in ['q','Q']:
	#    rep = raw_input('enter "q" to quit: ')
	#    if 1 < len(rep):
	#      rep = rep[0]

	#usage = "usage: %prog [options]"
	#parser = optparse.OptionParser(usage)
	#parser.add_option("--var",action="store",type="string",dest="var",default='mjj')
	#parser.add_option("--xmin",action="store",type="float",dest="xmin",default=1)
	#parser.add_option("--xmax",action="store",type="float",dest="xmax",default=1)
	#parser.add_option("--xtitle",action="store",type="string",dest="xtitle",default='')
	#parser.add_option("--rebin",action="store",type="int",dest="rebin",default=1)
	#parser.add_option("--logy",action="store_true",default=False,dest="logy")
	#
	#(options, args) = parser.parse_args()
	#var = options.var
	#xmin = options.xmin
	#xmax = options.xmax
	#xtitle = options.xtitle
	#rebin = options.rebin
	#logy = options.logy
	#

def printHTML():
	if (options.asList):
	    print "<ul>"
	for displayName, Tuple in filesMap.iteritems():
	    sourceFile     = Tuple[0]
	    fullTargetFile = Tuple[1]
	    targetFile     = Tuple[2]
	    if (options.asList):
		print "   <li>",
	    # Get the extention
	    extMatch = re.search (r'\.([^\.]+)$', targetFile)
	    printed = False
	    if extMatch:
		extention = extMatch.group(1).lower()
		if extention in imageExtentions:
		    print '<p><img src="%s"><br>' % targetFile
		    printed = True
		elif extention in convertedToImageExtentions:
		    # Do we have a file of the same
		    extReg = "%s%s" % (extention, "$")
		    for imgExt in imageExtentions:
			imageFile = re.sub (extReg, imgExt, displayName, re.IGNORECASE)
			if imageFile in filesMap:
			    print '<p><a href="%s"><img src="%s"></a><br>' % \
				  (targetFile, imageFile)
			    printed = True
	    if not printed:
		print '<a href="%s"><tt>%s</tt></a>' % (targetFile, displayName)
	if (options.asList):
	    print "</ul>"

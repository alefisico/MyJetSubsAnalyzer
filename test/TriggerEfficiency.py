#!/usr/bin/env python

'''
File: TriggerEfficiency.py
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: Calculate the Trigger Efficiency
'''

import sys,os,time
import optparse
from collections import defaultdict
from ROOT import *
from setTDRStyle import setTDRStyle
from DataFormats.FWLite import Events, Handle

gROOT.SetBatch()
gROOT.Reset()
setTDRStyle()
gROOT.ForceStyle()
gROOT.SetStyle('tdrStyle')


###### Trick for add date or month to plots
dateKey   = time.strftime("%y%m%d%H%M")
monthKey   = time.strftime("%y%m%d")


################################################################################# Calculate Efficiency
def CalculateEff( inputFile, outputDir, sample, jetAlgo, grooming, weight, FNAL ):
	"""docstring for CalculateEff"""

	outputFileName = monthKey+'_'+sample+'_TriggerEfficiency_'+jetAlgo+'.pdf'  
	#outputFileName = monthKey+'_'+sample+'_TriggerEfficiency_'+jetAlgo+'_HT350.pdf'  
	print 'Processing.......', outputFileName
	targetDir = outputDir + monthKey + '/'
	if not ( os.path.exists( targetDir ) ): os.makedirs( targetDir )
	outputFile = targetDir + outputFileName

	inFile = TFile.Open( inputFile )

	HT350 = TH1F( inFile.Get('h_ht_PFHT350_'+jetAlgo+'_') )
	#HT350 = TH1F( inFile.Get('h_ht_HT350_'+jetAlgo+'_') )
	#HT650 = TH1F( inFile.Get('h_ht_PFHT650_'+jetAlgo+'_') )		##### is the one with HT350
	HT650 = TH1F( inFile.Get('h_ht_PFHT650_1_'+jetAlgo+'_') )	##### _1_ the one with PFHT350
	print TEfficiency.CheckConsistency(HT350, HT650)
	#if TEfficiency.CheckConsistency(ht_HT650, ht_HT350):
	can2 = TCanvas('can_TrigEff','can_TrigEff',900,600)
	eff = TEfficiency('efficiency','efficiency', 50, 400, 900.)
	eff.SetPassedHistogram(HT650,'f')
	eff.SetTotalHistogram(HT350,'f')
	eff.SetLineColor(ROOT.kBlack)
	eff.SetMarkerColor(ROOT.kBlack)
	eff.SetMarkerStyle(20)

	fit = TF1('fit','(1-[2])+[2]*TMath::Erf((x-[0])/[1])',450,750)
	fit.SetParameters(600,60,0.5)
	fit.SetLineColor(ROOT.kBlue)
	eff.Fit(fit,'RQ')
	eff.Fit(fit,'RQ')

	line = TF1('line','1',400,900)
	line.GetXaxis().SetTitle('H_{T} [GeV]')
	line.GetYaxis().SetTitle('Trigger Efficiency')
	line.SetLineColor(ROOT.kBlack)
	line.SetLineStyle(2)
	line.SetMinimum(-0.2)
	line.SetMaximum(1.3)
	line.Draw()
	eff.Draw('samePE1')

	textBox=TLatex()
	textBox.SetNDC()
	textBox.SetTextSize(0.05) 
	textBox.SetTextColor(kBlue)
	#textBox.DrawText(0.16,0.95,"CMS Preliminary Simulation")
	textBox.DrawText(0.16,0.95,"CMS Preliminary ")

	textBox1=TLatex()
	textBox1.SetNDC()
	textBox1.SetTextSize(0.04) 
	textBox1.SetTextColor(kBlue)
	textBox1.DrawText(0.20,0.85, sample)

	textBox3=TLatex()
	textBox3.SetNDC()
	textBox3.SetTextSize(0.04) 
	textBox3.DrawLatex(0.67,0.40, jetAlgo+" Jets")
	
	textBox4=TLatex()
	textBox4.SetNDC()
	textBox4.SetTextSize(0.04) 
	textBox4.DrawLatex(0.67,0.35,"Ref. Trigger: HT350")
	
	textBox2=TLatex()
	textBox2.SetNDC()
	textBox2.SetTextSize(0.04) 
	textBox2.DrawLatex(0.67,0.30,"Trigger: PFHT650")
	
	textBox5=TLatex()
	textBox5.SetNDC()
	textBox5.SetTextSize(0.04) 
	textBox5.DrawLatex(0.67,0.25,"trigger 99% efficient")
	
	textBox6=TLatex()
	textBox6.SetNDC()
	textBox6.SetTextSize(0.04) 
	textBox6.DrawLatex(0.67,0.20,"for HT > 720 GeV")
	
	can2.SaveAs( outputFile )

	gPad.Update()
	x0 = fit.GetX(0.99)
	cut = TLine(x0,gPad.GetFrame().GetY1(),x0,gPad.GetFrame().GetY2())
	cut.SetLineColor(ROOT.kRed)
	cut.SetLineStyle(2)
	cut.Draw()


	#####################################################################################################################


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

#	if 'QCD' in samples: 
#		sample = 'QCD_HT-'+QCD
#		if FNAL:
#			#list = os.popen('ls -1 /eos/uscms/store/user/algomez/'+sample+'_8TeV_Summer12_DR53X-PU_S10_START53_V7A-v1/*.root').read().splitlines()
#			tmpList = os.popen('ls -1v /eos/uscms/store/user/algomez/'+sample+'_8TeV_Summer12_DR53X-PU_S10_START53_V7A-v1/*.root').read().splitlines()
#			outputDir = '/uscms_data/d3/algomez/files/QCD_8TeV/treeResults/'
#		else:
#			tmpList = os.popen('ls -1v /cms/gomez/Files/QCD_8TeV/PATtuples/'+sample+'_8TeV_Summer12_DR53X-PU_S10_START53_V7A-v1/*.root').read().splitlines()
#			outputDir = '/cms/gomez/Files/QCD_8TeV/treeResults/'
#		filesPerJob = round(len(tmpList)/30)+1
#		iniList = int(filesPerJob*Job)
#		finList = int((filesPerJob*(Job+1))-1)
#		print filesPerJob, iniList, finList
#		list = tmpList[iniList:finList]
#		#list = tmpList[0:2]
#		inputList = [i if i.startswith('file') else 'file:' + i for i in list]
#		if '250To500' in QCD: weight = 19500*276000/27062078.0
#		elif '500To1000' in QCD: weight = 19500*8426/30599292.0
#		else: weight = 19500*204/13843863.0
#	elif 'Signal' in samples: 
#		sample = 'RPVSt'+str(mass)+'tojj_8TeV_HT500_'+str(Job)
#		#list = os.popen('ls -1 /cms/gomez/Substructure/Generation/Simulation/CMSSW_5_3_2_patch4/src/mySimulations/stop_UDD312_50/aodsim/*.root').read().splitlines()
#		#list = os.popen('ls -1v /cms/gomez/Stops/st_jj/patTuples/'+sample+'/results/140418/*.root').read().splitlines()
#		list = os.popen('ls -1v /cms/gomez/Files/RPVSttojj_8TeV/'+sample+'/PATtuples/*.root').read().splitlines()
#		#outputDir = '/cms/gomez/Stops/st_jj/treeResults/'
#		outputDir = '/cms/gomez/Files/RPVSttojj_8TeV/treeResults/'
#		#list = [ '/cms/gomez/Stops/st_jj/patTuples/stopUDD312_50_tree_test_grom.root' ]
#		inputList = [i if i.startswith('file') else 'file:' + i for i in list]
#		if mass == 50: weight = 1
#		#elif mass == 100: weight = 19500*559.757/100000.0
#		elif mass == 100: weight = 19500*559.757/443293086.50
#		elif mass == 200: weight = 19500*18.5245/100000.0
#	elif 'Data' in samples:
#		sample = 'Data_'+QCD
	sample = 'Data_HT-Run2012A-22Jan2013'
	if FNAL:
		inputFile = '/eos/uscms/store/user/algomez/Data/treeResults/'+sample+'_'+jetAlgo+'_'+grooming+'_Plots.root'
		outputDir = '/uscms_data/d3/algomez/Substructure/Analyzer/CMSSW_5_3_12/src/jetSubs/MyJetSubsAnalyzer/test/Plots/'

	else:
		list = os.popen('ls -1v /cms/gomez/Files/DATA/PATtuples/'+sample+'/*.root').read().splitlines()
		outputDir = '/cms/gomez/Files/DATA/treeResults/'
	weight = 1


	#outputDir = '/eos/uscms/store/user/algomez/'
	print 'InputFiles: ', inputFile
	print 'Output_Dir: ', outputDir
	print 'weight: ', weight

	CalculateEff( inputFile, outputDir, sample, jetAlgo, grooming, weight, FNAL )


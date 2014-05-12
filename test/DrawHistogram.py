#!/usr/bin/env python
'''
File: DrawHistogram.py
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Draw histograms. Check for options at the end.
'''

#from ROOT import TFile, TH1F, THStack, TCanvas, TMath, gROOT, gPad
from ROOT import *
from setTDRStyle import *
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
def analysisPlots( Sample, inputDir, outputName, outputDir, listHistos, Algo, groomed):
	"""create Analysis Plots """

	#gStyle.SetOptStat(0)
	targetDir = outputDir + dateKey + '/'
	print 'Output directory: ', targetDir
	if not ( os.path.exists( targetDir ) ): os.makedirs( targetDir )
	tarFile = dateKey+"files_"+Sample+"_"+Algo+"_"+groomed+".tar.gz"
	tar = tarfile.open( targetDir + tarFile, "w:gz")

	outputList = [] ### for format
	#---- open the files --------------------
	#inputFile1 = TFile.Open( inputDir+Sample+'_'+Algo+'_cutHT900_Plots.root' )
	inputFile1 = TFile.Open( inputDir+Sample+'_'+Algo+'_'+groomed+'_Plots.root' )
	print 'Drawing Histograms from: ', inputFile1.GetName()

	for histoInfo in listHistos:
	
		outputFileName = dateKey+'_'+histoInfo[0]+'_'+Sample+'_'+Algo+'with'+groomed+'.png'  
		#outputFileName = dateKey+'_'+histoInfo[0]+'_'+outputName+'_'+Algo+'_cutHT900.pdf'  
		print 'Processing.......', outputFileName
		outputFile = targetDir + outputFileName
		outputList.append( outputFileName )
		print histoInfo[0]
		h1 = inputFile1.Get('h_'+histoInfo[0]+'_'+Algo+'_'+groomed)
		#----- Drawing -----------------------
		h1.GetXaxis().SetTitle( histoInfo[1] )
		binWidth = h1.GetBinWidth(1)
		h1.GetYaxis().SetTitle( histoInfo[2]+str(binWidth) )
		h1.SetLineColor(4)
		h1.SetLineWidth(2)

		can = TCanvas('can_'+histoInfo[0],'can_'+histoInfo[0],800,500)
		#if 'Pt' in histoInfo[0]: can.SetLogy()
		#if 'Mass' in histoInfo[0]: can.SetLogy()
		h1.Sumw2()
		h1.Draw('histe ')
		if 'cut' in histoInfo[0]: setSelectionTitleCuts( outputName )
		else: setSelectionTitle( Sample )
		can.SaveAs( outputFile )
		del can
	
		tar.add( outputFile, outputFileName )

	tar.close()
	print 'Creating tar file with all plots named: ',  tarFile
	printHTML( outputList  )
	printLatex( outputList  )

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
	
		outputFileName = dateKey+'_'+histoInfo[0]+'_'+outputName+'.pdf'  
		print 'Processing.......', outputFileName
		outputFile = targetDir + outputFileName
		outputList.append( outputFileName )
		h = inputFile.Get('h_'+histoInfo[0])
		#----- Drawing -----------------------
		h.GetXaxis().SetTitle( histoInfo[4] )
		h.GetYaxis().SetTitle( histoInfo[5] )
		if ( 'numberPartonsSameJet' in histoInfo[0] ):
			h.GetXaxis().SetBinLabel( 1 , 'NoMerged' )
			h.GetXaxis().SetBinLabel( 2 , 'SinglyMerged' )
			h.GetXaxis().SetBinLabel( 3 , 'DoublyMerged' )
			h.GetXaxis().SetBinLabel( 4 , 'TriplyMerged' )
			h.GetXaxis().SetBinLabel( 5 , 'FourlyMerged' )
			h.GetXaxis().SetBinLabel( 6 , '' )
			h.GetXaxis().SetBinLabel( 7 , 'less 4 Jets' )

		can = TCanvas('can_'+histoInfo[0],'can_'+histoInfo[0],800,500)
		h.Draw('HISTE')
		setTitle( Sample )
		can.SaveAs( outputFile )
		del can
	
		tar.add( outputFile, dateKey+'_'+histoInfo[0]+'_'+outputName+'.pdf' )

	tar.close()
	print 'Creating tar file with all plots named: ',  tarFile
	printHTML( outputList  )

##########################################################################
### Draw Histograms from List, create tar file and HTML code    #####
##########################################################################
def DrawCmpAlgos( Sample, inputDir, outputName, outputDir, listHistos, Algo1, Algo2):
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
	
		outputFileName = dateKey+'_'+histoInfo[0]+'_'+outputName+'_'+Algo1+'vs'+Algo2+'.pdf'  
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
			h1.GetXaxis().SetBinLabel( 1 , 'NoMerged' )
			h1.GetXaxis().SetBinLabel( 2 , 'SinglyMerged' )
			h1.GetXaxis().SetBinLabel( 3 , 'DoublyMerged' )
			h1.GetXaxis().SetBinLabel( 4 , 'TriplyMerged' )
			h1.GetXaxis().SetBinLabel( 5 , 'FourlyMerged' )
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

####################################################################################################################
### Draw Histograms from List, Compare no groomed with groomed, same jetAlgo, create tar file and HTML code    #####
####################################################################################################################
def DrawCmp( Sample, inputDir, outputName, outputDir, listHistos, Algo, groomed):
	"""create analysis Plots """

	gStyle.SetOptStat(0)
	targetDir = outputDir + dateKey + '/'
	print 'Output directory: ', targetDir
	if not ( os.path.exists( targetDir ) ): os.makedirs( targetDir )
	tarFile = dateKey+"files_"+Sample+"_"+Algo+"_"+groomed+".tar.gz"
	tar = tarfile.open( targetDir + tarFile, "w:gz")

	outputList = [] ### for format
	#---- open the files --------------------
	inputFile1 = TFile.Open( inputDir+Sample+'_'+Algo+'__Plots.root' )
	inputFile2 = TFile.Open( inputDir+Sample+'_'+Algo+'_'+groomed+'_Plots.root' )
	print 'Drawing Histograms from: ', inputFile1.GetName(), 'and ', inputFile2.GetName()

	for histoInfo in listHistos:
	
		outputFileName = dateKey+'_'+histoInfo[0]+'_'+outputName+'_'+Algo+'with'+groomed+'.pdf'  
		print 'Processing.......', outputFileName
		outputFile = targetDir + outputFileName
		outputList.append( outputFileName )
		print histoInfo[0]
		h1 = inputFile1.Get('h_'+histoInfo[0]+'_'+Algo+'_')
		h2 = inputFile2.Get('h_'+histoInfo[0]+'_'+Algo+'_'+groomed)
		#----- Drawing -----------------------
		h1.GetXaxis().SetTitle( histoInfo[1] )
		binWidth = h1.GetBinWidth(1)
		h1.GetYaxis().SetTitle( histoInfo[2]+str(binWidth) )
		h1.SetLineColor(1)
		h1.SetLineWidth(2)
		h2.SetLineColor(2)
		h2.SetLineWidth(2)
		h1.SetMaximum(1.2*TMath.Max(h1.GetBinContent(h1.GetMaximumBin()),h2.GetBinContent(h2.GetMaximumBin())))

		legend=TLegend(0.75,0.65,0.90,0.85)
		legend.SetFillStyle(0)
		legend.AddEntry(h1, Algo+' only', "l")
		legend.AddEntry(h2, Algo+' '+groomed, "l")
		legend.SetTextSize(0.03)

		can = TCanvas('can_'+histoInfo[0],'can_'+histoInfo[0],800,500)
		if 'Pt' in histoInfo[0]: can.SetLogy()
		if 'Mass' in histoInfo[0]: can.SetLogy()
		h1.Sumw2()
		h2.Sumw2()
		h1.Draw('histe ')
		h2.Draw('same histe')
		legend.Draw()
		setSelectionTitle( Sample )
		can.SaveAs( outputFile )
		del can
	
		tar.add( outputFile, outputFileName )

	tar.close()
	print 'Creating tar file with all plots named: ',  tarFile
	printHTML( outputList  )
	printLatex( outputList  )

def DrawCmpDataQCD( Sample, inputDir, outputName, outputDir, listHistos, Algo, groomed):
	"""create analysis Plots """

	gStyle.SetOptStat(0)
	targetDir = outputDir + dateKey + '/'
	print 'Output directory: ', targetDir
	if not ( os.path.exists( targetDir ) ): os.makedirs( targetDir )
	tarFile = dateKey+"files_"+Sample+"_"+Algo+"_"+groomed+".tar.gz"
	tar = tarfile.open( targetDir + tarFile, "w:gz")

	outputList = [] ### for format
	#---- open the files --------------------
	inputFile1 = TFile.Open( inputDir+Sample+'_'+Algo+'_'+groomed+'_Plots.root' )
	inputFile2 = TFile.Open( '/cms/gomez/Files/QCD_8TeV/treeResults/rootFiles/QCD_HT-250To500_'+Algo+'_'+groomed+'_Plots.root' )
	inputFile3 = TFile.Open( '/cms/gomez/Files/QCD_8TeV/treeResults/rootFiles/QCD_HT-500To1000_'+Algo+'_'+groomed+'_Plots.root' )
	inputFile4 = TFile.Open( '/cms/gomez/Files/QCD_8TeV/treeResults/rootFiles/QCD_HT-1000ToInf_'+Algo+'_'+groomed+'_Plots.root' )
	print 'Drawing Histograms from: ', inputFile1.GetName(), 'and ', inputFile2.GetName()

	for histoInfo in listHistos:
	
		outputFileName = dateKey+'_'+histoInfo[0]+'_'+Sample+'_QCD_'+Algo+'with'+groomed+'.pdf'  
		print 'Processing.......', outputFileName
		outputFile = targetDir + outputFileName
		outputList.append( outputFileName )
		print histoInfo[0]
		h1 = inputFile1.Get('h_'+histoInfo[0]+'_'+Algo+'_'+groomed)
		h2 = inputFile2.Get('h_'+histoInfo[0]+'_'+Algo+'_'+groomed)
		h3 = inputFile3.Get('h_'+histoInfo[0]+'_'+Algo+'_'+groomed)
		h4 = inputFile4.Get('h_'+histoInfo[0]+'_'+Algo+'_'+groomed)
		h2.Scale( 800/19500. )
		h3.Scale( 800/19500. )
		h4.Scale( 800/19500. )
		#----- Drawing -----------------------
		h1.GetXaxis().SetTitle( histoInfo[1] )
		binWidth = h1.GetBinWidth(1)
		h1.GetYaxis().SetTitle( histoInfo[2]+str(binWidth) )
		h2.Add( h3 )
		h2.Add( h4 )
		h2.Scale( 1.3 )
		h1.SetLineColor(1)
		h1.SetLineWidth(2)
		h2.SetLineColor(2)
		h2.SetLineWidth(2)
		h1.SetMaximum(1.2*TMath.Max(h1.GetBinContent(h1.GetMaximumBin()),h2.GetBinContent(h2.GetMaximumBin())))

		legend=TLegend(0.70,0.65,0.90,0.85)
		legend.SetFillStyle(0)
		legend.AddEntry(h1, 'Data '+Algo+' '+groomed, "l")
		legend.AddEntry(h2, 'QCD '+Algo+' '+groomed, "l")
		legend.SetTextSize(0.03)

		can = TCanvas('can_'+histoInfo[0],'can_'+histoInfo[0],800,500)
		#if 'Pt' in histoInfo[0]: can.SetLogy()
		#if 'Mass' in histoInfo[0]: can.SetLogy()
		h1.Sumw2()
		h2.Sumw2()
		h1.Draw('histe ')
		h2.Draw('same histe')
		legend.Draw()
		if 'cut' in histoInfo[0]: setSelectionTitleCuts( outputName )
		else: setSelectionTitle( outputName )
		can.SaveAs( outputFile )
		del can
	
		tar.add( outputFile, outputFileName )

	tar.close()
	print 'Creating tar file with all plots named: ',  tarFile
	printHTML( outputList  )
	printLatex( outputList  )



def DrawCmpMatching( Sample, inputDir, outputName, outputDir, listHistos, Algo, groomed, cat):
	"""create Plots from MCTruth"""

	gStyle.SetOptStat(0)
	targetDir = outputDir + dateKey + '/'
	print 'Output directory: ', targetDir
	if not ( os.path.exists( targetDir ) ): os.makedirs( targetDir )
	tarFile = dateKey+"files_"+Sample+"_"+Algo+"_"+groomed+".tar.gz"
	tar = tarfile.open( targetDir + tarFile, "w:gz")

	outputList = [] ### for format
	#---- open the files --------------------
	if not 'Merged' in cat:
		inputFile1 = TFile.Open( inputDir+Sample+'_Matching_'+Algo+'__Plots.root' )
		inputFile2 = TFile.Open( inputDir+Sample+'_Matching_'+Algo+'_'+groomed+'_Plots.root' )
	else: 
		inputFile1 = TFile.Open( inputDir+Sample+'_Matching_'+Algo+'__Plots.root' )
		inputFile2 = TFile.Open( inputDir+Sample+'_Matching_'+Algo+'_'+groomed+'_'+cat+'_Plots.root' )
	print 'Drawing Histograms from: ', inputFile1.GetName(), 'and ', inputFile2.GetName()

	for histoInfo in listHistos:
	
#		if cat in histoInfo[0]:
		outputFileName = dateKey+'_'+histoInfo[0]+'_'+outputName+'_'+Algo+'with'+groomed+'.pdf'  
		print 'Processing.......', outputFileName
		outputFile = targetDir + outputFileName
		outputList.append( outputFileName )
		print histoInfo[0]
		h1 = inputFile1.Get('h_'+histoInfo[0]+'_'+Algo+'_')
		h2 = inputFile2.Get('h_'+histoInfo[0]+'_'+Algo+'_'+groomed)
		#----- Drawing -----------------------
		h1.GetXaxis().SetTitle( histoInfo[1] )
		binWidth = h1.GetBinWidth(1)
		h1.GetYaxis().SetTitle( histoInfo[2]+str(binWidth) )
		h1.SetLineColor(1)
		h1.SetLineWidth(2)
		h2.SetLineColor(2)
		h2.SetLineWidth(2)
		h1.SetMaximum(1.2*TMath.Max(h1.GetBinContent(h1.GetMaximumBin()),h2.GetBinContent(h2.GetMaximumBin())))

		legend=TLegend(0.75,0.65,0.90,0.85)
		legend.SetFillColor(0)
		legend.AddEntry(h1, Algo+' only', "l")
		legend.AddEntry(h2, Algo+' '+groomed, "l")
		legend.SetTextSize(0.03)

		if ( 'numberPartonsSameJet' in histoInfo[0] ):
			h1.GetXaxis().SetBinLabel( 1 , 'NoMerged' )
			h1.GetXaxis().SetBinLabel( 2 , 'SinglyMerged' )
			h1.GetXaxis().SetBinLabel( 3 , 'DoublyMerged' )
			h1.GetXaxis().SetBinLabel( 4 , 'TriplyMerged' )
			h1.GetXaxis().SetBinLabel( 5 , 'FourlyMerged' )
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

def DrawCmpAllGrom( Sample, inputDir, outputName, outputDir, listHistos, Algo):
	"""create analysis Plots """

	gStyle.SetOptStat(0)
	targetDir = outputDir + dateKey + '/'
	print 'Output directory: ', targetDir
	if not ( os.path.exists( targetDir ) ): os.makedirs( targetDir )
	tarFile = dateKey+"files_"+Sample+"_"+Algo+"_"+groomed+".tar.gz"
	tar = tarfile.open( targetDir + tarFile, "w:gz")

	outputList = [] ### for format
	#---- open the files --------------------
	inputFile1 = TFile.Open( inputDir+Sample+'_'+Algo+'__Plots.root' )
	inputFile2 = TFile.Open( inputDir+Sample+'_'+Algo+'_Trimmed_Plots.root' )
	inputFile3 = TFile.Open( inputDir+Sample+'_'+Algo+'_Pruned_Plots.root' )
	inputFile4 = TFile.Open( inputDir+Sample+'_'+Algo+'_Filtered_Plots.root' )
	#inputFile4 = TFile.Open( inputDir+Sample+'_'+Algo+'_FilteredN2_Plots.root' )
	#inputFile6 = TFile.Open( inputDir+Sample+'_'+Algo+'_FilteredN3_Plots.root' )
	inputFile5 = TFile.Open( inputDir+Sample+'_'+Algo+'_MassDropFiltered_Plots.root' )
	#print 'Drawing Histograms from: ', inputFile1.GetName(), inputFile2.GetName(), inputFile3.GetName(), inputFile4.GetName(), inputFile5.GetName(), inputFile5.GetName()
	print 'Drawing Histograms from: ', inputFile1.GetName(), inputFile2.GetName(), inputFile3.GetName(), inputFile4.GetName(), inputFile5.GetName()

	for histoInfo in listHistos:
	
		outputFileName = dateKey+'_'+histoInfo[0]+'_'+Sample+'_'+Algo+'_cmpAllGroomed.png'  
		print 'Processing.......', outputFileName
		outputFile = targetDir + outputFileName
		outputList.append( outputFileName )
		print histoInfo[0]
		h1 = inputFile1.Get('h_'+histoInfo[0]+'_'+Algo+'_')
		h2 = inputFile2.Get('h_'+histoInfo[0]+'_'+Algo+'_Trimmed')
		h3 = inputFile3.Get('h_'+histoInfo[0]+'_'+Algo+'_Pruned')
		h4 = inputFile4.Get('h_'+histoInfo[0]+'_'+Algo+'_Filtered')
		#h4 = inputFile4.Get('h_'+histoInfo[0]+'_'+Algo+'_FilteredN2')
		#h6 = inputFile6.Get('h_'+histoInfo[0]+'_'+Algo+'_FilteredN3')
		h5 = inputFile5.Get('h_'+histoInfo[0]+'_'+Algo+'_MassDropFiltered')
		#----- Drawing -----------------------
		h1.GetXaxis().SetTitle( histoInfo[1] )
		binWidth = h1.GetBinWidth(1)
		h1.GetYaxis().SetTitle( histoInfo[2]+str(binWidth) )
		h1.SetLineColor(1)
		h1.SetLineWidth(2)
		h2.SetLineColor(2)
		h2.SetLineWidth(2)
		h3.SetLineColor(3)
		h3.SetLineWidth(2)
		h4.SetLineColor(4)
		h4.SetLineWidth(2)
		h5.SetLineColor(6)
		h5.SetLineWidth(2)
		#h6.SetLineColor(7)
		#h6.SetLineWidth(2)
		#h1.SetMaximum(1.2*max(h1.GetBinContent(h1.GetMaximumBin()),h2.GetBinContent(h2.GetMaximumBin()),h3.GetBinContent(h3.GetMaximumBin()),h4.GetBinContent(h4.GetMaximumBin()),h5.GetBinContent(h5.GetMaximumBin()),h5.GetBinContent(h5.GetMaximumBin())))
		h1.SetMaximum(1.2*max(h1.GetBinContent(h1.GetMaximumBin()),h2.GetBinContent(h2.GetMaximumBin()),h3.GetBinContent(h3.GetMaximumBin()),h4.GetBinContent(h4.GetMaximumBin()),h5.GetBinContent(h5.GetMaximumBin())))

		legend=TLegend(0.70,0.70,0.90,0.90)
		legend.SetFillStyle(0)
		legend.AddEntry(h1, Algo+' only', "l")
		legend.AddEntry(h2, Algo+' Trimmed', "l")
		legend.AddEntry(h3, Algo+' Pruned', "l")
		legend.AddEntry(h4, Algo+' Filtered N=2', "l")
		#legend.AddEntry(h4, Algo+' Filtered N=2', "l")
		#legend.AddEntry(h6, Algo+' Filtered N=3', "l")
		legend.AddEntry(h5, Algo+' MassDropFiltered', "l")
		legend.SetTextSize(0.03)

		can = TCanvas('can_'+histoInfo[0],'can_'+histoInfo[0],800,500)
		#if 'Pt' in histoInfo[0]: can.SetLogy()
		#if 'Mass' in histoInfo[0]: can.SetLogy()
		h1.Sumw2()
		h2.Sumw2()
		h3.Sumw2()
		h4.Sumw2()
		h5.Sumw2()
		#h6.Sumw2()
		h1.Draw('histe ')
		h2.Draw('same histe')
		h3.Draw('same histe')
		h4.Draw('same histe')
		h5.Draw('same histe')
		#h6.Draw('same histe')
		legend.Draw()
		if 'cut' in histoInfo[0]: setSelectionTitleCuts( outputName )
		else: setSelectionTitle( Sample )
		can.SaveAs( outputFile )
		del can
	
		tar.add( outputFile, outputFileName )

	tar.close()
	print 'Creating tar file with all plots named: ',  tarFile
	printHTML( outputList  )
	printLatex( outputList  )

def DrawCmpAllGromQCD( Sample, inputDir, outputDir, listHistos, Algo):
	"""create analysis Plots """

	gStyle.SetOptStat(0)
	targetDir = outputDir + dateKey + '/'
	print 'Output directory: ', targetDir
	if not ( os.path.exists( targetDir ) ): os.makedirs( targetDir )
	tarFile = dateKey+"files_"+Sample+"_"+Algo+"_"+groomed+".tar.gz"
	tar = tarfile.open( targetDir + tarFile, "w:gz")

	outputList = [] ### for format
	#---- open the files --------------------
	inputFile1 = TFile.Open( inputDir+'/QCD_HT-250To500_'+Algo+'__Plots.root' )
	inputFile11 = TFile.Open( inputDir+'/QCD_HT-500To1000_'+Algo+'__Plots.root' )
	inputFile12 = TFile.Open( inputDir+'/QCD_HT-1000ToInf_'+Algo+'__Plots.root' )
	inputFile2 = TFile.Open( inputDir+'/QCD_HT-250To500_'+Algo+'_Trimmed_Plots.root' )
	inputFile21 = TFile.Open( inputDir+'/QCD_HT-500To1000_'+Algo+'_Trimmed_Plots.root' )
	inputFile22 = TFile.Open( inputDir+'/QCD_HT-1000ToInf_'+Algo+'_Trimmed_Plots.root' )
	inputFile3 = TFile.Open( inputDir+'/QCD_HT-250To500_'+Algo+'_Pruned_Plots.root' )
	inputFile31 = TFile.Open( inputDir+'/QCD_HT-500To1000_'+Algo+'_Pruned_Plots.root' )
	inputFile32 = TFile.Open( inputDir+'/QCD_HT-1000ToInf_'+Algo+'_Pruned_Plots.root' )
	inputFile4 = TFile.Open( inputDir+'/QCD_HT-250To500_'+Algo+'_Filtered_Plots.root' )
	inputFile41 = TFile.Open( inputDir+'/QCD_HT-500To1000_'+Algo+'_Filtered_Plots.root' )
	inputFile42 = TFile.Open( inputDir+'/QCD_HT-1000ToInf_'+Algo+'_Filtered_Plots.root' )
	#inputFile4 = TFile.Open( inputDir+Sample+'_'+Algo+'_FilteredN2_Plots.root' )
	#inputFile6 = TFile.Open( inputDir+Sample+'_'+Algo+'_FilteredN3_Plots.root' )
	inputFile5 = TFile.Open( inputDir+'/QCD_HT-250To500_'+Algo+'_MassDropFiltered_Plots.root' )
	inputFile51 = TFile.Open( inputDir+'/QCD_HT-500To1000_'+Algo+'_MassDropFiltered_Plots.root' )
	inputFile52 = TFile.Open( inputDir+'/QCD_HT-1000ToInf_'+Algo+'_MassDropFiltered_Plots.root' )
	#print 'Drawing Histograms from: ', inputFile1.GetName(), inputFile2.GetName(), inputFile3.GetName(), inputFile4.GetName(), inputFile5.GetName(), inputFile5.GetName()
	print 'Drawing Histograms from: ', inputFile1.GetName(), inputFile2.GetName(), inputFile3.GetName(), inputFile4.GetName(), inputFile5.GetName()

	for histoInfo in listHistos:
	
		outputFileName = dateKey+'_'+histoInfo[0]+'_'+Sample+'_'+Algo+'_cmpAllGroomed.pdf'  
		print 'Processing.......', outputFileName
		outputFile = targetDir + outputFileName
		outputList.append( outputFileName )
		print histoInfo[0]
		h1 = inputFile1.Get('h_'+histoInfo[0]+'_'+Algo+'_')
		h11 = inputFile11.Get('h_'+histoInfo[0]+'_'+Algo+'_')
		h12 = inputFile12.Get('h_'+histoInfo[0]+'_'+Algo+'_')
		h1.Add( h11 )
		h1.Add( h12 )
		h2 = inputFile2.Get('h_'+histoInfo[0]+'_'+Algo+'_Trimmed')
		h21 = inputFile21.Get('h_'+histoInfo[0]+'_'+Algo+'_Trimmed')
		h22 = inputFile22.Get('h_'+histoInfo[0]+'_'+Algo+'_Trimmed')
		h2.Add( h21 )
		h2.Add( h22 )
		h3 = inputFile3.Get('h_'+histoInfo[0]+'_'+Algo+'_Pruned')
		h31 = inputFile31.Get('h_'+histoInfo[0]+'_'+Algo+'_Pruned')
		h32 = inputFile32.Get('h_'+histoInfo[0]+'_'+Algo+'_Pruned')
		h3.Add( h31 )
		h3.Add( h32 )
		h4 = inputFile4.Get('h_'+histoInfo[0]+'_'+Algo+'_Filtered')
		h41 = inputFile41.Get('h_'+histoInfo[0]+'_'+Algo+'_Filtered')
		h42 = inputFile42.Get('h_'+histoInfo[0]+'_'+Algo+'_Filtered')
		h4.Add( h41 )
		h4.Add( h42 )
		#h4 = inputFile4.Get('h_'+histoInfo[0]+'_'+Algo+'_FilteredN2')
		#h6 = inputFile6.Get('h_'+histoInfo[0]+'_'+Algo+'_FilteredN3')
		h5 = inputFile5.Get('h_'+histoInfo[0]+'_'+Algo+'_MassDropFiltered')
		h51 = inputFile51.Get('h_'+histoInfo[0]+'_'+Algo+'_MassDropFiltered')
		h52 = inputFile52.Get('h_'+histoInfo[0]+'_'+Algo+'_MassDropFiltered')
		h5.Add( h51 )
		h5.Add( h52 )
		#----- Drawing -----------------------
		h1.GetXaxis().SetTitle( histoInfo[1] )
		binWidth = h1.GetBinWidth(1)
		h1.GetYaxis().SetTitle( histoInfo[2]+str(binWidth) )
		h1.SetLineColor(1)
		h1.SetLineWidth(2)
		h2.SetLineColor(2)
		h2.SetLineWidth(2)
		h3.SetLineColor(3)
		h3.SetLineWidth(2)
		h4.SetLineColor(4)
		h4.SetLineWidth(2)
		h5.SetLineColor(6)
		h5.SetLineWidth(2)
		#h6.SetLineColor(7)
		#h6.SetLineWidth(2)
		#h1.SetMaximum(1.2*max(h1.GetBinContent(h1.GetMaximumBin()),h2.GetBinContent(h2.GetMaximumBin()),h3.GetBinContent(h3.GetMaximumBin()),h4.GetBinContent(h4.GetMaximumBin()),h5.GetBinContent(h5.GetMaximumBin()),h5.GetBinContent(h5.GetMaximumBin())))
		h1.SetMaximum(1.2*max(h1.GetBinContent(h1.GetMaximumBin()),h2.GetBinContent(h2.GetMaximumBin()),h3.GetBinContent(h3.GetMaximumBin()),h4.GetBinContent(h4.GetMaximumBin()),h5.GetBinContent(h5.GetMaximumBin())))

		legend=TLegend(0.70,0.70,0.90,0.90)
		legend.SetFillStyle(0)
		legend.AddEntry(h1, Algo+' only', "l")
		legend.AddEntry(h2, Algo+' Trimmed', "l")
		legend.AddEntry(h3, Algo+' Pruned', "l")
		legend.AddEntry(h4, Algo+' Filtered N=2', "l")
		#legend.AddEntry(h4, Algo+' Filtered N=2', "l")
		#legend.AddEntry(h6, Algo+' Filtered N=3', "l")
		legend.AddEntry(h5, Algo+' MassDropFiltered', "l")
		legend.SetTextSize(0.03)

		can = TCanvas('can_'+histoInfo[0],'can_'+histoInfo[0],800,500)
		#if 'Pt' in histoInfo[0]: can.SetLogy()
		#if 'Mass' in histoInfo[0]: can.SetLogy()
		h1.Sumw2()
		h2.Sumw2()
		h3.Sumw2()
		h4.Sumw2()
		h5.Sumw2()
		#h6.Sumw2()
		h1.Draw('histe ')
		h2.Draw('same histe')
		h3.Draw('same histe')
		h4.Draw('same histe')
		h5.Draw('same histe')
		#h6.Draw('same histe')
		legend.Draw()
		if 'cut' in histoInfo[0]: setSelectionTitleCuts( Sample )
		else: setSelectionTitle( Sample )
		can.SaveAs( outputFile )
		del can
	
		tar.add( outputFile, outputFileName )

	tar.close()
	print 'Creating tar file with all plots named: ',  tarFile
	printHTML( outputList  )
	printLatex( outputList  )

def DrawMatchCmpAllGrom( Sample, inputDir, outputName, outputDir, listHistos, Algo):
	"""create analysis Plots """

	gStyle.SetOptStat(0)
	targetDir = outputDir + dateKey + '/'
	print 'Output directory: ', targetDir
	if not ( os.path.exists( targetDir ) ): os.makedirs( targetDir )
	tarFile = dateKey+"files_"+Sample+"_"+Algo+"_"+groomed+".tar.gz"
	tar = tarfile.open( targetDir + tarFile, "w:gz")

	outputList = [] ### for format
	#---- open the files --------------------
	inputFile1 = TFile.Open( inputDir+Sample+'_Matching_'+Algo+'__Plots.root' )
	inputFile2 = TFile.Open( inputDir+Sample+'_Matching_'+Algo+'_Trimmed_Plots.root' )
	inputFile3 = TFile.Open( inputDir+Sample+'_Matching_'+Algo+'_Pruned_Plots.root' )
	inputFile4 = TFile.Open( inputDir+Sample+'_Matching_'+Algo+'_Filtered_Plots.root' )
	inputFile5 = TFile.Open( inputDir+Sample+'_Matching_'+Algo+'_MassDropFiltered_Plots.root' )
	print 'Drawing Histograms from: ', inputFile1.GetName(), inputFile2.GetName(), inputFile3.GetName(), inputFile4.GetName(), inputFile5.GetName()

	for histoInfo in listHistos:
	
		outputFileName = dateKey+'_'+histoInfo[0]+'_'+outputName+'_'+Algo+'_Matching_cmpAllGroomed.pdf'  
		print 'Processing.......', outputFileName
		outputFile = targetDir + outputFileName
		outputList.append( outputFileName )
		print histoInfo[0]
		h1 = inputFile1.Get('h_'+histoInfo[0]+'_'+Algo+'_')
		h2 = inputFile2.Get('h_'+histoInfo[0]+'_'+Algo+'_Trimmed')
		h3 = inputFile3.Get('h_'+histoInfo[0]+'_'+Algo+'_Pruned')
		h4 = inputFile4.Get('h_'+histoInfo[0]+'_'+Algo+'_Filtered')
		h5 = inputFile5.Get('h_'+histoInfo[0]+'_'+Algo+'_MassDropFiltered')
		#----- Drawing -----------------------
		h1.GetXaxis().SetTitle( histoInfo[1] )
		binWidth = h1.GetBinWidth(1)
		h1.GetYaxis().SetTitle( histoInfo[2]+str(binWidth) )
		h1.SetLineColor(1)
		h1.SetLineWidth(2)
		h2.SetLineColor(2)
		h2.SetLineWidth(2)
		h3.SetLineColor(3)
		h3.SetLineWidth(2)
		h4.SetLineColor(4)
		h4.SetLineWidth(2)
		h5.SetLineColor(6)
		h5.SetLineWidth(2)
		h1.SetMaximum(1.2*max(h1.GetBinContent(h1.GetMaximumBin()),h2.GetBinContent(h2.GetMaximumBin()),h3.GetBinContent(h3.GetMaximumBin()),h4.GetBinContent(h4.GetMaximumBin()),h5.GetBinContent(h5.GetMaximumBin())))

		legend=TLegend(0.75,0.65,0.90,0.85)
		legend.SetFillStyle(0)
		legend.AddEntry(h1, Algo+' only', "l")
		legend.AddEntry(h2, Algo+' Trimmed', "l")
		legend.AddEntry(h3, Algo+' Pruned', "l")
		legend.AddEntry(h4, Algo+' Filtered', "l")
		legend.AddEntry(h5, Algo+' MassDropFiltered', "l")
		legend.SetTextSize(0.03)

		can = TCanvas('can_'+histoInfo[0],'can_'+histoInfo[0],800,500)
		#if 'Pt' in histoInfo[0]: can.SetLogy()
		#if 'Mass' in histoInfo[0]: can.SetLogy()
		h1.Sumw2()
		h2.Sumw2()
		h1.Draw('histe ')
		h2.Draw('same histe')
		h3.Draw('same histe')
		h4.Draw('same histe')
		h5.Draw('same histe')
		legend.Draw()
		setSelectionTitle( Sample )
		can.SaveAs( outputFile )
		del can
	
		tar.add( outputFile, outputFileName )

	tar.close()
	print 'Creating tar file with all plots named: ',  tarFile
	printHTML( outputList  )
	printLatex( outputList  )




####################################################################################################################
### Draw 2D Histograms from List create tar file and HTML code    #####
####################################################################################################################
def Draw2D( Sample, inputDir, outputName, outputDir, listHistos, Algo, groomed):
	"""create Plots from MCTruth"""

	gStyle.SetOptStat(1111)
	targetDir = outputDir + dateKey + '/'
	print 'Output directory: ', targetDir
	if not ( os.path.exists( targetDir ) ): os.makedirs( targetDir )
	tarFile = dateKey+"files_"+Sample+"_"+Algo+"_"+groomed+".tar.gz"
	tar = tarfile.open( targetDir + tarFile, "w:gz")

	outputList = [] ### for format
	#---- open the files --------------------
	inputFile1 = TFile.Open( inputDir+Sample+'_'+Algo+'_'+groomed+'_Plots.root' )
	#inputFile1 = TFile.Open( inputDir+Sample+'_Matching_'+Algo+'_'+groomed+'_Plots.root' )
	print 'Drawing Histograms from: ', inputFile1.GetName()

	for histoInfo in listHistos:
	
		outputFileName = dateKey+'_'+histoInfo[0]+'_'+Sample+'_'+Algo+'with'+groomed+'.pdf'  
		print 'Processing.......', outputFileName
		outputFile = targetDir + outputFileName
		outputList.append( outputFileName )
		print histoInfo[0]
		h1 = inputFile1.Get('h_'+histoInfo[0]+'_'+Algo+'_'+groomed)
		#----- Drawing -----------------------
		h1.GetXaxis().SetTitle( histoInfo[1] )
		binWidth = h1.GetBinWidth(1)
		h1.GetYaxis().SetTitle( histoInfo[2] )
		#h1.SetLineColor(1)
		#h1.SetLineWidth(2)
		#h1.SetMaximum(1.2*TMath.Max(h1.GetBinContent(h1.GetMaximumBin()),h2.GetBinContent(h2.GetMaximumBin())))

#		legend=TLegend(0.75,0.65,0.90,0.85)
#		legend.SetFillColor(0)
#		legend.AddEntry(h1, Algo+' only', "l")
#		legend.AddEntry(h2, Algo+' '+groomed, "l")
#		legend.SetTextSize(0.03)

		can = TCanvas('can_'+histoInfo[0],'can_'+histoInfo[0],800,500)
		can.SetLogz()
		gStyle.SetPadRightMargin(0.1)
		gStyle.SetStatY(0.9)
		gStyle.SetStatX(0.90)
		h1.Draw("colz")
		#legend.Draw()
		if 'cut' in histoInfo[0]: setSelectionTitleCuts2D( outputName )
		else: setSelectionTitle( Sample )
		can.SaveAs( outputFile )
		del can
	
		tar.add( outputFile, outputFileName )

	tar.close()
	print 'Creating tar file with all plots named: ',  tarFile
	printHTML( outputList  )
	printLatex( outputList  )

def Draw2DQCD( Sample, inputDir, outputName, outputDir, listHistos, Algo, groomed):
	"""create Plots from MCTruth"""

	gStyle.SetOptStat(1111)
	targetDir = outputDir + dateKey + '/'
	print 'Output directory: ', targetDir
	if not ( os.path.exists( targetDir ) ): os.makedirs( targetDir )
	tarFile = dateKey+"files_"+Sample+"_"+Algo+"_"+groomed+".tar.gz"
	tar = tarfile.open( targetDir + tarFile, "w:gz")

	outputList = [] ### for format
	#---- open the files --------------------
	inputFile1 = TFile.Open( inputDir+'/QCD_HT-250To500_'+Algo+'_'+groomed+'_Plots.root' )
	inputFile2 = TFile.Open( inputDir+'/QCD_HT-500To1000_'+Algo+'_'+groomed+'_Plots.root' )
	inputFile3 = TFile.Open( inputDir+'/QCD_HT-1000ToInf_'+Algo+'_'+groomed+'_Plots.root' )
	#inputFile1 = TFile.Open( inputDir+Sample+'_Matching_'+Algo+'_'+groomed+'_Plots.root' )
	print 'Drawing Histograms from: ', inputFile1.GetName()

	for histoInfo in listHistos:
	
		outputFileName = dateKey+'_'+histoInfo[0]+'_'+Sample+'_'+Algo+'with'+groomed+'.pdf'  
		print 'Processing.......', outputFileName
		outputFile = targetDir + outputFileName
		outputList.append( outputFileName )
		print histoInfo[0]
		h1 = inputFile1.Get('h_'+histoInfo[0]+'_'+Algo+'_'+groomed)
		h2 = inputFile2.Get('h_'+histoInfo[0]+'_'+Algo+'_'+groomed)
		h3 = inputFile3.Get('h_'+histoInfo[0]+'_'+Algo+'_'+groomed)
		h1.Add( h2 )
		h1.Add( h3 )
		#----- Drawing -----------------------
		h1.GetXaxis().SetTitle( histoInfo[1] )
		binWidth = h1.GetBinWidth(1)
		h1.GetYaxis().SetTitle( histoInfo[2] )

		can = TCanvas('can_'+histoInfo[0],'can_'+histoInfo[0],800,500)
		can.SetLogz()
		gStyle.SetPadRightMargin(0.1)
		gStyle.SetStatY(0.9)
		gStyle.SetStatX(0.90)
		h1.Draw("colz")
		#legend.Draw()
		if 'cut' in histoInfo[0]: setSelectionTitleCuts2D( outputName )
		else: setSelectionTitle( Sample )
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
	parser.add_option( '-j', '--jetAlgo1', action='store', type='string', dest='jetAlgo1', default='AK5', help='Jet Algorithm 1' )
	parser.add_option( '-2', '--jetAlgo2', action='store', type='string', dest='jetAlgo2', default='AK7', help='Jet Algorithm 2' )
	parser.add_option( '-g', '--groomed', action='store', type='string', dest='groomed', default='', help='Type of Grooming technique' )
	parser.add_option( '-c', '--cat', action='store', type='string', dest='cat', default='NO', help='Type of merging category' )

	(options, args) = parser.parse_args()

	mass = options.mass
	jetAlgo1 = options.jetAlgo1
	jetAlgo2 = options.jetAlgo2
	process = options.process
	groomed = options.groomed
	cat = options.cat

	listHistos = [
		[ 'ht', 'H_{T} [GeV]', 'Events / '], 
		[ 'numberPV', 'Number of Primary Vertex', 'Events / '], 
		[ 'MET', 'MET [GeV]', 'Events / '], 
		[ 'numberJets', 'Number of Jets', 'Events / '], 
		[ 'jetPt', 'Jets p_{T} [GeV]', 'Jets per Events / ' ],
		[ 'jetEta', 'Jets #eta', 'Jets per Events / ' ],
		[ 'jetPhi', 'Jets #phi', 'Jets per Events / ' ],
		[ 'jetMass', 'Jets Mass [GeV]', 'Jets per Events / ' ],
		[ 'jetArea', 'Jets Area', 'Jets per Events / ' ],
		[ 'jetTau1', '#tau_{1}', 'Jets per Events / ' ],
		[ 'jetTau2', '#tau_{2}', 'Jets per Events / ' ],
		[ 'jetTau3', '#tau_{3}', 'Jets per Events / ' ],
		[ 'jetTau21', '#tau_{2} / #tau_{1}', 'Jets per Events / ' ],
		[ 'jetTau31', '#tau_{3} / #tau_{1}', 'Jets per Events / ' ],
		[ 'jetTau32', '#tau_{3} / #tau_{2}', 'Jets per Events / ' ],

		[ 'jet1Pt', 'Leading Jet p_{T} [GeV]', 'Events / ' ],
		[ 'jet1Eta', 'Leading Jet #eta', 'Events / ' ],
		[ 'jet1Phi', 'Leading Jet #phi', 'Events / ' ],
		[ 'jet1Mass', 'Leading Jet Mass [GeV]', 'Events / ' ],
		[ 'jet1Area', 'Leading Jet Area', 'Events / ' ],
		[ 'jet1Tau1', '#tau_{1} Leading Jet', 'Events / ' ],
		[ 'jet1Tau2', '#tau_{2} Leading Jet', 'Events / ' ],
		[ 'jet1Tau3', '#tau_{3} Leading Jet', 'Events / ' ],
		[ 'jet1Tau21', '#tau_{2} / #tau_{1} Leading Jet', 'Events / ' ],
		[ 'jet1Tau31', '#tau_{3} / #tau_{1} Leading Jet', 'Events / ' ],
		[ 'jet1Tau32', '#tau_{3} / #tau_{2} Leading Jet', 'Events / ' ],

		[ 'jet2Pt', '2nd Leading Jet p_{T} [GeV]', 'Events / ' ],
		[ 'jet2Eta', '2nd Leading Jet #eta', 'Events / ' ],
		[ 'jet2Phi', '2nd Leading Jet #phi', 'Events / ' ],
		[ 'jet2Mass', '2nd Leading Jet Mass [GeV]', 'Events / ' ],
		[ 'jet2Area', '2nd Leading Jet Area', 'Events / ' ],
		[ 'jet2Tau1', '#tau_{1} 2nd Leading Jet', 'Events / ' ],
		[ 'jet2Tau2', '#tau_{2} 2nd Leading Jet', 'Events / ' ],
		[ 'jet2Tau3', '#tau_{3} 2nd Leading Jet', 'Events / ' ],
		[ 'jet2Tau21', '#tau_{2} / #tau_{1} 2nd Leading Jet', 'Events / ' ],
		[ 'jet2Tau31', '#tau_{3} / #tau_{1} 2nd Leading Jet', 'Events / ' ],
		[ 'jet2Tau32', '#tau_{3} / #tau_{2} 2nd Leading Jet', 'Events / ' ],

#		[ 'jet3Pt', '3rd Leading Jet p_{T} [GeV]', 'Events / ' ],
#		[ 'jet3Eta', '3rd Leading Jet #eta', 'Events / ' ],
#		[ 'jet3Phi', '3rd Leading Jet #phi', 'Events / ' ],
#		[ 'jet3Mass', '3rd Leading Jet Mass [GeV]', 'Events / ' ],
#		[ 'jet3Area', '3rd Leading Jet Area', 'Events / ' ],
#		[ 'jet3Tau1', '#tau_{1} 3rd Leading Jet', 'Events / ' ],
#		[ 'jet3Tau2', '#tau_{2} 3rd Leading Jet', 'Events / ' ],
#		[ 'jet3Tau3', '#tau_{3} 3rd Leading Jet', 'Events / ' ],
#		[ 'jet3Tau21', '#tau_{2} / #tau_{1} 3rd Leading Jet', 'Events / ' ],
#		[ 'jet3Tau31', '#tau_{3} / #tau_{1} 3rd Leading Jet', 'Events / ' ],
#		[ 'jet3Tau32', '#tau_{3} / #tau_{2} 3rd Leading Jet', 'Events / ' ],

		[ 'cut_ht', 'H_{T} [GeV]', 'Events / '], 
		[ 'cut_numberJets', 'Number of Jets', 'Events / '], 
#		[ 'cut_numberPV', 'Number of Primary Vertex', 'Events / '], 
#		[ 'cut_MET', 'MET [GeV]', 'Events / '], 
#		[ 'cut_jetPt', 'Jets p_{T} [GeV]', 'Jets per Events / ' ],
#		[ 'cut_jetEta', 'Jets #eta', 'Jets per Events / ' ],
#		[ 'cut_jetPhi', 'Jets #phi', 'Jets per Events / ' ],
#		[ 'cut_jetMass', 'Jets Mass [GeV]', 'Jets per Events / ' ],
#		[ 'cut_jetArea', 'Jets Area', 'Jets per Events / ' ],
#		[ 'cut_jetTau1', '#tau_{1}', 'Jets per Events / ' ],
#		[ 'cut_jetTau2', '#tau_{2}', 'Jets per Events / ' ],
#		[ 'cut_jetTau3', '#tau_{3}', 'Jets per Events / ' ],
#		[ 'cut_jetTau21', '#tau_{2} / #tau_{1}', 'Jets per Events / ' ],
#		[ 'cut_jetTau31', '#tau_{3} / #tau_{1}', 'Jets per Events / ' ],
#		[ 'cut_jetTau32', '#tau_{3} / #tau_{2}', 'Jets per Events / ' ],

		[ 'cut_jet1Pt', 'Leading Jet p_{T} [GeV]', 'Events / ' ],
		[ 'cut_jet1Eta', 'Leading Jet #eta', 'Events / ' ],
		[ 'cut_jet1Phi', 'Leading Jet #phi', 'Events / ' ],
		[ 'cut_jet1Mass', 'Leading Jet Mass [GeV]', 'Events / ' ],
		[ 'cut_jet1Area', 'Leading Jet Area', 'Events / ' ],
		[ 'cut_jet1Tau1', '#tau_{1} Leading Jet', 'Events / ' ],
		[ 'cut_jet1Tau2', '#tau_{2} Leading Jet', 'Events / ' ],
		[ 'cut_jet1Tau3', '#tau_{3} Leading Jet', 'Events / ' ],
		[ 'cut_jet1Tau21', '#tau_{2} / #tau_{1} Leading Jet', 'Events / ' ],
		[ 'cut_jet1Tau31', '#tau_{3} / #tau_{1} Leading Jet', 'Events / ' ],
		[ 'cut_jet1Tau32', '#tau_{3} / #tau_{2} Leading Jet', 'Events / ' ],

		[ 'cut_jet2Pt', '2nd Leading Jet p_{T} [GeV]', 'Events / ' ],
		[ 'cut_jet2Eta', '2nd Leading Jet #eta', 'Events / ' ],
		[ 'cut_jet2Phi', '2nd Leading Jet #phi', 'Events / ' ],
		[ 'cut_jet2Mass', '2nd Leading Jet Mass [GeV]', 'Events / ' ],
		[ 'cut_jet2Area', '2nd Leading Jet Area', 'Events / ' ],
		[ 'cut_jet2Tau1', '#tau_{1} 2nd Leading Jet', 'Events / ' ],
		[ 'cut_jet2Tau2', '#tau_{2} 2nd Leading Jet', 'Events / ' ],
		[ 'cut_jet2Tau3', '#tau_{3} 2nd Leading Jet', 'Events / ' ],
		[ 'cut_jet2Tau21', '#tau_{2} / #tau_{1} 2nd Leading Jet', 'Events / ' ],
		[ 'cut_jet2Tau31', '#tau_{3} / #tau_{1} 2nd Leading Jet', 'Events / ' ],
		[ 'cut_jet2Tau32', '#tau_{3} / #tau_{2} 2nd Leading Jet', 'Events / ' ],
	]
	#if ('analysis' in process ): analysisPlots( 'stopUDD312_'+mass, '/cms/gomez/Stops/st_jj/treeResults/rootFiles/140423/', 'stopUDD312_'+mass+'', '/cms/gomez/Stops/st_jj/treeResults/Plots/', listHistos, jetAlgo1, groomed )
	if ('analysis' in process ): analysisPlots( 'RPVSt'+mass+'tojj_8TeV_HT500', '/cms/gomez/Files/RPVSttojj_8TeV/treeResults/rootFiles/', 'RPV Stop '+mass+' GeV', '/cms/gomez/Files/Plots/', listHistos, jetAlgo1, groomed )
	if ('anaCmpGrom' in process ): DrawCmp( 'stopUDD312_'+mass, '/cms/gomez/Stops/st_jj/treeResults/rootFiles/140417/', 'stopUDD312_'+mass+'', '/cms/gomez/Stops/st_jj/treeResults/Plots/', listHistos, jetAlgo1, groomed )
	#if ('anaCmpAll' in process ): DrawCmpAllGrom( 'stopUDD312_'+mass, '/cms/gomez/Stops/st_jj/treeResults/rootFiles/140417/', 'stopUDD312_'+mass+'', '/cms/gomez/Stops/st_jj/treeResults/Plots/', listHistos, jetAlgo1 )
	if ('anaCmpAll' in process ): DrawCmpAllGrom( 'RPVSt'+mass+'tojj_8TeV_HT500', '/cms/gomez/Files/RPVSttojj_8TeV/treeResults/rootFiles/', 'RPV Stop '+mass+' GeV', '/cms/gomez/Files/Plots/', listHistos, jetAlgo1 )
	if ('dataCmpAll' in process ): DrawCmpAllGrom( 'Data_HT-Run2012A-22Jan2013', '/cms/gomez/Files/DATA/treeResults/rootFiles/140510/', 'Data', '/cms/gomez/Files/Plots/', listHistos, jetAlgo1 )
	if ('QCDCmpAll' in process ): DrawCmpAllGromQCD( 'QCD_8TeV', '/cms/gomez/Files/QCD_8TeV/treeResults/rootFiles/', '/cms/gomez/Files/Plots/', listHistos, jetAlgo1 )
	if ('DATAQCD' in process ): DrawCmpDataQCD( 'Data_HT-Run2012A-22Jan2013', '/cms/gomez/Files/DATA/treeResults/rootFiles/140510/', '', '/cms/gomez/Files/Plots/', listHistos, jetAlgo1, groomed )

	list2DHistos = [

			[ 'jet1PtvsMass', 'Leading Jet p_{T} [GeV]', 'Leading Jet Mass [GeV]' ],
			[ 'jet1Tau2vsTau1', '#tau_{1} Leading Jet', '#tau_{2} Leading Jet' ],
			[ 'jet1Tau3vsTau1', '#tau_{1} Leading Jet', '#tau_{3} Leading Jet' ],
			[ 'jet1Tau3vsTau2', '#tau_{2} Leading Jet', '#tau_{3} Leading Jet' ],
			[ 'jet1Ptvsht', 'Leading Jet p_{T} [GeV]', 'H_{t} [GeV]' ],
			[ 'jet1Massvsht', 'Leading Jet Mass [GeV]', 'H_{t} [GeV]' ],
			[ 'jet1MassvsTau21', 'Leading Jet Mass [GeV]', '#tau_{2}/#tau_{1} Leading Jet' ],

			[ 'jet2PtvsMass', '2nd Leading Jet p_{T} [GeV]', '2nd Leading Jet Mass [GeV]' ],
			[ 'jet2Tau2vsTau1', '#tau_{1} 2nd Leading Jet', '#tau_{2} 2nd Leading Jet' ],
			[ 'jet2Tau3vsTau1', '#tau_{1} 2nd Leading Jet', '#tau_{3} 2nd Leading Jet' ],
			[ 'jet2Tau3vsTau2', '#tau_{2} 2nd Leading Jet', '#tau_{3} 2nd Leading Jet' ],
			[ 'jet2Ptvsht', '2nd Leading Jet p_{T} [GeV]', 'H_{t} [GeV]' ],
			[ 'jet2Massvsht', '2nd Leading Jet Mass [GeV]', 'H_{t} [GeV]' ],
			[ 'jet2MassvsTau21', '2nd Leading Jet Mass [GeV]', '#tau_{2}/#tau_{1} 2nd Leading Jet' ],

			[ 'jet1vsjet2Mass', 'Leading Jet Mass [GeV]', '2nd Leading Jet Mass [GeV]' ],
			[ 'jet1vsjet2Tau21', '#tau_{2}/#tau_{1} Leading Jet', '#tau_{2}/#tau_{1} 2nd Leading Jet' ],

			[ 'cut_jet1PtvsMass', 'Leading Jet p_{T} [GeV]', 'Leading Jet Mass [GeV]' ],
			[ 'cut_jet1Tau2vsTau1', '#tau_{1} Leading Jet', '#tau_{2} Leading Jet' ],
			[ 'cut_jet1Tau3vsTau1', '#tau_{1} Leading Jet', '#tau_{3} Leading Jet' ],
			[ 'cut_jet1Tau3vsTau2', '#tau_{2} Leading Jet', '#tau_{3} Leading Jet' ],
			[ 'cut_jet1Ptvsht', 'Leading Jet p_{T} [GeV]', 'H_{t} [GeV]' ],
			[ 'cut_jet1Massvsht', 'Leading Jet Mass [GeV]', 'H_{t} [GeV]' ],
			[ 'cut_jet1MassvsTau21', 'Leading Jet Mass [GeV]', '#tau_{2}/#tau_{1} Leading Jet' ],

			[ 'cut_jet2PtvsMass', '2nd Leading Jet p_{T} [GeV]', '2nd Leading Jet Mass [GeV]' ],
			[ 'cut_jet2Tau2vsTau1', '#tau_{1} 2nd Leading Jet', '#tau_{2} 2nd Leading Jet' ],
			[ 'cut_jet2Tau3vsTau1', '#tau_{1} 2nd Leading Jet', '#tau_{3} 2nd Leading Jet' ],
			[ 'cut_jet2Tau3vsTau2', '#tau_{2} 2nd Leading Jet', '#tau_{3} 2nd Leading Jet' ],
			[ 'cut_jet2Ptvsht', '2nd Leading Jet p_{T} [GeV]', 'H_{t} [GeV]' ],
			[ 'cut_jet2Massvsht', '2nd Leading Jet Mass [GeV]', 'H_{t} [GeV]' ],
			[ 'cut_jet2MassvsTau21', '2nd Leading Jet Mass [GeV]', '#tau_{2}/#tau_{1} 2nd Leading Jet' ],

			[ 'cut_jet1vsjet2Mass', 'Leading Jet Mass [GeV]', '2nd Leading Jet Mass [GeV]' ],
			[ 'cut_jet1vsjet2Tau21', '#tau_{2}/#tau_{1} Leading Jet', '#tau_{2}/#tau_{1} 2nd Leading Jet' ],

			]

	#if ('2d' in process): Draw2D( 'stopUDD312_'+mass, '/cms/gomez/Stops/st_jj/treeResults/rootFiles/140408/', 'stopUDD312_'+mass+'', '/cms/gomez/Stops/st_jj/treeResults/Plots/', list2DHistos, jetAlgo1, groomed )
	if ('2dS' in process): Draw2D( 'RPVSt'+mass+'tojj_8TeV_HT500', '/cms/gomez/Files/RPVSttojj_8TeV/treeResults/rootFiles/', 'RPV Stop '+mass+' GeV', '/cms/gomez/Files/Plots/', list2DHistos, jetAlgo1, groomed )
	if ('2dD' in process): Draw2D( 'Data_HT-Run2012A-22Jan2013', '/cms/gomez/Files/DATA/treeResults/rootFiles/140510/', 'Data', '/cms/gomez/Files/Plots/', list2DHistos, jetAlgo1, groomed )
	if ('2dQ' in process): Draw2DQCD( 'QCD_8TeV', '/cms/gomez/Files/QCD_8TeV/treeResults/rootFiles/', 'QCD', '/cms/gomez/Files/Plots/', list2DHistos, jetAlgo1, groomed )

	##################################################################### Matching
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
		[ 'jetPt', 'Jets p_{T} [GeV]', 'Jets per Events / ' ],

		[ 'numberPartonsSameJet', 'Number of Partons with Same Jet', 'Events / ' ],
		[ 'minDeltaRPartonJet', 'min #DeltaR(parton, jet) (All Jets)', 'Parton per Event / ' ],
		[ 'secMinDeltaRPartonJet', '2nd min #DeltaR(parton, jet) (All Jets)', 'Parton per Event / '  ],
		#[ 'minvsSecMinDeltaRPartonJet 	= TH2F('h_minDeltaRvsSecMinDeltaR',	'h_minDeltaRvsSecMinDeltaR',   maxDeltaR ],

		[ 'numberPartonsWithDeltaR0p4_NoMerged', 'Number of Match Partons (NoMerged)', 'Events / ' ],
		[ 'minDeltaRPartonJet_NoMerged','min #DeltaR(parton, jet) (NoMerged)', 'Event / ' ],
		[ 'minDeltaRPartonJet_NoMerged_0','min #DeltaR(parton, jet) (NoMerged)', 'Event / ' ],
		[ 'minDeltaRPartonJet_NoMerged_1','min #DeltaR(parton, jet) (NoMerged)', 'Event / ' ],
		[ 'minDeltaRPartonJet_NoMerged_2','min #DeltaR(parton, jet) (NoMerged)', 'Event / ' ],
		[ 'minDeltaRPartonJet_NoMerged_3','min #DeltaR(parton, jet) (NoMerged)', 'Event / ' ],
		[ 'invMass_NoMerged', 'Invariant Mass of Match Jets (NoMerged) from Stop [GeV]', 'Event / ' ],
		[ 'jetPt_NoMerged', 'Jets p_{T} [GeV] (NoMerged)', 'Jets per Events / ' ],
		
		['minDeltaRPartonJet_SinglyMerged_Merged','min #DeltaR(parton, jet) Merged (SinglyMerged)', 'Parton per Event / ' ],
		['secMinDeltaRPartonJet_SinglyMerged_Merged', '2nd min #DeltaR(parton, jet) Merged (SinglyMerged)', 'Parton per Event / ' ],
		['minDeltaRPartonJet_SinglyMerged_NOMerged', 'min #DeltaR(parton, jet) Match (SinglyMerged)', 'Parton per Event / ' ],
		['secMinDeltaRPartonJet_SinglyMerged_NOMerged', '2nd min #DeltaR(parton, jet) Match (SinglyMerged)', 'Parton per Event / ' ],
		#[ 'minvsSecMinDeltaRPartonJet_SinglyMerged_Merged 	= TH2F('h_minvsSecMinDeltaRPartonJet_SinglyMerged_Merged',	'h_minvsSecMinDeltaRPartonJet_SinglyMerged_Merged', 	 maxDeltaR ],
		#[ 'minvsSecMinDeltaRPartonJet_SinglyMerged_NOMerged 	= TH2F('h_minvsSecMinDeltaRPartonJet_SinglyMerged_NOMerged',	'h_minvsSecMinDeltaRPartonJet_SinglyMerged_NOMerged',maxDeltaR ],
		['invMass_SinglyMerged_NOMerged', 'Invariant Mass of Match Jets (SinglyMerged) from Stop [GeV]', 'Event / '  ],
		['jetMass_SinglyMerged_Merged', 'Jet Mass of Merged Jets (SinglyMerged) from Stop [GeV]', 'Event / '  ],
		[ 'jetPt_SinglyMerged_NOMerged', 'Matched Jets p_{T} [GeV] (SinglyMerged)', 'Jets per Events / ' ],
		[ 'jetPt_SinglyMerged_Merged', 'Merged Jets p_{T} [GeV] (SinglyMerged)', 'Jets per Events / ' ],

		['minDeltaRPartonJet_DoublyMerged', 'min #DeltaR(parton, jet) (DoublyMerged)', 'Parton per Event / ' ],
		['secMinDeltaRPartonJet_DoublyMerged', '2nd min #DeltaR(parton, jet) (DoublyMerged)', 'Parton per Event / ' ],
		#['minvsSecMinDeltaRPartonJet_DoublyMerged',   	   maxDeltaR ],
		['jetMass_DoublyMerged_Merged', 	'Jet Mass of Merged Jets (DoublyMerged) from Stop [GeV]', 'Event / '  ],
		[ 'jetPt_DoublyMerged', 'Merged Jets p_{T} [GeV] (DoublyMerged)', 'Jets per Events / ' ],

		['minDeltaRPartonJet_TriplyMerged','min #DeltaR(parton, jet) (TriplyMerged)', 'Parton per Event / '],
		['secMinDeltaRPartonJet_TriplyMerged', '2nd min #DeltaR(parton, jet) (TriplyMerged)', 'Parton per Event / '],
		#[ 'minvsSecMinDeltaRPartonJet_TriplyMerged 	= TH2F('h_minvsSecMinDeltaRPartonJet_TriplyMerged','h_minvsSecMinDeltaRPartonJet_TriplyMerged',maxDeltaR ],
		['jetMass_TriplyMerged_Merged', 'Jet Mass of Merged Jets (TriplyMerged) from Stop [GeV]', 'Event / '  ],
		[ 'jetPt_TriplyMerged_Merged', 'Merged Jets p_{T} [GeV] (TriplyMerged)', 'Jets per Events / ' ],

		['minDeltaRPartonJet_FourlyMerged',	   'min #DeltaR(parton, jet) (FourlyMerged)', 'Parton per Event / '],

		#### with DeltaR0p4,
		['numberPartonsSameJet_DeltaR0p4','Number of Partons with Same Jet Matched', 'Events / ' ],
		[ 'jetPt_DeltaR0p4', 'Matched Jets p_{T} [GeV]', 'Jets per Events / ' ],
		['minDeltaRPartonJet_DeltaR0p4','min #DeltaR(parton, jet) (No Merged)', 'Parton per Event / ' ],
		['secMinDeltaRPartonJet_DeltaR0p4','2nd min #DeltaR(parton, jet) (No Merged)', 'Parton per Event / ' ],
		
		['minDeltaRPartonJet_NoMerged_DeltaR0p4','min #DeltaR(parton, jet) (No Merged)', 'Parton per Event / ' ],
		['minDeltaRPartonJet_NoMerged_DeltaR0p4_0','min #DeltaR(parton, jet) (No Merged)', 'Parton per Event / '  ],
		['minDeltaRPartonJet_NoMerged_DeltaR0p4_1','min #DeltaR(parton, jet) (No Merged)', 'Parton per Event / '  ],
		['minDeltaRPartonJet_NoMerged_DeltaR0p4_2','min #DeltaR(parton, jet) (No Merged)', 'Parton per Event / '  ],
		['minDeltaRPartonJet_NoMerged_DeltaR0p4_3','min #DeltaR(parton, jet) (No Merged)', 'Parton per Event / '  ],
		['invMass_NoMerged_DeltaR0p4', 	'Invariant Mass of Match Jets (NoMerged) from Stop [GeV]', 'Event / '  ],
		[ 'jetPt_NoMerged_DeltaR0p4', 'Matched Jets p_{T} [GeV] (NoMerged)', 'Jets per Events / ' ],

		['minDeltaRPartonJet_SinglyMerged_Merged_DeltaR0p4',	'min #DeltaR(parton, jet) Merged (SinglyMerged)', 'Parton per Event / '  ],
		['secMinDeltaRPartonJet_SinglyMerged_Merged_DeltaR0p4', '2nd min #DeltaR(parton, jet) Merged (SinglyMerged)', 'Parton per Event / '  ],
		['minDeltaRPartonJet_SinglyMerged_NOMerged_DeltaR0p4','min #DeltaR(parton, jet) Merged (SinglyMerged)', 'Parton per Event / '  ],
		['secMinDeltaRPartonJet_SinglyMerged_NOMerged_DeltaR0p4', '2nd min #DeltaR(parton, jet) Merged (SinglyMerged)', 'Parton per Event / '  ],
		#['minvsSecMinDeltaRPartonJet_SinglyMerged_Merged_DeltaR0p4', 	 	 	 	 	 	maxDeltaR ],
		#['minvsSecMinDeltaRPartonJet_SinglyMerged_NOMerged_DeltaR0p4', 	 	 	 	 	 	maxDeltaR ],
		['invMass_SinglyMerged_DeltaR0p4_NOMerged', 'Invariant Mass of No Merged Jets (SinglyMerged) from Stop [GeV]', 'Event / '  ],
		['jetMass_SinglyMerged_DeltaR0p4_Merged', 'jet Mass of Merged Jets (SinglyMerged) from Stop [GeV]', 'Event / '  ],
		[ 'jetPt_SinglyMerged_DeltaR0p4_NOMerged', 'No Merged Jets p_{T} [GeV] (SinglyMerged)', 'Jets per Events / ' ],
		[ 'jetPt_SinglyMerged_DeltaR0p4_Merged', 'Merged Jets p_{T} [GeV] (SinglyMerged)', 'Jets per Events / ' ],
		[ 'jetTau1_SinglyMerged_DeltaR0p4_NOMerged', '#tau_{1} NO Merged Jets (SinglyMerged)', 'Jets per Events / ' ],
		[ 'jetTau2_SinglyMerged_DeltaR0p4_NOMerged', '#tau_{2} NO Merged Jets (SinglyMerged)', 'Jets per Events / ' ],
		[ 'jetTau3_SinglyMerged_DeltaR0p4_NOMerged', '#tau_{3} NO Merged Jets (SinglyMerged)', 'Jets per Events / ' ],
		[ 'jetTau21_SinglyMerged_DeltaR0p4_NOMerged', '#tau_{2} / #tau_{1} NO Merged Jets (SinglyMerged)', 'Jets per Events / ' ],
		[ 'jetTau31_SinglyMerged_DeltaR0p4_NOMerged', '#tau_{3} / #tau_{1} NO Merged Jets (SinglyMerged)', 'Jets per Events / ' ],
		[ 'jetTau32_SinglyMerged_DeltaR0p4_NOMerged', '#tau_{3} / #tau_{2} NO Merged Jets (SinglyMerged)', 'Jets per Events / ' ],
		[ 'jetArea_SinglyMerged_DeltaR0p4_NOMerged', 'jet Area NO Merged Jets (SinglyMerged)', 'Jets per Events / ' ],
		[ 'jetMass_SinglyMerged_DeltaR0p4_NOMerged', 'jet Mass NO Merged Jets (SinglyMerged) [GeV]', 'Jets per Events / ' ],
		[ 'jetTau1_SinglyMerged_DeltaR0p4_Merged', '#tau_{1}  Merged Jets (SinglyMerged)', 'Jets per Events / ' ],
		[ 'jetTau2_SinglyMerged_DeltaR0p4_Merged', '#tau_{2}  Merged Jets (SinglyMerged)', 'Jets per Events / ' ],
		[ 'jetTau3_SinglyMerged_DeltaR0p4_Merged', '#tau_{3}  Merged Jets (SinglyMerged)', 'Jets per Events / ' ],
		[ 'jetTau21_SinglyMerged_DeltaR0p4_Merged', '#tau_{2} / #tau_{1}  Merged Jets (SinglyMerged)', 'Jets per Events / ' ],
		[ 'jetTau31_SinglyMerged_DeltaR0p4_Merged', '#tau_{3} / #tau_{1}  Merged Jets (SinglyMerged)', 'Jets per Events / ' ],
		[ 'jetTau32_SinglyMerged_DeltaR0p4_Merged', '#tau_{3} / #tau_{2}  Merged Jets (SinglyMerged)', 'Jets per Events / ' ],
		[ 'jetArea_SinglyMerged_DeltaR0p4_Merged', 'jet Area  Merged Jets (SinglyMerged)', 'Jets per Events / ' ],

		['minDeltaRPartonJet_DoublyMerged_DeltaR0p4_A',	'min #DeltaR(parton, jet) MergedA (DoublyMerged)', 'Parton per Event / '  ],
		['secMinDeltaRPartonJet_DoublyMerged_DeltaR0p4_A','2nd min #DeltaR(parton, jet) MergedA (DoublyMerged)', 'Parton per Event / '  ],
		['minDeltaRPartonJet_DoublyMerged_DeltaR0p4_B',	'min #DeltaR(parton, jet) MergedB (DoublyMerged)', 'Parton per Event / '  ],
		['secMinDeltaRPartonJet_DoublyMerged_DeltaR0p4_B','2nd min #DeltaR(parton, jet) MergedB (DoublyMerged)', 'Parton per Event / '  ],
		['jetMass_DoublyMerged_DeltaR0p4', 'Jet Mass of Merged Jets (DoublyMerged) from Stop [GeV]', 'Event / '  ],
		[ 'jetPt_DoublyMerged_DeltaR0p4', 'Merged Jets p_{T} [GeV] (DoublyMerged)', 'Jets per Events / ' ],
		[ 'jetTau1_DoublyMerged_DeltaR0p4', '#tau_{1} Merged Jets (DoublyMerged)', 'Jets per Events / ' ],
		[ 'jetTau2_DoublyMerged_DeltaR0p4', '#tau_{2} Merged Jets (DoublyMerged)', 'Jets per Events / ' ],
		[ 'jetTau3_DoublyMerged_DeltaR0p4', '#tau_{3} Merged Jets (DoublyMerged)', 'Jets per Events / ' ],
		[ 'jetTau21_DoublyMerged_DeltaR0p4', '#tau_{2} / #tau_{1} Merged Jets (DoublyMerged)', 'Jets per Events / ' ],
		[ 'jetTau31_DoublyMerged_DeltaR0p4', '#tau_{3} / #tau_{1} Merged Jets (DoublyMerged)', 'Jets per Events / ' ],
		[ 'jetTau32_DoublyMerged_DeltaR0p4', '#tau_{3} / #tau_{2} Merged Jets (DoublyMerged)', 'Jets per Events / ' ],
		[ 'jetArea_DoublyMerged_DeltaR0p4', 'jet Area Merged Jets (DoublyMerged)', 'Jets per Events / ' ],

		['minDeltaRPartonJet_TriplyMerged_DeltaR0p4',	'min #DeltaR(parton, jet) (TriplyMergeded)', 'Parton per Event / '  ],
		['secMinDeltaRPartonJet_TriplyMerged_DeltaR0p4','2nd min #DeltaR(parton, jet) (TriplyMergeded)', 'Parton per Event / '  ],
		['jetMass_TriplyMerged_DeltaR0p4_Merged', 'Invariant Mass of Match Jets (3Matched1Match) from Stop [GeV]', 'Event / '  ],
		[ 'jetPt_TriplyMerged_DeltaR0p4_Merged', 'Merged Jets p_{T} [GeV] (TriplyMerged)', 'Jets per Events / ' ],

		['minDeltaRPartonJet_FourlyMerged_DeltaR0p4','min #DeltaR(parton, jet) (FourlyMerged)', 'Parton per Event / ' ]
	]

	#if ('Matching' in sys.argv): Draw( 'stopUDD312_50', 'stop_UDD312_50_Matching_Plots', '/cms/gomez/Stops/st_jj/MCTruth/rootFiles/140314/', 'stopUDD312_50_Matching', '/cms/gomez/Stops/st_jj/MCTruth/Plots/', listMatchingHistos )

	if ('jetAlgoCmp' in process): DrawCmpMatching( 'stopUDD312_'+mass, '/cms/gomez/Stops/st_jj/treeResults/rootFiles/140327/', 'stopUDD312_'+mass+'_Matching', '/cms/gomez/Stops/st_jj/treeResults/Plots/', listMatchingHistos, jetAlgo1, jetAlgo2 )
	if ('jetGroomCmp' in process): DrawCmpMatching( 'stopUDD312_'+mass, '/cms/gomez/Stops/st_jj/treeResults/rootFiles/140418/', 'stopUDD312_'+mass+'_Matching', '/cms/gomez/Stops/st_jj/treeResults/Plots/', listMatchingHistos, jetAlgo1, groomed, cat )
	#if ('jetGroomCmp' in process): DrawCmp( 'stopUDD312_'+mass, '/cms/gomez/Stops/st_jj/treeResults/rootFiles/140402/', 'stopUDD312_'+mass+'_Matching', '', listMatchingHistos, jetAlgo1, groomed )

	listMatching2DHistos = [
			[ 'jetTau21_SinglyMerged_DeltaR0p4_NOMerged_2D', '#tau_{1} NO Merged Jets (SinglyMerged)', '#tau_{2} NO Merged Jets (SinglyMerged)'  ],
			[ 'jetTau31_SinglyMerged_DeltaR0p4_NOMerged_2D', '#tau_{1} NO Merged Jets (SinglyMerged)', '#tau_{3} NO Merged Jets (SinglyMerged)'  ],
			[ 'jetTau32_SinglyMerged_DeltaR0p4_NOMerged_2D', '#tau_{2} NO Merged Jets (SinglyMerged)', '#tau_{3} NO Merged Jets (SinglyMerged)'  ],
			[ 'jetMassVsPt_SinglyMerged_DeltaR0p4_NOMerged_2D', 'jet Mass NO Merged Jets (SinglyMerged) [GeV]', 'NO Merged Jets p_{T} (SinglyMerged) [GeV]'  ],
			[ 'jetTau21_SinglyMerged_DeltaR0p4_Merged_2D', '#tau_{1}  Merged Jets (SinglyMerged)', '#tau_{2}  Merged Jets (SinglyMerged)'  ],
			[ 'jetTau31_SinglyMerged_DeltaR0p4_Merged_2D', '#tau_{1}  Merged Jets (SinglyMerged)', '#tau_{3}  Merged Jets (SinglyMerged)'  ],
			[ 'jetTau32_SinglyMerged_DeltaR0p4_Merged_2D', '#tau_{2}  Merged Jets (SinglyMerged)', '#tau_{3}  Merged Jets (SinglyMerged)'  ],
			[ 'jetMassVsPt_SinglyMerged_DeltaR0p4_Merged_2D', 'jet Mass  Merged Jets (SinglyMerged) [GeV]', ' Merged Jets p_{T} (SinglyMerged) [GeV]'  ],
			[ 'jetTau21_DoublyMerged_DeltaR0p4_2D', '#tau_{1}  Merged Jets (DoublyMerged)', '#tau_{2}  Merged Jets (DoublyMerged)'  ],
			[ 'jetTau31_DoublyMerged_DeltaR0p4_2D', '#tau_{1}  Merged Jets (DoublyMerged)', '#tau_{3}  Merged Jets (DoublyMerged)'  ],
			[ 'jetTau32_DoublyMerged_DeltaR0p4_2D', '#tau_{2}  Merged Jets (DoublyMerged)', '#tau_{3}  Merged Jets (DoublyMerged)'  ],
			[ 'jetMassVsPt_DoublyMerged_DeltaR0p4_2D', 'jet Mass  Merged Jets (DoublyMerged) [GeV]', ' Merged Jets p_{T} (DoublyMerged) [GeV]'  ],
			]

	if ('Match2D' in process): Draw2D( 'stopUDD312_'+mass, '/cms/gomez/Stops/st_jj/treeResults/rootFiles/140418/', 'stopUDD312_'+mass+'_Matching', '/cms/gomez/Stops/st_jj/treeResults/Plots/', listMatching2DHistos, jetAlgo1, groomed )

	tmp = [
		['invMass_SinglyMerged_DeltaR0p4_Merged', 'jet Mass Merged Jets (SinglyMerged) from Stop [GeV]', 'Event / '  ],
		[ 'jetMass_SinglyMerged_DeltaR0p4_NOMerged', 'jet Mass NO Merged Jets (SinglyMerged) [GeV]', 'Jets per Events / ' ],
		['invMass_DoublyMerged_DeltaR0p4', 'jet Mass Merged Jets (DoublyMerged) from Stop [GeV]', 'Event / '  ],
		]
	if ('matchCmpAll' in process ): DrawMatchCmpAllGrom( 'stopUDD312_'+mass, '/cms/gomez/Stops/st_jj/treeResults/rootFiles/140418/', 'stopUDD312_'+mass+'', '/cms/gomez/Stops/st_jj/treeResults/Plots/', listMatchingHistos, jetAlgo1 )

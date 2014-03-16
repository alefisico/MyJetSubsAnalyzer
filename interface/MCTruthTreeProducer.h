// MCTruthTreeProducer.h  : Head of MCTruthTreeProducer.cc 
// Created by         : Alejandro Gomez Espinosa
// Contact            : gomez@physics.rutgers.edu
//
// system include files
#include <memory>
#include <vector>

// user include files
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include <TH1.h>
#include <TFile.h>
#include <TTree.h>
#include <TLorentzVector.h>
//
// class declaration
//

class MCTruthTreeProducer : public edm::EDAnalyzer {
	public:
		explicit MCTruthTreeProducer(const edm::ParameterSet&);
		virtual void beginJob() ;
		virtual void analyze(const edm::Event&, const edm::EventSetup&);
		virtual void endJob() ;
		virtual ~MCTruthTreeProducer();

		
	private:
		void initialize();

	// ----------member data ---------------------------
	edm::Service<TFileService> fs;						// Output File 
	std::string src_;
	int stopMass_;
	/*double stop1Mass_;
	double stop2Mass_;
	double st1decay_;*/

	std::map<TString, TH1*> histNames1D;

	////// Tree
	TTree* mcTruthTree_;	
	std::vector<float> *test, *stopsPt_, *stopsEta_, *stopsMass_, *stopsPhi_, *stopAPt_, *stopAEta_, *stopAEnergy_, *stopAPhi_, *stopAPartonID_, *stopBPt_, *stopBEta_, *stopBEnergy_, *stopBPhi_, *stopBPartonID_;

	///// Variables
	int numStops, numPartonsStopA, numPartonsStopB;

};

// Bool to Sort by Pt
bool ComparePt(TLorentzVector a, TLorentzVector b) { return a.Pt() > b.Pt(); }


// MCTruthAnalyzer.cc : read GenParticles from AOD and save into a tree some info
// 			(in this case an stop)
// Created by         : Alejandro Gomez Espinosa
// Contact            : gomez@physics.rutgers.edu
//

#include "../interface/MCTruthAnalyzer.h"
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/FWLite/interface/Handle.h"

#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Common/interface/Ref.h"

#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/Vector3D.h"

#include "TVector3.h"


MCTruthAnalyzer::MCTruthAnalyzer(const edm::ParameterSet& iConfig){
	src_  = iConfig.getParameter<std::string> ( "src" );   			// Obtain inputs
	/*stop1Mass_( iConfig.getParameter<double>( "stop1Mass" ) ),
	stop2Mass_( iConfig.getParameter<double>( "stop2Mass" ) ),
	st1decay_( iConfig.getParameter<double>( "st1decay" ) )*/
}

void 
MCTruthAnalyzer::beginJob() {
	//now do what ever initialization is needed

	// Initialize Histograms
	//histo = fs->make<TH1D>("jetpt" , "Jet p_{T}" , 30 ,0., 300. );		// test histo
	//histNames1D['jetpt'] = new TH1F( )
	
	/// Tree Variables
	mcTruthTree_ = fs->make<TTree>("mcTruthTree", "mcTruthTree");
	mcTruthTree_ -> Branch("numStops",		&numStops,		"numStops/I" );
	mcTruthTree_ -> Branch("numPartonsStopA",		&numPartonsStopA,		"numPartonsStopA/I" );
	mcTruthTree_ -> Branch("numPartonsStopB",		&numPartonsStopB,		"numPartonsStopB/I" );

	test		= new std::vector<float>;
	stopsPt_	= new std::vector<float>;
	stopsEta_	= new std::vector<float>;
	stopsMass_	= new std::vector<float>;
	stopsPhi_	= new std::vector<float>;
	stopAPt_	= new std::vector<float>;
	stopAEta_	= new std::vector<float>;
	stopAEnergy_	= new std::vector<float>;
	stopAPhi_	= new std::vector<float>;
	stopAPartonID_	= new std::vector<float>;
	stopBPt_	= new std::vector<float>;
	stopBEta_	= new std::vector<float>;
	stopBEnergy_	= new std::vector<float>;
	stopBPhi_	= new std::vector<float>;
	stopBPartonID_	= new std::vector<float>;
	mcTruthTree_ -> Branch("test",		"vector<float>", 	&test );
	mcTruthTree_ -> Branch("stopsPt",	"vector<float>", 	&stopsPt_ );
	mcTruthTree_ -> Branch("stopsEta",	"vector<float>", 	&stopsEta_ );
	mcTruthTree_ -> Branch("stopsMass",	"vector<float>", 	&stopsMass_ );
	mcTruthTree_ -> Branch("stopsPhi",	"vector<float>", 	&stopsPhi_ );
	mcTruthTree_ -> Branch("stopAPt",	"vector<float>", 	&stopAPt_ );
	mcTruthTree_ -> Branch("stopAEta",	"vector<float>", 	&stopAEta_ );
	mcTruthTree_ -> Branch("stopAEnergy",	"vector<float>", 	&stopAEnergy_ );
	mcTruthTree_ -> Branch("stopAPhi",	"vector<float>", 	&stopAPhi_ );
	mcTruthTree_ -> Branch("stopAPartonID",	"vector<float>", 	&stopAPartonID_ );
	mcTruthTree_ -> Branch("stopBPt",	"vector<float>", 	&stopBPt_ );
	mcTruthTree_ -> Branch("stopBEta",	"vector<float>", 	&stopBEta_ );
	mcTruthTree_ -> Branch("stopBEnergy",	"vector<float>", 	&stopBEnergy_ );
	mcTruthTree_ -> Branch("stopBPhi",	"vector<float>", 	&stopBPhi_ );
	mcTruthTree_ -> Branch("stopBPartonID",	"vector<float>", 	&stopBPartonID_ );

}

//
// member functions
//

// ------------ method called to for each event  ------------
void MCTruthAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){

	initialize();

	using namespace std;
	using namespace edm;
	using namespace reco;

	// Way to call GenParticle from root
	edm::Handle<std::vector<reco::GenParticle>> particles;
	iEvent.getByLabel( src_ , particles );
	const std::vector<reco::GenParticle> & p = *particles; 

	//cout<< iEvent.id().event() << endl;

	// Begin Loop for GenParticles
	numStops = 0;
	numPartonsStopA = 0;
	numPartonsStopB = 0;

	for(unsigned int i = 0; i < particles->size(); ++ i) {

		if( p[i].pdgId() == 1 ) test -> push_back( p[i].pt() ); 			// test
		if( p[i].status() != 3 ) continue;				// Make sure only "final" particles are present
		
		const Candidate * mom = p[i].mother();				// call mother particle

		//////////// MCTruth Stops
		if( abs( p[i].pdgId() ) == 1000002 ){
			//cout<< p[i].pdgId() << " " << p[i].mass() << endl;
			stopsPt_	->push_back( p[i].pt() );
			stopsEta_	->push_back( p[i].eta() );
			stopsMass_	->push_back( p[i].mass() );
			stopsPhi_	->push_back( p[i].phi() );
			numStops++;			
		}
		
		bool partonJet = ( ( abs ( p[i].pdgId() ) == 1 ) || ( abs( p[i].pdgId() == 2 ) ) || ( abs( p[i].pdgId() == 3 ) ) || ( abs( p[i].pdgId() == 4 ) ) || ( abs( p[i].pdgId() == 5 ) ) || ( abs( p[i].pdgId() == 21 ) ) );

		if( mom ){

			if( mom->pdgId() == 1000002 ){
				stopAPt_	->push_back( p[i].pt() );
				stopAEta_	->push_back( p[i].eta() );
				stopAEnergy_	->push_back( p[i].energy() );
				stopAPhi_	->push_back( p[i].phi() );
				stopAPartonID_	->push_back( p[i].pdgId() );
				numPartonsStopA++;			
			}

			if( mom->pdgId() == -1000002 ){
				stopBPt_	->push_back( p[i].pt() );
				stopBEta_	->push_back( p[i].eta() );
				stopBEnergy_	->push_back( p[i].energy() );
				stopBPhi_	->push_back( p[i].phi() );
				stopBPartonID_	->push_back( p[i].pdgId() );
				numPartonsStopB++;			
			}
			//std::sort(p4Stop1B.begin(), p4Stop1B.end(), ComparePt);
			//std::sort(p4Stop1jet.begin(), p4Stop1jet.end(), ComparePt);
			//std::sort(p4Stop1jetsB.begin(), p4Stop1jetsB.end(), ComparePt);
		}
	}  // end GenParticles loop 

	mcTruthTree_->Fill();


}

// ------------ method called once each job just after ending the event loop  ------------
void 
MCTruthAnalyzer::endJob() {
	delete test;
	delete stopsPt_;
	delete stopsEta_;
	delete stopsMass_;
	delete stopsPhi_;
	delete stopAPt_;
	delete stopAEta_;
	delete stopAEnergy_;
	delete stopAPhi_;
	delete stopAPartonID_;
	delete stopBPt_;
	delete stopBEta_;
	delete stopBEnergy_;
	delete stopBPhi_;
	delete stopBPartonID_;
}

void MCTruthAnalyzer::initialize() {
	numStops	= -999;
	numPartonsStopA	= -999;
	numPartonsStopB	= -999;
	test 		-> clear();
	stopsPt_ 	-> clear();
	stopsEta_ 	-> clear();
	stopsMass_ 	-> clear();
	stopsPhi_ 	-> clear();
	stopAPt_ 	-> clear();
	stopAEta_ 	-> clear();
	stopAEnergy_ 	-> clear();
	stopAPhi_ 	-> clear();
	stopAPartonID_ 	-> clear();
	stopBPt_ 	-> clear();
	stopBEta_ 	-> clear();
	stopBEnergy_ 	-> clear();
	stopBPhi_ 	-> clear();
	stopBPartonID_ 	-> clear();
}

MCTruthAnalyzer::~MCTruthAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}

//define this as a plug-in
DEFINE_FWK_MODULE(MCTruthAnalyzer);

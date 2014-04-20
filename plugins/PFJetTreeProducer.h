#ifndef PFJetTreeProducer_h
#define PFJetTreeProducer_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "HLTrigger/HLTcore/interface/TriggerExpressionData.h"
#include "HLTrigger/HLTcore/interface/TriggerExpressionEvaluator.h"
#include "HLTrigger/HLTcore/interface/TriggerExpressionParser.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "TTree.h"
#include "TH1F.h"

class PFJetTreeProducer : public edm::EDAnalyzer {

	public:
		typedef reco::Particle::LorentzVector LorentzVector;
		explicit PFJetTreeProducer(edm::ParameterSet const& cfg);
		virtual void beginJob();
		virtual void analyze(edm::Event const& iEvent, edm::EventSetup const& iSetup);
		virtual void endJob();
		virtual ~PFJetTreeProducer();

	private:  
		void initialize();
		//---- configurable parameters --------   
		double mjjMin_,ptMin_,dEtaMax_,etaMax_,stopMass_;
		edm::InputTag srcJets_,srcJetsPruned_,srcMET_,srcPU_,srcVrtx_, genSrc_;
		edm::Service<TFileService> fs_;
		TTree *outTree_; 
		//---- TRIGGER -------------------------
		triggerExpression::Data triggerCache_;
		std::vector<triggerExpression::Evaluator*> vtriggerSelector_;
		std::vector<std::string> vtriggerAlias_,vtriggerSelection_;
		TH1F *triggerPassHisto_,*triggerNamesHisto_,*puHisto_;
		//---- output TREE variables ------
		//---- global event variables -----
		int   run_,evt_,nVtx_,lumi_,nJets_;
		float rho_,met_,metSig_,ht_,mjj_,dEtajj_,dPhijj_ ;
		std::vector<bool> *triggerResult_;
		//---- jet variables --------------
		std::vector<float> *pt_,*jec_,*eta_,*phi_,*mass_,*massPruned_,*dR_,*tau1_,*tau2_,*tau3_,*energy_,*chf_,*nhf_,*phf_,*elf_,*muf_,*area_,*numJetConst_;
		//---- MC variables ---------------
		int npu_;
		int numStops, numPartonsStopA, numPartonsStopB;
		std::vector<float> *stopsPt_, *stopsEta_, *stopsMass_, *stopsPhi_, *stopAPt_, *stopAEta_, *stopAEnergy_, *stopAPhi_, *stopAPartonID_, *stopBPt_, *stopBEta_, *stopBEnergy_, *stopBPhi_, *stopBPartonID_;
};

/*typedef struct {
	TLorentzVector TL;
	double tau1;
	double tau2;
	double tau3;
	bool Btagged;
} jetInfo;*/


#endif

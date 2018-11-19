void combineData_leptonic(){

	std::string dir="/afs/cern.ch/user/j/jolangfo/public/ForNick/btag_correction/ws";
	//std::string dir="/afs/cern.ch/user/j/jolangfo/public/ForNick/binv2/ws/";
	
	TFile *f1 = TFile::Open(Form("%s/ttHLep/bkg/output_diphoton_plus_gjet_13TeV.root",dir.c_str()));
	RooWorkspace *wspace1 = (RooWorkspace*)f1->Get("tagsDumper/cms_hgg_13TeV");
	
	TFile *f2 = TFile::Open(Form("%s/ttHLep/bkg/output_ttbar_13TeV.root",dir.c_str()));
	RooWorkspace *wspace2 = (RooWorkspace*)f2->Get("tagsDumper/cms_hgg_13TeV");
	
	TFile *f3 = TFile::Open(Form("%s/ttHLep/bkg/output_tgjet_13TeV.root",dir.c_str()));
	RooWorkspace *wspace3 = (RooWorkspace*)f3->Get("tagsDumper/cms_hgg_13TeV");
	
	TFile *f4 = TFile::Open(Form("%s/ttHLep/bkg/output_ttgamma_13TeV.root",dir.c_str()));
	RooWorkspace *wspace4 = (RooWorkspace*)f4->Get("tagsDumper/cms_hgg_13TeV");
	
	TFile *f5 = TFile::Open(Form("%s/ttHLep/bkg/output_ttgammagamma_13TeV.root",dir.c_str()));
	RooWorkspace *wspace5 = (RooWorkspace*)f5->Get("tagsDumper/cms_hgg_13TeV");

	TFile * out = new TFile("backgrounds_leptonic_extended_tracker_binv2.root","RECREATE");
	out->mkdir("tagsDumper");
	out->cd("tagsDumper");
	RooWorkspace * out_ws = new RooWorkspace("cms_hgg_13TeV");

	RooRealVar *mgg = (RooRealVar*)wspace1->var("CMS_hgg_mass");
	RooRealVar *dZ = (RooRealVar*)wspace1->var("dZ");
	RooRealVar *weight = new RooRealVar("weight","weight",1.);

//	std::string boundaries[6] = {"0-50","50-100","100-150","150-250","250-400","400-inf"};
	std::string boundaries[6] = {"0","1","2","3","4","5"};
/*	std::string boundaries[11] = {
		 "0-50_BDTa"
		,"0-50_BDTb"
		,"50-100_BDTa"
		,"50-100_BDTb"
		,"100-150_BDTa"
		,"100-150_BDTb"
		,"150-250_BDTa"
		,"150-250_BDTb"
		,"250-400_BDTa"
		,"250-400_BDTb"
		,"400-inf"
		};
*/

	for (int i=0;i<6;i++){
		std::cout << " ds " << i << std::endl;
		RooDataSet *ds1 = (RooDataSet*) wspace1->data(Form("diphoton_plus_gjet_13TeV_lep_reco%s",boundaries[i].c_str())) ;
		RooDataSet *ds2 = (RooDataSet*) wspace2->data(Form("ttbar_13TeV_lep_reco%s",boundaries[i].c_str())) ;
		RooDataSet *ds3 = (RooDataSet*) wspace3->data(Form("tgjet_13TeV_lep_reco%s",boundaries[i].c_str())) ;
		RooDataSet *ds4 = (RooDataSet*) wspace4->data(Form("ttgamma_13TeV_lep_reco%s",boundaries[i].c_str())) ;
		RooDataSet *ds5 = (RooDataSet*) wspace5->data(Form("ttgammagamma_13TeV_lep_reco%s",boundaries[i].c_str())) ;

		RooDataSet *dsnew = new RooDataSet("tmp","tmpname",RooArgSet(*mgg,*dZ,*weight),"weight");

		
		for (int j=0;j<ds1->numEntries();j++){
			RooArgSet *arg = (RooArgSet*)ds1->get(j);
			weight->setVal(ds1->weight());
			arg->add(*weight);
			dsnew->add(*arg,weight->getVal());
		}
		for (int j=0;j<ds2->numEntries();j++){
			RooArgSet *arg = (RooArgSet*)ds2->get(j);
			weight->setVal(ds2->weight());
			arg->add(*weight);
			dsnew->add(*arg,weight->getVal());
		}
		for (int j=0;j<ds3->numEntries();j++){
			RooArgSet *arg = (RooArgSet*)ds3->get(j);
			weight->setVal(ds3->weight());
			arg->add(*weight);
			dsnew->add(*arg,weight->getVal());
		}
		for (int j=0;j<ds4->numEntries();j++){
			RooArgSet *arg = (RooArgSet*)ds4->get(j);
			weight->setVal(ds4->weight());
			arg->add(*weight);
			dsnew->add(*arg,weight->getVal());
		}
		for (int j=0;j<ds5->numEntries();j++){
			RooArgSet *arg = (RooArgSet*)ds5->get(j);
			weight->setVal(ds5->weight());
			arg->add(*weight);
			dsnew->add(*arg,weight->getVal());
		}

		dsnew->SetName(Form("allBackground_13TeV_lep_reco%s",boundaries[i].c_str()));
		out_ws->import(*dsnew);
	}

	RooRealVar *intL = wspace1->var("IntLumi");
	out_ws->import(*intL);
	out_ws->Write();
}

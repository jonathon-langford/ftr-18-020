void scaling_function(){

  TString proc = "VH";
  TString gen = "gen5";
  TString pTlow, pThigh;
  if( gen == "gen0" ){ pTlow = "0"; pThigh = "45";}
  else if( gen == "gen1" ){ pTlow = "45"; pThigh = "80";}
  else if( gen == "gen2" ){ pTlow = "80"; pThigh = "120";}
  else if( gen == "gen3" ){ pTlow = "120"; pThigh = "200";}
  else if( gen == "gen4" ){ pTlow = "200"; pThigh = "350";}
  else if( gen == "gen5" ){ pTlow = "350"; pThigh = "inf";}

  TFile *f = new TFile("input/datacard_combinedKLambdaScan.root" );

  TCanvas *c = new TCanvas("c","c");

  RooWorkspace *w = (RooWorkspace*)f->Get("w");
  
  RooRealVar *klambda = w->var("k_lambda");

  TString sXSscal = "XSscal_" + proc + "_" + gen;
  TString sXSBRscal = "XSBRscal_" + proc + "_" + gen + "_hgg";
  RooAbsReal *BRscal = w->function("BRscal_hgg");
  RooAbsReal *XSscal = w->function( sXSscal );
  RooAbsReal *XSBRscal = w->function( sXSBRscal );
  
  RooPlot *pl = klambda->frame();
  
  BRscal->plotOn( pl , RooFit::Name("BRscal"), RooFit::LineColor(8) );  
  XSscal->plotOn( pl , RooFit::Name("XSscal"), RooFit::LineColor(9) );  
  XSBRscal->plotOn( pl , RooFit::Name("XSBRscal"), RooFit::LineColor(kRed), RooFit::LineStyle(kDashed), RooFit::LineWidth(5) );

  pl->SetTitle("");
  pl->GetXaxis()->SetTitle("#kappa_{#lambda}");
  pl->GetXaxis()->SetLabelSize(0.03);
  pl->GetXaxis()->SetTitleSize(0.05);
  pl->GetXaxis()->SetTitleOffset(0.8);
  //TString s_yTitle = "Signal scaling: " + proc + gen; 
  pl->GetYaxis()->SetTitle( "Scaling function" );
  pl->GetYaxis()->SetLabelSize(0.03);
  pl->GetYaxis()->SetTitleSize(0.05);
  pl->GetYaxis()->SetTitleOffset(0.9);

  pl->Draw();
   
  TLegend *leg1 = new TLegend(0.600156,0.147575,0.875587,0.554852);
  leg1->SetFillColor(kWhite);
  leg1->SetLineColor(kWhite);
  if( proc == "tHq" || proc == "tHW" ){ proc = "tH"; }
  TString processID = gen + "," + proc;
  //TString processID = proc;
  leg1->AddEntry("XSBRscal","#mu_{"+processID+"}","L");
  leg1->AddEntry("XSscal","#mu^{prod}: #sigma/#sigma_{SM}","L");
  leg1->AddEntry("BRscal","#mu^{decay}: BR/BR_{SM}","L");
  leg1->Draw("Same");  

  TLatex *lat = new TLatex();
  lat->SetTextFont(42);
  lat->SetLineWidth(2);
  lat->SetTextAlign(11);
  lat->SetNDC();
  lat->SetTextSize(0.05);
  if( proc == "tHq" || proc == "tHW" ){ proc = "tH"; }
  TString plotID = proc + " " + gen + ": p_{T}^{H} #in [" + pTlow + "," + pThigh + "] GeV";
  //TString plotID = proc + " for all p_{T}^{H}";
  lat->DrawLatex(0.5,0.94,plotID);

  TString pdf_name = "output/" + proc + gen + "_scal_vs_klambda.pdf";
  //TString png_name = "/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/code/ext_tracker_recat/output/klambda/" + proc + gen + "_scal_vs_klambda.png";
  c->Print( pdf_name );
  //c->Print( png_name );
}


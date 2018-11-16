void makeKLam2D(){


  int ncontours = 99; 
  double stops[5]   = {0.0 ,  .1,   .25    , .5      , 1    };  
  double blue[5]    = {1.0 ,  1.  , 1  , 1           , 1.00   }; 
  double green[5]   = {0.25 , 0.3 ,   0.5  , 0.75    , 1.00   }; 
  double red [5]    = {0.1,  0.15 ,   0.4 , 0.6      , 1.00   }; 

  int npoints = 5; 

  TColor::CreateGradientColorTable(npoints, stops, red, green, blue, ncontours); 
  gStyle->SetNumberContours(ncontours); 

  TFile *f = TFile::Open("klambda_vs_muH.root");
  TTree *limit = (TTree*) f->Get("limit");
  limit->Draw("2*deltaNLL:mu_Higgs:k_lambda>>h4(44,-10,20,44,0,3)","deltaNLL<80", "prof colz");

  TH2F *h2D = (TH2F*) gROOT->FindObject("h4");
  h2D->SetContour(ncontours);

  TCanvas *can = new TCanvas("c","c",700,600);
  can->SetRightMargin(0.15);
  can->SetLeftMargin(0.115);
  can->SetBottomMargin(0.115);

  gStyle->SetOptStat(0);
  h2D->SetTitle("");
  h2D->Draw("colz");
  h2D->GetYaxis()->SetRangeUser(0.4,2);
  h2D->GetXaxis()->SetRangeUser(-10,18);
  
  TH2F *c1 = (TH2F*) h2D->Clone();
  TH2F *c2 = (TH2F*) h2D->Clone();
  c1->SetContour(2); c1->SetContourLevel(1,2.3);
  c2->SetContour(2); c2->SetContourLevel(1,5.99);

  c1->SetLineWidth(3);
  c2->SetLineWidth(3);
  c1->SetLineColor(kBlack);
  c2->SetLineColor(kBlack);
  c2->SetLineStyle(2);

  h2D->SetMaximum(15);
  c1->Draw("cont3same");
  c2->Draw("cont3same");

  h2D->GetXaxis()->SetTitle("#kappa_{#lambda}");
  h2D->GetYaxis()->SetTitle("#mu_{H}");
  h2D->GetXaxis()->SetTitleSize(0.055);
  h2D->GetYaxis()->SetTitleSize(0.055);
  h2D->GetZaxis()->SetTitleSize(0.035);
  h2D->GetZaxis()->SetTitle("-2 #Delta ln L");

  TGraph *gSM = new TGraph();
  gSM->SetPoint(0,1,1);
  gSM->SetMarkerStyle(34);
  gSM->SetMarkerSize(2.0);
  gSM->SetMarkerColor(kBlack);
  gSM->Draw("P");

  TLatex *lat =  new TLatex();
  lat->SetTextFont(42);
  lat->SetLineWidth(2);
  lat->SetTextAlign(11);
  lat->SetNDC();
  lat->SetTextSize(0.042);
  lat->DrawLatex(0.1,0.92,"#bf{CMS Phase-2} #it{Simulation Preliminary}");
  lat->DrawLatex(0.69,0.92,"3 ab^{-1} (14#scale[0.75]{ }TeV)");

  TLegend *leg = new TLegend(0.55,0.66,0.8,0.86);
  leg->SetBorderSize(0);
  leg->SetFillColor(0);

  leg->AddEntry(gSM,  "SM"     , "P" );
  leg->AddEntry(c1,   "68% CL" , "L" );
  leg->AddEntry(c2,   "95% CL" , "L" );
  leg->Draw();

  can->SetTicky();
  can->SetTickx();
  can->RedrawAxis();
  can->Update(); 

  can->SaveAs("2D_kappa_mu_scan.pdf");
  //can->SaveAs("2D_kappa_mu_scan.png");
}

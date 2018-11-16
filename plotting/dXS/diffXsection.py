import ROOT
import numpy as np
import math
import sys
from array import array

#print ROOT.gROOT.GetVersion()
#sys.exit(1)

ROOT.gStyle.SetOptStat(0)

#For showing how different values of klambda change diff cross-sections
def XSscal( _C1, klambda ):
  dZH = -1.536e-3
  XSscalefactor = (1+klambda*_C1+dZH)/((1-(klambda*klambda-1)*dZH)*(1+_C1+dZH))
  return XSscalefactor

def BRscal( klambda ):
  dZH = -1.536e-3
  C1_hgg = 0.0049
  C1_tot = 2.5e-3
  BRscalefactor = 1+(((klambda-1)*(C1_hgg-C1_tot))/(1+(klambda-1)*C1_tot))
  return BRscalefactor

def XSBRscal( _C1, klambda ):
  return XSscal( _C1, klambda)*BRscal( klambda ) 

#Extract C1 values from files
f_C1_ttH = open("/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/btag_correction/C1/ttH_C1.txt","r")
f_C1_tH = open("/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/btag_correction/C1/tHj_C1.txt","r")
C1 = {}
gen_idx = 0
for genbin in f_C1_ttH:
  genbinName = "ttH_gen%g"%gen_idx
  C1[ genbinName ] = float(genbin[ genbin.find(":")+1:-2])
  gen_idx += 1

gen_idx = 0
for genbin in f_C1_tH: 
  genbinName_tHq = "tHq_gen%g"%gen_idx
  genbinName_tHW = "tHW_gen%g"%gen_idx
  C1[ genbinName_tHq ] = float(genbin[ genbin.find(":")+1:-2])
  C1[ genbinName_tHW ] = float(genbin[ genbin.find(":")+1:-2])
  gen_idx += 1

#Define luminosity
intLumi = 3000

#Hadronic
f_had = ROOT.TFile("input/datacard_ttHHad_preappPerProcessMu.root")
#Extract workspace
ws = f_had.Get("w")
ws.var("MH").setVal(125.09)
#Sum normalisation for process across norm bins
nexp_gen_had = [0,0,0,0,0,0]
#sum for different klambda
nexp_k10_had = [0,0,0,0,0,0]
nexp_k10_lep = [0,0,0,0,0,0]
nexp_km5_had = [0,0,0,0,0,0]
nexp_km5_lep = [0,0,0,0,0,0]

for gen_idx in range(0,6):
  for proc in ['ttH','tHq','tHW']:
    for reco_idx in range(0,6):
      if( reco_idx != 5 ):
        for BDT_idx in ["a","b"]:
          norm = "n_exp_bindatacard_ttHHad_reco%g_BDT%s_proc_%s_gen%g_hgg"%(reco_idx,BDT_idx,proc,gen_idx)
          nexp = ws.function( norm ).getVal()
          nexp_gen_had[gen_idx] += nexp
          #extract value with klambda = 10
          #mu = XSBRscal( C1[ "%s_gen%g"%(proc,gen_idx)], 10 )
          #nexp_k10 = nexp*mu
          #print "(gen%g,%s,reco%g,BDT%s): Nexp = %5.4f, C1 = %5.4f --> k_lambda = 10: mu = %5.4f, Nexp = %5.4f"%(gen_idx,proc,reco_idx,BDT_idx,nexp,C1[ "%s_gen%g"%(proc,gen_idx)],mu,nexp_k10)
          nexp_k10_had[gen_idx] += nexp*XSBRscal( C1[ "%s_gen%g"%(proc,gen_idx)], 10 )
          nexp_km5_had[gen_idx] += nexp*XSBRscal( C1[ "%s_gen%g"%(proc,gen_idx)], -5 )
      else: 
        norm = "n_exp_bindatacard_ttHHad_reco%g_proc_%s_gen%g_hgg"%(reco_idx,proc,gen_idx)
        nexp = ws.function( norm ).getVal()
        nexp_gen_had[gen_idx] += nexp
        nexp_k10_had[gen_idx] += nexp*XSBRscal( C1[ "%s_gen%g"%(proc,gen_idx)], 10 )
        nexp_km5_had[gen_idx] += nexp*XSBRscal( C1[ "%s_gen%g"%(proc,gen_idx)], -5 )
#close file
f_had.Close()

#Leptonic
f_lep = ROOT.TFile("input/datacard_ttHLep_preappPerProcessMu.root")
#Extract workspace
ws = f_lep.Get("w")
ws.var("MH").setVal(125.09)
#Sum normalisation for process across norm bins
nexp_gen_lep = [0,0,0,0,0,0]
for gen_idx in range(0,6):
  for proc in ['ttH','tHq','tHW']:
    for reco_idx in range(0,6):
      if( reco_idx != 5 ):
        norm = "n_exp_bindatacard_ttHLep_lep_reco%g_proc_%s_gen%g_hgg"%(reco_idx,proc,gen_idx)
        nexp = ws.function( norm ).getVal()
        nexp_gen_lep[gen_idx] += nexp
        nexp_k10_lep[gen_idx] += nexp*XSBRscal( C1[ "%s_gen%g"%(proc,gen_idx)], 10 )
        nexp_km5_lep[gen_idx] += nexp*XSBRscal( C1[ "%s_gen%g"%(proc,gen_idx)], -5 )
      else: 
        norm = "n_exp_bindatacard_ttHLep_lep_reco%g_proc_%s_gen%g_hgg"%(reco_idx,proc,gen_idx)
        nexp = ws.function( norm ).getVal()
        nexp_gen_lep[gen_idx] += nexp
        nexp_k10_lep[gen_idx] += nexp*XSBRscal( C1[ "%s_gen%g"%(proc,gen_idx)], 10 )
        nexp_km5_lep[gen_idx] += nexp*XSBRscal( C1[ "%s_gen%g"%(proc,gen_idx)], -5 )
#close file
f_lep.Close()

#Read in r_values with uncertainties
#combined
f_rcomb = open("input/rcomb.txt")
rcomb = []
rcomb_sigma_up = []
rcomb_sigma_down = []
for genbin in f_rcomb:
  val = genbin.split(" ")
  rcomb.append(1.0)
  rcomb_sigma_up.append(float( val[2] ))
  rcomb_sigma_down.append(float( val[3][:-1] ))
#hadronic
f_rhad = open("input/rhad.txt")
rhad = []
rhad_sigma_up = []
rhad_sigma_down = []
for genbin in f_rhad:
  val = genbin.split(" ")
  rhad.append(1.0)
  rhad_sigma_up.append(float( val[2] ))
  rhad_sigma_down.append(float( val[3][:-1] ))
#combined
f_rlep = open("input/rlep.txt")
rlep = []
rlep_sigma_up = []
rlep_sigma_down = []
for genbin in f_rlep:
  val = genbin.split(" ")
  rlep.append(1.0)
  rlep_sigma_up.append(float( val[2] ))
  rlep_sigma_down.append(float( val[3][:-1] ))

#Read in acceptance values
#hadronic
f_ahad = open("input/acceptance_ttHHad_new.txt")
acc_had = []
for genbin in f_ahad:
  acc_had.append( float( genbin.split(" ")[1][:-1] ) )
#leptonic
f_alep = open("input/acceptance_ttHLep_new.txt")
acc_lep = []
for genbin in f_alep:
  acc_lep.append( float( genbin.split(" ")[1][:-1] ) )

#Total number in fiducial region
#Combined
Nfid_comb = (np.array( rcomb )/2.)*((np.array(nexp_gen_had)/np.array(acc_had))+(np.array(nexp_gen_lep)/np.array(acc_lep)))
Nfid_comb_sigma_up = (np.array( rcomb_sigma_up )/2.)*((np.array(nexp_gen_had)/np.array(acc_had))+(np.array(nexp_gen_lep)/np.array(acc_lep)))
Nfid_comb_sigma_down = (np.array( rcomb_sigma_down )/2.)*((np.array(nexp_gen_had)/np.array(acc_had))+(np.array(nexp_gen_lep)/np.array(acc_lep)))
#Hadronic
Nfid_had = (np.array( nexp_gen_had )*np.array( rhad ))/np.array( acc_had )
Nfid_had_sigma_up = (np.array( nexp_gen_had )*np.array( rhad_sigma_up ))/np.array( acc_had )
Nfid_had_sigma_down = (np.array( nexp_gen_had )*np.array( rhad_sigma_down ))/np.array( acc_had )
#Leptonic
Nfid_lep = (np.array( nexp_gen_lep )*np.array( rlep ))/np.array( acc_lep )
Nfid_lep_sigma_up = (np.array( nexp_gen_lep )*np.array( rlep_sigma_up ))/np.array( acc_lep )
Nfid_lep_sigma_down = (np.array( nexp_gen_lep )*np.array( rlep_sigma_down ))/np.array( acc_lep )

#Total number for different values of klambda
Nfid_comb_k10 = (np.array( rcomb )/2.)*((np.array(nexp_k10_had)/np.array(acc_had))+(np.array(nexp_k10_lep)/np.array(acc_lep))) 
Nfid_comb_km5 = (np.array( rcomb )/2.)*((np.array(nexp_km5_had)/np.array(acc_had))+(np.array(nexp_km5_lep)/np.array(acc_lep))) 

#Also total ttH+tH fiducial number across all bins
Nfid_tot = Nfid_comb.sum()
Nfid_tot_sigma_up = math.sqrt( (Nfid_comb_sigma_up**2).sum() )
Nfid_tot_sigma_down = math.sqrt( (Nfid_comb_sigma_down**2).sum() )

#Define bin widths
pTH_binWidths = np.array([45.,35.,40.,80.,150.,150.])

#Convert to diff cross-section: divide by luminosity * bin width
XS_ttHptH_comb = Nfid_comb/(intLumi*pTH_binWidths)
XS_ttHptH_comb_sigma_up = Nfid_comb_sigma_up/(intLumi*pTH_binWidths)
XS_ttHptH_comb_sigma_down = Nfid_comb_sigma_down/(intLumi*pTH_binWidths)
XS_ttHptH_had = Nfid_had/(intLumi*pTH_binWidths)
XS_ttHptH_had_sigma_up = Nfid_had_sigma_up/(intLumi*pTH_binWidths)
XS_ttHptH_had_sigma_down = Nfid_had_sigma_down/(intLumi*pTH_binWidths)
XS_ttHptH_lep = Nfid_lep/(intLumi*pTH_binWidths)
XS_ttHptH_lep_sigma_up = Nfid_lep_sigma_up/(intLumi*pTH_binWidths)
XS_ttHptH_lep_sigma_down = Nfid_lep_sigma_down/(intLumi*pTH_binWidths)
XS_tot_ttHptH = Nfid_tot/intLumi
XS_tot_ttHptH_sigma_up = Nfid_tot_sigma_up/intLumi
XS_tot_ttHptH_sigma_down = Nfid_tot_sigma_down/intLumi

#XS for different kappa_lambda
XS_ttHptH_comb_k10 = Nfid_comb_k10/(intLumi*pTH_binWidths)
XS_ttHptH_comb_km5 = Nfid_comb_km5/(intLumi*pTH_binWidths)

#Theory uncertainties
XS_ttHptH_th_up = XS_ttHptH_comb*np.array([0.117331396659,0.0960935487586,0.0618824597217,0.0718885019794,0.0671531097929,0.0954138592947])
XS_ttHptH_th_down = XS_ttHptH_comb*np.array([0.117331396659,0.0960935487586,0.0618824597217,0.0718885019794,0.0671531097929,0.0954138592947])

#Define histogram to get bin centers and X-errors
canv = ROOT.TCanvas("c","c")
canv.SetLogy()

bin_pTH = [0,45,80,120,200,350,500]
Xbincenter = []
Xbincenter_lep = []
Xbincenter_had = []
Xerror = []
h_XS = ROOT.TH1F("h_XS","",6,array('f',bin_pTH))
for gen_idx in range( len( XS_ttHptH_comb ) ):
  Xbincenter.append( h_XS.GetXaxis().GetBinCenter( gen_idx+1 ) )
  Xbincenter_lep.append( h_XS.GetXaxis().GetBinCenter( gen_idx+1 )-5 )
  Xbincenter_had.append( h_XS.GetXaxis().GetBinCenter( gen_idx+1 )+5 )
  Xerror.append(abs( Xbincenter[gen_idx]-bin_pTH[gen_idx] ))

#Graph for Theory uncertainty
gr_th_unc = ROOT.TGraphAsymmErrors(6, array('f',Xbincenter), array('f', XS_ttHptH_comb.tolist() ), array('f', (np.array(Xerror)/2).tolist() ), array('f', (np.array(Xerror)/2).tolist()), array('f', XS_ttHptH_th_up.tolist() ), array('f', XS_ttHptH_th_down.tolist() ) ) 
gr_th_unc.SetMarkerSize(0)
gr_th_unc.SetLineWidth(0)
gr_th_unc.SetFillColor(5)
#gr_th_unc.SetFillStyle(3008)
#Configure graph
gr_th_unc.SetTitle("")
gr_th_unc.GetYaxis().SetTitle("d#sigma_{fid}^{ttH+tH} x BR(H#rightarrow#gamma#gamma) / dp_{T}^{H}   (fb/GeV)")
gr_th_unc.GetYaxis().SetRangeUser(10e-5,.02)
gr_th_unc.GetYaxis().SetLabelSize(0.03)
gr_th_unc.GetYaxis().SetTitleSize(0.04)
gr_th_unc.GetYaxis().SetTitleOffset(1.0)
gr_th_unc.GetXaxis().SetTitle("p_{T}^{H}   (GeV)")
gr_th_unc.GetXaxis().SetLimits(0.,500.)
gr_th_unc.GetXaxis().SetLabelSize(0.03)
gr_th_unc.GetXaxis().SetTitleSize(0.04)
gr_th_unc.GetXaxis().SetTitleOffset(0.95)
#Modified x-axis
gr_th_unc.GetXaxis().SetLabelSize(0)
gr_th_unc.GetXaxis().SetNdivisions(0)
gr_th_unc.Draw("A E2")

#Leptonic graph
#gr_lep = ROOT.TGraphAsymmErrors(6, array('f',Xbincenter), array('f', XS_ttHptH_lep.tolist() ), array('f', Xerror), array('f', Xerror), array('f', XS_ttHptH_lep_sigma_down.tolist() ), array('f', XS_ttHptH_lep_sigma_up.tolist() ) ) 
gr_lep = ROOT.TGraphAsymmErrors(6, array('f',Xbincenter_lep), array('f', XS_ttHptH_lep.tolist() ), array('f', [0.,0.,0.,0.,0.,0.] ), array('f', [0.,0.,0.,0.,0.,0.]), array('f', XS_ttHptH_lep_sigma_down.tolist() ), array('f', XS_ttHptH_lep_sigma_up.tolist() ) ) 
gr_lep.SetMarkerSize(0)
gr_lep.SetMarkerColor(9)
gr_lep.SetLineColor(9)
gr_lep.SetLineWidth(2)
#gr_lep.GetYaxis().SetRangeUser(10e-5,.02)
#gr_lep.GetXaxis().SetRangeUser(0,500)
gr_lep.Draw("P Same")


#Hadronic graph
#gr_had = ROOT.TGraphAsymmErrors(6, array('f',Xbincenter), array('f', XS_ttHptH_had.tolist() ), array('f', Xerror), array('f', Xerror), array('f', XS_ttHptH_had_sigma_down.tolist() ), array('f', XS_ttHptH_had_sigma_up.tolist() ) ) 
gr_had = ROOT.TGraphAsymmErrors(6, array('f',Xbincenter_had), array('f', XS_ttHptH_had.tolist() ), array('f', [0.,0.,0.,0.,0.,0.] ), array('f', [0.,0.,0.,0.,0.,0.]), array('f', XS_ttHptH_had_sigma_down.tolist() ), array('f', XS_ttHptH_had_sigma_up.tolist() ) ) 
gr_had.SetMarkerSize(0)
gr_had.SetMarkerColor(2)
gr_had.SetLineColor(2)
gr_had.SetLineWidth(2)
#gr_had.GetYaxis().SetRangeUser(10e-5,.02)
#gr_had.GetXaxis().SetRangeUser(0,500)
gr_had.Draw("P Same")

#Graph for klambda = 10
gr_comb_k10 = ROOT.TGraphAsymmErrors(6, array('f',Xbincenter), array('f', XS_ttHptH_comb_k10.tolist() ), array('f', Xerror), array('f', Xerror), array('f', [0.,0.,0.,0.,0.,0.] ), array('f', [0.,0.,0.,0.,0.,0.] ) ) 
gr_comb_k10.SetMarkerSize(0)
gr_comb_k10.SetMarkerColor(16)
gr_comb_k10.SetLineColor(16)
gr_comb_k10.SetLineWidth(2)
gr_comb_k10.SetLineStyle(2)
#gr_comb_k10.GetYaxis().SetRangeUser(10e-5,.02)
#gr_comb_k10.GetXaxis().SetRangeUser(0,500)
gr_comb_k10.Draw("P Same")

#Graph for klambda = -5
gr_comb_km5 = ROOT.TGraphAsymmErrors(6, array('f',Xbincenter), array('f', XS_ttHptH_comb_km5.tolist() ), array('f', Xerror), array('f', Xerror), array('f', [0.,0.,0.,0.,0.,0.] ), array('f', [0.,0.,0.,0.,0.,0.] ) ) 
gr_comb_km5.SetMarkerSize(0)
gr_comb_km5.SetMarkerColor(36)
gr_comb_km5.SetLineColor(36)
gr_comb_km5.SetLineWidth(2)
gr_comb_km5.SetLineStyle(2)
#gr_comb_km5.GetYaxis().SetRangeUser(10e-5,.02)
#gr_comb_km5.GetXaxis().SetRangeUser(0,500)
gr_comb_km5.Draw("P Same")

#Combined graph
gr_comb = ROOT.TGraphAsymmErrors(6, array('f',Xbincenter), array('f', XS_ttHptH_comb.tolist() ), array('f', Xerror), array('f', Xerror), array('f', XS_ttHptH_comb_sigma_down.tolist() ), array('f', XS_ttHptH_comb_sigma_up.tolist() ) ) 
gr_comb.SetMarkerStyle(21)
gr_comb.SetMarkerSize(.75)
gr_comb.SetMarkerColor(1)
gr_comb.SetLineColor(1)
gr_comb.SetLineWidth(2)
#gr_comb.GetYaxis().SetRangeUser(10e-5,.02)
#gr_comb.GetXaxis().SetRangeUser(0,500)
gr_comb.Draw("P Same")

#Dashed line for bin
line1 = ROOT.TLine(350,10e-5,350,20e-4)
line1.SetLineWidth(2)
line1.SetLineStyle(2)
line1.Draw("Same")

#Custom ticks from tlines
lines = []
for x in [0,45,80,120,200,350]:
  line = ROOT.TLine(x,10e-5,x,11e-5)
  lines.append(line)
for line in lines:
  line.Draw("same")
#custom axis labels
lat2 = ROOT.TLatex()
lat2.SetTextFont(42)
lat2.SetLineWidth(2)
lat2.SetTextAlign(11)
lat2.SetTextSize(0.03)
lat2.DrawLatex(-3,8e-5,"0")
lat2.DrawLatex(39,8e-5,"45")
lat2.DrawLatex(74,8e-5,"80")
lat2.DrawLatex(110,8e-5,"120")
lat2.DrawLatex(190,8e-5,"200")
lat2.DrawLatex(340,8e-5,"350")
#lat2.DrawLatex(495,8.2e-5,"#scale[1.3]{#infty}")

#Legend
leg1 = ROOT.TLegend(0.45,0.6,0.89,0.867089);
leg1.SetFillColor(0);
leg1.SetLineColor(0);
leg1.AddEntry(gr_comb,"Stat + exp. syst. + ggH+VH theo. uncert.","PEL");
leg1.AddEntry(gr_had,"Hadronic categories only","PE");
leg1.AddEntry(gr_lep,"Leptonic categories only","PE");
leg1.AddEntry(gr_comb_k10,"Expectation #kappa_{#lambda} = 10","L");
leg1.AddEntry(gr_comb_km5,"Expectation #kappa_{#lambda} = -5","L");
leg1.AddEntry(gr_th_unc,"ttH+tH theo. uncert.","F");
leg1.Draw("Same");

#Text
t = ROOT.TPaveText(0.675616,0.35865,0.882436,0.413502,"brNDC");
t.SetTextFont(42);
t.SetTextAlign(11);
t.AddText( "(p_{T}^{H} > 350 GeV)/150 GeV" );
t.SetShadowColor(0);
t.SetLineColor(0);
t.SetLineStyle(0);
t.SetFillColor(0);
t.SetFillStyle(0);
t.Draw("Same");
lat = ROOT.TLatex()
lat.SetTextFont(42)
lat.SetLineWidth(2)
lat.SetTextAlign(11)
lat.SetNDC()
lat.SetTextSize(0.042)
lat.DrawLatex(0.1,0.92,"#bf{CMS Phase-2} #it{Simulation Preliminary}")
lat.DrawLatex(0.72,0.92,"3 ab^{-1} (14#scale[0.75]{ }TeV)")

lat2 = ROOT.TLatex()
lat2.SetTextFont(42)
lat2.SetLineWidth(2)
lat2.SetTextAlign(11)
lat2.SetNDC()
lat2.SetTextSize(0.03)
#lat2.DrawLatex(0.13,0.30,"#bf{Fiducial phase space definition}")
#lat2.DrawLatex(0.13,0.25,"#bullet |Y^{H}| < 2.5")
#lat2.DrawLatex(0.13,0.20,"#bullet H#rightarrow#gamma#gamma: p_{T}^{#gamma} > 20 GeV, |#eta^{#gamma}| < 2.5")
#lat2.DrawLatex(0.13,0.15,"#bullet >=2 jets: p_{T}^{j} > 25 GeV, |#eta^{j}| < 4, at least one b jet")
lat2.DrawLatex(0.13,0.25,"|Y^{H}| < 2.5")
lat2.DrawLatex(0.13,0.20,"H#rightarrow#gamma#gamma: p_{T}^{#gamma} > 20 GeV, |#eta^{#gamma}| < 2.5")
lat2.DrawLatex(0.13,0.15,">=2 jets: p_{T}^{j} > 25 GeV, |#eta^{j}| < 4, at least one b jet")




canv.Update()
canv.Print("output/dXS_dpTH.pdf")
#canv.Print("/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/combined/code/output/dXS_dpTH_combined.png")
#Print results to user
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "XS*BR for ttH+tH (H->gg) @14TeV                         "
print ""
gen_text = ['[  0, 45]','[ 45, 80]','[ 80,120]','[120,200]','[200,350]','[350,inf]']
for i in range( 0,6 ):
  print "  > pT(H) = %s GeV: %5.3f + %5.3f - %5.3f [fb]"%(gen_text[i],XS_ttHptH_comb[i],XS_ttHptH_comb_sigma_up[i],XS_ttHptH_comb_sigma_down[i])
print ""
print "    > Total: %5.3f + %5.3f - %5.3f [fb]"%(XS_tot_ttHptH,XS_tot_ttHptH_sigma_up,XS_tot_ttHptH_sigma_down)
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

raw_input("Press Enter to continue...")

import sys
import ROOT
import math
from array import array

intLumi = 3000

#BDT cuts
lep_BDT_cut = 0.13

#Background chains
chain_ttgg = ROOT.TChain("trilinearTree")
chain_ttgg.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/background/output_ttHLep_ttgammagamma_1fb.root")

chain_ttg = ROOT.TChain("trilinearTree")
chain_ttg.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/background/output_ttHLep_ttgamma_1fb.root")

chain_gg = ROOT.TChain("trilinearTree")
chain_gg.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/background/output_ttHLep_DiPhotonJetsBox_MGG-80toInf_1fb.root")

chain_gjet = ROOT.TChain("trilinearTree")
chain_gjet.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/background/output_ttHLep_GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_1fb.root")

chain_tt = ROOT.TChain("trilinearTree")
chain_tt.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/background/output_ttHLep_ttbar_1fb.root")

chain_tgjet = ROOT.TChain("trilinearTree")
chain_tgjet.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/background/output_ttHLep_TGJet_inclusive_1fb.root")

#Signal chains
chain_ttH = ROOT.TChain("trilinearTree")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen0_M125_1fb.root")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen1_M125_1fb.root")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen2_M125_1fb.root")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen3_M125_1fb.root")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen4_M125_1fb.root")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen5_M125_1fb.root")

chain_ggH = ROOT.TChain("trilinearTree")
chain_ggH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ggHgen0_M125_1fb.root")
chain_ggH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ggHgen1_M125_1fb.root")
chain_ggH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ggHgen2_M125_1fb.root")
chain_ggH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ggHgen3_M125_1fb.root")
chain_ggH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ggHgen4_M125_1fb.root")
chain_ggH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ggHgen5_M125_1fb.root")

chain_VH = ROOT.TChain("trilinearTree")
chain_VH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_VHgen0_M125_1fb.root")
chain_VH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_VHgen1_M125_1fb.root")
chain_VH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_VHgen2_M125_1fb.root")
chain_VH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_VHgen3_M125_1fb.root")
chain_VH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_VHgen4_M125_1fb.root")
chain_VH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_VHgen5_M125_1fb.root")

chain_tH = ROOT.TChain("trilinearTree")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen0_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen1_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen2_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen3_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen4_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen5_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen0_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen1_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen2_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen3_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen4_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen5_M125_1fb.root")

chain_THQ = ROOT.TChain("trilinearTree")
chain_THQ.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen0_M125_1fb.root")
chain_THQ.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen1_M125_1fb.root")
chain_THQ.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen2_M125_1fb.root")
chain_THQ.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen3_M125_1fb.root")
chain_THQ.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen4_M125_1fb.root")
chain_THQ.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen5_M125_1fb.root")

chain_THW = ROOT.TChain("trilinearTree")
chain_THW.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen0_M125_1fb.root")
chain_THW.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen1_M125_1fb.root")
chain_THW.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen2_M125_1fb.root")
chain_THW.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen3_M125_1fb.root")
chain_THW.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen4_M125_1fb.root")
chain_THW.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen5_M125_1fb.root")

#Define counters to output number of events remaining
N_gg_pre = 0
N_gjet_pre = 0
N_ttg_pre = 0
N_ttgg_pre = 0
N_tt_pre = 0
N_tgjet_pre = 0
N_bkg_pre = 0

N_ttH_pre = 0
N_ggH_pre = 0
N_VH_pre = 0
N_tH_pre = 0
N_THQ_pre = 0
N_THW_pre = 0

N_gg_BDTa = 0
N_gjet_BDTa = 0
N_ttg_BDTa = 0
N_ttgg_BDTa = 0
N_tt_BDTa = 0
N_tgjet_BDTa = 0
N_bkg_BDTa = 0

N_ttH_BDTa = 0
N_ggH_BDTa = 0
N_VH_BDTa = 0
N_tH_BDTa = 0

#Counters for inside mass mindow
N_bkg_massWindow_BDTa = 0
N_ttHptH_massWindow_BDTa = 0

massLow = 120
massHigh = 130

#Counters for signal splitting
N_ttH_gen0 = 0
N_ttH_gen1 = 0
N_ttH_gen2 = 0
N_ttH_gen3 = 0
N_ttH_gen4 = 0
N_ttH_gen5 = 0

N_ggH_gen0 = 0
N_ggH_gen1 = 0
N_ggH_gen2 = 0
N_ggH_gen3 = 0
N_ggH_gen4 = 0
N_ggH_gen5 = 0

N_VH_gen0 = 0
N_VH_gen1 = 0
N_VH_gen2 = 0
N_VH_gen3 = 0
N_VH_gen4 = 0
N_VH_gen5 = 0

N_THQ_gen0 = 0
N_THQ_gen1 = 0
N_THQ_gen2 = 0
N_THQ_gen3 = 0
N_THQ_gen4 = 0
N_THQ_gen5 = 0

N_THW_gen0 = 0
N_THW_gen1 = 0
N_THW_gen2 = 0
N_THW_gen3 = 0
N_THW_gen4 = 0
N_THW_gen5 = 0

for ev in chain_gg:
  
  N_gg_pre += ev.weight_LO*intLumi
  N_bkg_pre += ev.weight_LO*intLumi
  #if( ev.BDT > 0.45 )&( ev.BDT < 0.75 ): 
  #  N_gg_BDTb += ev.weight_LO*intLumi
  #  N_bkg_BDTb += ev.weight_LO*intLumi
  #  if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTb += ev.weight_LO*intLumi
  #elif( ev.BDT >= 0.75 ):
  if( ev.BDT >= lep_BDT_cut ):
    N_gg_BDTa += ev.weight_LO*intLumi
    N_bkg_BDTa += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTa += ev.weight_LO*intLumi

for ev in chain_gjet:
  
  N_gjet_pre += ev.weight_LO*intLumi
  N_bkg_pre += ev.weight_LO*intLumi
  if( ev.BDT >= lep_BDT_cut ):
    N_gjet_BDTa += ev.weight_LO*intLumi
    N_bkg_BDTa += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTa += ev.weight_LO*intLumi


for ev in chain_ttg:
  
  N_ttg_pre += ev.weight_LO*intLumi
  N_bkg_pre += ev.weight_LO*intLumi
  if( ev.BDT >= lep_BDT_cut ):
    N_ttg_BDTa += ev.weight_LO*intLumi
    N_bkg_BDTa += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTa += ev.weight_LO*intLumi

for ev in chain_ttgg:
  
  N_ttgg_pre += ev.weight_LO*intLumi
  N_bkg_pre += ev.weight_LO*intLumi
  if( ev.BDT >= lep_BDT_cut ):
    N_ttgg_BDTa += ev.weight_LO*intLumi
    N_bkg_BDTa += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTa += ev.weight_LO*intLumi


for ev in chain_tt:
  
  N_tt_pre += ev.weight_LO*intLumi
  N_bkg_pre += ev.weight_LO*intLumi
  if( ev.BDT >= lep_BDT_cut ):
    N_tt_BDTa += ev.weight_LO*intLumi
    N_bkg_BDTa += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTa += ev.weight_LO*intLumi


for ev in chain_tgjet:
  
  N_tgjet_pre += ev.weight_LO*intLumi
  N_bkg_pre += ev.weight_LO*intLumi
  if( ev.BDT >= lep_BDT_cut ):
    N_tgjet_BDTa += ev.weight_LO*intLumi
    N_bkg_BDTa += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTa += ev.weight_LO*intLumi

for ev in chain_ttH:
  
  N_ttH_pre += ev.weight_LO*intLumi
  if( ev.BDT >= lep_BDT_cut ):
    N_ttH_BDTa += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_ttHptH_massWindow_BDTa += ev.weight_LO*intLumi

  if( ev.pTH_gen >= 0. )&( ev.pTH_gen < 45. ): N_ttH_gen0 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 45. )&( ev.pTH_gen < 80. ): N_ttH_gen1 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 80. )&( ev.pTH_gen < 120. ): N_ttH_gen2 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 120. )&( ev.pTH_gen < 200. ): N_ttH_gen3 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 200. )&( ev.pTH_gen < 350. ): N_ttH_gen4 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 350 ): N_ttH_gen5 += ev.weight_LO*intLumi

for ev in chain_ggH:
  
  N_ggH_pre += ev.weight_LO*intLumi
  if( ev.BDT >= lep_BDT_cut ):
    N_ggH_BDTa += ev.weight_LO*intLumi

  if( ev.pTH_gen >= 0. )&( ev.pTH_gen < 45. ): N_ggH_gen0 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 45. )&( ev.pTH_gen < 80. ): N_ggH_gen1 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 80. )&( ev.pTH_gen < 120. ): N_ggH_gen2 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 120. )&( ev.pTH_gen < 200. ): N_ggH_gen3 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 200. )&( ev.pTH_gen < 350. ): N_ggH_gen4 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 350 ): N_ggH_gen5 += ev.weight_LO*intLumi

for ev in chain_VH:
  
  N_VH_pre += ev.weight_LO*intLumi
  if( ev.BDT >= lep_BDT_cut ):
    N_VH_BDTa += ev.weight_LO*intLumi

  if( ev.pTH_gen >= 0. )&( ev.pTH_gen < 45. ): N_VH_gen0 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 45. )&( ev.pTH_gen < 80. ): N_VH_gen1 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 80. )&( ev.pTH_gen < 120. ): N_VH_gen2 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 120. )&( ev.pTH_gen < 200. ): N_VH_gen3 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 200. )&( ev.pTH_gen < 350. ): N_VH_gen4 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 350 ): N_VH_gen5 += ev.weight_LO*intLumi



for ev in chain_tH:

  N_tH_pre += ev.weight_LO*intLumi
  if( ev.BDT >= lep_BDT_cut ):
    N_tH_BDTa += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_ttHptH_massWindow_BDTa += ev.weight_LO*intLumi

for ev in chain_THQ:

  N_THQ_pre += ev.weight_LO*intLumi
  if( ev.pTH_gen >= 0. )&( ev.pTH_gen < 45. ): N_THQ_gen0 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 45. )&( ev.pTH_gen < 80. ): N_THQ_gen1 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 80. )&( ev.pTH_gen < 120. ): N_THQ_gen2 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 120. )&( ev.pTH_gen < 200. ): N_THQ_gen3 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 200. )&( ev.pTH_gen < 350. ): N_THQ_gen4 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 350 ): N_THQ_gen5 += ev.weight_LO*intLumi

for ev in chain_THW:

  N_THW_pre += ev.weight_LO*intLumi
  if( ev.pTH_gen >= 0. )&( ev.pTH_gen < 45. ): N_THW_gen0 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 45. )&( ev.pTH_gen < 80. ): N_THW_gen1 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 80. )&( ev.pTH_gen < 120. ): N_THW_gen2 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 120. )&( ev.pTH_gen < 200. ): N_THW_gen3 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 200. )&( ev.pTH_gen < 350. ): N_THW_gen4 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 350 ): N_THW_gen5 += ev.weight_LO*intLumi

print "ttHLep: Analysis cut flow:"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "~       Process      ~         Total           ~      Pre-selection      ~        BDT>%5.2f       ~"%lep_BDT_cut
print "~                    ~                         ~                         ~                       ~"
print "~        ttH         ~         1.393           ~          %5.4f          ~         %5.4f         ~"%(N_ttH_pre,N_ttH_BDTa)
print "~        ggH         ~         124.1           ~          %5.4f          ~         %5.4f         ~"%(N_ggH_pre,N_ggH_BDTa)
print "~        VH          ~         5.XXX           ~          %5.4f          ~         %5.4f         ~"%(N_VH_pre,N_VH_BDTa)
print "~        tH          ~         0.245           ~          %5.4f          ~         %5.4f         ~"%(N_tH_pre,N_tH_BDTa)
print "~                    ~                         ~                         ~                       ~"
print "~        g-g         ~         94610           ~          %5.4f          ~         %5.4f         ~"%(N_gg_pre,N_gg_BDTa)
print "~        gjet        ~         1.0e6           ~          %5.4f          ~         %5.4f         ~"%(N_gjet_pre,N_gjet_BDTa)
print "~        ttg         ~          2186           ~          %5.4f          ~         %5.4f         ~"%(N_ttg_pre,N_ttg_BDTa)
print "~        ttgg        ~         20.43           ~          %5.4f          ~         %5.4f         ~"%(N_ttgg_pre,N_ttgg_BDTa)
print "~        tt          ~         8.6e5           ~          %5.4f          ~         %5.4f         ~"%(N_tt_pre,N_tt_BDTa)
print "~        tgjet       ~          1139           ~          %5.4f          ~         %5.4f         ~"%(N_tgjet_pre,N_tgjet_BDTa)
print "~                    ~                         ~                         ~                       ~"
print "~        totbkg      ~         1.1e6           ~          %5.4f          ~         %5.4f         ~"%(N_bkg_pre,N_bkg_BDTa)
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print ""
print "Signal-to-background ratios:"
print "1) BDT > %5.2f ..."%lep_BDT_cut
print "   For " + str(massLow) + " < m_gg < " + str(massHigh) + " GeV: S(ttH+tH)/B =", (N_ttHptH_massWindow_BDTa)/(N_bkg_massWindow_BDTa)
print ""
print "Signal composition (% in each gen bin at pre-selection):"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "~       Process      ~      0-45      ~     45-80      ~     80-120     ~    120-200     ~    200-350     ~    350-inf     ~"
print "~                                                                                                                          ~"
print "~         ttH        ~      %s     ~      %s     ~      %s     ~      %s     ~      %s     ~      %s     ~"%(str(N_ttH_gen0/N_ttH_pre)[:5],str(N_ttH_gen1/N_ttH_pre)[:5],str(N_ttH_gen2/N_ttH_pre)[:5],str(N_ttH_gen3/N_ttH_pre)[:5],str(N_ttH_gen4/N_ttH_pre)[:5],str(N_ttH_gen5/N_ttH_pre)[:5])    
print "~         ggH        ~      %s     ~      %s     ~      %s     ~      %s     ~      %s     ~      %s     ~"%(str(N_ggH_gen0/N_ggH_pre)[:5],str(N_ggH_gen1/N_ggH_pre)[:5],str(N_ggH_gen2/N_ggH_pre)[:5],str(N_ggH_gen3/N_ggH_pre)[:5],str(N_ggH_gen4/N_ggH_pre)[:5],str(N_ggH_gen5/N_ggH_pre)[:5])    
print "~         VH         ~      %s     ~      %s     ~      %s     ~      %s     ~      %s     ~      %s     ~"%(str(N_VH_gen0/N_VH_pre)[:5],str(N_VH_gen1/N_VH_pre)[:5],str(N_VH_gen2/N_VH_pre)[:5],str(N_VH_gen3/N_VH_pre)[:5],str(N_VH_gen4/N_VH_pre)[:5],str(N_VH_gen5/N_VH_pre)[:5])    
print "~         THQ        ~      %s     ~      %s     ~      %s     ~      %s     ~      %s     ~      %s     ~"%(str(N_THQ_gen0/N_THQ_pre)[:5],str(N_THQ_gen1/N_THQ_pre)[:5],str(N_THQ_gen2/N_THQ_pre)[:5],str(N_THQ_gen3/N_THQ_pre)[:5],str(N_THQ_gen4/N_THQ_pre)[:5],str(N_THQ_gen5/N_THQ_pre)[:5])    
print "~         THW        ~      %s     ~      %s     ~      %s     ~      %s     ~      %s     ~      %s     ~"%(str(N_THW_gen0/N_THW_pre)[:5],str(N_THW_gen1/N_THW_pre)[:5],str(N_THW_gen2/N_THW_pre)[:5],str(N_THW_gen3/N_THW_pre)[:5],str(N_THW_gen4/N_THW_pre)[:5],str(N_THW_gen5/N_THW_pre)[:5])    
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

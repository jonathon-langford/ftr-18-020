import sys
import ROOT
import math
from array import array

intLumi = 3000

#BDT cuts
had_BDT_low = 0.28
had_BDT_high = 0.61

#Background chains
chain_ttgg = ROOT.TChain("trilinearTree")
chain_ttgg.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/background/output_ttHHad_ttgammagamma_1fb.root")

chain_ttg = ROOT.TChain("trilinearTree")
chain_ttg.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/background/output_ttHHad_ttgamma_1fb.root")

chain_gg = ROOT.TChain("trilinearTree")
chain_gg.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/background/output_ttHHad_DiPhotonJetsBox_MGG-80toInf_1fb.root")

chain_gjet = ROOT.TChain("trilinearTree")
chain_gjet.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/background/output_ttHHad_GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_1fb.root")

chain_tt = ROOT.TChain("trilinearTree")
chain_tt.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/background/output_ttHHad_ttbar_1fb.root")

chain_tgjet = ROOT.TChain("trilinearTree")
chain_tgjet.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/background/output_ttHHad_TGJet_inclusive_1fb.root")

#Signal chains
chain_ttH = ROOT.TChain("trilinearTree")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_ttHgen0_M125_1fb.root")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_ttHgen1_M125_1fb.root")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_ttHgen2_M125_1fb.root")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_ttHgen3_M125_1fb.root")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_ttHgen4_M125_1fb.root")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_ttHgen5_M125_1fb.root")

chain_ggH = ROOT.TChain("trilinearTree")
chain_ggH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_ggHgen0_M125_1fb.root")
chain_ggH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_ggHgen1_M125_1fb.root")
chain_ggH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_ggHgen2_M125_1fb.root")
chain_ggH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_ggHgen3_M125_1fb.root")
chain_ggH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_ggHgen4_M125_1fb.root")
chain_ggH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_ggHgen5_M125_1fb.root")

chain_VH = ROOT.TChain("trilinearTree")
chain_VH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_VHgen0_M125_1fb.root")
chain_VH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_VHgen1_M125_1fb.root")
chain_VH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_VHgen2_M125_1fb.root")
chain_VH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_VHgen3_M125_1fb.root")
chain_VH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_VHgen4_M125_1fb.root")
chain_VH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_VHgen5_M125_1fb.root")

chain_tH = ROOT.TChain("trilinearTree")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THQgen0_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THQgen1_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THQgen2_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THQgen3_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THQgen4_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THQgen5_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THWgen0_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THWgen1_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THWgen2_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THWgen3_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THWgen4_M125_1fb.root")
chain_tH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THWgen5_M125_1fb.root")

chain_THQ = ROOT.TChain("trilinearTree")
chain_THQ.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THQgen0_M125_1fb.root")
chain_THQ.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THQgen1_M125_1fb.root")
chain_THQ.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THQgen2_M125_1fb.root")
chain_THQ.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THQgen3_M125_1fb.root")
chain_THQ.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THQgen4_M125_1fb.root")
chain_THQ.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THQgen5_M125_1fb.root")

chain_THW = ROOT.TChain("trilinearTree")
chain_THW.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THWgen0_M125_1fb.root")
chain_THW.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THWgen1_M125_1fb.root")
chain_THW.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THWgen2_M125_1fb.root")
chain_THW.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THWgen3_M125_1fb.root")
chain_THW.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THWgen4_M125_1fb.root")
chain_THW.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHHad/signal/output_ttHHad_THWgen5_M125_1fb.root")

#Define counters to output number of events remaining
N_gg_pre = 0
N_gjet_pre = 0
N_ttgg_pre = 0
N_ttg_pre = 0
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
N_ttgg_BDTa = 0
N_ttg_BDTa = 0
N_tt_BDTa = 0
N_tgjet_BDTa = 0
N_bkg_BDTa = 0

N_ttH_BDTa = 0
N_ggH_BDTa = 0
N_VH_BDTa = 0
N_tH_BDTa = 0

N_gg_BDTb = 0
N_gjet_BDTb = 0
N_ttgg_BDTb = 0
N_ttg_BDTb = 0
N_tt_BDTb = 0
N_tgjet_BDTb = 0
N_bkg_BDTb = 0

N_ttH_BDTb = 0
N_ggH_BDTb = 0
N_VH_BDTb = 0
N_tH_BDTb = 0

#Counters for inside mass mindow
N_bkg_massWindow_BDTa = 0
N_ttHptH_massWindow_BDTa = 0

N_bkg_massWindow_BDTb = 0
N_ttHptH_massWindow_BDTb = 0

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
  if( ev.BDT > had_BDT_low )&( ev.BDT < had_BDT_high ): 
    N_gg_BDTb += ev.weight_LO*intLumi
    N_bkg_BDTb += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTb += ev.weight_LO*intLumi
  elif( ev.BDT >= had_BDT_high ):
    N_gg_BDTa += ev.weight_LO*intLumi
    N_bkg_BDTa += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTa += ev.weight_LO*intLumi

for ev in chain_gjet:
  
  N_gjet_pre += ev.weight_LO*intLumi
  N_bkg_pre += ev.weight_LO*intLumi
  if( ev.BDT > had_BDT_low )&( ev.BDT < had_BDT_high ): 
    N_gjet_BDTb += ev.weight_LO*intLumi
    N_bkg_BDTb += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTb += ev.weight_LO*intLumi
  elif( ev.BDT >= had_BDT_high ):
    N_gjet_BDTa += ev.weight_LO*intLumi
    N_bkg_BDTa += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTa += ev.weight_LO*intLumi

for ev in chain_ttgg:
  
  N_ttgg_pre += ev.weight_LO*intLumi
  N_bkg_pre += ev.weight_LO*intLumi
  if( ev.BDT > had_BDT_low )&( ev.BDT < had_BDT_high ): 
    N_ttgg_BDTb += ev.weight_LO*intLumi
    N_bkg_BDTb += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTb += ev.weight_LO*intLumi
  elif( ev.BDT >= had_BDT_high ):
    N_ttgg_BDTa += ev.weight_LO*intLumi
    N_bkg_BDTa += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTa += ev.weight_LO*intLumi


for ev in chain_ttg:
  
  N_ttg_pre += ev.weight_LO*intLumi
  N_bkg_pre += ev.weight_LO*intLumi
  if( ev.BDT > had_BDT_low )&( ev.BDT < had_BDT_high ): 
    N_ttg_BDTb += ev.weight_LO*intLumi
    N_bkg_BDTb += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTb += ev.weight_LO*intLumi
  elif( ev.BDT >= had_BDT_high ):
    N_ttg_BDTa += ev.weight_LO*intLumi
    N_bkg_BDTa += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTa += ev.weight_LO*intLumi


for ev in chain_tt:
  
  N_tt_pre += ev.weight_LO*intLumi
  N_bkg_pre += ev.weight_LO*intLumi
  if( ev.BDT > had_BDT_low )&( ev.BDT < had_BDT_high ): 
    N_tt_BDTb += ev.weight_LO*intLumi
    N_bkg_BDTb += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTb += ev.weight_LO*intLumi
  elif( ev.BDT >= had_BDT_high ):
    N_tt_BDTa += ev.weight_LO*intLumi
    N_bkg_BDTa += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTa += ev.weight_LO*intLumi


for ev in chain_tgjet:
  
  N_tgjet_pre += ev.weight_LO*intLumi
  N_bkg_pre += ev.weight_LO*intLumi
  if( ev.BDT > had_BDT_low )&( ev.BDT < had_BDT_high ): 
    N_tgjet_BDTb += ev.weight_LO*intLumi
    N_bkg_BDTb += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTb += ev.weight_LO*intLumi
  elif( ev.BDT >= had_BDT_high ):
    N_tgjet_BDTa += ev.weight_LO*intLumi
    N_bkg_BDTa += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_bkg_massWindow_BDTa += ev.weight_LO*intLumi

for ev in chain_ttH:
  
  N_ttH_pre += ev.weight_LO*intLumi
  if( ev.BDT > had_BDT_low )&( ev.BDT < had_BDT_high ): 
    N_ttH_BDTb += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_ttHptH_massWindow_BDTb += ev.weight_LO*intLumi
  elif( ev.BDT >= had_BDT_high ):
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
  if( ev.BDT > had_BDT_low )&( ev.BDT < had_BDT_high ): 
    N_ggH_BDTb += ev.weight_LO*intLumi
  elif( ev.BDT >= had_BDT_high ):
    N_ggH_BDTa += ev.weight_LO*intLumi

  if( ev.pTH_gen >= 0. )&( ev.pTH_gen < 45. ): N_ggH_gen0 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 45. )&( ev.pTH_gen < 80. ): N_ggH_gen1 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 80. )&( ev.pTH_gen < 120. ): N_ggH_gen2 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 120. )&( ev.pTH_gen < 200. ): N_ggH_gen3 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 200. )&( ev.pTH_gen < 350. ): N_ggH_gen4 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 350 ): N_ggH_gen5 += ev.weight_LO*intLumi


for ev in chain_VH:
  
  N_VH_pre += ev.weight_LO*intLumi
  if( ev.BDT > had_BDT_low )&( ev.BDT < had_BDT_high ): 
    N_VH_BDTb += ev.weight_LO*intLumi
  elif( ev.BDT >= had_BDT_high ):
    N_VH_BDTa += ev.weight_LO*intLumi

  if( ev.pTH_gen >= 0. )&( ev.pTH_gen < 45. ): N_VH_gen0 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 45. )&( ev.pTH_gen < 80. ): N_VH_gen1 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 80. )&( ev.pTH_gen < 120. ): N_VH_gen2 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 120. )&( ev.pTH_gen < 200. ): N_VH_gen3 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 200. )&( ev.pTH_gen < 350. ): N_VH_gen4 += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 350 ): N_VH_gen5 += ev.weight_LO*intLumi


for ev in chain_tH:

  N_tH_pre += ev.weight_LO*intLumi
  if( ev.BDT > had_BDT_low )&( ev.BDT < had_BDT_high ): 
    N_tH_BDTb += ev.weight_LO*intLumi
    if( ev.mgg > massLow )&( ev.mgg < massHigh ): N_ttHptH_massWindow_BDTb += ev.weight_LO*intLumi
  elif( ev.BDT >= had_BDT_high ):
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

print "Analysis cut flow:"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "~       Process      ~         Total           ~      Pre-selection      ~        BDT>%5.2f       ~     %5.2f<BDT<%5.2f     ~        BDT>%5.2f       ~"%(had_BDT_low,had_BDT_low,had_BDT_high,had_BDT_high)
print "~                    ~                         ~                         ~                       ~                       ~                       ~"
print "~        ttH         ~         1.393           ~          %5.4f          ~         %5.4f         ~         %5.4f         ~         %5.4f         ~"%(N_ttH_pre,N_ttH_BDTa+N_ttH_BDTb,N_ttH_BDTb,N_ttH_BDTa)
print "~        ggH         ~         124.1           ~          %5.4f          ~         %5.4f         ~         %5.4f         ~         %5.4f         ~"%(N_ggH_pre,N_ggH_BDTa+N_ggH_BDTb,N_ggH_BDTb,N_ggH_BDTa)
print "~        VH          ~         5.XXX           ~          %5.4f          ~         %5.4f         ~         %5.4f         ~         %5.4f         ~"%(N_VH_pre,N_VH_BDTa+N_VH_BDTb,N_VH_BDTb,N_VH_BDTa)
print "~        tH          ~         0.245           ~          %5.4f          ~         %5.4f         ~         %5.4f         ~         %5.4f         ~"%(N_tH_pre,N_tH_BDTa+N_tH_BDTb,N_tH_BDTb,N_tH_BDTa)
print "~                    ~                         ~                         ~                       ~                       ~                       ~"
print "~        g-g         ~         94610           ~          %5.4f          ~         %5.4f         ~         %5.4f         ~         %5.4f         ~"%(N_gg_pre,N_gg_BDTa+N_gg_BDTb,N_gg_BDTb,N_gg_BDTa)
print "~        gjet        ~         1.0e6           ~          %5.4f          ~         %5.4f         ~         %5.4f         ~         %5.4f         ~"%(N_gjet_pre,N_gjet_BDTa+N_gjet_BDTb,N_gjet_BDTb,N_gjet_BDTa)
print "~        ttgg        ~         20.43           ~          %5.4f          ~         %5.4f         ~         %5.4f         ~         %5.4f         ~"%(N_ttgg_pre,N_ttgg_BDTa+N_ttgg_BDTb,N_ttgg_BDTb,N_ttgg_BDTa)
print "~        ttg         ~          2186           ~          %5.4f          ~         %5.4f         ~         %5.4f         ~         %5.4f         ~"%(N_ttg_pre,N_ttg_BDTa+N_ttg_BDTb,N_ttg_BDTb,N_ttg_BDTa)
print "~        tt          ~         8.6e5           ~          %5.4f          ~         %5.4f         ~         %5.4f         ~         %5.4f         ~"%(N_tt_pre,N_tt_BDTa+N_tt_BDTb,N_tt_BDTb,N_tt_BDTa)
print "~        tgjet       ~          1139           ~          %5.4f          ~         %5.4f         ~         %5.4f         ~         %5.4f         ~"%(N_tgjet_pre,N_tgjet_BDTa+N_tgjet_BDTb,N_tgjet_BDTb,N_tgjet_BDTa)
print "~                    ~                         ~                         ~                       ~                       ~                       ~"
print "~        totbkg      ~         1.1e6           ~          %5.4f          ~         %5.4f         ~         %5.4f         ~         %5.4f         ~"%(N_bkg_pre,N_bkg_BDTa+N_bkg_BDTb,N_bkg_BDTb,N_bkg_BDTa)
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print ""
print "Signal-to-background ratios:"
print "1) BDT > %5.2f ..."%had_BDT_low
print "   For " + str(massLow) + " < m_gg < " + str(massHigh) + " GeV: S(ttH+tH)/B =", (N_ttHptH_massWindow_BDTa+N_ttHptH_massWindow_BDTb)/(N_bkg_massWindow_BDTa+N_bkg_massWindow_BDTb)
print "2) %5.2f < BDT < %5.2f    i.e. BDTb   ..."%(had_BDT_low,had_BDT_high)
print "   For " + str(massLow) + " < m_gg < " + str(massHigh) + " GeV: S(ttH+tH)/B =", (N_ttHptH_massWindow_BDTb)/(N_bkg_massWindow_BDTb)
print "3) BDT > %5.2f    i.e. BDTa   ..."%had_BDT_high
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

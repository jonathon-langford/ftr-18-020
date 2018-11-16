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
N_gg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
N_gjet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
N_ttgg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
N_ttg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
N_tt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
N_tgjet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

N_ttH = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
N_tHq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
N_tHW = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
N_ggH = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
N_VH = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

reco_dict = {0:[0,45,had_BDT_high,1.],1:[0,45,had_BDT_low,had_BDT_high],2:[45.,80.,had_BDT_high,1.],3:[45.,80.,had_BDT_low,had_BDT_high],4:[80.,120.,had_BDT_high,1.],5:[80.,120.,had_BDT_low,had_BDT_high],6:[120.,200.,had_BDT_high,1.],7:[120.,200.,had_BDT_low,had_BDT_high],8:[200.,350.,had_BDT_high,1.],9:[200.,350.,had_BDT_low,had_BDT_high],10:[350.,99999999.,had_BDT_low,1.]}

for ev in chain_gg:
  
  cat_found = False
  cat = -1
  for cat_idx in reco_dict:
    if( not cat_found ):
      if( ev.pTH_reco > reco_dict[cat_idx][0] )&( ev.pTH_reco <= reco_dict[cat_idx][1] )&( ev.BDT > reco_dict[cat_idx][2] )&( ev.BDT <= reco_dict[cat_idx][3] ):
        cat = cat_idx
        cat_found = True
  
  if( cat_found ):
    N_gg[cat] += ev.weight_LO*intLumi

for ev in chain_gjet:

  cat_found = False
  cat = -1
  for cat_idx in reco_dict:
    if( not cat_found ):
      if( ev.pTH_reco > reco_dict[cat_idx][0] )&( ev.pTH_reco <= reco_dict[cat_idx][1] )&( ev.BDT > reco_dict[cat_idx][2] )&( ev.BDT <= reco_dict[cat_idx][3] ):
        cat = cat_idx
        cat_found = True
  
  if( cat_found ):
    N_gjet[cat] += ev.weight_LO*intLumi
 

for ev in chain_ttgg:

  cat_found = False
  cat = -1
  for cat_idx in reco_dict:
    if( not cat_found ):
      if( ev.pTH_reco > reco_dict[cat_idx][0] )&( ev.pTH_reco <= reco_dict[cat_idx][1] )&( ev.BDT > reco_dict[cat_idx][2] )&( ev.BDT <= reco_dict[cat_idx][3] ):
	cat = cat_idx
	cat_found = True
  
  if( cat_found ):
    N_ttgg[cat] += ev.weight_LO*intLumi
  

for ev in chain_ttg:
 
  cat_found = False
  cat = -1
  for cat_idx in reco_dict:
    if( not cat_found ):
      if( ev.pTH_reco > reco_dict[cat_idx][0] )&( ev.pTH_reco <= reco_dict[cat_idx][1] )&( ev.BDT > reco_dict[cat_idx][2] )&( ev.BDT <= reco_dict[cat_idx][3] ):
        cat = cat_idx
        cat_found = True
  
  if( cat_found ):
    N_ttg[cat] += ev.weight_LO*intLumi
 

for ev in chain_tt:
 
  cat_found = False
  cat = -1
  for cat_idx in reco_dict:
    if( not cat_found ):
      if( ev.pTH_reco > reco_dict[cat_idx][0] )&( ev.pTH_reco <= reco_dict[cat_idx][1] )&( ev.BDT > reco_dict[cat_idx][2] )&( ev.BDT <= reco_dict[cat_idx][3] ):
        cat = cat_idx
        cat_found = True
  
  if( cat_found ):
    N_tt[cat] += ev.weight_LO*intLumi
 

for ev in chain_tgjet:
 
  cat_found = False
  cat = -1
  for cat_idx in reco_dict:
    if( not cat_found ):
      if( ev.pTH_reco > reco_dict[cat_idx][0] )&( ev.pTH_reco <= reco_dict[cat_idx][1] )&( ev.BDT > reco_dict[cat_idx][2] )&( ev.BDT <= reco_dict[cat_idx][3] ):
        cat = cat_idx
        cat_found = True
  
  if( cat_found ):
    N_tgjet[cat] += ev.weight_LO*intLumi
 

for ev in chain_ttH:
 
  cat_found = False
  cat = -1
  for cat_idx in reco_dict:
    if( not cat_found ):
      if( ev.pTH_reco > reco_dict[cat_idx][0] )&( ev.pTH_reco <= reco_dict[cat_idx][1] )&( ev.BDT > reco_dict[cat_idx][2] )&( ev.BDT <= reco_dict[cat_idx][3] ):
        cat = cat_idx
        cat_found = True
  
  if( cat_found ):
    N_ttH[cat] += ev.weight_LO*intLumi
 

for ev in chain_ggH:
 
  cat_found = False
  cat = -1
  for cat_idx in reco_dict:
    if( not cat_found ):
      if( ev.pTH_reco > reco_dict[cat_idx][0] )&( ev.pTH_reco <= reco_dict[cat_idx][1] )&( ev.BDT > reco_dict[cat_idx][2] )&( ev.BDT <= reco_dict[cat_idx][3] ):
        cat = cat_idx
        cat_found = True
  
  if( cat_found ):
    N_ggH[cat] += ev.weight_LO*intLumi
 

for ev in chain_VH:
 
  cat_found = False
  cat = -1
  for cat_idx in reco_dict:
    if( not cat_found ):
      if( ev.pTH_reco > reco_dict[cat_idx][0] )&( ev.pTH_reco <= reco_dict[cat_idx][1] )&( ev.BDT > reco_dict[cat_idx][2] )&( ev.BDT <= reco_dict[cat_idx][3] ):
        cat = cat_idx
        cat_found = True
  
  if( cat_found ):
    N_VH[cat] += ev.weight_LO*intLumi
 

for ev in chain_THQ:

  cat_found = False
  cat = -1
  for cat_idx in reco_dict:
    if( not cat_found ):
      if( ev.pTH_reco > reco_dict[cat_idx][0] )&( ev.pTH_reco <= reco_dict[cat_idx][1] )&( ev.BDT > reco_dict[cat_idx][2] )&( ev.BDT <= reco_dict[cat_idx][3] ):
        cat = cat_idx
        cat_found = True
  
  if( cat_found ):
    N_tHq[cat] += ev.weight_LO*intLumi


for ev in chain_THW:

  cat_found = False
  cat = -1
  for cat_idx in reco_dict:
    if( not cat_found ):
      if( ev.pTH_reco > reco_dict[cat_idx][0] )&( ev.pTH_reco <= reco_dict[cat_idx][1] )&( ev.BDT > reco_dict[cat_idx][2] )&( ev.BDT <= reco_dict[cat_idx][3] ):
        cat = cat_idx
        cat_found = True
  
  if( cat_found ):
    N_tHW[cat] += ev.weight_LO*intLumi

recobin_names = ['reco0_BDTa','reco0_BDTb','reco1_BDTa','reco1_BDTb','reco2_BDTa','reco2_BDTb','reco3_BDTa','reco3_BDTb','reco4_BDTa','reco4_BDTb','reco5']

print ""
print "Event counter: Reco-level categories"
for cat_idx in reco_dict:

  print "  %s"%recobin_names[cat_idx]
  print "    Signal"
  print "      ttH: %5.4f"%N_ttH[cat_idx]
  print "      tHq: %5.4f"%N_tHq[cat_idx]
  print "      tHW: %5.4f"%N_tHW[cat_idx]
  print "    Backgrounds (Higgs)"
  print "      ggH: %5.4f"%N_ggH[cat_idx]
  print "       VH: %5.4f"%N_VH[cat_idx]
  print "    Backgrounds (other)"
  print "       gg: %5.4f"%N_gg[cat_idx]
  print "     gjet: %5.4f"%N_gjet[cat_idx]
  print "     ttgg: %5.4f"%N_ttgg[cat_idx]
  print "      ttg: %5.4f"%N_ttg[cat_idx]
  print "       tt: %5.4f"%N_tt[cat_idx]
  print "    tgjet: %5.4f"%N_tgjet[cat_idx]
  print ""

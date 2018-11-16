import ROOT
import numpy as np
import math
import sys
from array import array

#BDT cut
lep_BDT_cut = 0.13

#response matrix generator

# Two options: a) normalise by category
#              b) normalise by process

#User input for signal process
if( len(sys.argv) != 3 ):
  print "Usage: resmat.py <signal process e.g. ttH> <normalisation: proc/cat>"
  sys.exit(1)
processID = sys.argv[1]
normalisation = sys.argv[2]

#Open canvas
canv = ROOT.TCanvas("c","c")
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat('4.1f')
ROOT.gStyle.SetPalette(57)

#Define signal chains and add appropriate files
chain = ROOT.TChain("trilinearTree")
#if( processID == "ttH" )|( processID == "ggH" ):
chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_%sgen0_M125_1fb.root"%processID )
chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_%sgen1_M125_1fb.root"%processID )
chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_%sgen2_M125_1fb.root"%processID )
chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_%sgen3_M125_1fb.root"%processID )
chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_%sgen4_M125_1fb.root"%processID )
chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_%sgen5_M125_1fb.root"%processID )
#else:
#  chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/trees_manip_ttHLep/signal/output_ttHLep_THQgen0_M125_1fb.root")
#  chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/trees_manip_ttHLep/signal/output_ttHLep_THQgen1_M125_1fb.root")
#  chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/trees_manip_ttHLep/signal/output_ttHLep_THQgen2_M125_1fb.root")
#  chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/trees_manip_ttHLep/signal/output_ttHLep_THQgen3_M125_1fb.root")
#  chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/trees_manip_ttHLep/signal/output_ttHLep_THQgen4_M125_1fb.root")
#  chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/trees_manip_ttHLep/signal/output_ttHLep_THQgen5_M125_1fb.root")
#  chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/trees_manip_ttHLep/signal/output_ttHLep_THWgen0_M125_1fb.root")
#  chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/trees_manip_ttHLep/signal/output_ttHLep_THWgen1_M125_1fb.root")
#  chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/trees_manip_ttHLep/signal/output_ttHLep_THWgen2_M125_1fb.root")
#  chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/trees_manip_ttHLep/signal/output_ttHLep_THWgen3_M125_1fb.root")
#  chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/trees_manip_ttHLep/signal/output_ttHLep_THWgen4_M125_1fb.root")
#  chain.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/trees_manip_ttHLep/signal/output_ttHLep_THWgen5_M125_1fb.root")

#Define 2D histogram and bin labels
h_resmat = ROOT.TH2F("h_resmat","", 6, 0, 6, 6, 0, 6)
xbin_label = ['lep_reco0','lep_reco1','lep_reco2','lep_reco3','lep_reco4','lep_reco5']
#xbin_label = ['p_{T}^{#gamma#gamma} #in [0,50] GeV, BDT > 0.75','p_{T}^{#gamma#gamma} #in [0,50] GeV, 0.45 < BDT < 0.75', 'p_{T}^{#gamma#gamma} #in [50,100] GeV, BDT > 0.75','p_{T}^{#gamma#gamma} #in [50,100] GeV, 0.45 < BDT < 0.75','p_{T}^{#gamma#gamma} #in [100,150] GeV, BDT > 0.75','p_{T}^{#gamma#gamma} #in [100,150] GeV, 0.45 < BDT < 0.75','p_{T}^{#gamma#gamma} #in [150,250] GeV, BDT > 0.75','p_{T}^{#gamma#gamma} #in [150,250] GeV, 0.45 < BDT < 0.75','p_{T}^{#gamma#gamma} #in [250,400] GeV, BDT > 0.75','p_{T}^{#gamma#gamma} #in [250,400] GeV, 0.45 < BDT < 0.75','p_{T}^{#gamma#gamma} #in [400,inf] GeV']
ybin_label = ['gen0','gen1','gen2','gen3','gen4','gen5']
#ybin_label = ['p_{T}^{H} #in [0,50] GeV','p_{T}^{H} #in [50,100] GeV','p_{T}^{H} #in [100,150] GeV','p_{T}^{H} #in [150,250] GeV','p_{T}^{H} #in [250,400] GeV','p_{T}^{H} #in [400,inf] GeV']

#Set bin labels
for xbin_idx in range(1,h_resmat.GetNbinsX()+1): h_resmat.GetXaxis().SetBinLabel( xbin_idx, xbin_label[xbin_idx-1] )
#h_resmat.GetXaxis().LabelsOption("v")
for ybin_idx in range(1,h_resmat.GetNbinsY()+1): h_resmat.GetYaxis().SetBinLabel( ybin_idx, ybin_label[ybin_idx-1] )

#Define dict to relate pTH+BDT to correct bin
reco_dict = { 0:[0.,45.,lep_BDT_cut,1.], 1:[45.,80.,lep_BDT_cut,1.], 2:[80.,120.,lep_BDT_cut,1.], 3:[120.,200.,lep_BDT_cut,1.], 4:[200.,350.,lep_BDT_cut,1.], 5:[350.,9999999999999.,lep_BDT_cut,1.] }
gen_dict = { 0:[0.,45.], 1:[45.,80.], 2:[80.,120.], 3:[120.,200.], 4:[200.,350.], 5:[350.,9999999999999.] }

ev_idx = 0
N_tot = 0
for ev in chain:
  #if ev_idx > 50: continue

  if( ev.BDT > lep_BDT_cut ): N_tot += ev.weight_LO

  recobin_found = False
  recobin = -1
  for bin_idx in reco_dict:
    if( not recobin_found ):
      if( ev.pTH_reco > reco_dict[bin_idx][0] )&( ev.pTH_reco <= reco_dict[bin_idx][1] )&( ev.BDT > reco_dict[bin_idx][2] )&( ev.BDT <= reco_dict[bin_idx][3] ): 
        recobin = bin_idx
        recobin_found = True
       
  genbin_found = False
  genbin = -1
  for bin_idx in gen_dict:
    if( not genbin_found ):
      if( ev.pTH_gen > gen_dict[bin_idx][0] )&( ev.pTH_gen <= gen_dict[bin_idx][1] ):
        genbin = bin_idx
        genbin_found = True

  h_resmat.SetBinContent( recobin+1, genbin+1, h_resmat.GetBinContent( recobin+1, genbin+1 )+ev.weight_LO )

  #print "Entry %g: pTH(gen) = %s GeV,   pTH(reco) = %s GeV,   BDT = %4.2f ------> Reco:%g  Gen:%g"%(ev_idx, str(ev.pTH_gen)[:5], str(ev.pTH_reco)[:5], ev.BDT, recobin, genbin)
  ev_idx += 1


if( normalisation == "cat" ):
  #Sum entries in each column (category)
  for cat in range( 1, h_resmat.GetNbinsX()+1 ):
    N_cat = 0
    for proc in range( 1, h_resmat.GetNbinsY()+1 ):
      N_cat += h_resmat.GetBinContent( cat, proc )
    #re-loop over bins and set as %
    for proc in range( 1, h_resmat.GetNbinsY()+1 ):
      if( N_cat != 0 ): h_resmat.SetBinContent( cat, proc, (h_resmat.GetBinContent(cat,proc)*100)/N_cat )

if( normalisation == "proc" ):
  #Sum entries in each row (proc)
  for proc in range( 1, h_resmat.GetNbinsY()+1 ):
    N_proc = 0
    for cat in range( 1, h_resmat.GetNbinsX()+1 ):
      N_proc += h_resmat.GetBinContent( cat, proc )
    #re-loop over bins and set as %
    for cat in range( 1, h_resmat.GetNbinsX()+1 ):
      h_resmat.SetBinContent( cat, proc, (h_resmat.GetBinContent(cat,proc)*100)/N_proc )

h_resmat.GetYaxis().SetTitle("Gen-level process")
h_resmat.GetYaxis().SetLabelSize(0.04)
h_resmat.GetYaxis().SetTitleSize(0.04)
h_resmat.GetYaxis().SetTitleOffset(1.1)
h_resmat.GetXaxis().SetTitle("Reco-level categorisation")
h_resmat.GetXaxis().SetLabelSize(0.04)
h_resmat.GetXaxis().SetTitleSize(0.04)
h_resmat.GetXaxis().SetTitleOffset(1.4)
h_resmat.GetZaxis().SetTitle("[%]")

h_resmat.SetMaximum(100.)
h_resmat.SetMinimum(0.)
h_resmat.SetMarkerSize(1.5)
h_resmat.Draw("COLZ TEXT")
canv.SetRightMargin(0.15)
canv.SetBottomMargin(0.15)

lat = ROOT.TLatex()
lat.SetTextFont(42)
lat.SetLineWidth(2)
lat.SetTextAlign(11)
lat.SetNDC()
lat.SetTextSize(0.05)
lat.DrawLatex(0.1,0.92,"#bf{CMS Simulation}")
if( normalisation == "cat" ): lat.DrawLatex(0.6,0.92,"%s Response Matrix"%processID)
elif( normalisation == "proc" ): lat.DrawLatex(0.6,0.92,"%s Purity Matrix"%processID)
canv.Update()

canv.Print("output/resmat_ttHLep_%s_normby%s.pdf"%(processID,normalisation))

raw_input("Press Enter to continue...")

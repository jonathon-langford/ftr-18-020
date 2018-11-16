import sys
import ROOT
import math
from array import array

intLumi = 1

#BDT cut
lep_BDT_cut = 0.13

#Signal chains
chain_ttH = ROOT.TChain("trilinearTree")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen0_M125_1fb.root")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen1_M125_1fb.root")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen2_M125_1fb.root")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen3_M125_1fb.root")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen4_M125_1fb.root")
chain_ttH.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen5_M125_1fb.root")

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

chain_tot = ROOT.TChain("trilinearTree")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen0_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen1_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen2_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen3_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen4_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_ttHgen5_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen0_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen1_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen2_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen3_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen4_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THQgen5_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen0_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen1_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen2_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen3_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen4_M125_1fb.root")
chain_tot.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/signal/output_ttHLep_THWgen5_M125_1fb.root")

#Fiducial chains
chain_ttH_fid = ROOT.TChain("trilinearTree")
chain_ttH_fid.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/gen_acceptance/ttH_fiducial.root")

chain_THQ_fid = ROOT.TChain("trilinearTree")
chain_THQ_fid.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/gen_acceptance/THQ_fiducial.root")

chain_THW_fid = ROOT.TChain("trilinearTree")
chain_THW_fid.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/gen_acceptance/THW_fiducial.root")

chain_tot_fid = ROOT.TChain("trilinearTree")
chain_tot_fid.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/gen_acceptance/ttH_fiducial.root")
chain_tot_fid.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/gen_acceptance/THQ_fiducial.root")
chain_tot_fid.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_9_4_4/src/btag_correction/ttHLep/gen_acceptance/THW_fiducial.root")

#Define counters to output number of events in each gen bin
N_ttH_gen0_fiducial = 0
N_ttH_gen0_selected = 0
N_ttH_gen1_fiducial = 0
N_ttH_gen1_selected = 0
N_ttH_gen2_fiducial = 0
N_ttH_gen2_selected = 0
N_ttH_gen3_fiducial = 0
N_ttH_gen3_selected = 0
N_ttH_gen4_fiducial = 0
N_ttH_gen4_selected = 0
N_ttH_gen5_fiducial = 0
N_ttH_gen5_selected = 0

N_THQ_gen0_fiducial = 0
N_THQ_gen0_selected = 0
N_THQ_gen1_fiducial = 0
N_THQ_gen1_selected = 0
N_THQ_gen2_fiducial = 0
N_THQ_gen2_selected = 0
N_THQ_gen3_fiducial = 0
N_THQ_gen3_selected = 0
N_THQ_gen4_fiducial = 0
N_THQ_gen4_selected = 0
N_THQ_gen5_fiducial = 0
N_THQ_gen5_selected = 0

N_THW_gen0_fiducial = 0
N_THW_gen0_selected = 0
N_THW_gen1_fiducial = 0
N_THW_gen1_selected = 0
N_THW_gen2_fiducial = 0
N_THW_gen2_selected = 0
N_THW_gen3_fiducial = 0
N_THW_gen3_selected = 0
N_THW_gen4_fiducial = 0
N_THW_gen4_selected = 0
N_THW_gen5_fiducial = 0
N_THW_gen5_selected = 0

N_tot_gen0_fiducial = 0
N_tot_gen0_selected = 0
N_tot_gen1_fiducial = 0
N_tot_gen1_selected = 0
N_tot_gen2_fiducial = 0
N_tot_gen2_selected = 0
N_tot_gen3_fiducial = 0
N_tot_gen3_selected = 0
N_tot_gen4_fiducial = 0
N_tot_gen4_selected = 0
N_tot_gen5_fiducial = 0
N_tot_gen5_selected = 0

for ev in chain_ttH_fid:
  if( ev.pTH_gen >= 0. )&( ev.pTH_gen < 45. ): N_ttH_gen0_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 45. )&( ev.pTH_gen < 80. ): N_ttH_gen1_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 80. )&( ev.pTH_gen < 120. ): N_ttH_gen2_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 120. )&( ev.pTH_gen < 200. ): N_ttH_gen3_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 200. )&( ev.pTH_gen < 350. ): N_ttH_gen4_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 350 ): N_ttH_gen5_fiducial += ev.weight_LO*intLumi

for ev in chain_ttH:
  if( ev.BDT > lep_BDT_cut ):
    if( ev.pTH_gen >= 0. )&( ev.pTH_gen < 45. ): N_ttH_gen0_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 45. )&( ev.pTH_gen < 80. ): N_ttH_gen1_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 80. )&( ev.pTH_gen < 120. ): N_ttH_gen2_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 120. )&( ev.pTH_gen < 200. ): N_ttH_gen3_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 200. )&( ev.pTH_gen < 350. ): N_ttH_gen4_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 350 ): N_ttH_gen5_selected += ev.weight_LO*intLumi

for ev in chain_THQ_fid:
  if( ev.pTH_gen >= 0. )&( ev.pTH_gen < 45. ): N_THQ_gen0_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 45. )&( ev.pTH_gen < 80. ): N_THQ_gen1_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 80. )&( ev.pTH_gen < 120. ): N_THQ_gen2_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 120. )&( ev.pTH_gen < 200. ): N_THQ_gen3_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 200. )&( ev.pTH_gen < 350. ): N_THQ_gen4_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 350 ): N_THQ_gen5_fiducial += ev.weight_LO*intLumi

for ev in chain_THQ:
  if( ev.BDT > lep_BDT_cut ):
    if( ev.pTH_gen >= 0. )&( ev.pTH_gen < 45. ): N_THQ_gen0_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 45. )&( ev.pTH_gen < 80. ): N_THQ_gen1_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 80. )&( ev.pTH_gen < 120. ): N_THQ_gen2_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 120. )&( ev.pTH_gen < 200. ): N_THQ_gen3_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 200. )&( ev.pTH_gen < 350. ): N_THQ_gen4_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 350 ): N_THQ_gen5_selected += ev.weight_LO*intLumi

for ev in chain_THW_fid:
  if( ev.pTH_gen >= 0. )&( ev.pTH_gen < 45. ): N_THW_gen0_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 45. )&( ev.pTH_gen < 80. ): N_THW_gen1_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 80. )&( ev.pTH_gen < 120. ): N_THW_gen2_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 120. )&( ev.pTH_gen < 200. ): N_THW_gen3_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 200. )&( ev.pTH_gen < 350. ): N_THW_gen4_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 350 ): N_THW_gen5_fiducial += ev.weight_LO*intLumi

for ev in chain_THW:
  if( ev.BDT > lep_BDT_cut ):
    if( ev.pTH_gen >= 0. )&( ev.pTH_gen < 45. ): N_THW_gen0_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 45. )&( ev.pTH_gen < 80. ): N_THW_gen1_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 80. )&( ev.pTH_gen < 120. ): N_THW_gen2_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 120. )&( ev.pTH_gen < 200. ): N_THW_gen3_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 200. )&( ev.pTH_gen < 350. ): N_THW_gen4_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 350 ): N_THW_gen5_selected += ev.weight_LO*intLumi

for ev in chain_tot_fid:
  if( ev.pTH_gen >= 0. )&( ev.pTH_gen < 45. ): N_tot_gen0_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 45. )&( ev.pTH_gen < 80. ): N_tot_gen1_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 80. )&( ev.pTH_gen < 120. ): N_tot_gen2_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 120. )&( ev.pTH_gen < 200. ): N_tot_gen3_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 200. )&( ev.pTH_gen < 350. ): N_tot_gen4_fiducial += ev.weight_LO*intLumi
  elif( ev.pTH_gen >= 350 ): N_tot_gen5_fiducial += ev.weight_LO*intLumi

for ev in chain_tot:
  if( ev.BDT > lep_BDT_cut ):
    if( ev.pTH_gen >= 0. )&( ev.pTH_gen < 45. ): N_tot_gen0_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 45. )&( ev.pTH_gen < 80. ): N_tot_gen1_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 80. )&( ev.pTH_gen < 120. ): N_tot_gen2_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 120. )&( ev.pTH_gen < 200. ): N_tot_gen3_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 200. )&( ev.pTH_gen < 350. ): N_tot_gen4_selected += ev.weight_LO*intLumi
    elif( ev.pTH_gen >= 350 ): N_tot_gen5_selected += ev.weight_LO*intLumi

#Write acceptance values to file
N_tot_selected = [N_tot_gen0_selected,N_tot_gen1_selected,N_tot_gen2_selected,N_tot_gen3_selected,N_tot_gen4_selected,N_tot_gen5_selected]
N_tot_fiducial = [N_tot_gen0_fiducial,N_tot_gen1_fiducial,N_tot_gen2_fiducial,N_tot_gen3_fiducial,N_tot_gen4_fiducial,N_tot_gen5_fiducial]
fOutname = "/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/btag_correction/diffXS/input/acceptance_ttHLep_new.txt"
f_out = open( fOutname, "w" )
for gen_idx in range(0,6):
  f_out.write( "gen%g %s\n"%(gen_idx,str(N_tot_selected[gen_idx]/N_tot_fiducial[gen_idx])) )
f_out.close()

print "Fiducial Region:   * Y(H) < 2.5"
print "                   * pT(\gamma) > 20 GeV && |\eta| < 2.5   for \gamma_1/2"
print "                   * Atleast 2 jets w/ pT(jet) > 25 GeV && |\eta| < 4"
print "                   * Atleast one bjet"
print ""
print "Acceptance:"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "~         Bin        ~       Process      ~        Fiducial         ~        Pre+BDT        ~        Acc (x)        ~"
print "~                    ~                    ~                         ~                       ~                       ~"
print "~                    ~        ttH         ~        %s         ~       %s        ~       %s        ~"%(str(N_ttH_gen0_fiducial)[:8],str(N_ttH_gen0_selected)[:8],str(N_ttH_gen0_selected/N_ttH_gen0_fiducial)[:8])
print "~        gen0        ~        THQ         ~        %s         ~       %s        ~       %s        ~"%(str(N_THQ_gen0_fiducial)[:8],str(N_THQ_gen0_selected)[:8],str(N_THQ_gen0_selected/N_THQ_gen0_fiducial)[:8])
print "~                    ~        THW         ~        %s         ~       %s        ~       %s        ~"%(str(N_THW_gen0_fiducial)[:8],str(N_THW_gen0_selected)[:8],str(N_THW_gen0_selected/N_THW_gen0_fiducial)[:8])
print "~                    ~        tot         ~        %s         ~       %s        ~       %s        ~"%(str(N_tot_gen0_fiducial)[:8],str(N_tot_gen0_selected)[:8],str(N_tot_gen0_selected/N_tot_gen0_fiducial)[:8])
print "~                    ~                    ~                         ~                       ~                       ~"
print "~                    ~        ttH         ~        %s         ~       %s        ~       %s        ~"%(str(N_ttH_gen1_fiducial)[:8],str(N_ttH_gen1_selected)[:8],str(N_ttH_gen1_selected/N_ttH_gen1_fiducial)[:8])
print "~        gen1        ~        THQ         ~        %s         ~       %s        ~       %s        ~"%(str(N_THQ_gen1_fiducial)[:8],str(N_THQ_gen1_selected)[:8],str(N_THQ_gen1_selected/N_THQ_gen1_fiducial)[:8])
print "~                    ~        THW         ~        %s         ~       %s        ~       %s        ~"%(str(N_THW_gen1_fiducial)[:8],str(N_THW_gen1_selected)[:8],str(N_THW_gen1_selected/N_THW_gen1_fiducial)[:8])
print "~                    ~        tot         ~        %s         ~       %s        ~       %s        ~"%(str(N_tot_gen1_fiducial)[:8],str(N_tot_gen1_selected)[:8],str(N_tot_gen1_selected/N_tot_gen1_fiducial)[:8])
print "~                    ~                    ~                         ~                       ~                       ~"
print "~                    ~        ttH         ~        %s         ~       %s        ~       %s        ~"%(str(N_ttH_gen2_fiducial)[:8],str(N_ttH_gen2_selected)[:8],str(N_ttH_gen2_selected/N_ttH_gen2_fiducial)[:8])
print "~        gen2        ~        THQ         ~        %s         ~       %s        ~       %s        ~"%(str(N_THQ_gen2_fiducial)[:8],str(N_THQ_gen2_selected)[:8],str(N_THQ_gen2_selected/N_THQ_gen2_fiducial)[:8])
print "~                    ~        THW         ~        %s         ~       %s        ~       %s        ~"%(str(N_THW_gen2_fiducial)[:8],str(N_THW_gen2_selected)[:8],str(N_THW_gen2_selected/N_THW_gen2_fiducial)[:8])
print "~                    ~        tot         ~        %s         ~       %s        ~       %s        ~"%(str(N_tot_gen2_fiducial)[:8],str(N_tot_gen2_selected)[:8],str(N_tot_gen2_selected/N_tot_gen2_fiducial)[:8])
print "~                    ~                    ~                         ~                       ~                       ~"
print "~                    ~        ttH         ~        %s         ~       %s        ~       %s        ~"%(str(N_ttH_gen3_fiducial)[:8],str(N_ttH_gen3_selected)[:8],str(N_ttH_gen3_selected/N_ttH_gen3_fiducial)[:8])
print "~        gen3        ~        THQ         ~        %s         ~       %s        ~       %s        ~"%(str(N_THQ_gen3_fiducial)[:8],str(N_THQ_gen3_selected)[:8],str(N_THQ_gen3_selected/N_THQ_gen3_fiducial)[:8])
print "~                    ~        THW         ~        %s         ~       %s        ~       %s        ~"%(str(N_THW_gen3_fiducial)[:8],str(N_THW_gen3_selected)[:8],str(N_THW_gen3_selected/N_THW_gen3_fiducial)[:8])
print "~                    ~        tot         ~        %s         ~       %s        ~       %s        ~"%(str(N_tot_gen3_fiducial)[:8],str(N_tot_gen3_selected)[:8],str(N_tot_gen3_selected/N_tot_gen3_fiducial)[:8])
print "~                    ~                    ~                         ~                       ~                       ~"
print "~                    ~        ttH         ~        %s         ~       %s        ~       %s        ~"%(str(N_ttH_gen4_fiducial)[:8],str(N_ttH_gen4_selected)[:8],str(N_ttH_gen4_selected/N_ttH_gen4_fiducial)[:8])
print "~        gen4        ~        THQ         ~        %s         ~       %s        ~       %s        ~"%(str(N_THQ_gen4_fiducial)[:8],str(N_THQ_gen4_selected)[:8],str(N_THQ_gen4_selected/N_THQ_gen4_fiducial)[:8])
print "~                    ~        THW         ~        %s         ~       %s        ~       %s        ~"%(str(N_THW_gen4_fiducial)[:8],str(N_THW_gen4_selected)[:8],str(N_THW_gen4_selected/N_THW_gen4_fiducial)[:8])
print "~                    ~        tot         ~        %s         ~       %s        ~       %s        ~"%(str(N_tot_gen4_fiducial)[:8],str(N_tot_gen4_selected)[:8],str(N_tot_gen4_selected/N_tot_gen4_fiducial)[:8])
print "~                    ~                    ~                         ~                       ~                       ~"
print "~                    ~        ttH         ~        %s         ~       %s        ~       %s        ~"%(str(N_ttH_gen5_fiducial)[:8],str(N_ttH_gen5_selected)[:8],str(N_ttH_gen5_selected/N_ttH_gen5_fiducial)[:8])
print "~        gen5        ~        THQ         ~        %s         ~       %s        ~       %s        ~"%(str(N_THQ_gen5_fiducial)[:8],str(N_THQ_gen5_selected)[:8],str(N_THQ_gen5_selected/N_THQ_gen5_fiducial)[:8])
print "~                    ~        THW         ~        %s         ~       %s        ~       %s        ~"%(str(N_THW_gen5_fiducial)[:8],str(N_THW_gen5_selected)[:8],str(N_THW_gen5_selected/N_THW_gen5_fiducial)[:8])
print "~                    ~        tot         ~        %s         ~       %s        ~       %s        ~"%(str(N_tot_gen5_fiducial)[:8],str(N_tot_gen5_selected)[:8],str(N_tot_gen5_selected/N_tot_gen5_fiducial)[:8])
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print ""

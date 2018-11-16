import ROOT
import numpy as np
import math
import sys
from copy import deepcopy
from array import array

#BDT cut
lep_BDT_cut = 0.13

# Systematics calc: outputs line o add to datacard

#User input for signal process
if( len(sys.argv) != 3 ):
  print "Usage: systematics.py <hadronic/leptonic> <systematic>"
  sys.exit(1)
channelID = sys.argv[1]
syst_type = sys.argv[2]


#Define signal chains to read from
chain_ttH_nominal = ROOT.TChain("trilinearTree")
chain_THQ_nominal = ROOT.TChain("trilinearTree")
chain_THW_nominal = ROOT.TChain("trilinearTree")

chain_ttH_syst_up = ROOT.TChain("trilinearTree")
chain_THQ_syst_up = ROOT.TChain("trilinearTree")
chain_THW_syst_up = ROOT.TChain("trilinearTree")

chain_ttH_syst_down = ROOT.TChain("trilinearTree")
chain_THQ_syst_down = ROOT.TChain("trilinearTree")
chain_THW_syst_down = ROOT.TChain("trilinearTree")

#Add relevant files to chains
chain_ttH_nominal.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/btag_correction/systematics/input/ttHLep/nominal/output_ttHLep_ttH_M125.root" )
chain_THQ_nominal.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/btag_correction/systematics/input/ttHLep/nominal/output_ttHLep_THQ_M125_bugged.root" )
chain_THW_nominal.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/btag_correction/systematics/input/ttHLep/nominal/output_ttHLep_THW_M125_bugged.root" )

chain_ttH_syst_up.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/btag_correction/systematics/input/ttHLep/%s/output_ttHLep_ttH_M125_%s_up.root"%(syst_type,syst_type) )
chain_THQ_syst_up.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/btag_correction/systematics/input/ttHLep/%s/output_ttHLep_THQ_M125_%s_up.root"%(syst_type,syst_type) )
chain_THW_syst_up.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/btag_correction/systematics/input/ttHLep/%s/output_ttHLep_THW_M125_%s_up.root"%(syst_type,syst_type) )

chain_ttH_syst_down.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/btag_correction/systematics/input/ttHLep/%s/output_ttHLep_ttH_M125_%s_down.root"%(syst_type,syst_type) )
chain_THQ_syst_down.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/btag_correction/systematics/input/ttHLep/%s/output_ttHLep_THQ_M125_%s_down.root"%(syst_type,syst_type) )
chain_THW_syst_down.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/btag_correction/systematics/input/ttHLep/%s/output_ttHLep_THW_M125_%s_down.root"%(syst_type,syst_type) )

#Create lists of chains
chains_ttH = []
chains_THQ = []
chains_THW = []
chains_ttH.extend([ chain_ttH_nominal, chain_ttH_syst_up, chain_ttH_syst_down ])
chains_THQ.extend([ chain_THQ_nominal, chain_THQ_syst_up, chain_THQ_syst_down ])
chains_THW.extend([ chain_THW_nominal, chain_THW_syst_up, chain_THW_syst_down ])

#Count events in each proc * reco category: first initialise counters
n_cats = 6
n_proc = 6
N_tmp = []
for i in range(0,n_proc):
  x = []
  for j in range(0,n_cats):
    x.append(0.)
  N_tmp.append( x )
N_ttH = []
N_THQ = []
N_THW = []

#Define bin labels
xbin_label = ['lep_reco0','lep_reco0','lep_reco1','lep_reco1','lep_reco2','lep_reco2','lep_reco3','lep_reco3','lep_reco4','lep_reco4','lep_reco5']
ybin_label = ['gen0','gen1','gen2','gen3','gen4','gen5']
 
#Define dict to relate pTH+BDT to correct bin
reco_dict = { 0:[0.,45.,lep_BDT_cut,1.], 1:[45.,80.,lep_BDT_cut,1.], 2:[80.,120.,lep_BDT_cut,1.], 3:[120.,200.,lep_BDT_cut,1.], 4:[200.,350.,lep_BDT_cut,1.], 5:[350.,9999999999999.,lep_BDT_cut,1.] }
gen_dict = { 0:[0.,45.], 1:[45.,80.], 2:[80.,120.], 3:[120.,200.], 4:[200.,350.], 5:[350.,9999999999999.] }

#ttH:
for chain_idx in range( len(chains_ttH) ):
  print "ttH: chain = %g, entries = %g"%(chain_idx,chains_ttH[chain_idx].GetEntries())
  #1) nominal, 2) syst up, 3) syst down
  #Re-set counters
  for i in range(0,n_proc):
    for j in range(0,n_cats):
      N_tmp[i][j] = 0.
  ev_idx = 0
  #Loop over events in chain
  for ev in chains_ttH[ chain_idx ]:

    #Find recobin 
    recobin_found = False
    recobin = -1
    for bin_idx in reco_dict:
      if( not recobin_found ):
        if( ev.pTH_reco > reco_dict[bin_idx][0] )&( ev.pTH_reco <= reco_dict[bin_idx][1] )&( ev.BDT > reco_dict[bin_idx][2] )&( ev.BDT <= reco_dict[bin_idx][3] ): 
          recobin = bin_idx
          recobin_found = True
    #Find genbin
    genbin_found = False
    genbin = -1
    for bin_idx in gen_dict:
      if( not genbin_found ):
        if( ev.pTH_gen > gen_dict[bin_idx][0] )&( ev.pTH_gen <= gen_dict[bin_idx][1] ):
          genbin = bin_idx
          genbin_found = True
    #Add event weight to matrix
    if( genbin != -1 )&( recobin != -1 ):
      N_tmp[genbin][recobin] += ev.weight_LO
      #if( ev_idx % 500 == 0 ): print "chain = %g, event = %g --> pTgen = %4.2f GeV, pTreco = %4.2f, BDT = %4.2f, genbin = %g, recobin = %g"%(chain_idx,ev_idx,ev.pTH_gen,ev.pTH_reco,ev.BDT,genbin,recobin)

  #Push deepcopy back onto N_ttH list
  N_ttH.append( deepcopy(N_tmp) )

syst_ttH_up = (np.array( N_ttH[1] )/np.array( N_ttH[0] )).tolist()
syst_ttH_down = (np.array( N_ttH[2] )/np.array( N_ttH[0] )).tolist()

print "ttH:      N =", N_ttH[0]
print "ttH:   N_up =", N_ttH[1]
print "ttH: N_down =", N_ttH[2]
print "ttH:   %s_up ="%(syst_type), syst_ttH_up
print "ttH: %s_down ="%(syst_type), syst_ttH_down
print ""
##################################################
#THQ:
for chain_idx in range( len(chains_THQ) ):
  print "THQ: chain = %g, entries = %g"%(chain_idx,chains_THQ[chain_idx].GetEntries())
  #1) nominal, 2) syst up, 3) syst down
  #Re-set counters
  for i in range(0,n_proc):
    for j in range(0,n_cats):
      N_tmp[i][j] = 0.
  ev_idx = 0
  #Loop over events in chain
  for ev in chains_THQ[ chain_idx ]:

    #Find recobin 
    recobin_found = False
    recobin = -1
    for bin_idx in reco_dict:
      if( not recobin_found ):
        if( ev.pTH_reco > reco_dict[bin_idx][0] )&( ev.pTH_reco <= reco_dict[bin_idx][1] )&( ev.BDT > reco_dict[bin_idx][2] )&( ev.BDT <= reco_dict[bin_idx][3] ): 
          recobin = bin_idx
          recobin_found = True
    #Find genbin
    genbin_found = False
    genbin = -1
    for bin_idx in gen_dict:
      if( not genbin_found ):
        if( ev.pTH_gen > gen_dict[bin_idx][0] )&( ev.pTH_gen <= gen_dict[bin_idx][1] ):
          genbin = bin_idx
          genbin_found = True
    #Add event weight to matrix
    if( genbin != -1 )&( recobin != -1 ):
      N_tmp[genbin][recobin] += ev.weight_LO

  #Push deepcopy back onto N_ttH list
  N_THQ.append( deepcopy(N_tmp) )

#Calc ratio of up to down
syst_THQ_up = (np.array( N_THQ[1] )/np.array( N_THQ[0] )).tolist()
syst_THQ_down = (np.array( N_THQ[2] )/np.array( N_THQ[0] )).tolist()

print "THQ:      N =", N_THQ[0]
print "THQ:   N_up =", N_THQ[1]
print "THQ: N_down =", N_THQ[2]
print "THQ: %s_up ="%(syst_type), syst_THQ_up
print "THQ: %s_down ="%(syst_type), syst_THQ_down
print ""
##################################################
#THW:
for chain_idx in range( len(chains_THW) ):
  print "THW: chain = %g, entries = %g"%(chain_idx,chains_THW[chain_idx].GetEntries())
  #1) nominal, 2) syst up, 3) syst down
  #Re-set counters
  for i in range(0,n_proc):
    for j in range(0,n_cats):
      N_tmp[i][j] = 0.
  ev_idx = 0
  #Loop over events in chain
  for ev in chains_THW[ chain_idx ]:

    #Find recobin 
    recobin_found = False
    recobin = -1
    for bin_idx in reco_dict:
      if( not recobin_found ):
        if( ev.pTH_reco > reco_dict[bin_idx][0] )&( ev.pTH_reco <= reco_dict[bin_idx][1] )&( ev.BDT > reco_dict[bin_idx][2] )&( ev.BDT <= reco_dict[bin_idx][3] ): 
          recobin = bin_idx
          recobin_found = True
    #Find genbin
    genbin_found = False
    genbin = -1
    for bin_idx in gen_dict:
      if( not genbin_found ):
        if( ev.pTH_gen > gen_dict[bin_idx][0] )&( ev.pTH_gen <= gen_dict[bin_idx][1] ):
          genbin = bin_idx
          genbin_found = True
    #Add event weight to matrix
    if( genbin != -1 )&( recobin != -1 ):
      N_tmp[genbin][recobin] += ev.weight_LO

  #Push deepcopy back onto N_THW list
  N_THW.append( deepcopy(N_tmp) )

#Calc ratio of up to down
syst_THW_up = (np.array( N_THW[1] )/np.array( N_THW[0] )).tolist()
syst_THW_down = (np.array( N_THW[2] )/np.array( N_THW[0] )).tolist()

print "THW:      N =", N_THQ[0]
print "THW:   N_up =", N_THQ[1]
print "THW: N_down =", N_THQ[2]
print "THW: %s_up ="%(syst_type), syst_THW_up
print "THW: %s_down ="%(syst_type), syst_THW_down
print ""
#####################################################

dat_procs = ['VH_gen0_hgg','VH_gen1_hgg','VH_gen2_hgg','VH_gen3_hgg','VH_gen4_hgg','VH_gen5_hgg','tHq_gen3_hgg', 'ttH_gen3_hgg', 'tHq_gen1_hgg', 'tHq_gen5_hgg', 'ggH_gen2_hgg', 'tHq_gen4_hgg', 'tHW_gen3_hgg', 'tHW_gen2_hgg', 'ttH_gen4_hgg', 'ggH_gen3_hgg', 'tHq_gen2_hgg', 'ttH_gen0_hgg', 'ggH_gen4_hgg', 'ttH_gen1_hgg', 'tHW_gen1_hgg', 'ttH_gen2_hgg', 'ggH_gen0_hgg', 'ggH_gen1_hgg', 'tHW_gen0_hgg', 'tHW_gen5_hgg', 'tHq_gen0_hgg', 'ttH_gen5_hgg', 'ggH_gen5_hgg', 'tHW_gen4_hgg', 'bkg_mass']
proc_dict = {'ttH':[syst_ttH_up,syst_ttH_down],'tHq':[syst_THQ_up,syst_THQ_down],'tHW':[syst_THW_up,syst_THW_down]}

cat_line = 'bin '
proc_line = 'process '
syst_line = '%s lnN '%syst_type
for reco_idx in range(0,n_cats):
  for proc in dat_procs: 
  #for gen_idx in range(0,n_proc):
    cat_line += '%s '%('datacard_ttH_differential_'+xbin_label[reco_idx])
    proc_line += '%s '%(proc)
    #get gen bin from process
    if( 'ttH' in proc )|( 'tHq' in proc )|( 'tHW' in proc ):
      gen_idx = int(proc.split("_")[1][-1])
      #get process and look up systematic in dictionary
      processID = proc.split("_")[0]
      if processID in proc_dict.keys():
        up_v = proc_dict[processID][0][gen_idx][reco_idx]
        down_v = proc_dict[processID][1][gen_idx][reco_idx]
        if( np.isnan( up_v ) )|( np.isnan( down_v ) ): syst_line += '- '
        elif( up_v == 1. )&( down_v == 1. ): syst_line += '- '
        elif '%4.3f/%4.3f '%(up_v,down_v) == '1.000/1.000 ': syst_line += '- '
        else:  syst_line += '%4.3f/%4.3f '%(up_v,down_v)
      else: syst_line += 'ERROR '
    else: syst_line += '- '

print ""
print cat_line
print ""
print proc_line
print ""
print syst_line


raw_input("Press Enter to continue...")

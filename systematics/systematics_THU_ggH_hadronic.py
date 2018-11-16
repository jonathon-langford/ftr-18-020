import ROOT
import numpy as np
import math
import sys
from copy import deepcopy
from array import array

#BDT cuts
had_BDT_low = 0.28
had_BDT_high = 0.61

# Systematics calc: outputs line o add to datacard

#User input for signal process
if( len(sys.argv) != 3 ):
  print "Usage: systematics.py <hadronic/leptonic> <systematic>"
  sys.exit(1)
channelID = sys.argv[1]
syst_type = sys.argv[2]


#Define signal chains to read from
chain_ggH_nominal = ROOT.TChain("trilinearTree")
chain_ggH_syst_up = ROOT.TChain("trilinearTree")
chain_ggH_syst_down = ROOT.TChain("trilinearTree")

#Add relevant files to chains
chain_ggH_nominal.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/btag_correction/systematics/input/ttHHad/nominal/output_ttHHad_ggH_M125.root" )
chain_ggH_syst_up.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/btag_correction/systematics/input/ttHHad/%s/output_ttHHad_ggH_M125_%s_up.root"%(syst_type,syst_type) )
chain_ggH_syst_down.Add( "/vols/build/cms/jl2117/trilinear/CMSSW_8_1_0/src/triFinalFit/btag_correction/systematics/input/ttHHad/%s/output_ttHHad_ggH_M125_%s_down.root"%(syst_type,syst_type) )

#Create lists of chains
chains_ggH = []
chains_ggH.extend([ chain_ggH_nominal, chain_ggH_syst_up, chain_ggH_syst_down ])

#Count events in each proc * reco category: first initialise counters
n_cats = 11
n_proc = 6
N_tmp = []
for i in range(0,n_proc):
  x = []
  for j in range(0,n_cats):
    x.append(0.)
  N_tmp.append( x )
N_ggH = []
 
#Define bin labels
xbin_label = ['reco0_BDTa','reco0_BDTb','reco1_BDTa','reco1_BDTb','reco2_BDTa','reco2_BDTb','reco3_BDTa','reco3_BDTb','reco4_BDTa','reco4_BDTb','reco5']
ybin_label = ['gen0','gen1','gen2','gen3','gen4','gen5']

#Define dict to relate pTH+BDT to correct bin
reco_dict = { 0:[0.,45.,had_BDT_high,1.], 1:[0.,45.,had_BDT_low,had_BDT_high], 2:[45.,80.,had_BDT_high,1.], 3:[45.,80.,had_BDT_low,had_BDT_high],4:[80.,120.,had_BDT_high,1.], 5:[80.,120.,had_BDT_low,had_BDT_high],6:[120.,200.,had_BDT_high,1.], 7:[120.,200.,had_BDT_low,had_BDT_high],8:[200.,350.,had_BDT_high,1.], 9:[200.,350.,had_BDT_low,had_BDT_high], 10:[350.,9999999999999.,had_BDT_low,1.] }
gen_dict = { 0:[0.,45.], 1:[45.,80.], 2:[80.,120.], 3:[120.,200.], 4:[200.,350.], 5:[350.,9999999999999.] }

##################################################
#ggH:
for chain_idx in range( len(chains_ggH) ):
  print "ggH: chain = %g, entries = %g"%(chain_idx,chains_ggH[chain_idx].GetEntries())
  #1) nominal, 2) syst up, 3) syst down
  #Re-set counters
  for i in range(0,n_proc):
    for j in range(0,n_cats):
      N_tmp[i][j] = 0.
  ev_idx = 0
  #Loop over events in chain
  for ev in chains_ggH[ chain_idx ]:

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
  N_ggH.append( deepcopy(N_tmp) )

#Calc ratio of up to down
syst_ggH_up = (np.array( N_ggH[1] )/np.array( N_ggH[0] )).tolist()
syst_ggH_down = (np.array( N_ggH[2] )/np.array( N_ggH[0] )).tolist()


#print "ggH:      N =", N_ggH[0]
#print "ggH:   N_up =", N_ggH[1]
#print "ggH: N_down =", N_ggH[2]
#print "ggH:   %s_up ="%(syst_type), syst_ggH_up
#print "ggH: %s_down ="%(syst_type), syst_ggH_down
#print ""
i########################################################################################

dat_procs = ['VH_gen0_hgg','VH_gen1_hgg','VH_gen2_hgg','VH_gen3_hgg','VH_gen4_hgg','VH_gen5_hgg','tHq_gen3_hgg', 'ttH_gen3_hgg', 'tHq_gen1_hgg', 'tHq_gen5_hgg', 'ggH_gen2_hgg', 'tHq_gen4_hgg', 'tHW_gen3_hgg', 'tHW_gen2_hgg', 'ttH_gen4_hgg', 'ggH_gen3_hgg', 'tHq_gen2_hgg', 'ttH_gen0_hgg', 'ggH_gen4_hgg', 'ttH_gen1_hgg', 'tHW_gen1_hgg', 'ttH_gen2_hgg', 'ggH_gen0_hgg', 'ggH_gen1_hgg', 'tHW_gen0_hgg', 'tHW_gen5_hgg', 'tHq_gen0_hgg', 'ttH_gen5_hgg', 'ggH_gen5_hgg', 'tHW_gen4_hgg', 'bkg_mass']
proc_dict = {'ggH':[syst_ggH_up,syst_ggH_down]}

cat_line = 'bin '
proc_line = 'process '
syst_line = '%s lnN '%syst_type
for reco_idx in range(0,n_cats):
  for proc in dat_procs: 
  #for gen_idx in range(0,n_proc):
    cat_line += '%s '%('datacard_ttH_differential_'+xbin_label[reco_idx])
    proc_line += '%s '%(proc)
    #get gen bin from process
    if( 'ggH' in proc ):
      gen_idx = int(proc.split("_")[1][-1])
      #get process and look up systematic in dictionary
      processID = proc.split("_")[0]
      if processID in proc_dict.keys():
        up_v = proc_dict[processID][0][gen_idx][reco_idx]
        down_v = proc_dict[processID][1][gen_idx][reco_idx]
        if( np.isnan( up_v ) )|( np.isnan( down_v ) ): syst_line += '- '
        elif( up_v == 1. )&( down_v == 1. ): syst_line += '- '
        else:  syst_line += '%4.3f/%4.3f '%(up_v,down_v)
      else: syst_line += 'X '
    else: syst_line += '- '

#print ""
#print cat_line
#print ""
#print proc_line
print ""
print syst_line


#raw_input("Press Enter to continue...")

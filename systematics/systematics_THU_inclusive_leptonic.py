import ROOT
import numpy as np
import math
import sys
from copy import deepcopy
from array import array

dat_procs = ['VH_gen0_hgg','VH_gen1_hgg','VH_gen2_hgg','VH_gen3_hgg','VH_gen4_hgg','VH_gen5_hgg','tHq_gen3_hgg', 'ttH_gen3_hgg', 'tHq_gen1_hgg', 'tHq_gen5_hgg', 'ggH_gen2_hgg', 'tHq_gen4_hgg', 'tHW_gen3_hgg', 'tHW_gen2_hgg', 'ttH_gen4_hgg', 'ggH_gen3_hgg', 'tHq_gen2_hgg', 'ttH_gen0_hgg', 'ggH_gen4_hgg', 'ttH_gen1_hgg', 'tHW_gen1_hgg', 'ttH_gen2_hgg', 'ggH_gen0_hgg', 'ggH_gen1_hgg', 'tHW_gen0_hgg', 'tHW_gen5_hgg', 'tHq_gen0_hgg', 'ttH_gen5_hgg', 'ggH_gen5_hgg', 'tHW_gen4_hgg', 'bkg_mass']

n_cats = 6

for syst_type in ['THU_QCDscale_inc','THU_PDF_inc','THU_alpha_inc']:

  syst_line = '%s lnN '%syst_type

  for reco_idx in range(0,n_cats):
    for proc in dat_procs: 
      if( 'VH' in proc ):
        if syst_type == 'THU_QCDscale_inc': syst_line += '1.015/0.987 '
        elif syst_type == 'THU_PDF_inc': syst_line += '1.011/0.989 '
        elif syst_type == 'THU_alpha_inc': syst_line += '1.007/0.993 '
      elif( 'ttH' in proc ):
        if syst_type == 'THU_QCDscale_inc': syst_line += '1.060/0.908 '
        elif syst_type == 'THU_PDF_inc': syst_line += '1.029/0.971 '
        elif syst_type == 'THU_alpha_inc': syst_line += '1.019/0.981 '
      elif( 'tHq' in proc ):
        if syst_type == 'THU_QCDscale_inc': syst_line += '1.064/0.853 '
        elif syst_type == 'THU_PDF_inc': syst_line += '1.034/0.966 '
        elif syst_type == 'THU_alpha_inc': syst_line += '1.012/0.988 '
      elif( 'tHW' in proc ):
        if syst_type == 'THU_QCDscale_inc': syst_line += '1.050/0.931 '
        elif syst_type == 'THU_PDF_inc': syst_line += '1.060/0.940 '
        elif syst_type == 'THU_alpha_inc': syst_line += '1.015/0.985 '
      else: syst_line += '- '

  print ""
  print syst_line

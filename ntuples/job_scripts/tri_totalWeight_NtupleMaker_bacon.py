#!/usr/bin/env python

# Author: Jonathon Langford
#         Imperial College London
#         CMS, Hgg IC group

# Description: To perform trilinear analysis on ttHHadronic tagged events for signal samples
###############################################################################
#	PRELIMINARIES

#Import Libraries
import sys
import ROOT
import math
from array import array
from optparse import OptionParser

def get_options():
  parser = OptionParser()
  parser = OptionParser( usage="usage: python %prog [input file] [signal type]" )
  parser.add_option("-i", "--inp", dest="input_file", default='', help="Input file to analyse")
  parser.add_option("-s", "--signal", dest="signal", default='ttH', help="Define which signal process running over, for correct XS")
  parser.add_option("-u","--systematic", dest="systematic", default='JES', help="Define which systematic uncertainty")
  parser.add_option("-d","--direction",dest="direction", default='up',help="[UP/DOWN]")
  return parser.parse_args()

(opt,args) = get_options()
f_input = opt.input_file
signal_type = opt.signal
syst_type = opt.systematic
syst_direction = opt.direction

#Extract number from output file: remove ".root" 
f_split = f_input.split("_")
nOut = "ERROR"
if( f_split[-2].isdigit() ):
  nOut = f_split[-2] + "_" + f_split[-1][:-5]
else:
  nOut = f_split[-1][:-5]

#Load delphes ROOT libraries
ROOT.gSystem.Load("libDelphes")

#Including packages to read TTree
try:
  ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
  ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
except:
  pass

# Create chain of root trees
chain = ROOT.TChain("Delphes")
chain.Add( f_input )

# Create objects of class ExRootTreeReader
treeReader = ROOT.ExRootTreeReader(chain)
numberOfEntries = treeReader.GetEntries()
#numberOfEntries = 100

# Get pointers to branches used in this analysis
branchEvent = treeReader.UseBranch("Event")
branchWeight = treeReader.UseBranch("Weight")

#Define cross sections [fb] for various processes and uncomment required one
#also calc total weight (check == numberOfEntries)
if( signal_type == "ttH" ):
  Xsection = 1.393
  totalWeight = 61505.9956

elif( signal_type == "THQ" ):
  Xsection = 0.212
  totalWeight = 1906318

elif( signal_type == "THW" ):
  Xsection = 0.0421
  totalWeight = 817000
##############################################################################
#	CONFIGURE OUTPUT

print "Configuring output Ntuple..."
# Initialise TTree and open files to write to
w_nominal = array( 'f', [-1.] )
w_reweighted = array( 'f', [-1.] )
w_nominal_XSscaled = array( 'f', [-1.] )
w_reweighted_XSscaled = array( 'f', [-1.] )

if( signal_type == "ttH" ): filename = "tri_ntuples_totalWeight/" + syst_type + "/ttH/ttH_" + nOut  + "_" + syst_direction +".root"
elif( signal_type == "THQ" ): filename = "tri_ntuples_totalWeight/" + syst_type + "/THQ/THQ_" + nOut  + "_" + syst_direction + ".root"
elif( signal_type == "THW" ): filename = "tri_ntuples_totalWeight/" + syst_type + "/THW/THW_" + nOut  + "_" + syst_direction + ".root"

f_0 = ROOT.TFile.Open( filename ,"RECREATE")
tree_0 = ROOT.TTree("trilinearTree","trilinearTree")

tree_0.Branch("w_nominal", w_nominal, 'w_nominal/F')
tree_0.Branch("w_reweighted", w_reweighted, 'w_reweighted/F')
tree_0.Branch("w_nominal_XSscaled", w_nominal_XSscaled, 'w_nominal_XSscaled/F')
tree_0.Branch("w_reweighted_XSscaled", w_reweighted_XSscaled, 'w_reweighted_XSscaled/F')


###############################################################################
#For systematic use correct weight ID
w_ID = -1
if( syst_type == "factor" ):
  if( syst_direction == "up" ): w_ID = 1
  else: w_ID = 2
elif( syst_type == "renorm" ):
  if( syst_direction == "up" ): w_ID = 3
  else: w_ID = 6

#	EVENTS LOOP

# Loop over all events
for entry in range(0, numberOfEntries ):
 
  # Load selected branches with data from specified event
  treeReader.ReadEntry(entry)
  w_nominal[0] = branchEvent.At(0).Weight
  if( branchWeight.At(0).Weight == 0 ): 
    w_reweighted[0] = w_nominal[0]
  elif( (branchWeight.At(w_ID).Weight/branchWeight.At(0).Weight) > 2. )|( (branchWeight.At(w_ID).Weight/branchWeight.At(0).Weight) < 0. ):
    w_reweighted[0] = w_nominal[0]
  else:
    w_reweighted[0] = w_nominal[0]*(branchWeight.At(w_ID).Weight/branchWeight.At(0).Weight)
  w_nominal_XSscaled[0] = (branchEvent.At(0).Weight/totalWeight)*Xsection
  if( branchWeight.At(0).Weight == 0 ): 
    w_reweighted_XSscaled[0] = w_nominal_XSscaled[0]
  else:
    w_reweighted_XSscaled[0] = w_nominal_XSscaled[0]*(branchWeight.At(w_ID).Weight/branchWeight.At(0).Weight)
  
  tree_0.Fill()

#END OF EVENT LOOP
##############################################################################
f_0.Write()
f_0.Close()

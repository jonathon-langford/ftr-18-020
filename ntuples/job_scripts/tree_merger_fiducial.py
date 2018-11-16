#!/usr/bin/env python

import sys
import ROOT
import math
from array import array

if len(sys.argv) != 2:
  print "Usage: python tree_merger_GEN_acceptance.py <processID>"
  sys.exit(1)

processID = sys.argv[1]

Nmerge = 1
if( processID == 'ttH' ): Nmerge = 103
elif( processID == 'ggH' ): Nmerge = 56
elif( processID == 'THQ' ): Nmerge = 44
elif( processID == 'THW' ): Nmerge = 36

print "Merging: processID = %s"%(processID)

# Create chain of root trees
chain = ROOT.TChain("trilinearTree")

baseName = "ttHHad_tri_ntuples_signal/gen_acceptance/%s/%s_"%(processID,processID)
output_file = "ttHHad_tri_ntuples_signal/gen_acceptance/%s_fiducial.root"%(processID)
for fileNum in range(1,Nmerge):
  if( processID == 'THQ' ):
    fileName = "%s%g.root"%(baseName,fileNum)
    fileNameb = "%s%gb.root"%(baseName,fileNum)
    chain.Add( fileName )
    chain.Add( fileNameb )
  else:
    fileName = "%s%g.root"%(baseName,fileNum)
    chain.Add( fileName )

print "  entries =", chain.GetEntries()

print "  configuring combined ntuple..."
#Initialise ttree and open files to write to
#Main variables
pTH_gen_v = array( 'f', [-1.] )
LO_w = array( 'f', [-1.] )

#Open .root file to write combined ttree to
f_0 = ROOT.TFile.Open( output_file ,"RECREATE")
tree_0 = ROOT.TTree("trilinearTree","trilinearTree_0")

tree_0.Branch("pTH_gen", pTH_gen_v, 'pTH_gen/F')
tree_0.Branch("weight_LO", LO_w, 'weight_LO/F')

###############################################################################

#EVENTS LOOP
for event in chain:
  pTH_gen_v[0] = event.pTH_gen
  LO_w[0] = event.weight_LO

  tree_0.Fill()

f_0.Write()
f_0.Close()

raw_input("Press Enter to continue...")

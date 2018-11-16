#!/usr/bin/env python

import sys
import ROOT
import math
from array import array

# Create chain of root trees
chain = ROOT.TChain("trilinearTree")

if len( sys.argv ) < 4:
  print "Usage: python tree_merger_totalWeight.py <processID> <systematic> <direction>"
processID = sys.argv[1]
syst_type = sys.argv[2]
syst_direction = sys.argv[3]

Nmerge = 1
if( processID == 'ttH' ): Nmerge = 103
elif( processID == 'ggH' ): Nmerge = 56
elif( processID == 'THQ' ): Nmerge = 44
elif( processID == 'THW' ): Nmerge = 36
elif( processID == "VH" ): Nmerge = 38

print ""
print "processID = %s, systematic = %s, direction = %s"%(processID,syst_type,syst_direction)

baseName = "tri_ntuples_totalWeight/%s/%s/%s_"%(syst_type,processID,processID)
output_file = "tri_ntuples_totalWeight/%s/totalWeight_%s_M125_%s_%s.root"%(syst_type,processID,syst_type,syst_direction)
for fileNum in range(1,Nmerge):
  if( processID == 'THQ' ):
    fileName = "%s%g_%s.root"%(baseName,fileNum,syst_direction)
    fileNameb = "%s%gb_%s.root"%(baseName,fileNum,syst_direction)
    chain.Add( fileName )
    chain.Add( fileNameb )
  else:
    fileName = "%s%g_%s.root"%(baseName,fileNum,syst_direction)
    chain.Add( fileName )

print "ENTRIES =", chain.GetEntries()

print "Configuring combined ntuple..."
w_nominal = array( 'f', [-1.] )
w_reweighted = array( 'f', [-1.] )
w_nominal_XSscaled = array( 'f', [-1.] )
w_reweighted_XSscaled = array( 'f', [-1.] )

#Open .root file to write combined ttree to
f_0 = ROOT.TFile.Open( output_file ,"RECREATE")
tree_0 = ROOT.TTree("trilinearTree","trilinearTree_0")

tree_0.Branch("w_nominal", w_nominal, 'w_nominal/F')
tree_0.Branch("w_reweighted", w_reweighted, 'w_reweighted/F')
tree_0.Branch("w_nominal_XSscaled", w_nominal_XSscaled, 'w_nominal_XSscaled/F')
tree_0.Branch("w_reweighted_XSscaled", w_reweighted_XSscaled, 'w_reweighted_XSscaled/F')
###############################################################################

#EVENTS LOOP
for event in chain:
  
  w_nominal[0] = event.w_nominal
  w_reweighted[0] = event.w_reweighted
  w_nominal_XSscaled[0] = event.w_nominal_XSscaled
  w_reweighted_XSscaled[0] = event.w_reweighted_XSscaled

  tree_0.Fill()

f_0.Write()
f_0.Close()

#raw_input("Press Enter to continue...")

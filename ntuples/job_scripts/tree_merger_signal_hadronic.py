#!/usr/bin/env python

import sys
import ROOT
import math
from array import array

if len( sys.argv ) < 2:
  print "Usage: python tree_merger_signal.py <processID>"
processID = sys.argv[1]

Nmerge = 1
if( processID == 'ttH' ): Nmerge = 103
elif( processID == 'ggH' ): Nmerge = 56
elif( processID == 'THQ' ): Nmerge = 44
elif( processID == 'THW' ): Nmerge = 36
elif( processID == "VH" ): Nmerge = 38

print "Merging: processID = %s"%(processID)

# Create chain of root trees
chain = ROOT.TChain("trilinearTree")

baseName = "ttHHad_tri_ntuples_signal/%s/%s_"%(processID,processID)
output_file = "ttHHad_tri_ntuples_signal/ttHHad_signal_%s_M125_bugged.root"%processID
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
pTH_reco_v = array( 'f', [-1.] )
mgg_v = array( 'f', [-1.] )
LO_w = array( 'f', [-1.] )
#Reco photon variables
pho1_pT = array( 'f', [-1.] )
pho1_eta = array( 'f', [-1.] )
pho1_phi = array( 'f', [-1.] )
pho1_E = array( 'f', [-1.] )
pho1_IsolationVar = array( 'f', [-1.] )
pho2_pT = array( 'f', [-1.] )
pho2_eta = array( 'f', [-1.] )
pho2_phi = array( 'f', [-1.] )
pho2_E = array( 'f', [-1.] )
pho2_IsolationVar = array( 'f', [-1.] )
#Gen photon variables
pho1_gen_pT = array( 'f', [-1.] )
pho1_gen_eta = array( 'f', [-1.] )
pho1_gen_phi = array( 'f', [-1.] )
pho1_gen_E = array( 'f', [-1.] )
pho2_gen_pT = array( 'f', [-1.] )
pho2_gen_eta = array( 'f', [-1.] )
pho2_gen_phi = array( 'f', [-1.] )
pho2_gen_E = array( 'f', [-1.] )
#First six jets info
jet1_pT = array( 'f', [-1.] )
jet1_eta = array( 'f', [-1.] )
jet1_phi = array( 'f', [-1.] )
jet1_mass = array( 'f', [-1.] )
jet1_btag = array( 'i', [-1] )
jet1_inTop = array( 'i', [-1] )
jet2_pT = array( 'f', [-1.] )
jet2_eta = array( 'f', [-1.] )
jet2_phi = array( 'f', [-1.] )
jet2_mass = array( 'f', [-1.] )
jet2_btag = array( 'i', [-1] )
jet2_inTop = array( 'i', [-1] )
jet3_pT = array( 'f', [-1.] )
jet3_eta = array( 'f', [-1.] )
jet3_phi = array( 'f', [-1.] )
jet3_mass = array( 'f', [-1.] )
jet3_btag = array( 'i', [-1] )
jet3_inTop = array( 'i', [-1] )
jet4_pT = array( 'f', [-1.] )
jet4_eta = array( 'f', [-1.] )
jet4_phi = array( 'f', [-1.] )
jet4_mass = array( 'f', [-1.] )
jet4_btag = array( 'i', [-1] )
jet4_inTop = array( 'i', [-1] )
jet5_pT = array( 'f', [-1.] )
jet5_eta = array( 'f', [-1.] )
jet5_phi = array( 'f', [-1.] )
jet5_mass = array( 'f', [-1.] )
jet5_btag = array( 'i', [-1] )
jet5_inTop = array( 'i', [-1] )
jet6_pT = array( 'f', [-1.] )
jet6_eta = array( 'f', [-1.] )
jet6_phi = array( 'f', [-1.] )
jet6_mass = array( 'f', [-1.] )
jet6_btag = array( 'i', [-1] )
jet6_inTop = array( 'i', [-1] )
#Global jet variables
Njets = array( 'i', [0] )
Nbjets = array( 'i', [0] )
#Other
MET = array( 'f', [-1.] )
MET_eta = array( 'f', [-1.] )
MET_phi = array( 'f', [-1.] )
scalarHT = array( 'f', [-1.] )

#Open .root file to write combined ttree to
f_0 = ROOT.TFile.Open( output_file ,"RECREATE")
tree_0 = ROOT.TTree("trilinearTree","trilinearTree_0")

tree_0.Branch("pTH_gen", pTH_gen_v, 'pTH_gen/F')
tree_0.Branch("pTH_reco", pTH_reco_v, 'pTH_reco/F')
tree_0.Branch("mgg", mgg_v, 'mgg/F')
tree_0.Branch("weight_LO", LO_w, 'weight_LO/F')
#Reco photon info
tree_0.Branch("pho1_pT", pho1_pT, 'pho1_pT/F')
tree_0.Branch("pho1_eta", pho1_eta, 'pho1_eta/F')
tree_0.Branch("pho1_phi", pho1_phi, 'pho1_phi/F')
tree_0.Branch("pho1_E", pho1_E, 'pho1_E/F')
tree_0.Branch("pho1_IsolationVar", pho1_IsolationVar, 'pho1_IsolationVar/F')
tree_0.Branch("pho2_pT", pho2_pT, 'pho2_pT/F')
tree_0.Branch("pho2_eta", pho2_eta, 'pho2_eta/F')
tree_0.Branch("pho2_phi", pho2_phi, 'pho2_phi/F')
tree_0.Branch("pho2_E", pho2_E, 'pho2_E/F')
tree_0.Branch("pho2_IsolationVar", pho2_IsolationVar, 'pho2_IsolationVar/F')
#Gen photon info
tree_0.Branch("pho1_gen_pT", pho1_gen_pT, 'pho1_gen_pT/F')
tree_0.Branch("pho1_gen_eta", pho1_gen_eta, 'pho1_gen_eta/F')
tree_0.Branch("pho1_gen_phi", pho1_gen_phi, 'pho1_gen_phi/F')
tree_0.Branch("pho1_gen_E", pho1_gen_E, 'pho1_gen_E/F')
tree_0.Branch("pho2_gen_pT", pho2_gen_pT, 'pho2_gen_pT/F')
tree_0.Branch("pho2_gen_eta", pho2_gen_eta, 'pho2_gen_eta/F')
tree_0.Branch("pho2_gen_phi", pho2_gen_phi, 'pho2_gen_phi/F')
tree_0.Branch("pho2_gen_E", pho2_gen_E, 'pho2_gen_E/F')
#First six jet into
tree_0.Branch("jet1_pT", jet1_pT, 'jet1_pT/F')
tree_0.Branch("jet1_eta", jet1_eta, 'jet1_eta/F')
tree_0.Branch("jet1_phi", jet1_phi, 'jet1_phi/F')
tree_0.Branch("jet1_mass", jet1_mass, 'jet1_mass/F')
tree_0.Branch("jet1_btag", jet1_btag, 'jet1_btag/I')
tree_0.Branch("jet1_inTop", jet1_inTop, 'jet1_inTop/I')
tree_0.Branch("jet2_pT", jet2_pT, 'jet2_pT/F')
tree_0.Branch("jet2_eta", jet2_eta, 'jet2_eta/F')
tree_0.Branch("jet2_phi", jet2_phi, 'jet2_phi/F')
tree_0.Branch("jet2_mass", jet2_mass, 'jet2_mass/F')
tree_0.Branch("jet2_btag", jet2_btag, 'jet2_btag/I')
tree_0.Branch("jet2_inTop", jet2_inTop, 'jet2_inTop/I')
tree_0.Branch("jet3_pT", jet3_pT, 'jet3_pT/F')
tree_0.Branch("jet3_eta", jet3_eta, 'jet3_eta/F')
tree_0.Branch("jet3_phi", jet3_phi, 'jet3_phi/F')
tree_0.Branch("jet3_mass", jet3_mass, 'jet3_mass/F')
tree_0.Branch("jet3_btag", jet3_btag, 'jet3_btag/I')
tree_0.Branch("jet3_inTop", jet3_inTop, 'jet3_inTop/I')
tree_0.Branch("jet4_pT", jet4_pT, 'jet4_pT/F')
tree_0.Branch("jet4_eta", jet4_eta, 'jet4_eta/F')
tree_0.Branch("jet4_phi", jet4_phi, 'jet4_phi/F')
tree_0.Branch("jet4_mass", jet4_mass, 'jet4_mass/F')
tree_0.Branch("jet4_btag", jet4_btag, 'jet4_btag/I')
tree_0.Branch("jet4_inTop", jet4_inTop, 'jet4_inTop/I')
tree_0.Branch("jet5_pT", jet5_pT, 'jet5_pT/F')
tree_0.Branch("jet5_eta", jet5_eta, 'jet5_eta/F')
tree_0.Branch("jet5_phi", jet5_phi, 'jet5_phi/F')
tree_0.Branch("jet5_mass", jet5_mass, 'jet5_mass/F')
tree_0.Branch("jet5_btag", jet5_btag, 'jet5_btag/I')
tree_0.Branch("jet5_inTop", jet5_inTop, 'jet5_inTop/I')
tree_0.Branch("jet6_pT", jet6_pT, 'jet6_pT/F')
tree_0.Branch("jet6_eta", jet6_eta, 'jet6_eta/F')
tree_0.Branch("jet6_phi", jet6_phi, 'jet6_phi/F')
tree_0.Branch("jet6_mass", jet6_mass, 'jet6_mass/F')
tree_0.Branch("jet6_btag", jet6_btag, 'jet6_btag/I')
tree_0.Branch("jet6_inTop", jet6_inTop, 'jet6_inTop/I')
#Global jet variables
tree_0.Branch("Njets", Njets, 'Njets/I')
tree_0.Branch("Nbjets", Nbjets, 'Nbjets/I')
#Other
tree_0.Branch("MET", MET, 'MET/F')
tree_0.Branch("MET_eta", MET_eta, 'MET_eta/F')
tree_0.Branch("MET_phi", MET_phi, 'MET_phi/F')
tree_0.Branch("scalarHT", scalarHT, 'scalarHT/F')

###############################################################################

#EVENTS LOOP
for event in chain:
  pTH_gen_v[0] = event.pTH_gen
  pTH_reco_v[0] = event.pTH_reco
  mgg_v[0] = event.mgg
  LO_w[0] = event.weight_LO
  pho1_pT[0] = event.pho1_pT
  pho1_eta[0] = event.pho1_eta
  pho1_phi[0] = event.pho1_phi
  pho1_E[0] = event.pho1_E
  pho1_IsolationVar[0] = event.pho1_IsolationVar
  pho2_pT[0] = event.pho2_pT
  pho2_eta[0] = event.pho2_eta
  pho2_phi[0] = event.pho2_phi
  pho2_E[0] = event.pho2_E
  pho2_IsolationVar[0] = event.pho2_IsolationVar
  pho1_gen_pT[0] = event.pho1_gen_pT
  pho1_gen_eta[0] = event.pho1_gen_eta
  pho1_gen_phi[0] = event.pho1_gen_phi
  pho1_gen_E[0] = event.pho1_gen_E
  pho2_gen_pT[0] = event.pho2_gen_pT
  pho2_gen_eta[0] = event.pho2_gen_eta
  pho2_gen_phi[0] = event.pho2_gen_phi
  pho2_gen_E[0] = event.pho2_gen_E
  #jet variables
  jet1_pT[0] = event.jet1_pT
  jet1_eta[0] = event.jet1_eta
  jet1_phi[0] = event.jet1_phi
  jet1_mass[0] = event.jet1_mass
  jet1_btag[0] = event.jet1_btag
  jet1_inTop[0] = event.jet1_inTop
  jet2_pT[0] = event.jet2_pT
  jet2_eta[0] = event.jet2_eta
  jet2_phi[0] = event.jet2_phi
  jet2_mass[0] = event.jet2_mass
  jet2_btag[0] = event.jet2_btag
  jet2_inTop[0] = event.jet2_inTop
  jet3_pT[0] = event.jet3_pT
  jet3_eta[0] = event.jet3_eta
  jet3_phi[0] = event.jet3_phi
  jet3_mass[0] = event.jet3_mass
  jet3_btag[0] = event.jet3_btag
  jet3_inTop[0] = event.jet3_inTop
  jet4_pT[0] = event.jet4_pT
  jet4_eta[0] = event.jet4_eta
  jet4_phi[0] = event.jet4_phi
  jet4_mass[0] = event.jet4_mass
  jet4_btag[0] = event.jet4_btag
  jet4_inTop[0] = event.jet4_inTop
  jet5_pT[0] = event.jet5_pT
  jet5_eta[0] = event.jet5_eta
  jet5_phi[0] = event.jet5_phi
  jet5_mass[0] = event.jet5_mass
  jet5_btag[0] = event.jet5_btag
  jet5_inTop[0] = event.jet5_inTop
  jet6_pT[0] = event.jet6_pT
  jet6_eta[0] = event.jet6_eta
  jet6_phi[0] = event.jet6_phi
  jet6_mass[0] = event.jet6_mass
  jet6_btag[0] = event.jet6_btag
  jet6_inTop[0] = event.jet6_inTop
  #Global jet variables
  Njets[0] = event.Njets
  Nbjets[0] = event.Nbjets
  #Other variables
  MET[0] = event.MET
  MET_eta[0] = event.MET_eta
  MET_phi[0] = event.MET_phi
  scalarHT[0] = event.scalarHT

  tree_0.Fill()

f_0.Write()
f_0.Close()

#!/usr/bin/env python

import sys
import ROOT
import math
from array import array

if len( sys.argv ) < 2:
  print "Usage: python tree_merger_background.py <processID>"
processID = sys.argv[1]

#Load delphes ROOT libraries
ROOT.gSystem.Load("libDelphes")

Nmerge = 1
if( processID == 'gg' ): Nmerge = 365 
elif( processID == 'gjet' ): Nmerge = 111
elif( processID == 'tgjet' ): Nmerge = 37
elif( processID == 'ttbar' ): Nmerge = 3750
elif( processID == "ttgamma_hadronic" ): Nmerge = 236 
elif( processID == "ttgamma_singlelepfromt" ): Nmerge = 226
elif( processID == "ttgamma_singlelepfromtbar" ): Nmerge = 182
elif( processID == "ttgamma_dilepton" ): Nmerge = 439
elif( processID == "ttgammagamma" ): Nmerge = 69

print "Merging: processID = %s"%(processID)

# Create chain of root trees
chain = ROOT.TChain("trilinearTree")

if( processID[0:8] == "ttgamma_" ):
  baseName = "ttHHad_tri_ntuples_background/ttgamma/%s_"%processID
else:
  baseName = "ttHHad_tri_ntuples_background/%s/%s_"%(processID,processID)

if( processID == "gg" ): output_file = "ttHHad_tri_ntuples_background/ttHHad_background_DiPhotonJetsBox_MGG-80toInf.root"
elif( processID == "gjet" ): output_file = "ttHHad_tri_ntuples_background/ttHHad_background_GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf.root"
elif( processID == "tgjet" ): output_file = "ttHHad_tri_ntuples_background/ttHHad_background_TGJet_inclusive.root"
else: output_file = "ttHHad_tri_ntuples_background/ttHHad_background_%s.root"%processID

for fileNum in range(1,Nmerge):
  if( processID == 'gg' )|( processID == 'ttgamma_singlelepfromt' )|( processID == 'ttgamma_singlelepfromtbar' )|( processID == 'ttgamma_hadronic' )|( processID == 'ttgamma_dilepton' )|( processID == 'ttbar' ):
    fileName_0 = "%s%g_0.root"%(baseName,fileNum)
    fileName_1 = "%s%g_1.root"%(baseName,fileNum)
    chain.Add( fileName_0 )
    chain.Add( fileName_1 )
  elif( processID == 'tgjet' )|( processID == 'ttgammagamma' ):
    fileName_0 = "%s%g_0.root"%(baseName,fileNum)
    chain.Add( fileName_0 )
  else:
    fileName = "%s%g.root"%(baseName,fileNum)
    chain.Add( fileName )

print "  entries =", chain.GetEntries()

print "  configuring combined ntuple..."
#Initialise ttree and open files to write to
#Main variables
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

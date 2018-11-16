#!/usr/bin/env python

import sys
import ROOT
import math
from array import array

# Create chain of root trees
chain = ROOT.TChain("trilinearTree")

if len( sys.argv ) < 4:
  print "Usage: python tree_merger_syst_ttHLep.py <processID> <systematic> <direction>"
processID = sys.argv[1]
syst_type = sys.argv[2]
syst_direction = sys.argv[3]

Nmerge = 1
if( processID == 'ttH' ): Nmerge = 103
elif( processID == 'ggH' ): Nmerge = 56
elif( processID == 'THQ' ): Nmerge = 44
elif( processID == 'THW' ): Nmerge = 36
elif( processID == 'VH' ): Nmerge = 38


print ""
print "processID = %s, systematic = %s, direction = %s"%(processID,syst_type,syst_direction)

baseName = "ttHLep_tri_ntuples_syst/%s/%s/%s_"%(syst_type,processID,processID)
output_file = "ttHLep_tri_ntuples_syst/%s/ttHLep_syst_%s_M125_%s_%s.root"%(syst_type,processID,syst_type,syst_direction)
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
jet2_pT = array( 'f', [-1.] )
jet2_eta = array( 'f', [-1.] )
jet2_phi = array( 'f', [-1.] )
jet2_mass = array( 'f', [-1.] )
jet2_btag = array( 'i', [-1] )
jet3_pT = array( 'f', [-1.] )
jet3_eta = array( 'f', [-1.] )
jet3_phi = array( 'f', [-1.] )
jet3_mass = array( 'f', [-1.] )
jet3_btag = array( 'i', [-1] )
#Global jet variables
Njets = array( 'i', [0] )
Nbjets = array( 'i', [0] )
#Lepton variables
Nleptons = array( 'i', [0] )
lep_pT = array( 'f', [-1.] )
lep_eta = array( 'f', [-1.] )
lep_phi = array( 'f', [-1.] )
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
tree_0.Branch("jet2_pT", jet2_pT, 'jet2_pT/F')
tree_0.Branch("jet2_eta", jet2_eta, 'jet2_eta/F')
tree_0.Branch("jet2_phi", jet2_phi, 'jet2_phi/F')
tree_0.Branch("jet2_mass", jet2_mass, 'jet2_mass/F')
tree_0.Branch("jet2_btag", jet2_btag, 'jet2_btag/I')
tree_0.Branch("jet3_pT", jet3_pT, 'jet3_pT/F')
tree_0.Branch("jet3_eta", jet3_eta, 'jet3_eta/F')
tree_0.Branch("jet3_phi", jet3_phi, 'jet3_phi/F')
tree_0.Branch("jet3_mass", jet3_mass, 'jet3_mass/F')
tree_0.Branch("jet3_btag", jet3_btag, 'jet3_btag/I')
#Global jet variables
tree_0.Branch("Njets", Njets, 'Njets/I')
tree_0.Branch("Nbjets", Nbjets, 'Nbjets/I')
#Lepton variables
tree_0.Branch("Nleptons", Nleptons, 'Nleptons/I')
tree_0.Branch("lep_pT", lep_pT, 'lep_pT/F')
tree_0.Branch("lep_eta", lep_eta, 'lep_eta/F')
tree_0.Branch("lep_phi", lep_phi, 'lep_phi/F')
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
  jet2_pT[0] = event.jet2_pT
  jet2_eta[0] = event.jet2_eta
  jet2_phi[0] = event.jet2_phi
  jet2_mass[0] = event.jet2_mass
  jet2_btag[0] = event.jet2_btag
  jet3_pT[0] = event.jet3_pT
  jet3_eta[0] = event.jet3_eta
  jet3_phi[0] = event.jet3_phi
  jet3_mass[0] = event.jet3_mass
  jet3_btag[0] = event.jet3_btag
  #Global jet variables
  Njets[0] = event.Njets
  Nbjets[0] = event.Nbjets
  #Lepton variables
  Nleptons[0] = event.Nleptons
  lep_pT[0] = event.lep_pT
  lep_eta[0] = event.lep_eta
  lep_phi[0] = event.lep_phi
  #Other variables
  MET[0] = event.MET
  MET_eta[0] = event.MET_eta
  MET_phi[0] = event.MET_phi
  scalarHT[0] = event.scalarHT

  tree_0.Fill()

f_0.Write()
f_0.Close()

#raw_input("Press Enter to continue...")

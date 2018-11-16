import sys
import ROOT
import math
from array import array

if len(sys.argv) != 2:
  print "Usage: python BDT_output.py <processID>"
  sys.exit(1)

processID = sys.argv[1]

chain = ROOT.TChain("trilinearTree")

if( processID == 'gg' ):
  chain.Add( "ntuples/ttHLep_background_DiPhotonJetsBox_MGG-80toInf.root")
  f_0 = ROOT.TFile.Open( "output_ttHLep_DiPhotonJetsBox_MGG-80toInf_1fb.root" ,"RECREATE")
elif( processID == 'gjet' ):
  chain.Add( "ntuples/ttHLep_background_GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf.root" )
  f_0 = ROOT.TFile.Open( "output_ttHLep_GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_1fb.root" ,"RECREATE")
elif( processID == 'tgjet' ):
  chain.Add( "ntuples/ttHLep_background_TGJet_inclusive.root" )
  f_0 = ROOT.TFile.Open( "output_ttHLep_TGJet_inclusive_1fb.root" ,"RECREATE")
elif( processID == 'ttbar' ):
  chain.Add( "ntuples/ttHLep_background_ttbar.root" )
  f_0 = ROOT.TFile.Open( "output_ttHLep_ttbar_1fb.root" ,"RECREATE")
elif( processID == 'ttgamma' ):
  chain.Add( "ntuples/ttHLep_background_ttgamma_dilepton.root" )
  chain.Add( "ntuples/ttHLep_background_ttgamma_hadronic.root" )
  chain.Add( "ntuples/ttHLep_background_ttgamma_singlelepfromt.root" )
  chain.Add( "ntuples/ttHLep_background_ttgamma_singlelepfromtbar.root" )
  f_0 = ROOT.TFile.Open( "output_ttHLep_ttgamma_1fb.root" ,"RECREATE")
elif( processID == 'ttgammagamma' ):
  chain.Add( "ntuples/ttHLep_background_ttgammagamma.root" )
  f_0 = ROOT.TFile.Open( "output_ttHLep_ttgammagamma_1fb.root" ,"RECREATE")

#Configure output ntuples
pTH_reco_v = array( 'f', [0.] )
mgg_v = array( 'f', [0.] )
BDT_v = array( 'f', [0.] )
LO_w = array( 'f', [0.] )

tree_0 = ROOT.TTree("trilinearTree","trilinearTree")
tree_0.Branch("pTH_reco", pTH_reco_v, 'pTH_reco/F')
tree_0.Branch("mgg", mgg_v, 'mgg/F')
tree_0.Branch("BDT", BDT_v, 'BDT/F')
tree_0.Branch("weight_LO", LO_w, 'weight_LO/F')

#Book MVA reader
b_weight  = array('f',[0])
b_Njets   = array('f',[0])
b_Nbjets  = array('f',[0])
b_Nleptons  = array('f',[0])
b_scalarHT= array('f',[0])
b_MET     = array('f',[0])
b_mindphi_gg_l = array('f',[0])
b_pho1_ptom     = array('f',[0])
b_pho2_ptom     = array('f',[0])
b_pho1_eta      = array('f',[0])
b_pho2_eta      = array('f',[0])
b_pho1_ch_isolation = array('f',[0])
b_pho2_ch_isolation = array('f',[0])
b_j1_pt        = array('f',[0])
b_j1_eta    = array('f',[0])
b_j2_pt        = array('f',[0])
b_j2_eta       = array('f',[0])
b_j3_pt        = array('f',[0])
b_j3_eta       = array('f',[0])
b_lep_pt        = array('f',[0])
b_lep_eta       = array('f',[0])

tmvaReader_ = ROOT.TMVA.Reader()
tmvaReader_.AddVariable("Njets"  ,b_Njets)
tmvaReader_.AddVariable("Nbjets" ,b_Nbjets)
tmvaReader_.AddVariable("Nleptons" ,b_Nleptons)
tmvaReader_.AddVariable("scalarHT",	b_scalarHT)
tmvaReader_.AddVariable("MET",		b_MET	  )
tmvaReader_.AddVariable("mindphi_gg_l",		b_mindphi_gg_l)
tmvaReader_.AddVariable("pho1_ptom",	b_pho1_ptom)
tmvaReader_.AddVariable("pho2_ptom",	b_pho2_ptom)
tmvaReader_.AddVariable("pho1_eta",	b_pho1_eta)
tmvaReader_.AddVariable("pho2_eta",	b_pho2_eta)
tmvaReader_.AddVariable("pho1_ch_isolation",	b_pho1_ch_isolation)
tmvaReader_.AddVariable("pho2_ch_isolation",	b_pho2_ch_isolation)
tmvaReader_.AddVariable("j1_pt",	b_j1_pt )
tmvaReader_.AddVariable("j1_eta",	b_j1_eta)
tmvaReader_.AddVariable("j2_pt",	b_j2_pt )
tmvaReader_.AddVariable("j2_eta",	b_j2_eta)
tmvaReader_.AddVariable("j3_pt",	b_j3_pt )
tmvaReader_.AddVariable("j3_eta",	b_j3_eta)
tmvaReader_.AddVariable("lep_pt",	b_lep_pt )
tmvaReader_.AddVariable("lep_eta",	b_lep_eta)

tmvaReader_.BookMVA("BDTG","weights/TMVAClassification_BDTG.weights.xml")

for ev in chain:
  #Calc variables
  pt1om = ev.pho1_pT/ev.mgg
  pt2om = ev.pho2_pT/ev.mgg
  #dPhi between diphoton and lead lepton
  pho1 = ROOT.TLorentzVector(); pho1.SetPtEtaPhiE(ev.pho1_pT,ev.pho1_eta,ev.pho1_phi,ev.pho1_E)
  pho2 = ROOT.TLorentzVector(); pho2.SetPtEtaPhiE(ev.pho2_pT,ev.pho2_eta,ev.pho2_phi,ev.pho2_E)
  diphoton = pho1+pho2
  lep_p4 = ROOT.TLorentzVector()
  lep_p4.SetPtEtaPhiM( ev.lep_pT, ev.lep_eta, ev.lep_phi, 0. )
  dPhi_gg_l = diphoton.DeltaPhi( lep_p4 )

  b_weight[0] = ev.weight_LO*3000 # you don't need this for the actual BDT
  b_Njets[0]  = ev.Njets
  b_Nbjets[0]  = ev.Nbjets
  b_Nleptons[0]  = ev.Nleptons
  b_scalarHT[0]    = ev.scalarHT
  b_MET[0]          = ev.MET
  b_mindphi_gg_l[0] = dPhi_gg_l
  b_pho1_ptom[0]     = pt1om
  b_pho2_ptom[0]     = pt2om
  b_pho1_eta[0]      = abs(ev.pho1_eta)
  b_pho2_eta[0]      = abs(ev.pho2_eta)
  b_pho1_ch_isolation[0] = ev.pho1_IsolationVar
  b_pho2_ch_isolation[0] = ev.pho2_IsolationVar
  b_j1_pt[0]        = ev.jet1_pT
  b_j1_eta[0]     = abs(ev.jet1_eta)
  b_j2_pt[0]        = ev.jet2_pT
  b_j2_eta[0]    = abs(ev.jet2_eta)
  b_j3_pt[0]        = ev.jet3_pT
  b_j3_eta[0]    = abs(ev.jet3_eta)
  b_lep_pt[0]        = ev.lep_pT
  b_lep_eta[0]    = abs(ev.lep_eta)

  #Determine BDT score for event
  bdtg = tmvaReader_.EvaluateMVA("BDTG")
 
  #Write relevant variables to output trees
  pTH_reco_v[0] = ev.pTH_reco
  mgg_v[0] = ev.mgg
  BDT_v[0] = bdtg
  LO_w[0] = ev.weight_LO

  tree_0.Fill()

f_0.Write()
f_0.Close()

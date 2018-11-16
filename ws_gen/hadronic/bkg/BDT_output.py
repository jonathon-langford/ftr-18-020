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
  chain.Add( "ntuples/ttHHad_background_DiPhotonJetsBox_MGG-80toInf.root")
  f_0 = ROOT.TFile.Open( "output_ttHHad_DiPhotonJetsBox_MGG-80toInf_1fb.root" ,"RECREATE")
elif( processID == 'gjet' ):
  chain.Add( "ntuples/ttHHad_background_GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf.root" )
  f_0 = ROOT.TFile.Open( "output_ttHHad_GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_1fb.root" ,"RECREATE")
elif( processID == 'tgjet' ):
  chain.Add( "ntuples/ttHHad_background_TGJet_inclusive.root" )
  f_0 = ROOT.TFile.Open( "output_ttHHad_TGJet_inclusive_1fb.root" ,"RECREATE")
elif( processID == 'ttbar' ):
  chain.Add( "ntuples/ttHHad_background_ttbar.root" )
  f_0 = ROOT.TFile.Open( "output_ttHHad_ttbar_1fb.root" ,"RECREATE")
elif( processID == 'ttgamma' ):
  chain.Add( "ntuples/ttHHad_background_ttgamma_dilepton.root" )
  chain.Add( "ntuples/ttHHad_background_ttgamma_hadronic.root" )
  chain.Add( "ntuples/ttHHad_background_ttgamma_singlelepfromt.root" )
  chain.Add( "ntuples/ttHHad_background_ttgamma_singlelepfromtbar.root" )
  f_0 = ROOT.TFile.Open( "output_ttHHad_ttgamma_1fb.root" ,"RECREATE")
elif( processID == 'ttgammagamma' ):
  chain.Add( "ntuples/ttHHad_background_ttgammagamma.root" )
  f_0 = ROOT.TFile.Open( "output_ttHHad_ttgammagamma_1fb.root" ,"RECREATE")

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
b_scalarHT= array('f',[0])
b_MET     = array('f',[0])
b_mindphi_gg_jets = array('f',[0])
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
b_j4_pt        = array('f',[0])
b_j4_eta       = array('f',[0])

tmvaReader_ = ROOT.TMVA.Reader()
tmvaReader_.AddVariable("Njets"  ,b_Njets)
tmvaReader_.AddVariable("Nbjets" ,b_Nbjets)
tmvaReader_.AddVariable("scalarHT",	b_scalarHT)
tmvaReader_.AddVariable("MET",		b_MET	  )
tmvaReader_.AddVariable("mindphi_gg_jets",		b_mindphi_gg_jets)
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
tmvaReader_.AddVariable("j4_pt",	b_j4_pt )
tmvaReader_.AddVariable("j4_eta",	b_j4_eta)

tmvaReader_.BookMVA("BDTG","weights/TMVAClassification_BDTG.weights.xml")

for ev in chain:
  #Calc variables
  pt1om = ev.pho1_pT/ev.mgg
  pt2om = ev.pho2_pT/ev.mgg
  pho1 = ROOT.TLorentzVector(); pho1.SetPtEtaPhiE(ev.pho1_pT,ev.pho1_eta,ev.pho1_phi,ev.pho1_E)
  pho2 = ROOT.TLorentzVector(); pho2.SetPtEtaPhiE(ev.pho2_pT,ev.pho2_eta,ev.pho2_phi,ev.pho2_E)
  diphoton = pho1+pho2
  min_dPhi = 999
  for j_idx in range(1,5):
    if getattr(ev, "jet%d_pT"%j_idx) < 0: continue
    jet_p4 = ROOT.TLorentzVector()
    jet_p4.SetPtEtaPhiM( getattr(ev,"jet%d_pT"%j_idx),getattr(ev,"jet%d_eta"%j_idx),getattr(ev,"jet%d_phi"%j_idx),getattr(ev,"jet%d_mass"%j_idx) )
    dPhi = diphoton.DeltaPhi( jet_p4 )
    if abs(dPhi) < min_dPhi: min_dPhi = abs(dPhi)

  b_weight[0] = ev.weight_LO*3000 # you don't need this for the actual BDT
  b_Njets[0]  = ev.Njets
  b_Nbjets[0]  = ev.Nbjets
  b_scalarHT[0]    = ev.scalarHT
  b_MET[0]          = ev.MET
  b_mindphi_gg_jets[0] = min_dPhi
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
  b_j4_pt[0]        = ev.jet4_pT
  b_j4_eta[0]    = abs(ev.jet4_eta)

  #Determine BDT score for event: if BDT > XX then write info to ntuple
  bdtg = tmvaReader_.EvaluateMVA("BDTG")
 
  #Write relevant variables to output trees
  pTH_reco_v[0] = ev.pTH_reco
  mgg_v[0] = ev.mgg
  BDT_v[0] = bdtg
  LO_w[0] = ev.weight_LO

  tree_0.Fill()

f_0.Write()
f_0.Close()

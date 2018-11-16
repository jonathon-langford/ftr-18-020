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
  return parser.parse_args()

(opt,args) = get_options()
f_input = opt.input_file
signal_type = opt.signal
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
#numberOfEntries = 1000

# Get pointers to branches used in this analysis
branchEvent = treeReader.UseBranch("Event")
branchGenParticle = treeReader.UseBranch("Particle")
branchPhoton =  treeReader.UseBranch("PhotonTight")
branchElectron = treeReader.UseBranch("Electron")
branchMuon = treeReader.UseBranch("MuonTight")
branchJet = treeReader.UseBranch("JetPUPPI")
branchMET = treeReader.UseBranch("PuppiMissingET")
branchScalarHT = treeReader.UseBranch("ScalarHT")

#Define cross sections [fb] for various processes and uncomment required one
#also calc total weight (check == numberOfEntries)
if( signal_type == "ttH" ):
  Xsection = 1.393
  totalWeight = 61505.9956

elif( signal_type == "ggH" ):
  Xsection = 124.1
  totalWeight = 85889211
  print "ggH: totalWeight = 85889211 (Mean x entries)"

elif( signal_type == "THQ" ):
  Xsection = 0.212
  #totalWeight = 1906318
  #BUGGED TOTAL WEIGHT: FILE_38 network error
  totalWeight = 1882919
  print "THQ: totalWeight = 1906318 (Mean x Entries)"  

elif( signal_type == "THW" ):
  Xsection = 0.0421
  #totalWeight = 817000
  #BUGGED TOTAL WEIGHT: FILE_6 network error
  totalWeight = 779000
  print "THW: totalWeight = 817000 (Mean x Entries)"  

elif( signal_type == "VH" ):
  Xsection = 5.660
  totalWeight = 7937535.474
  print "VH: totalWeight = 7937535.474 (Mean x Entries)"

##############################################################################
#	CONFIGURE OUTPUT

print "Configuring output Ntuple..."
# Initialise TTree and open files to write to
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

#Save one tree, can split into different gen pT trees later
#if( signal_type == "ttH" ): filename = "ttHHad_tri_ntuples/ttHHad_signal_ttH_M125.root"
if( signal_type == "ttH" ): filename = "ttHHad_tri_ntuples_signal/ttH/ttH_" + nOut  + ".root"
elif( signal_type == "ggH" ): filename = "ttHHad_tri_ntuples_signal/ggH/ggH_" + nOut  + ".root"
elif( signal_type == "THQ" ): filename = "ttHHad_tri_ntuples_signal/THQ/THQ_" + nOut  + ".root"
elif( signal_type == "THW" ): filename = "ttHHad_tri_ntuples_signal/THW/THW_" + nOut  + ".root"
elif( signal_type == "VH" ): filename = "ttHHad_tri_ntuples_signal/VH/VH_" + nOut  + ".root"

f_0 = ROOT.TFile.Open( filename ,"RECREATE")
tree_0 = ROOT.TTree("trilinearTree","trilinearTree")

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

######################################################################
#	FUNCTIONS FOR KINEMATICS

def deltaR( eta1, phi1, eta2, phi2 ):
  return math.sqrt( (eta1-eta2)*(eta1-eta2) + (phi1-phi2)*(phi1-phi2) )

def pT_vector_calc( part1, part2 ):
  Px1 = part1.PT*math.cos( part1.Phi )
  Px2 = part2.PT*math.cos( part2.Phi )
  Py1 = part1.PT*math.sin( part1.Phi )
  Py2 = part2.PT*math.sin( part2.Phi )
  return math.sqrt( (Px1+Px2)*(Px1+Px2) + (Py1+Py2)*(Py1+Py2) )

def JetPermutationfMassCalc( bjet, ljet1, ljet2 ):
  M_W = 80.4
  M_t = 172.44
  q_j1 = ljet1.P4()
  q_j2 = ljet2.P4()
  q_b = bjet.P4()
  if( (q_j1+q_j2)*(q_j1+q_j2) < 0 ): return 99999999999999999999999999999.
  M_j1j2 = math.sqrt( (q_j1+q_j2)*(q_j1+q_j2) )
  M_bj1j2 = math.sqrt( (q_b+q_j1+q_j2)*(q_b+q_j1+q_j2) )

  return (M_j1j2-M_W)*(M_j1j2-M_W)+(M_bj1j2-M_t)*(M_bj1j2-M_t)


def JetPermutationEtaCalc( bjet, ljet1, ljet2 ):
  q_perm = bjet.P4()+ljet1.P4()+ljet2.P4()
  return q_perm.Eta()

def JetPermutationPhiCalc( bjet, ljet1, ljet2 ):
  q_perm = bjet.P4()+ljet1.P4()+ljet2.P4()
  return q_perm.Phi()

###############################################################################
#	FUNCTIONS FOR EVENT SELECTION

def SelectPhoton( _photon, photonPtThreshold, photonEtaThresholds, phoIsoChRelThreshold ):
  photon_pass = True
  if( _photon.PT < photonPtThreshold ): photon_pass = False
  #Eta: inc outside transition region between barrel and endcap 
  if( ( abs( _photon.Eta ) > photonEtaThresholds[2] ) | ( ( abs( _photon.Eta ) > photonEtaThresholds[0] ) & ( abs( _photon.Eta ) < photonEtaThresholds[1] ) ) ): photon_pass = False
  #Isolation: currently only using Ich, need Ipho and Itrk
  if( (_photon.SumPtCharged/_photon.PT) > phoIsoChRelThreshold ): photon_pass = False
  #SHOWER SHAPE VARIABLES: R9, sigma_etaeta, need to access from Delphes in some way

  return photon_pass


def SelectDiPhoton( _leadPhoton, _subleadPhoton, leadPhoPTOverMassThreshold, subleadPhoPTOverMassThreshold, deltaRLeadPhoSubleadPhoThreshold ):
  diphoton_pass = True
  q_gg = _leadPhoton.P4()+_subleadPhoton.P4()
  m_gg = math.sqrt( q_gg*q_gg )
  if( _leadPhoton.PT/m_gg < leadPhoPTOverMassThreshold ) | ( _subleadPhoton.PT/m_gg < subleadPhoPTOverMassThreshold ): diphoton_pass = False
  #DIPHOTON MVA EQUIVALENT
  #Require diphoton mass to be between 100 and 180 GeV
  if( m_gg < 100 )|(m_gg > 180 ): diphoton_pass = False

  #Make sure photons are seperated in dR
  dR_gg = deltaR( _leadPhoton.Eta, _leadPhoton.Phi, _subleadPhoton.Eta, _subleadPhoton.Phi )
  if dR_gg < deltaRLeadPhoSubleadPhoThreshold: diphoton_pass = False
  return diphoton_pass


def SelectMuon( _muon, _dipho, muonPtThreshold, muonEtaThreshold, muPFIsoSumRelThreshold, deltaRMuonPhoThreshold ):
  muon_pass = True
  if( _muon.PT < muonPtThreshold ): muon_pass = False
  if( abs( _muon.Eta ) > muonEtaThreshold ): muon_pass = False
  #Vertex: missing, require vertex info in CMS card, copy isTightMuon() (see implementation on git)
  #Isolation: using sumPt variable: assuming same as hard sum in flashgg::LeptonSelection.cc
  if( (_muon.SumPt/_muon.PT) > muPFIsoSumRelThreshold ): muon_pass = False
  
  #if muon passed then calc dR between leadPho and subleadPho
  if muon_pass:
    dR_Muon_LeadPho = deltaR( _dipho[0][0].Eta, _dipho[0][0].Phi, _muon.Eta, _muon.Phi )
    dR_Muon_SubleadPho = deltaR( _dipho[0][1].Eta, _dipho[0][1].Phi, _muon.Eta, _muon.Phi )
    if( dR_Muon_LeadPho < deltaRMuonPhoThreshold ) | ( dR_Muon_SubleadPho < deltaRMuonPhoThreshold ): muon_pass = False

  return muon_pass


def SelectElectron( _electron, _dipho, electronPtThreshold , electronEtaThresholds, electronPhoMassThreshold , deltaRElectronPhoThreshold ):
  electron_pass = True
  if( _electron.PT < electronPtThreshold ): electron_pass = False
  #Eta: inc outside transition region between barrel and endcap 
  if( ( abs( _electron.Eta ) > electronEtaThresholds[2] ) | ( ( abs( _electron.Eta ) > electronEtaThresholds[0] ) & ( abs( _electron.Eta ) < electronEtaThresholds[1] ) ) ): electron_pass = False 
  #Vertex: missing, require vertex info
  #ID: flashgg::passLooseID()

  #mass of electron+photon not close to Z mass: fasely recon electrons
  if electron_pass:
    m_eLeadPho = math.sqrt( abs((_dipho[0][0].P4()+_electron.P4())*(_dipho[0][0].P4()+_electron.P4())) )
    m_eSubleadPho = math.sqrt( abs((_dipho[0][1].P4()+_electron.P4())*(_dipho[0][1].P4()+_electron.P4())) )
    if( abs( m_eLeadPho-91.2 ) < 5. ) | ( abs( m_eSubleadPho-91.2 ) < 5. ): electron_pass = False

  #if electron passed then calc dR between leadPho and subleadPho
  if electron_pass:
    dR_Electron_LeadPho = deltaR( _dipho[0][0].Eta, _dipho[0][0].Phi, _electron.Eta, _electron.Phi )
    dR_Electron_SubleadPho = deltaR( _dipho[0][1].Eta, _dipho[0][1].Phi, _electron.Eta, _electron.Phi )
    if( dR_Electron_LeadPho < deltaRElectronPhoThreshold ) | ( dR_Electron_SubleadPho < deltaRElectronPhoThreshold ): electron_pass = False

  return electron_pass


def SelectJet( _jet, _dipho, jetPtThreshold, jetEtaThreshold, deltaRJetPhoThreshold, isBtagged ):
  jet_pass = True
  if( _jet.PT < jetPtThreshold ): jet_pass = False
  if( abs( _jet.Eta ) > jetEtaThreshold ): jet_pass = False
  
  #if jet passed then calc dR between it and leadPho and subleadPho
  if jet_pass:
    dR_Jet_LeadPho = deltaR( _dipho[0][0].Eta, _dipho[0][0].Phi, _jet.Eta, _jet.Phi )
    dR_Jet_SubleadPho = deltaR( _dipho[0][1].Eta, _dipho[0][1].Phi, _jet.Eta, _jet.Phi )
    if( dR_Jet_LeadPho < deltaRJetPhoThreshold ) | ( dR_Jet_SubleadPho < deltaRJetPhoThreshold ): jet_pass = False

  #B tagging: set isBtagged=1 to output b-jets only
  #Using medium w/ MTD as working point: extract the write bit
  if( isBtagged == 0 ):
    if( _jet.BTag & 0b010000 ): jet_pass = False
  else:
    if( not _jet.BTag & 0b010000 ): jet_pass = False

  return jet_pass

###############################################################################
#	EVENTS LOOP

# Loop over all events
for entry in range(0, numberOfEntries ):
 
  if entry % 10000 == 0: print "Processing event: (", entry, "/", numberOfEntries, ")"

  #Define boolean for event passing selection
  event_pass = False
  # Load selected branches with data from specified event
  treeReader.ReadEntry(entry)

  #Event branch: get event weight
  _event = branchEvent.At(0)
  LO_weight = (_event.Weight/totalWeight)*Xsection

  #Extract genLevel higgs
  #Some events do not have gen-level higgs: remove these events
  hasHiggs = False
  Higgs_gen_idx = -1
  if( branchGenParticle.GetEntries > 0 ):
    for i in range( branchGenParticle.GetEntries() ):
      genPart = branchGenParticle.At(i)
      if( genPart.PID == 25 )&( genPart.Status == 22 ): 
        hasHiggs = True
        Higgs_gen_idx = i

  if( not hasHiggs ): continue 
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #Perform event selection: ttHHad
  if( branchPhoton.GetEntries() < 2 ): continue

  #list to hold photon and lepton candidates
  photons = []
  diphotons = []
  photon_pair = []
  muons = []
  electrons = []
  jets = []
  bjets = []

  #booleans describing event passing different stages of selection
  photons_pass = False
  leptonVeto_pass = True
  top_pass = False

  #------------------------------------------------------------------------------------
  #Photon Selection
  if branchPhoton.GetEntries() > 0:

    #Loop over photons in event and apply photon selection
    for i in range( branchPhoton.GetEntries() ):
      photon = branchPhoton.At(i)
      #Apply selection on single photons
      if( SelectPhoton( photon, photonPtThreshold=20., photonEtaThresholds=[1.4442,1.566,2.5], phoIsoChRelThreshold=0.3 ) ): photons.append( photon )
  
    #if atleast 2 photons in event
    if len( photons ) >= 2:
    
      #sort photons according to pT (descending)
      photons.sort( key=lambda g: g.PT, reverse=True )

      #Loop over photon pairs in event and apply diphoton selection
      for leadPho_idx in range( len( photons ) ):
        for subleadPho_idx in range( len( photons ) ):
          #Only once for each pair
          if subleadPho_idx > leadPho_idx:
            if( SelectDiPhoton( photons[leadPho_idx], photons[subleadPho_idx], leadPhoPTOverMassThreshold=0.333, subleadPhoPTOverMassThreshold=0.25, deltaRLeadPhoSubleadPhoThreshold=0.4) ): diphotons.append( [photons[leadPho_idx],photons[subleadPho_idx]] )
      
      #If atleast one diphoton pair passing selection: choose pair with mass closest to Higgs mass
      if( len( diphotons ) > 1 ):
        mgg_opt = -999.
        dipho_idx_opt = -999
        for dipho_idx in range( len(diphotons) ):
          m_gg = math.sqrt( abs((diphotons[dipho_idx][0].P4()+diphotons[dipho_idx][1].P4())*(diphotons[dipho_idx][0].P4()+diphotons[dipho_idx][1].P4())) )
          if( abs( m_gg - 125.0 ) < abs( mgg_opt - 125.0 ) ):
            mgg_opt = m_gg
            dipho_idx_opt = dipho_idx
        photon_pair.append( diphotons[ dipho_idx_opt ] )
        photons_pass = True
      #else if one pair, then set
      elif( len( diphotons ) == 1 ):
        photon_pair.append( diphotons[0] )
        photons_pass = True

  #-------------------------------------------------------------------------------------------------
  #Lepton VETO: only perform if photon pair selected
  if( photons_pass ):
    #Muons
    if branchMuon.GetEntries() > 0:
      #loop over Muons in event and extract those which satisfy criteria
      for i in range( branchMuon.GetEntries() ):
        muon = branchMuon.At(i)
        if( SelectMuon( muon, photon_pair, muonPtThreshold=20., muonEtaThreshold=3, muPFIsoSumRelThreshold=0.25, deltaRMuonPhoThreshold=0.35 ) ):
          muons.append( muon )

    #Electron
    if branchElectron.GetEntries() > 0:
      #loop over Electrons in event and extract those which satisfy criteria
      for i in range( branchElectron.GetEntries() ):
        electron = branchElectron.At(i)
        if( SelectElectron( electron, photon_pair, electronPtThreshold=20., electronEtaThresholds=[1.4442,1.566,3], electronPhoMassThreshold=5., deltaRElectronPhoThreshold=0.35 ) ):
          electrons.append( electron )
  
    #check for size of lists: If greater than zero then lepton tagged and veto event
    if( len(muons) > 0 ) | ( len(electrons) > 0 ): leptonVeto_pass = False

  #-------------------------------------------------------------------------------------------------
  #Top reconstruction:
  if( photons_pass ) & ( leptonVeto_pass ):
    if branchJet.GetEntries() > 0:
      #loop over jets in event and extract those which satisfy criteria
      for i in range( branchJet.GetEntries() ):
        jet = branchJet.At(i)
        #Jet selection: without b tag
        #UPDATE: CMS-PHASE II TRACKER IMPROVEMENTS, change jet eta threshold to 4
        if( SelectJet( jet, photon_pair, jetPtThreshold=25., jetEtaThreshold=4, deltaRJetPhoThreshold=0.4, isBtagged=0 ) ): jets.append( jet )
        #Jet selection: with b tag
        elif( SelectJet( jet, photon_pair, jetPtThreshold=25., jetEtaThreshold=4, deltaRJetPhoThreshold=0.4, isBtagged=1 ) ): bjets.append( jet )

      #Require >=3 jets in events and that atleast one of jets is b-tagged
      if( len(jets)+len(bjets) >= 3 ) & ( len(bjets) >= 1 ):

        #Order jets according to pT (descending)
        jets.sort( key=lambda J: J.PT, reverse=True )
        bjets.sort( key=lambda bJ: bJ.PT, reverse=True )
        
        #Reconstructing top: events with at-least one b-jet
        #define variables to store index of best jet permutation
        bjet_idx_opt = -999
        leadJet_idx_opt = -999
        subleadJet_idx_opt = -999
        fMass_min = 99999999999999999999999999999.

        #loop over b-jets in event
        for bjet_idx in range( len( bjets ) ):

          #loop over light quark jets in event and choose permutation which minimises function
          for leadJet_idx in range( len( jets ) ):
            for subleadJet_idx in range( len( jets ) ):

              #Calc once for each pair of light quark jets
              if subleadJet_idx > leadJet_idx:
                fMass = JetPermutationfMassCalc( bjets[bjet_idx], jets[leadJet_idx], jets[subleadJet_idx] )

                if( fMass < fMass_min ):
                  fMass_min = fMass
                  bjet_idx_opt = bjet_idx
                  leadJet_idx_opt = leadJet_idx
                  subleadJet_idx_opt = subleadJet_idx
        
        #if found permutation which gives sensible fMass measurement then set top finder to true   
        if( fMass_min != 99999999999999999999999999999. ): top_pass = True
 
##############################################################################
#	EVENTS PASSING SELECTION
  if( hasHiggs ) & (photons_pass) & (leptonVeto_pass) & (top_pass):

    #Define final photons
    leadPhoton = photon_pair[0][0]
    subleadPhoton = photon_pair[0][1]

    #Define top jets
    bjet_inTop = bjets[ bjet_idx_opt ]
    leadJet_inTop = jets[ leadJet_idx_opt ]
    subleadJet_inTop = jets[ subleadJet_idx_opt ] 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # GEN PARTICLE EXTRACTION

    #Higgs
    higgs_gen = branchGenParticle.At( Higgs_gen_idx )

    #Photons from Higgs decay
    mass_pass = False
    dR_pass = False
    higgsPhotons_Found = False
    genPhotons = []
    higgsPhotons_gen = []
    #Define hash table to save unique ID of genParticles and respective position in branch
    hash_ID = {}
    if branchGenParticle.GetEntries() > 0:
      baseUniqueID = branchGenParticle.At(0).GetUniqueID()
      for i in range( branchGenParticle.GetEntries() ):
        #Only save the ID of top quarks as this is where photons originate
        if( abs( branchGenParticle.At(i).PID ) == 6 ):
          hash_ID[ branchGenParticle.At(i).GetUniqueID() - baseUniqueID ] = i
        
        #extract gen Photons
        if( branchGenParticle.At(i).PID == 22 ):
          genPhotons.append( branchGenParticle.At(i) )

      #Extract PID of genPhotons mothers
      for i in range( len( genPhotons ) ):
        motherPID = -999
        if genPhotons[i].M1 in hash_ID.keys():
          motherPID = branchGenParticle.At( hash_ID[ genPhotons[i].M1 ] ).PID
        if abs( motherPID ) == 6:
          higgsPhotons_gen.append( genPhotons[i] )

      if( len( higgsPhotons_gen ) > 1 ):
        #Checks on genPhotons: 
        #dR between genPhotons and one of reco photons is > 0.2
        gen_leadPhoton_idx = -999
        dR_leadPho_min = 999
        for i in range( len( higgsPhotons_gen ) ):
          dR = deltaR( higgsPhotons_gen[i].Eta, higgsPhotons_gen[i].Phi, leadPhoton.Eta, leadPhoton.Phi )
          if( dR < dR_leadPho_min ):
            dR_leadPho_min = dR
            gen_leadPhoton_idx = i
      
        gen_subleadPhoton_idx = -999
        dR_subleadPho_min = 999
        for i in range( len( higgsPhotons_gen ) ):
          dR = deltaR( higgsPhotons_gen[i].Eta, higgsPhotons_gen[i].Phi, subleadPhoton.Eta, subleadPhoton.Phi )
          if( dR < dR_subleadPho_min ):
            dR_subleadPho_min = dR
            gen_subleadPhoton_idx = i

        #Demand criteria and two photons are different
        if( dR_leadPho_min < 0.2 )&( dR_subleadPho_min < 0.2 )&( gen_leadPhoton_idx != gen_subleadPhoton_idx ):
          dR_pass = True
          gen_leadPhoton = higgsPhotons_gen[ gen_leadPhoton_idx ]
          gen_subleadPhoton = higgsPhotons_gen[ gen_subleadPhoton_idx ]

        #Mass criteria: within 3GeV of Higgs mass
        if( dR_pass ):
          m_gg = math.sqrt( abs( (gen_leadPhoton.P4()+gen_subleadPhoton.P4())*(gen_leadPhoton.P4()+gen_subleadPhoton.P4()) ) )
          if( abs( m_gg -125.0 ) < 3. ): mass_pass = True

        if( dR_pass )&( mass_pass ): higgsPhotons_Found = True
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    #Reset var that need resetting
    jet4_pT[0] = -1.
    jet5_pT[0] = -1.
    jet6_pT[0] = -1.
    jet4_eta[0] = -999.
    jet5_eta[0] = -999.
    jet6_eta[0] = -999.
    jet4_phi[0] = -999.
    jet5_phi[0] = -999.
    jet6_phi[0] = -999.
    jet4_mass[0] = -1.
    jet5_mass[0] = -1.
    jet6_mass[0] = -1.
    jet4_btag[0] = -1      
    jet5_btag[0] = -1      
    jet6_btag[0] = -1      
    jet4_inTop[0] = -1      
    jet5_inTop[0] = -1      
    jet6_inTop[0] = -1      
    pho1_gen_pT[0] = -1. 
    pho1_gen_eta[0] = -999.
    pho1_gen_phi[0] = -999. 
    pho1_gen_E[0] = -1. 
    pho2_gen_pT[0] = -1.
    pho2_gen_eta[0] = -999.
    pho2_gen_phi[0] = -999.
    pho2_gen_E[0] = -1.

    #Fill Ntuples with relevant variables
    pTH_gen_v[0] = higgs_gen.PT
    pTH_reco_v[0] = pT_vector_calc( leadPhoton, subleadPhoton )
    mgg_v[0] = math.sqrt( (leadPhoton.P4()+subleadPhoton.P4())*(leadPhoton.P4()+subleadPhoton.P4()) )
    LO_w[0] = LO_weight
    pho1_pT[0] = leadPhoton.PT
    pho1_eta[0] = leadPhoton.Eta
    pho1_phi[0] = leadPhoton.Phi
    pho1_E[0] = leadPhoton.E
    pho1_IsolationVar[0] = leadPhoton.IsolationVarRhoCorr
    pho2_pT[0] = subleadPhoton.PT
    pho2_eta[0] = subleadPhoton.Eta
    pho2_phi[0] = subleadPhoton.Phi
    pho2_E[0] = subleadPhoton.E
    pho2_IsolationVar[0] = subleadPhoton.IsolationVarRhoCorr

    if( higgsPhotons_Found ):
      pho1_gen_pT[0] = gen_leadPhoton.PT
      pho1_gen_eta[0] = gen_leadPhoton.Eta
      pho1_gen_phi[0] = gen_leadPhoton.Phi
      pho1_gen_E[0] = gen_leadPhoton.E
      pho2_gen_pT[0] = gen_subleadPhoton.PT
      pho2_gen_eta[0] = gen_subleadPhoton.Eta
      pho2_gen_phi[0] = gen_subleadPhoton.Phi
      pho2_gen_E[0] = gen_subleadPhoton.E

    #jet variables
    #create list combining jets w/ bjets, order by pT
    merged_jets = jets + bjets
    merged_jets.sort( key=lambda J: J.PT, reverse=True )
    #first jet
    jet1_pT[0] = merged_jets[0].PT
    jet1_eta[0] = merged_jets[0].Eta
    jet1_phi[0] = merged_jets[0].Phi
    jet1_mass[0] = merged_jets[0].Mass
    jet1_btag[0] = merged_jets[0].BTag
    if(merged_jets[0] == leadJet_inTop )|( merged_jets[0] == subleadJet_inTop)|( merged_jets[0] == bjet_inTop):
      jet1_inTop[0] = 1
    else: jet1_inTop[0] = 0
    #second jet
    jet2_pT[0] = merged_jets[1].PT
    jet2_eta[0] = merged_jets[1].Eta
    jet2_phi[0] = merged_jets[1].Phi
    jet2_mass[0] = merged_jets[1].Mass
    jet2_btag[0] = merged_jets[1].BTag
    if(merged_jets[1] == leadJet_inTop )|( merged_jets[1] == subleadJet_inTop)|( merged_jets[1] == bjet_inTop):
      jet2_inTop[0] = 1
    else: jet2_inTop[0] = 0
    #third jet
    jet3_pT[0] = merged_jets[2].PT
    jet3_eta[0] = merged_jets[2].Eta
    jet3_phi[0] = merged_jets[2].Phi
    jet3_mass[0] = merged_jets[2].Mass
    jet3_btag[0] = merged_jets[2].BTag
    if(merged_jets[2] == leadJet_inTop )|( merged_jets[2] == subleadJet_inTop)|( merged_jets[2] == bjet_inTop):
      jet3_inTop[0] = 1
    else: jet3_inTop[0] = 0
    #4 jets in event
    if( len(merged_jets) > 3 ):
      jet4_pT[0] = merged_jets[3].PT
      jet4_eta[0] = merged_jets[3].Eta
      jet4_phi[0] = merged_jets[3].Phi
      jet4_mass[0] = merged_jets[3].Mass
      jet4_btag[0] = merged_jets[3].BTag
      if(merged_jets[3] == leadJet_inTop )|( merged_jets[3] == subleadJet_inTop)|( merged_jets[3] == bjet_inTop):
        jet4_inTop[0] = 1
      else: jet4_inTop[0] = 0
      #5 jets in event
      if( len(merged_jets) > 4 ):
        jet5_pT[0] = merged_jets[4].PT
        jet5_eta[0] = merged_jets[4].Eta
        jet5_phi[0] = merged_jets[4].Phi
        jet5_mass[0] = merged_jets[4].Mass
        jet5_btag[0] = merged_jets[4].BTag
        if(merged_jets[4] == leadJet_inTop )|( merged_jets[4] == subleadJet_inTop)|( merged_jets[4] == bjet_inTop):
          jet5_inTop[0] = 1
        else: jet5_inTop[0] = 0
        #6 jets in event
        if( len(merged_jets) > 5 ):
          jet6_pT[0] = merged_jets[5].PT
          jet6_eta[0] = merged_jets[5].Eta
          jet6_phi[0] = merged_jets[5].Phi
          jet6_mass[0] = merged_jets[5].Mass
          jet6_btag[0] = merged_jets[5].BTag
          if(merged_jets[5] == leadJet_inTop )|( merged_jets[5] == subleadJet_inTop)|( merged_jets[5] == bjet_inTop):
            jet6_inTop[0] = 1
          else: jet6_inTop[0] = 0

    #Global jet variables
    Njets[0] = len( merged_jets )
    Nbjets[0] = len( bjets )
    #Other variables
    MET[0] = branchMET.At(0).MET
    MET_eta[0] = branchMET.At(0).Eta
    MET_phi[0] = branchMET.At(0).Phi 
    scalarHT[0] = branchScalarHT.At(0).HT
    tree_0.Fill()

    #END OF EVENT LOOP
##############################################################################
f_0.Write()
f_0.Close()
#raw_input("Press Enter to continue...")

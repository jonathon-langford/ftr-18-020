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
  parser.add_option("-p", "--proc", dest="process", default='ttbar', help="Define which background process running over, for correct XS")
  return parser.parse_args()

(opt,args) = get_options()
f_input = opt.input_file
background_type = opt.process
#Extract end of input file for output file name
nOut = "ERROR"
f_split = f_input.split("_")
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
if( background_type == "ttgammagamma" ):
  Xsection = 20.43
  totalWeight = 20020.81257
  print "ttgammagamma: totalWeight = (Mean x entries in all files) = 20020.81257"

elif( background_type == "ttgamma_singlelepfromt" ):
  Xsection = 770.9
  totalWeight = 14936850 
  print "ttgamma_singlelepfromt: totalWeight = (Mean x entries in all files) = 14936850"

elif( background_type == "ttgamma_singlelepfromtbar" ):
  Xsection = 769.0
  totalWeight = 14999640
  print "ttgamma_singlelepfromtbar: totalWeight = (Mean x entries in all files) = 14999640"

elif( background_type == "ttgamma_hadronic" ):
  Xsection = 791.5
  totalWeight = 14032230
  print "ttgamma_hadronic: totalWeight = (Mean x entries in all files) = 14032230"

elif( background_type == "ttgamma_dilepton" ):
  Xsection = 623.1
  totalWeight = 26949130
  print "ttgamma_dilepton: totalWeight = (Mean x entries in all files) = 26949130"

elif( background_type == "ttbar" ):
  Xsection = 864400
  totalWeight = 269589975 
  print "ttbar: totalWeight = (Mean x entries in files: 1-100) = 269589975" 

elif( background_type == "TGJet" ):
  Xsection = 3424
  totalWeight = 3413276.402
  print "TGJet: totalWeight = (Mean x entries in all files) = 3413276.402" 

elif( background_type == "QCD" ):
  Xsection = 141200000
  totalWeight = 20291694 
  print "QCD: totalWeight = (Mean x entries in all files) = 20291694"

elif( background_type == "GJet" ):
  Xsection = 1038000
  totalWeight = 19793170
  print "GJet: totalWeight = (Mean x entries in all files) = 19793170"

elif( background_type == "diphoton" ):
  Xsection = 94610
  totalWeight = 8361729.216 
  print "diphoton: totalWeight = (Mean x entries in all files) = 8361729.216"


##############################################################################
#	CONFIGURE OUTPUT

print "Configuring output Ntuple..."
# Initialise TTree and open files to write to
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
#lepton variables
Nleptons = array( 'i', [0] )
lep_pT = array( 'f', [-1.] )
lep_eta = array( 'f', [-1.] )
lep_phi = array( 'f', [-1.] )
#Other
MET = array( 'f', [-1.] )
MET_eta = array( 'f', [-1.] )
MET_phi = array( 'f', [-1.] )
scalarHT = array( 'f', [-1.] )

#Save one tree, can split into different gen pT trees later
if( background_type == "ttgammagamma" ): filename = "ttHLep_tri_ntuples_background/ttgammagamma/ttgammagamma_" + nOut  + ".root"
if( background_type == "ttgamma_singlelepfromt" ): filename = "ttHLep_tri_ntuples_background/ttgamma/ttgamma_singlelepfromt_" + nOut  + ".root" 
elif( background_type == "ttgamma_singlelepfromtbar" ): filename = "ttHLep_tri_ntuples_background/ttgamma/ttgamma_singlelepfromtbar_" + nOut  + ".root" 
elif( background_type == "ttgamma_hadronic" ): filename = "ttHLep_tri_ntuples_background/ttgamma/ttgamma_hadronic_" + nOut  + ".root"
elif( background_type == "ttgamma_dilepton" ): filename = "ttHLep_tri_ntuples_background/ttgamma/ttgamma_dilepton_" + nOut  + ".root"
elif( background_type == "ttbar" ): filename = "ttHLep_tri_ntuples_background/ttbar/ttbar_" + nOut  + ".root"
elif( background_type == "TGJet" ): filename = "ttHLep_tri_ntuples_background/tgjet/tgjet_" + nOut  + ".root"
elif( background_type == "QCD" ): filename = "ttHLep_tri_ntuples_background/qcd/qcd_" + nOut  + ".root"
elif( background_type == "GJet" ): filename = "ttHLep_tri_ntuples_background/gjet/gjet_" + nOut  + ".root"
elif( background_type == "diphoton" ): filename = "ttHLep_tri_ntuples_background/gg/gg_" + nOut  + ".root"

f_0 = ROOT.TFile.Open( filename ,"RECREATE")
tree_0 = ROOT.TTree("trilinearTree","trilinearTree")

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
#First three jet into
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

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #Perform event selection: ttHLep
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
  lepton_pass = False
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
  #Lepton: only perform if photon pair selected
  if( photons_pass ):
    #Muons
    if branchMuon.GetEntries() > 0:
      #loop over Muons in event and extract those which satisfy criteria
      for i in range( branchMuon.GetEntries() ):
        muon = branchMuon.At(i)
        if( SelectMuon( muon, photon_pair, muonPtThreshold=20., muonEtaThreshold=3., muPFIsoSumRelThreshold=0.25, deltaRMuonPhoThreshold=0.35 ) ):
          muons.append( muon )

    #Electron
    if branchElectron.GetEntries() > 0:
      #loop over Electrons in event and extract those which satisfy criteria
      for i in range( branchElectron.GetEntries() ):
        electron = branchElectron.At(i)
        if( SelectElectron( electron, photon_pair, electronPtThreshold=20., electronEtaThresholds=[1.4442,1.566,3.], electronPhoMassThreshold=5., deltaRElectronPhoThreshold=0.35 ) ):
          electrons.append( electron )

    #Sort electrons and muons according to pT
    electrons.sort( key=lambda e: e.PT, reverse=True )
    muons.sort( key=lambda mu: mu.PT, reverse=True )

    #check for size of lists: If greater than zero then pass
    if( len(muons) > 0 ) | ( len(electrons) > 0 ): lepton_pass = True

  #-------------------------------------------------------------------------------------------------
  #jet requirements:
  if( photons_pass ) & ( lepton_pass ):
    if branchJet.GetEntries() > 0:
      #loop over jets in event and extract those which satisfy criteria
      for i in range( branchJet.GetEntries() ):
        jet = branchJet.At(i)
        #Jet selection: without b tag
        if( SelectJet( jet, photon_pair, jetPtThreshold=25., jetEtaThreshold=4, deltaRJetPhoThreshold=0.4, isBtagged=0 ) ): jets.append( jet )
        #Jet selection: with b tag
        elif( SelectJet( jet, photon_pair, jetPtThreshold=25., jetEtaThreshold=4, deltaRJetPhoThreshold=0.4, isBtagged=1 ) ): bjets.append( jet )

      #Require >=2 jets in events and that atleast one of jets is b-tagged
      if( len(jets)+len(bjets) >= 2 ) & ( len(bjets) >= 1 ):

        #Order jets according to pT (descending)
        jets.sort( key=lambda J: J.PT, reverse=True )
        bjets.sort( key=lambda bJ: bJ.PT, reverse=True )
        #Set top pass to true 
        top_pass = True
        
##############################################################################
#	EVENTS PASSING SELECTION
  if(photons_pass) & (lepton_pass) & (top_pass):

    #Define final photons
    leadPhoton = photon_pair[0][0]
    subleadPhoton = photon_pair[0][1]

    #Reset var that need resetting
    jet3_pT[0] = -1.
    jet3_eta[0] = -999.
    jet3_phi[0] = -999.
    jet3_mass[0] = -1.
    jet3_btag[0] = -1      

    #Fill Ntuples with relevant variables
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
    #second jet
    jet2_pT[0] = merged_jets[1].PT
    jet2_eta[0] = merged_jets[1].Eta
    jet2_phi[0] = merged_jets[1].Phi
    jet2_mass[0] = merged_jets[1].Mass
    jet2_btag[0] = merged_jets[1].BTag
    #third jet
    if( len( merged_jets ) > 2 ):
      jet3_pT[0] = merged_jets[2].PT
      jet3_eta[0] = merged_jets[2].Eta
      jet3_phi[0] = merged_jets[2].Phi
      jet3_mass[0] = merged_jets[2].Mass
      jet3_btag[0] = merged_jets[2].BTag

    #Global jet variables
    Njets[0] = len( merged_jets )
    Nbjets[0] = len( bjets )

    #create list combining electrons and muons
    merged_lep = electrons + muons
    merged_lep.sort( key=lambda lep: lep.PT, reverse=True )
    Nleptons[0] = len( merged_lep )
    lep_pT[0] = merged_lep[0].PT
    lep_eta[0] = merged_lep[0].Eta
    lep_phi[0] = merged_lep[0].Phi

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

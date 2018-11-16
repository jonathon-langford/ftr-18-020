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
#numberOfEntries = 3

# Get pointers to branches used in this analysis
branchEvent = treeReader.UseBranch("Event")
branchGenParticle = treeReader.UseBranch("Particle")
branchGenJet = treeReader.UseBranch("GenJet")
branchJet = treeReader.UseBranch("JetPUPPI")

#Define cross sections [fb] for various processes and uncomment required one
if( signal_type == "ttH" ):
  Xsection = 1.393
  totalWeight = 61505.9956

elif( signal_type == "THQ" ):
  Xsection = 0.212
  totalWeight = 1906318
  print "THQ: totalWeight = 1906318 (Mean x Entries)"  

elif( signal_type == "THW" ):
  Xsection = 0.0421
  totalWeight = 817000
  print "THW: totalWeight = 817000 (Mean x Entries)"  
##############################################################################
def pT_vector_calc( part1, part2 ):
  Px1 = part1.PT*math.cos( part1.Phi )
  Px2 = part2.PT*math.cos( part2.Phi )
  Py1 = part1.PT*math.sin( part1.Phi )
  Py2 = part2.PT*math.sin( part2.Phi )
  return math.sqrt( (Px1+Px2)*(Px1+Px2) + (Py1+Py2)*(Py1+Py2) )
##################################################################
#	CONFIGURE OUTPUT

print "Configuring output Ntuple..."
# Initialise TTree and open files to write to
#Main variables
pTH_gen_v = array( 'f', [-1.] )
eta_H_gen_v = array( 'f', [-1.] )
pho1_gen_pT_v = array( 'f', [-1.] )
pho2_gen_pT_v = array( 'f', [-1.] )
pho1_gen_eta_v = array( 'f', [-1.] )
pho2_gen_eta_v = array( 'f', [-1.] )
LO_w = array( 'f', [-1.] )

#Save one tree, can split into different gen pT trees later
if( signal_type == "ttH" ): filename = "ttHHad_tri_ntuples_signal/gen_acceptance/ttH/ttH_" + nOut  + ".root"
elif( signal_type == "THQ" ): filename = "ttHHad_tri_ntuples_signal/gen_acceptance/THQ/THQ_" + nOut  + ".root"
elif( signal_type == "THW" ): filename = "ttHHad_tri_ntuples_signal/gen_acceptance/THW/THW_" + nOut  + ".root"

f_0 = ROOT.TFile.Open( filename ,"RECREATE")
tree_0 = ROOT.TTree("trilinearTree","trilinearTree")

tree_0.Branch("pTH_gen", pTH_gen_v, 'pTH_gen/F')
tree_0.Branch("weight_LO", LO_w, 'weight_LO/F')

#Define debug counters
N_tot = 0
N_fid = 0

###############################################################################
#	EVENTS LOOP

# Loop over all events
for entry in range(0,numberOfEntries):
 
  #if entry % 100 == 0: print "Processing event: (", entry, "/", numberOfEntries, ")"

  #Define boolean for event inside fiducial region
  event_fiducial = True

  # Load selected branches with data from specified event
  treeReader.ReadEntry(entry)

  #Event branch: get event weight
  _event = branchEvent.At(0)
  LO_weight = (_event.Weight/totalWeight)*Xsection

  #Some events do not have gen-level higgs: remove these events
  hasHiggs = False
  Higgs_gen_idx = -1
  if( branchGenParticle.GetEntries > 0 ):
    for i in range( branchGenParticle.GetEntries() ):
      genPart = branchGenParticle.At(i)
      if( genPart.PID == 25 )&( genPart.Status == 22 ): 
        hasHiggs = True
        Higgs_gen_idx = i
  if( hasHiggs ):

    N_tot += LO_weight

    #Gen Higgs extraction
    higgs_gen = branchGenParticle.At( Higgs_gen_idx )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #Apply fiducial region selection
 
    #Higgs rapidity
    if( abs( higgs_gen.Eta ) > 2.5 ): 
      event_fiducial = False
      continue
 
    #Extract gen photons
    #  > ttH: use mother PID abs(6): issue of not selecting right photon
    #  >  tH: use mass closest to Higgs mass
    gen_photons = []
    if( signal_type == 'ttH' ):
      hash_ID = {}
      baseUniqueID = branchGenParticle.At(0).GetUniqueID()
      for i in range( branchGenParticle.GetEntries() ):
        #save id of top quarks
        if( abs( branchGenParticle.At(i).PID ) == 6 ): hash_ID[ branchGenParticle.At(i).GetUniqueID()-baseUniqueID]=i

      #If gen photons mother in hash_ID then Higgs photon
      for i in range( branchGenParticle.GetEntries() ):
        gen = branchGenParticle.At(i)
        if( abs(gen.PID) == 22 )&( gen.M1 in hash_ID.keys() ): gen_photons.append( gen )

    else:
      gen_pho_candidates = []
      for i in range( branchGenParticle.GetEntries() ):
        gen = branchGenParticle.At(i)
        if( gen.PID == 22 ): gen_pho_candidates.append( gen )
      #loop over photon pairs: calc Higgs mass
      m_gg_opt = -999999
      pho1_idx = -999
      pho2_idx = -999
      for pho_i in range( len( gen_pho_candidates ) ):
        for pho_j in range( len( gen_pho_candidates ) ):
          if( pho_j > pho_i ):
            m_gg = (gen_pho_candidates[pho_i].P4()+gen_pho_candidates[pho_j].P4()).M()
            if( abs(m_gg-125.0) < abs( m_gg_opt-125.0) ):
              m_gg_opt = m_gg
              pho1_idx = pho_i
              pho2_idx = pho_j
      gen_photons.append( gen_pho_candidates[pho1_idx] )
      gen_photons.append( gen_pho_candidates[pho2_idx] )
         
    #if( len(gen_photons) == 2 ):
    #  print "Entry: %g"%entry
    #  print "      Higgs: pT = %5.4f, eta = %5.4f, phi = %5.4f"%(higgs_gen.PT,higgs_gen.Eta,higgs_gen.Phi)    
    #  print "   Diphoton: pT = %5.4f, eta = %5.4f, phi = %5.4f, mgg = %5.4f, deltaR = %5.4f"%((gen_photons[0].P4()+gen_photons[1].P4()).Pt(),(gen_photons[0].P4()+gen_photons[1].P4()).Eta(),(gen_photons[0].P4()+gen_photons[1].P4()).Phi(),(gen_photons[0].P4()+gen_photons[1].P4()).M(),(gen_photons[0].P4()+gen_photons[1].P4()).DeltaR( higgs_gen.P4()))    

    if( len( gen_photons ) != 2 ):
      event_fiducial = False
      continue
    else:
      #print "Entry: %g"%entry
      #print "      Higgs: pT = %5.4f, eta = %5.4f, phi = %5.4f"%(higgs_gen.PT,higgs_gen.Eta,higgs_gen.Phi)    
      #print "   Diphoton: pT = %5.4f, eta = %5.4f, phi = %5.4f, mgg = %5.4f, deltaR = %5.4f"%((gen_photons[0].P4()+gen_photons[1].P4()).Pt(),(gen_photons[0].P4()+gen_photons[1].P4()).Eta(),(gen_photons[0].P4()+gen_photons[1].P4()).Phi(),(gen_photons[0].P4()+gen_photons[1].P4()).M(),(gen_photons[0].P4()+gen_photons[1].P4()).DeltaR( higgs_gen.P4()))
      pho1 = gen_photons[0]
      pho2 = gen_photons[1]
      if( pho1.PT < 20. )|( pho2.PT < 20. ): event_fiducial = False
      if( abs( pho1.Eta ) > 2.5 )|( abs( pho2.Eta ) > 2.5 ): event_fiducial = False

      #print "    Photons:"
      #print "         pho1--> pT = %5.4f, eta = %5.4f"%(pho1.PT,pho1.Eta)
      #print "         pho2--> pT = %5.4f, eta = %5.4f"%(pho2.PT,pho2.Eta)
      #print "         Pass: %s"%event_fiducial
      #print "    Jets:" 
       
      #Atleast 2 jets in the event passing pT and eta requirements
      gen_jets = []
      for i in range( branchGenJet.GetEntries() ):
        genJet = branchGenJet.At(i)
        #remove gen photons from gen jet collection
        if( pho1.P4().DeltaR( genJet.P4() ) > 0.4 )&( pho2.P4().DeltaR( genJet.P4() ) > 0.4 ):
          if( genJet.PT > 25. )&( abs( genJet.Eta ) < 4. ): gen_jets.append( genJet )
        #print "         jet%g: pT = %5.4f, eta = %5.4f, dR_pho1 = %5.4f, dR_pho2 = %5.4f, PASS = %s"%(i,genJet.PT,genJet.Eta,pho1.P4().DeltaR( genJet.P4() ),pho2.P4().DeltaR( genJet.P4() ), genJet in gen_jets)
      #Check length of genJets > 2
      if( len( gen_jets ) < 2 ): event_fiducial = False

      #Check one of genjets originates from b-quark
      bjets = []
      #print "    B-TAGGING:"
      for i in range( len( gen_jets ) ):
        #Loop over recoJets: where gen parton info is stored
        #print "       genjet%g: pT = %5.4f, eta = %5.4f, dR_pho1 = %5.4f, dR_pho2 = %5.4f"%(i,gen_jets[i].PT,gen_jets[i].Eta,pho1.P4().DeltaR( gen_jets[i].P4() ),pho2.P4().DeltaR( gen_jets[i].P4() ))
        for j in range( branchJet.GetEntries() ):
          jet = branchJet.At(j)
          if( gen_jets[i].P4().DeltaR( jet.P4() ) < 1. ):
            if( abs(jet.Flavor)==5 ): bjets.append( jet )
          #print "              jet%g: pT = %5.4f, eta = %5.4f, dR = %5.4f, flavor = %g, B-PASS = %s"%(j,jet.PT,jet.Eta,jet.P4().DeltaR( gen_jets[i].P4() ),jet.Flavor,jet in bjets)
      #Check length of bjet
      if( len( bjets ) < 1 ): event_fiducial = False

      #if event_fiducial: print "EVENT %g PASSED"%entry
      #else: print "EVENT %g FAILED"%entry

    #Fill ntuple w/ events passing selection
    if( event_fiducial ):
      N_fid += LO_weight
      pTH_gen_v[0] = higgs_gen.PT
      LO_w[0] = LO_weight
      tree_0.Fill()
  #print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
#END OF EVENT LOOP
f_0.Write()
f_0.Close()

#Print total events plus events in fiducial region
#print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
#print "Total events: Ns =", N_tot
#print "    Fiducial: Ns =", N_fid
#print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

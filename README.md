# ftr-18-020

Constraints of the Higgs self coupling via ttH + tH, Hgg differential measurements at the HL-LHC (CMS Phase II). 

This repository contains the scripts used in the FTR-18-020 workflow. For information on how to run the scripts please see the relevant sub-directories. The workflow is as follows:

 * `ntuples`: preselection (hadronic + leptonic channels) by skimming of Delphes (eos) files. Outputs flat ntuples to be merged. Also creates ntuples for systematic variations.
 * `ws_gen`: apply BDT selection, output RooFit S and B workspaces: split up by pT(H) x production mode x reco category (pT(gg)xBDT)
 * `systematics`: scripts for calculating systematic yield variations.
 * `fitting`: extracting S + B models. Trilinear physics model and datacards. Instructions on how to extract results via combine.
 * `plotting`: scripts for plotting 

To add (from Nick):

 * BDT training
 * Background modelling script
 * S+B fit plotting script

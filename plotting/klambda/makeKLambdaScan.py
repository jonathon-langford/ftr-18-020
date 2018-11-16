#!/usr/bin/env python

#Import libs
import os
import sys
import shlex
import array
import math
import ROOT

#open file to write to
#outf = ROOT.TFile( "ttH_klambda_scan_combined.root", "RECREATE" )
ROOT.gStyle.SetOptStat(0)

#initiate canvas
canv = ROOT.TCanvas("c","c")
canv.SetTicks(1,1)

#1D log-likelihood scan
x = "k_lambda"
xtitle = "#kappa_{#lambda}"

graphs = []
for g in ['comb','comb_statonly','had','lep']:
  gr = ROOT.TGraph()
  gr.SetName("gr_%s_%s"%(x,g))
  if( g == 'comb' ): gr.SetLineColor(1)
  elif( g == 'comb_statonly' ): gr.SetLineColor(1)
  elif( g == 'had' ): gr.SetLineColor(2)
  elif( g == 'lep' ): gr.SetLineColor(9)
  gr.SetLineWidth(2)
  if( g == 'comb_statonly' ): gr.SetLineStyle(2)
  graphs.append( gr ) 

for gr_idx in range( len(graphs) ):
  
  #Read in file
  #tree = 0
  if gr_idx == 0: f_in = ROOT.TFile("combineJobs_combined_preapp/k_lambda/k_lambda.root")
  elif gr_idx == 1: f_in = ROOT.TFile("combineJobs_combined_preapp/klambda_systematics/k_lambda_StatOnly/k_lambda_StatOnly.root")
  elif gr_idx == 2: f_in = ROOT.TFile("combineJobs_hadronic_preapp/k_lambda/k_lambda.root")
  else: f_in = ROOT.TFile("combineJobs_leptonic_preapp/k_lambda/k_lambda.root")
  tree = f_in.Get('limit')

  points = []
  for i in range( tree.GetEntries() ):
    tree.GetEntry(i)
    x_val = getattr( tree, x )
    if x_val in [point[0] for point in points]: continue
    if 2*tree.deltaNLL < 100:
      points.append([x_val, 2*tree.deltaNLL])
  points.sort()

  #best fit point
  minNLL = min([point[1] for point in points])
  for point in points:
    #minus the minimum NLL
    point[1] -= minNLL

  #Fill graph with points
  p=0 #point itr
  lc_klambda_bestfit = 0
  lc_minNLL = 9999
  for k, nll in points:
    if nll >= 0:
      graphs[ gr_idx ].SetPoint( p, k, nll )
      if( nll < lc_minNLL ):
        lc_minNLL = nll
        lc_klambda_bestfit = k
      p += 1

#Draw axis
dH = ROOT.TH1D("dH","",1,-10.,20.)
dH.GetXaxis().SetTitle( xtitle )
dH.GetXaxis().SetTitleSize(0.05)
dH.GetYaxis().SetTitleSize(0.05)
dH.GetYaxis().SetTitle('-2 #Delta ln L')
dH.GetYaxis().SetRangeUser(0.,6.)
dH.SetLineColor(0)
dH.SetStats(0)
dH.Draw("AXIS")

for gr_idx in range( len(graphs) ):
  graphs[gr_idx].GetXaxis().SetRangeUser(-10.,20.)
  graphs[gr_idx].GetYaxis().SetRangeUser(0.,6.)
  if gr_idx == 0: graphs[gr_idx].Draw("L")
  else: graphs[gr_idx].Draw("L Same")

#make helpful TLatex box
lat = ROOT.TLatex()
lat.SetTextFont(42)
lat.SetLineWidth(2)
lat.SetTextAlign(11)
lat.SetNDC()
lat.SetTextSize(0.042)
lat.DrawLatex(0.1,0.92,"#bf{CMS Phase-2} #it{Simulation Preliminary}")
lat.DrawLatex(0.72,0.92,"3 ab^{-1} (14#scale[0.75]{ }TeV)")
lat.DrawLatex(0.4,0.48,"#kappa_{t} = 1")

#draw lines for 68% and 95% C.L.
line1 = ROOT.TLine(-10,3.84,-6.5,3.84)
line2 = ROOT.TLine(-10,1.00,-6.5,1.00)
line1.SetLineWidth(2)
line2.SetLineWidth(2)
line1.Draw("same")
line2.Draw("same")
lat.DrawLatex(0.12,0.205,"#font[62]{#scale[0.75]{68% CL}}")
lat.DrawLatex(0.12,0.582,"#font[62]{#scale[0.75]{95% CL}}")

#lat.Draw("same")

#Legend
leg1 = ROOT.TLegend(0.3,0.542373,0.67,0.88)
leg1.SetFillColor(0)
leg1.SetLineColor(0)
leg1.AddEntry("gr_k_lambda_comb","w/ YR18 syst. uncert.","L")
leg1.AddEntry("gr_k_lambda_comb_statonly","Stat. uncert. only","L")
leg1.AddEntry("gr_k_lambda_had","Hadronic categories only","L")
leg1.AddEntry("gr_k_lambda_lep","Leptonic categories only","L")
leg1.Draw("Same")

canv.RedrawAxis()
canv.Update()
#outf.cd()
canv.Write()
canv.Print("klambda_scan_preapp.pdf")
#canv.Print("klambda_scan_combined_incSyst.png")

raw_input("Press Enter to continue...")

#outf.Write()
#outf.Close()


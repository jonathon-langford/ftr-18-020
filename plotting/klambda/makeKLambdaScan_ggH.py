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
for g in ['ggH0','ggH1','ggH2']:
  gr = ROOT.TGraph()
  gr.SetName("gr_%s_%s"%(x,g))
  if( g == 'ggH0' ): gr.SetLineColor(2)
  elif( g == 'ggH1' ): gr.SetLineColor(1)
  elif( g == 'ggH2' ): gr.SetLineColor(9)
  gr.SetLineWidth(2)
  graphs.append( gr ) 

for gr_idx in range( len(graphs) ):
  
  #Read in file
  #tree = 0
  if gr_idx == 0: f_in = ROOT.TFile("combineJobs_combined_pasv3/k_lambda_ggH0/k_lambda_ggH0.root")
  elif gr_idx == 1: f_in = ROOT.TFile("combineJobs_combined_pasv3/k_lambda/k_lambda.root")
  elif gr_idx == 2: f_in = ROOT.TFile("combineJobs_combined_pasv3/k_lambda_ggH2/k_lambda_ggH2.root")
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
lat.SetTextSize(0.05)
lat.DrawLatex(0.1,0.92,"#bf{CMS Internal}")
lat.DrawLatex(0.6,0.92,"3000 fb^{-1} (14 TeV)")
lat.DrawLatex(0.4,0.5,"#kappa_{t} = 1")

#lat.Draw("same")

#Legend
leg1 = ROOT.TLegend(0.362069,0.542373,0.602011,0.830508)
leg1.SetFillColor(0)
leg1.SetLineColor(0)
leg1.AddEntry("gr_k_lambda_ggH1","YR18 syst. uncert.","L")
leg1.AddEntry("gr_k_lambda_ggH0","YR18 syst. uncert. (ggH x 0)","L")
leg1.AddEntry("gr_k_lambda_ggH2","YR18 syst. uncert. (ggH x 2)","L")
leg1.Draw("Same")

canv.RedrawAxis()
canv.Update()
#outf.cd()
canv.Write()
canv.Print("klambda_scan_combined_ggH.pdf")
#canv.Print("klambda_scan_combined_incSyst.png")

raw_input("Press Enter to continue...")

#outf.Write()
#outf.Close()


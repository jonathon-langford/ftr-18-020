#!/usr/bin/env python

#Import libs
import os
import sys
import shlex
import array
import math
import ROOT

#take as input parameter to plot
if len( sys.argv )!= 2:
  print "Usage: make1DScan.py <parameter>"
  sys.exit(1)

paramID = sys.argv[1]
if( paramID == "klambda" ):
  x = "k_lambda"
  xtitle = "#kappa_{#lambda}"
  other_paramID = "muH"
  other_x = "#mu_{H}"
elif( paramID == "muH" ):
  x = "mu_Higgs"
  xtitle = "#mu_{H}"
  other_paramID = "klambda"
  other_x = "#kappa_{#lambda}"

ROOT.gStyle.SetOptStat(0)

#initiate canvas
canv = ROOT.TCanvas("c","c")
canv.SetTicks(1,1)

graphs = []
for g in ['profiled','fixed']:
  gr = ROOT.TGraph()
  gr.SetName("gr_%s_%s"%(x,g))
  if( g == 'profiled' ): gr.SetLineColor(4)
  elif( g == 'fixed' ): gr.SetLineColor(1)
  gr.SetLineWidth(2)
  graphs.append( gr ) 

for gr_idx in range( len(graphs) ):
  
  #Read in file
  if gr_idx == 0: f_in = ROOT.TFile("%s_%sprofiled.root"%(paramID,other_paramID))
  elif gr_idx == 1: f_in = ROOT.TFile("%s_%sfixed.root"%(paramID,other_paramID))
  tree = f_in.Get('limit')

  points = []
  for i in range( tree.GetEntries() ):
    tree.GetEntry(i)
    x_val = getattr( tree, x )
    if x_val in [point[0] for point in points]: continue
    if 2*tree.deltaNLL < 6.5:
      points.append([x_val, 2*tree.deltaNLL])
  points.sort()

  #best fit point
  minNLL = min([point[1] for point in points])
  for point in points:
    #minus the minimum NLL
    point[1] -= minNLL

  #Fill graph with points
  p=0 #point itr
  lc_bestfit = 0
  lc_minNLL = 9999
  for k, nll in points:
    if nll >= 0:
      graphs[ gr_idx ].SetPoint( p, k, nll )
      if( nll < lc_minNLL ):
        lc_minNLL = nll
        lc_bestfit = k
      p += 1

#Draw axis
if( paramID == "klambda" ): dH = ROOT.TH1D("dH","",1,-10.,20.)
elif( paramID == "muH" ):  dH = ROOT.TH1D("dH","",1,0.7,1.5)
dH.GetXaxis().SetTitle( xtitle )
dH.GetXaxis().SetTitleSize(0.05)
dH.GetYaxis().SetTitleSize(0.05)
dH.GetYaxis().SetTitle('-2 #Delta ln L')
dH.GetYaxis().SetRangeUser(0.,6.)
dH.SetLineColor(0)
dH.SetStats(0)
dH.Draw("AXIS")

for gr_idx in range( len(graphs) ):
  if( paramID == "klambda" ): graphs[gr_idx].GetXaxis().SetRangeUser(-10.,20.)
  elif( paramID == "muH" ): graphs[gr_idx].GetXaxis().SetRangeUser(0.7,1.5)
  graphs[gr_idx].GetYaxis().SetRangeUser(0.,6.)
  if gr_idx == 0: graphs[gr_idx].Draw("L")
  else: graphs[gr_idx].Draw("L Same")

#make helpful TLatex box
lat = ROOT.TLatex()
lat.SetTextFont(42)
lat.SetLineWidth(2)
lat.SetTextAlign(11)
lat.SetNDC()
lat.SetTextSize(0.040)
lat.DrawLatex(0.1,0.92,"#bf{CMS Phase-2} #it{Simulation Preliminary}")
lat.DrawLatex(0.72,0.92,"3 ab^{-1} (14#scale[0.75]{ }TeV)")
#lat.DrawLatex(0.4,0.48,"#kappa_{t} = 1")

#draw lines for 68% and 95% C.L.
if( paramID == "klambda" ): 
  line1 = ROOT.TLine(-10,3.84,20,3.84)
  line2 = ROOT.TLine(-10,1.00,20,1.00)
elif( paramID == "muH" ): 
  line1 = ROOT.TLine(0.7,3.84,1.5,3.84)
  line2 = ROOT.TLine(0.7,1.00,1.5,1.00)
line1.SetLineWidth(1)
line1.SetLineStyle(2)
line2.SetLineWidth(1)
line2.SetLineStyle(2)
line1.Draw("same")
line2.Draw("same")
lat.DrawLatex(0.8,0.205,"#font[62]{#scale[0.75]{68% CL}}")
lat.DrawLatex(0.8,0.582,"#font[62]{#scale[0.75]{95% CL}}")

#lat.Draw("same")

#Legend
if( paramID == "klambda" ): leg1 = ROOT.TLegend(0.348851,0.622881,0.583046,0.881356)
elif( paramID == "muH" ): leg1 = ROOT.TLegend(0.298851,0.622881,0.533046,0.881356)
leg1.SetFillColor(0)
leg1.SetLineColor(0)
leg1.SetTextSize(0.05)
leg1.AddEntry("gr_%s_profiled"%x,"%s profiled"%(other_x),"L")
leg1.AddEntry("gr_%s_fixed"%x,"%s fixed"%(other_x),"L")
leg1.Draw("Same")

canv.RedrawAxis()
canv.Update()
#outf.cd()
canv.Write()
canv.Print("%s_2d.pdf"%paramID)

raw_input("Press Enter to continue...")

#outf.Write()
#outf.Close()


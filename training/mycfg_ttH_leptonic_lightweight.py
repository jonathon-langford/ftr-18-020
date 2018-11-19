# Configuration file for plotting
# L is the Luminosity in fb, signalScale is a factor for the signal to be scaled to - thats it 
import ROOT 
import math 
import csv
import array

treeName    = "trilinearTree"
Label 	    = "#splitline{ttH + tH, H#rightarrow#gamma#gamma}{Leptonic}"

L           = 3000 # = 100/fb
signalScale = 1
minWeight   = -9.e100
#odir 	    = "plots_extendtracker_preselection_cutBDT_gt_0p45"
odir 	    = "plots_ttH_leptonic_preapp"
runBDT      = True

cut_markers = [0.13]

#cutBDTMinimum = 0.45
cutBDTMinimum = -2

directory = "/afs/cern.ch/user/j/jolangfo/public/ForNick/trilinear_Ntuples/btag_correction/ttHLep/"

pre_backs = directory+"bkg/ttHLep_background_"
pre_sigas = directory+"sig/ttHLep_signal_"

samples = { 
	"#gamma-#gamma"	:[ [pre_backs+"DiPhotonJetsBox_MGG-80toInf.root"], [1], ROOT.kAzure-9 ]
	#"#gamma-#gamma"	:[ [pre_sigas+"ggH_M125.root"], [1], ROOT.kAzure-9 ]
	,"#gamma-j"	:[ [pre_backs+"GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf.root"], [1], ROOT.kAzure+2 ]
	,"tt+#gamma#gamma":[ [pre_backs+"ttgammagamma.root"], [1], ROOT.kGray ]
	,"tt+#gamma"	:[ [pre_backs+"ttgamma_dilepton.root",pre_backs+"ttgamma_hadronic.root",pre_backs+"ttgamma_singlelepfromt.root", pre_backs+"ttgamma_singlelepfromtbar.root"], [1,1,1,1], ROOT.kGray+1 ]
	,"tt"		:[ [pre_backs+"ttbar.root"], [1], ROOT.kGray+3 ]
	,"t+#gamma+j":[ [pre_backs+"TGJet_inclusive.root"], [1], ROOT.kGray+2 ]
	  }

order = ["tt+#gamma#gamma","tt+#gamma","t+#gamma+j","tt","#gamma-j","#gamma-#gamma"]
#order = ["#gamma-#gamma"]

signals = {
	"ttH" :[ [pre_sigas+"ttH_M125.root"],[1],ROOT.kRed+1]
	#,"ggH":[ [pre_sigas+"ggH_M125.root"],[1],ROOT.kGreen+2]
	,"tH" :[ [pre_sigas+"THQ_M125.root",pre_sigas+"THW_M125.root"],[1,1],ROOT.kPink+7]
	,"Other H prod." :[ [pre_sigas+"VH_M125.root",pre_sigas+"ggH_M125.root"],[1,1],ROOT.kGreen+2]
	}
sig_order = ["ttH","tH","Other H prod."]

variables = { 
	   "bdt_class":["Leptonic BDT output",10,-0.4,0.9,True,0,[],[]] 

	  }


# These get set by the plotter ------------
fName   = ""
fSample = ""
fLabel  = ""

def setInfo(fnam,pnam,label):
  fName   = fnam
  fSample = pnam
  fLabel  = label
#------------------------------------------

# book an output .csv file with two trees, signal and background ? - For training!
#writer =  open("events.csv","w")
#  writer = csv.writer(csvfile,delimiter=' ')
#writer.write(",".join(["file","process","entry_id","label","weight","Njets","Nbjets","scalarHT","MET","pho1_ptom","pho2_ptom","pho1_eta","pho2_eta", \
#"j1_pt","j1_eta","j2_pt","j2_eta","j3_pt","j3_eta","j4_pt","j4_eta"])+"\n")
# also make a TTree with all of the info :)
#fout    = ROOT.TFile("bdt_trees_leptonic_output.root","RECREATE")
fout    = ROOT.TFile("optimisation_leptonic_output.root","RECREATE")
fout.cd()
oTree_s = ROOT.TTree("tree_s","tree_s")
oTree_b = ROOT.TTree("tree_b","tree_b")


b_sample  = array.array('d',[0]) 
b_weight  = array.array('f',[0]) 
b_Njets   = array.array('f',[0]) 
b_Nlep    = array.array('f',[0]) 
b_Nbjets  = array.array('f',[0]) 
b_scalarHT= array.array('f',[0]) 
b_pTgg    = array.array('f',[0]) 
b_MET     = array.array('f',[0]) 
b_pho1_ptom     = array.array('f',[0]) 
b_pho2_ptom     = array.array('f',[0]) 
b_pho1_eta      = array.array('f',[0]) 
b_pho2_eta      = array.array('f',[0]) 
b_pho1_ch_isolation      = array.array('f',[0]) 
b_pho2_ch_isolation      = array.array('f',[0]) 
b_j1_pt		= array.array('f',[0]) 
b_j1_eta	= array.array('f',[0]) 
b_j2_pt		= array.array('f',[0]) 
b_j2_eta	= array.array('f',[0]) 
b_j3_pt		= array.array('f',[0]) 
b_j3_eta	= array.array('f',[0]) 
b_j4_pt		= array.array('f',[0]) 
b_j4_eta	= array.array('f',[0]) 
b_lep_pt	= array.array('f',[0]) 
b_lep_eta	= array.array('f',[0]) 
b_BDT		= array.array('f',[0]) 
b_mgg		= array.array('f',[0]) 
b_mindphi_gg_l = array.array('f',[0]) 

oTree_s.Branch("weight",	b_weight,"weight/F")
oTree_s.Branch("pTgg",		b_pTgg,"pTgg/F")
oTree_s.Branch("out_BDTG",		b_BDT,"out_BDTG/F")
oTree_s.Branch("mgg",		b_mgg,"mgg/F")
oTree_s.Branch("sample",		b_sample,"sample/D")


oTree_b.Branch("weight",b_weight,"weight/F")
oTree_b.Branch("pTgg",b_pTgg,"pTgg/F")
oTree_b.Branch("out_BDTG",b_BDT,"out_BDTG/F")
oTree_b.Branch("mgg",b_mgg,"mgg/F")
oTree_b.Branch("sample",		b_sample,"sample/D")


tmvaReader_ = ROOT.TMVA.Reader()
tmvaReader_.AddVariable("Njets"  ,b_Njets)
tmvaReader_.AddVariable("Nbjets" ,b_Nbjets)
tmvaReader_.AddVariable("Nleptons" ,b_Nlep)
tmvaReader_.AddVariable("scalarHT",	b_scalarHT)
tmvaReader_.AddVariable("MET",		b_MET	  )
tmvaReader_.AddVariable("mindphi_gg_l",		b_mindphi_gg_l	 )
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


tmvaReader_.BookMVA("BDTG","weights_leptonic/TMVAClassification_BDTG.weights.xml")

def preselection(tr):

     #if tr.scalarHT < 350 : return False
     #if tr.pho1_gen_pT<20 or tr.pho2_gen_pT< 20 : return False
     #if abs(tr.pho1_gen_eta)>2.5 or abs(tr.pho2_gen_eta)>2.5: return False
     if tr.mgg < 180 and tr.mgg > 100 : return True
     return False
# here define a simple analysis (selection of cuts or whatever)

def thingsToStrings(l):
    rlist = []
    for ll in l : rlist.append(str(ll))
    return rlist
 
def doAnalysis(tr,entry,i,w):
     #print fName, fSample, fLabel 
     # override weight variable : 
     w = tr.weight_LO*L

     pt1om = tr.pho1_pT/tr.mgg
     pt2om = tr.pho2_pT/tr.mgg

     #writer.write(",".join(thingsToStrings([fName,fSample,i,fLabel,w,tr.Njets,tr.Nbjets,tr.scalarHT,tr.MET,pt1om,pt2om,abs(tr.pho1_eta),abs(tr.pho2_eta),\
     #tr.jet1_pT,abs(tr.jet1_eta),tr.jet2_pT,abs(tr.jet2_eta),tr.jet3_pT,abs(tr.jet3_eta),tr.jet4_pT,abs(tr.jet4_eta)]))+"\n")

     b_weight[0] = w
     b_Njets[0]  = tr.Njets
     b_Nbjets[0]  = tr.Nbjets
     b_Nlep[0]  = tr.Nleptons
     b_scalarHT[0]	= tr.scalarHT 
     b_MET[0]      	= tr.MET
     b_pTgg[0]      	= tr.pTH_reco
     b_pho1_ptom[0]     = pt1om
     b_pho2_ptom[0]     = pt2om
     b_pho1_eta[0]      = abs(tr.pho1_eta)
     b_pho2_eta[0]      = abs(tr.pho2_eta) 
     b_j1_pt[0]		= tr.jet1_pT
     b_j1_eta[0] 	= abs(tr.jet1_eta)	
     b_j2_pt[0]		= tr.jet2_pT
     b_j2_eta[0]	= abs(tr.jet2_eta)
     b_lep_pt[0]	= tr.lep_pT
     b_lep_eta[0]	= abs(tr.lep_eta)
     b_mgg[0]		= tr.mgg
     b_pho1_ch_isolation[0]	= tr.pho1_IsolationVar
     b_pho2_ch_isolation[0]	= tr.pho2_IsolationVar


     if tr.jet3_pT < 0:
       b_j3_pt[0]	= -999
       b_j3_eta[0]	= -999
       
     else:
       b_j3_pt[0]	= tr.jet3_pT
       b_j3_eta[0]	= abs(tr.jet3_eta)

     # look for difference between higgs and closest jet ?
     photon_1 = ROOT.TLorentzVector(); photon_1.SetPtEtaPhiE(tr.pho1_pT,tr.pho1_eta,tr.pho1_phi,tr.pho1_E)
     photon_2 = ROOT.TLorentzVector(); photon_2.SetPtEtaPhiE(tr.pho2_pT,tr.pho2_eta,tr.pho2_phi,tr.pho2_E)

     diphoton = photon_1+photon_2;
     mindelphi = 999.

     l_p4 = ROOT.TLorentzVector()
     l_p4.SetPtEtaPhiM(getattr(tr,"lep_pT"),getattr(tr,"lep_eta"),getattr(tr,"lep_phi"),0)
       
     dphi = diphoton.DeltaPhi(l_p4)
     mindelphi = abs(dphi)

     b_mindphi_gg_l[0] = mindelphi

     bdtg = tmvaReader_.EvaluateMVA("BDTG") 
     #if bdtg<cutBDTMinimum: return 0
     b_BDT[0]		= bdtg


     # And fill the tree, only use ttH and TH in the signal, the rest are backgrounds! 
     if   fSample == "ttH": findex=0
     elif fSample == "tH" : findex=1
     elif fSample == "VH"  : findex=2
     elif fSample == "ggH" : findex=3
     else : findex=4

     b_sample[0]=findex
     #if fSample in ["ttH","tH"]: oTree_s.Fill()
     if fSample in ["ttH"]: oTree_s.Fill()
     elif fSample not in ["tH","ggH","VH"] :  oTree_b.Fill()
     #else:  oTree_b.Fill()

     variables["bdt_class"][entry][i].Fill(bdtg,w)
     return w 


# TMVA regression training for the response
import sys
import ROOT as r

(r.TMVA.gConfig().GetIONames()).fWeightFileDir="weights_hadronic"
fin     = r.TFile.Open("bdt_trees_hadronic.root")
tree_s = fin.Get("tree_s")
tree_b = fin.Get("tree_b")

fout     = r.TFile("classification_hadronic.root","RECREATE")
factory = r.TMVA.Factory ("TMVAClassification",fout,"!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification")

factory.AddVariable("Njets","N jets"," ","F")
factory.AddVariable("Nbjets","N bjets"," ","F")
factory.AddVariable("scalarHT","HT","GeV","F")	
factory.AddVariable("MET","p_{T}^{miss}","GeV","F")		
factory.AddVariable("mindphi_gg_jets","min #Delta#phi(#gamma#gamma,j)","","F")		
factory.AddVariable("pho1_ptom","p_{T}^{#gamma 1}/m_{#gamma#gamma}"," ","F")	
factory.AddVariable("pho2_ptom","p_{T}^{#gamma 2}/m_{#gamma#gamma}"," ","F")	
factory.AddVariable("pho1_eta","|#eta^{#gamma 1}|"," ","F")	
factory.AddVariable("pho2_eta","|#eta^{#gamma 2}|"," ","F")	
factory.AddVariable("pho1_ch_isolation","ch_isolation^{#gamma 1}"," ","F")	
factory.AddVariable("pho2_ch_isolation","ch_isolation^{#gamma 2}"," ","F")	
factory.AddVariable("j1_pt" ,"p_{T}^{j 1}","GeV","F")		
factory.AddVariable("j1_eta","|#eta^{j 1}|"," ","F")	
factory.AddVariable("j2_pt" ,"p_{T}^{j 2}","GeV","F")		
factory.AddVariable("j2_eta","|#eta^{j 2}|"," ","F")	
factory.AddVariable("j3_pt" ,"p_{T}^{j 3}","GeV","F")		
factory.AddVariable("j3_eta","|#eta^{j 3}|"," ","F")	
factory.AddVariable("j4_pt" ,"p_{T}^{j 4}","GeV","F")		
factory.AddVariable("j4_eta","|#eta^{j 4}|"," ","F")	

factory.SetWeightExpression("weight")

#factory.AddRegressionTree(tree,1.,r.TMVA.Types.kTraining)
factory.AddSignalTree(tree_s,1.) 
factory.AddBackgroundTree(tree_b,1.) 

#numTestTrain_s = int(tree_s.GetEntries()/2)
#numTestTrain_b = int(tree_b.GetEntries()/2)
numTestTrain_s=100
numTestTrain_b=100

factory.PrepareTrainingAndTestTree(r.TCut("1>0"),'!V:nTrain_Background=0:nTrain_Signal=0:nTest_Background=0:nTest_Signal=0:SplitMode=Random')
factory.BookMethod(r.TMVA.Types.kBDT,"BDTG","!H:!V:NTrees=500:BoostType=Grad:MaxDepth=6:Shrinkage=0.1:UseBaggedBoost:GradBaggingFraction=0.1");

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

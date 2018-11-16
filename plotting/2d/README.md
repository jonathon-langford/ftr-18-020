Add full instructions here.

To make the 2D Scan for `mu_H` vs `k_lambda`, you can do ... 

1. Add the following lines to the combined datacard ..

```
mu_Higgs rateParam * ttH* 1  [0.4,3]
mu_Higgs rateParam * tHW* 1  [0.4,3]
mu_Higgs rateParam * tHq* 1  [0.4,3]
mu_Higgs rateParam * ggH* 1  [0.4,3]
mu_Higgs rateParam * VH*  1  [0.4,3]
```

and make the klambda model 

2. get the "combineTool" following instructions here: https://cms-hcomb.gitbooks.io/combine/content/part1/#combine-tool 
   and run the following (assuming you ran `text2workspace.py` with option `-o datacard_combined.klambda.root`)

```
DATACARD="datacard_combined"
combineTool.py $DATACARD.klambda.root  -M MultiDimFit   -t -1 --setParameters pdfindex_reco0_BDTb_13TeV=1,pdfindex_lep_reco0_13TeV=1  -m 125.09 --freezeParameters MH  --redefineSignalPOIs k_lambda,mu_Higgs --setParameterRanges mu_Higgs=0,2:k_lambda=-10,20 --algo grid --points 2000 --job-mode lxbatch --split-points 10 --sub-opts='-q 8nh' --task-name kLambdaScan2D -n kLambdaScan2D --cminDefaultMinimizerStrategy 0
# for scanning over mu_H
combineTool.py $DATACARD.klambda.root  -M MultiDimFit   -t -1 --setParameters pdfindex_reco0_BDTb_13TeV=1,pdfindex_lep_reco0_13TeV=1  -m 125.09 --freezeParameters MH  --redefineSignalPOIs k_lambda,mu_Higgs --setParameterRanges mu_Higgs=0,2:k_lambda=-10,20 --algo grid --points 100 --job-mode lxbatch --split-points 10 --sub-opts='-q 8nh' --task-name MuScan1D -n MuScan1D --cminDefaultMinimizerStrategy 0 --parameters mu_Higgs --floatOtherPOI=1
```

3. after jobs finish run 

```
hadd -f all_points.root higgsCombinekLambdaScan2D.POINTS.* 
hadd -f all_points_1D.root higgsCombineMuScan1D.POINTS.* 
root -l -b -q makeKLam2D.C 
```

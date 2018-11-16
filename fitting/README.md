# Fitting Framework

Add instructions: follow setup of `flashggFinalFit`, switch to `jonathon-langford/trilinear-fit` branch

## Signal model

## Background model

## Extracting results
### Datacards
The final datacards used in FTR-18-020 are included in the `ftr-18-020_approval/datacards/` directory. These are as follows:

* `datacard_hadronic.txt` for the hadronic categories only
* `datacard_leptonic.txt` for the leptonic categories only
* `datacard_combined.txt` combined card
* `datacard_combined.txt` combined card for the 2D scan, in which a parameter which scales all Higgs processes is profiled

Also, you can find the `.root` workspaces extracted using `text2workspace.py` for the following:

* `datacards/dXS/` for the differential cross section measurements. Allows rate of ttH + tH to scale by parameter (mu) for each pT(H) bin.
* `datacards/klambda/` for the klambda scan. Employs scaling functions defined for each process in `physics_model/TrilinearCouplingModel.py`.

To generate the workspace for the differential cross sections, use the following:
```
text2workspace.py <path to datacard.txt> -o <output workspace e.g. datacard_combined_dXSsxan.root> -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel  --PO map='.*/(ttH|tHW|tHq)_gen0_*:r_gen0[1,-10,10]' --PO map='.*/(ttH|tHW|tHq)_gen1_*:r_gen1[1,-10,10]' --PO map='.*/(ttH|tHW|tHq)_gen2_*:r_gen2[1,-10,10]' --PO map='.*/(ttH|tHW|tHq)_gen3_*:r_gen3[1,-10,10]' --PO map='.*/(ttH|tHW|tHq)_gen4_*:r_gen4[1,-10,10]' --PO map='.*/(ttH|tHW|tHq)_gen5_*:r_gen5[1,-10,10]'
```
To generate the workspace for the trilinear coupling model see below: `Physics Model`.

### Workspaces
The signal and background model workspaces, used for the final analysis, are included in the `ftr-18-020_approval/workspaces/` directory. These are separated into the hadronic and leptonic categories.

### Physics model
The following physics model has been defined according to arXiv:1607.04251 and arXiv:1709.08649. Describes the effect of a modified trilinear coupling on single Higgs boson rates.

The cross section times branching ratio scaling functions for the different generator-level pT(H) bin times Higgs production mode are defined in `physics_model/TrilinearCouplingModel.py`. The scaling functions are calculated using the relevant C1 parameters, listed in `physics_model/C1` for the ttH, tH and VH production modes. These C1 are specific to the following binning scenario: pT(H) = [0,45,80,120,200,350,inf] GeV. If you require C1 for a different binning structure, please contact `jonathon.mark.langford@cern.ch'. 
 
This model is used as input for the `combine` tool. To use: copy the model, including the C1 folder into the relevant `HiggsAnalysis/CombinedLimit/python` directory, after installing `combine`. To generate the workspace use:

```
text2workspace.py <path to datacard.txt> -o <output workspace e.g. datacard_KLambdaScan.root> -P HiggsAnalysis.CombinedLimit.TrilinearCouplingModel:trilinearHiggs 
```

Add the option: --X-rescale-nuisance THU_* 0.50 to scale all theory uncert. down by factor of 2 (2018 YR recommendation).

### Extracting results
The following combine commands are used to run the fits:

#### Differential cross sections
```
#change POI accordingly to extract different dXS. Note the Theory uncertaintes related to ttH+tH (yellow bands in plot) are frozen here
combine <output workspace e.g. datacard_combined_dXSscan.root>  -M MultiDimFit --cminDefaultMinimizerType Minuit2 --cminDefaultMinimizerAlgo migrad --algo=grid  -P r_gen0 --floatOtherPOIs=1 -m 125.09 -t -1  --expectSignal 1.00 --freezeNuisances MH,THU_QCDscale_inc,THU_PDF_inc,THU_alpha_inc,THU_factor_shape,THU_renorm_shape  --setPhysicsModelParameters pdfindex_reco0_BDTb_13TeV=1,pdfindex_lep_reco0_13TeV=1
```

#### klambda scan
```
combine <output workspace e.g. datacard_combined_KLambdaScan.root>  -M MultiDimFit --cminDefaultMinimizerType Minuit2 --cminDefaultMinimizerAlgo migrad --algo=grid  -P k_lambda --setPhysicsModelParameterRanges k_lambda=-10.00,20.00  -m 125.09 -t -1  --freezeNuisances MH  --setPhysicsModelParameters k_lambda=1,pdfindex_reco0_BDTb_13TeV=1,pdfindex_lep_reco0_13TeV=1
```

These commands should be split up into different jobs to speed up the process.

# Training BDTs for lep/had selection 

Just launch  `runEverything.sh` and it should work !

Make sure to change the following to your own areas (not Nick's) in that script

```
USERBASE=/afs/cern.ch/user/n/nckw/
WEBBASE=/afs/cern.ch/user/n/nckw/www/higgs/projections/ttHdifferential/
WORKBASE=/afs/cern.ch/work/n/nckw/public/forJonno/weights_fixed_btags/
```

And you probably want to change the cut values in the efficiency plotting commands 

```
root -l -b -q 'makeEfficiencyVsPt.C("bdt_trees_hadronic_output.root","plots_ttH_hadronic_preapp",0.28,0.61)'
root -l -b -q 'makeEfficiencyVsPt.C("bdt_trees_leptonic_output.root","plots_ttH_leptonic_preapp",0.13,0.70)'
```

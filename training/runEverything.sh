#!/bin/bash

USERBASE=/afs/cern.ch/user/n/nckw/
WEBBASE=/afs/cern.ch/user/n/nckw/www/higgs/projections/ttHdifferential/
WORKBASE=/afs/cern.ch/work/n/nckw/public/forJonno/weights_fixed_btags/


# first block of things is run over the samples and run the training from the trees 
python plots.py mycfg_ttH_leptonic 
python plots.py mycfg_ttH_hadronic 

python runtraining_hadronic.py  > training_hadronic.txt
python runtraining_leptonic.py  > training_leptonic.txt

python plots.py mycfg_ttH_leptonic_lightweight 
python plots.py mycfg_ttH_hadronic_lightweight 

python makeROC_curve_Direct.py bdt_trees_hadronic_output.root plots_ttH_hadronic_preapp
python makeROC_curve_Direct.py bdt_trees_leptonic_output.root plots_ttH_leptonic_preapp

root -l -b -q 'makeEfficiencyVsPt.C("bdt_trees_hadronic_output.root","plots_ttH_hadronic_preapp",0.28,0.61)'
root -l -b -q 'makeEfficiencyVsPt.C("bdt_trees_leptonic_output.root","plots_ttH_leptonic_preapp",0.13,0.70)'

#echo "Done - will move some stuff to ~/www/ and to /afs/cern.ch/work/"
zip plots_ttH_hadronic_preapp/allpdfs plots_ttH_hadronic_preapp/*.pdf
zip plots_ttH_leptonic_preapp/allpdfs plots_ttH_leptonic_preapp/*.pdf
cp -r -v plots_ttH_hadronic_preapp $WEBBASE/hadronic
cp -r -v plots_ttH_leptonic_preapp $WEBBASE/leptonic

cp $USERBASE/index.php $WEBBASE/leptonic/plots_ttH_leptonic_preapp
cp $USERBASE/index.php $WEBBASE/hadronic/plots_ttH_hadronic_preapp

cp -r weights_leptonic $WORKBASE
cp -r weights_hadronic $WORKBASE

echo "Done - send message regarding "
echo $WEBBASE/leptonic
echo $WORKBASE

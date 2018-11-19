#!/bin/bash

DATA="backgrounds_hadronic_extended_tracker_binv2.root"

EXT="UGYR_background_fits_hadronic_binv2_bugged_btags"
echo "Ext is $EXT"
PROCS="ttHgen0,ttHgen1,ttHgen2,ttHgen3,ttHgen4,ttHgen5"
echo "Procs are $PROCS"
CATS="reco0_BDTa,reco0_BDTb,reco1_BDTa,reco1_BDTb,reco2_BDTa,reco2_BDTb,reco3_BDTa,reco3_BDTb,reco4_BDTa,reco4_BDTb,reco5"
echo "Cats are $CATS"
INTLUMI=3000
echo "Intlumi is $INTLUMI"
BATCH="LSF"
echo "Batch is $BATCH"
QUEUE="8nh"
echo "Batch is $QUEUE"

SIGFILE="/afs/cern.ch/user/j/jolangfo/public/ForNick/btag_correction/ws/ttHHad/sigfit/CMS-HGG_sigfit_ttHHad_pTH_14TeV_binv2.root"

#echo "./runBackgroundScripts.sh -i $DATA -p $PROCS -f $CATS --ext $EXT --intLumi $INTLUMI --batch $BATCH --sigFile $SIGFILE --isData --unblind"
#./runBackgroundScripts.sh -i $DATA -p $PROCS -f $CATS --ext $EXT --intLumi $INTLUMI --batch $BATCH --sigFile $SIGFILE --isData --unblind
echo "./runBackgroundScripts.sh -i $DATA -p $PROCS -f $CATS --ext $EXT --intLumi $INTLUMI --batch $BATCH --sigFile $SIGFILE  --fTestOnly --unblind"
./runBackgroundScripts.sh -i $DATA -p $PROCS -f $CATS --ext $EXT --intLumi $INTLUMI --batch $BATCH --sigFile $SIGFILE --fTestOnly --unblind --isData
#echo "./runBackgroundScripts.sh -i $DATA -p $PROCS -f $CATS --ext $EXT --intLumi $INTLUMI --batch $BATCH --sigFile $SIGFILE  --bkgPlotsOnly --unblind"
#./runBackgroundScripts.sh -i $DATA -p $PROCS -f $CATS --ext $EXT --intLumi 3000 --batch $BATCH --sigFile $SIGFILE  --bkgPlotsOnly --unblind --isData

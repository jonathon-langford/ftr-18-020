#!/bin/bash


#DATA="backgrounds_W.root"
DATA="backgrounds_leptonic_extended_tracker_binv2.root"

EXT="UGYR_background_fits_leptonic_binv2_bugged_btags"
echo "Ext is $EXT"
PROCS="ttHgen0,ttHgen1,ttHgen2,ttHgen3,ttHgen4,ttHgen5"
echo "Procs are $PROCS"
CATS="lep_reco0,lep_reco1,lep_reco2,lep_reco3,lep_reco4,lep_reco5"
echo "Cats are $CATS"
INTLUMI=3000
echo "Intlumi is $INTLUMI"
BATCH="LSF"
echo "Batch is $BATCH"
QUEUE="8nh"
echo "Batch is $QUEUE"

SIGFILE="/afs/cern.ch/user/j/jolangfo/public/ForNick/btag_correction/ws/ttHLep/sigfit/CMS-HGG_sigfit_ttHLep_pTH_14TeV_binv2.root"

#echo "./runBackgroundScripts.sh -i $DATA -p $PROCS -f $CATS --ext $EXT --intLumi $INTLUMI --batch $BATCH --sigFile $SIGFILE --isData --unblind"
#./runBackgroundScripts.sh -i $DATA -p $PROCS -f $CATS --ext $EXT --intLumi $INTLUMI --batch $BATCH --sigFile $SIGFILE --isData --unblind
echo "./runBackgroundScripts.sh -i $DATA -p $PROCS -f $CATS --ext $EXT --intLumi $INTLUMI --batch $BATCH --sigFile $SIGFILE  --fTestOnly --unblind"
./runBackgroundScripts.sh -i $DATA -p $PROCS -f $CATS --ext $EXT --intLumi $INTLUMI --batch $BATCH --sigFile $SIGFILE --fTestOnly --unblind --isData
#echo "./runBackgroundScripts.sh -i $DATA -p $PROCS -f $CATS --ext $EXT --intLumi $INTLUMI --batch $BATCH --sigFile $SIGFILE  --bkgPlotsOnly --unblind"
#./runBackgroundScripts.sh -i $DATA -p $PROCS -f $CATS --ext $EXT --intLumi 3000 --batch $BATCH --sigFile $SIGFILE  --bkgPlotsOnly --unblind --isData

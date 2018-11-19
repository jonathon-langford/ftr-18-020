#!/bin/bash
p=0 ; while (( $p<50 )); do bsub -q 1nh $PWD/scripts/s_sb_errorbands_noMuhat.sh $p $PWD 125.09 1 5 ; (( p=$p+1 )) ; done

../../Background/bin/plotweightedbands -i inputfile.root --name ttH_differential --lumi 3000 --verbose=1 --quoteMu=0

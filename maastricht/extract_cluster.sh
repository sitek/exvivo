#!/bin/bash

#SBATCH --qos=gablab
#SBATCH --time=1:00:00

for i in 1 2 3 4 5 6 7 8; do
    fslmaths /om/user/ksitek/exvivo/maastricht/maas-atlas2exvivo_fnirtref_warpcoef.nii.gz \
             -thr $i -uthr $i -bin \
             /om/user/ksitek/exvivo/maastricht/maas-atlas2exvivo_cluster-${i};
    done

#!/bin/bash

#SBATCH --qos=gablab
#SBATCH --time=1:00:00

transformed_atlas=/om/user/ksitek/exvivo/maastricht/atlas/maas-atlas2exvivo_ants.nii.gz

for i in 1 2 3 4 5 6 7 8; do
    fslmaths ${transformed_atlas} \
             -thr $i -uthr $i -bin \
             /om/user/ksitek/exvivo/maastricht/roi_ants/maas-atlas2exvivo_cluster-${i};
    done

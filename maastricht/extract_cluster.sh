#!/bin/bash

#SBATCH --qos=gablab
#SBATCH --time=1:00:00

maas_in_dir=/om/user/ksitek/maastricht/brainstem/
out_template=${maas_in_dir}roi/
orig_atlas=${maas_in_dir}corr_group_bin_thr0pt2_c300_bin_labels_fslreorient2std_200um.nii.gz

interp=Linear
transformed_atlas=/om/user/ksitek/exvivo/maastricht/atlas/maas-atlas2exvivo_ants_${interp}.nii.gz
out_template=/om/user/ksitek/exvivo/maastricht/roi_ants/maas-atlas2exvivo_${interp}_

dt=float
for i in 1 2 3 4 5 6 7 8; do
    fslmaths -dt $dt ${transformed_atlas} \
             -thr $i -uthr $i -bin\
             ${out_template}${dt}_cluster-${i};
    done

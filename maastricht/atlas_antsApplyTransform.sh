#!/bin/bash

#SBATCH --mem=50G
#SBATCH --time=1:00:00
#SBATCH --qos=gablab

data_dir=/om/user/ksitek/exvivo/data/
maas_dir=/om/user/ksitek/exvivo/maastricht/
maas_in_dir=/om/user/ksitek/maastricht/brainstem/

interp=Linear

antsApplyTransforms \
  --reference-image ${data_dir}Reg_S64550_nii_b0-slice.nii.gz \
  --input ${maas_in_dir}corr_group_bin_thr0pt2_c300_bin_labels_fslreorient2std_200um.nii.gz \
  --output ${maas_dir}atlas/maas-atlas2exvivo_ants_${interp}.nii.gz \
  --transform ${maas_dir}ants/maas2exvivo_ants_1Warp.nii.gz \
  --transform ${maas_dir}ants/maas2exvivo_ants_0GenericAffine.mat \
  --interpolation ${interp}

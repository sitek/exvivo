#!/bin/bash

#SBATCH --mem=50G
#SBATCH --time=1:00:00
#SBATCH --qos=gablab

#fslreorient2std /om/user/ksitek/maastricht/brainstem/corr_group_bin_thr0pt2_c300_bin_labels.nii.gz \
#                /om/user/ksitek/maastricht/brainstem/corr_group_bin_thr0pt2_c300_bin_labels_fslreorient2std.nii.gz

applywarp --ref=/om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice.nii.gz \
      --in=/om/user/ksitek/maastricht/brainstem/corr_group_bin_thr0pt2_c300_bin_labels_fslreorient2std_200um.nii.gz \
      --out=/om/user/ksitek/exvivo/maastricht/maas-atlas2exvivo_warp2-spline.nii.gz \
      --premat=/om/user/ksitek/exvivo/maastricht/maas7t_flirt_exvivo-space.mat \
      --warp=/om/user/ksitek/exvivo/maastricht/maas2exvivo_fnirt_warpfield_warp2-spline.nii.gz \
      --interp=spline -v

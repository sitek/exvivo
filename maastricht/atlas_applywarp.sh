#!/bin/bash

#SBATCH --mem=250G
#SBATCH --time=16:00:00
#SBATCH --qos=gablab

#fslreorient2std /om/user/ksitek/maastricht/brainstem/corr_group_bin_thr0pt2_c300_bin_labels.nii.gz \
#                /om/user/ksitek/maastricht/brainstem/corr_group_bin_thr0pt2_c300_bin_labels_fslreorient2std.nii.gz

applywarp --ref=/om/user/ksitek/exvivo/maastricht/maas2exvivo_fnirt_faruk-param.nii.gz \
      --in=/om/user/ksitek/maastricht/brainstem/corr_group_bin_thr0pt2_c300_bin_labels_fslreorient2std_200um.nii.gz \
      --out=/om/user/ksitek/exvivo/maastricht/maas-atlas2exvivo_faruk-param.nii.gz \
      --premat=/om/user/ksitek/exvivo/maastricht/maas7t_flirt_exvivo-space.mat \
      --warp=/om/user/ksitek/exvivo/maastricht/maas2exvivo_faruk-param.nii.gz \
      --interp=spline -v

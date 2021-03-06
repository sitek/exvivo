#!/bin/bash

# per https://www.jiscmail.ac.uk/cgi-bin/webadmin?A2=fsl;32d186a0.0812

#SBATCH --mem=20G
#SBATCH --time=1:00:00
#SBATCH --qos=gablab

flirt -in /om/user/ksitek/maastricht/brainstem/corr_group_bin_thr0pt2_c300_bin_labels_fslreorient2std.nii.gz \
      -ref /om/user/ksitek/maastricht/brainstem/corr_group_bin_thr0pt2_c300_bin_labels_fslreorient2std.nii.gz \
      -out /om/user/ksitek/maastricht/brainstem/corr_group_bin_thr0pt2_c300_bin_labels_fslreorient2std_200um.nii.gz \
      -applyisoxfm 0.2

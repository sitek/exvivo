#!/bin/bash

#SBATCH --mem=250G
#SBATCH --time=16:00:00
#SBATCH --qos=gablab

flirt -ref /om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice_fslreorient2std.nii.gz \
      -in /om/user/ksitek/maastricht/brainstem/fnirt_anat_siT1w_fslreorient2std.2.nii.gz \
      -out /om/user/ksitek/exvivo/maastricht/maas7t_flirt_exvivo-space.nii.gz \
      -omat /om/user/ksitek/exvivo/maastricht/maas7t_flirt_exvivo-space.mat \
      -nosearch

#!/bin/bash

#SBATCH --mem=250G
#SBATCH --time=16:00:00
#SBATCH --qos=gablab

fnirt --ref=/om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice_fslreorient2std.nii.gz \
      --in=/om/user/ksitek/maastricht/brainstem/fnirt_anat_siT1w_fslreorient2std.2.nii.gz \
      --aff=/om/user/ksitek/exvivo/maastricht/maas7t_flirt_exvivo-space.mat \
      --applyrefmask=/om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice_mask.nii.gz \
      --subsamp=2,2,1,1 \
      --miter=100,100,50,50 \
      --infwhm=2,2,1,1 \
      --reffwhm=2,2,0,0 \
      --lambda=100,50,20,5 \
      --estint=0,0,0,0 \
      --warpres=2,2,2 \
      --interp=spline \
      --regmod=bending_energy \
      --cout=/om/user/ksitek/exvivo/maastricht/maas2exvivo_faruk-param \
      --iout=/om/user/ksitek/exvivo/maastricht/maas2exvivo_fnirt_faruk-param.nii.gz \
      --fout=/om/user/ksitek/exvivo/maastricht/maas2exvivo_fnirt_warpfield_faruk-param

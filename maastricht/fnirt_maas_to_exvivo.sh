#!/bin/bash

#SBATCH --mem=250G
#SBATCH --time=16:00:00
#SBATCH --qos=gablab

fnirt --ref=/om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice_fslreorient2std.nii.gz \
      --in=/om/user/ksitek/maastricht/brainstem/fnirt_anat_siT1w_fslreorient2std.2.nii.gz \
      --aff=/om/user/ksitek/exvivo/maastricht/maas7t_flirt_exvivo-space.mat \
      --refmask=/om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice_mask.nii.gz \
      --warpres=2,2,2 \
      --interp=spline \
      --cout=/om/user/ksitek/exvivo/maastricht/maas2exvivo_warp2-spline_coef \
      --iout=/om/user/ksitek/exvivo/maastricht/maas2exvivo_fnirt_warp2-spline.nii.gz \
      --fout=/om/user/ksitek/exvivo/maastricht/maas2exvivo_fnirt_warpfield_warp2-spline

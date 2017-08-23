#!/bin/bash

#SBATCH --mem=250G
#SBATCH --time=15:00:00
#SBATCH --qos=gablab

maas_dir='/om/user/ksitek/exvivo/maastricht/'

warp=1
interp='spline'

fnirt --ref=/om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice_fslreorient2std.nii.gz \
      --in=/om/user/ksitek/maastricht/brainstem/fnirt_anat_siT1w_fslreorient2std.2.nii.gz \
      --aff=${maas_dir}maas7t_flirt_exvivo-space.mat \
      --refmask=/om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice_mask.nii.gz \
      --warpres=$warp,$warp,$warp \
      --subsamp=4,2,1,1 \
#      --miter=100,100,50,50 \
      --infwhm=2,2,1,1 \
      --reffwhm=0,0,0,0 \
      --interp=$interp \
      --cout=${maas_dir}maas2exvivo_fnirt_warp${warp}_reffwhm0_std-miter_${interp}_cout \
      --iout=${maas_dir}maas2exvivo_fnirt_warp${warp}_reffwhm0_std-miter_${interp}_iout \
      --fout=${maas_dir}maas2exvivo_fnirt_warp${warp}_reffwhm0_std-miter_${interp}_fout \
      --verbose

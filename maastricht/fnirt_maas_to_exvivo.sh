#!/bin/bash

#SBATCH --mem=250G
#SBATCH --time=24:00:00
#SBATCH --qos=gablab

data_dir='/om/user/ksitek/exvivo/data/'
maas_dir='/om/user/ksitek/exvivo/maastricht/'
maasdata_dir='/om/user/ksitek/maastricht/brainstem/'

warp=1
interp='spline'

fnirt --ref=${data_dir}Reg_S64550_nii_b0-slice_fslreorient2std.nii.gz \
      --in=${maasdata_dir}fnirt_anat_siT1w_fslreorient2std.2.nii.gz \
      --aff=${maas_dir}maas7t_flirt_exvivo-space.mat \
      --refmask=${data_dir}Reg_S64550_nii_b0-slice_mask.nii.gz \
      --warpres=$warp,$warp,$warp \
      --subsamp=4,2,1,1 \
      --miter=100,100,50,50 \
      --infwhm=2,2,1,1 \
      --reffwhm=1,1,0,0 \
      --interp=$interp \
      --cout=${maas_dir}maas2exvivo_fnirt_warp${warp}_reffwhm1-0_${interp}_cout \
      --iout=${maas_dir}maas2exvivo_fnirt_warp${warp}_reffwhm1-0_${interp}_iout \
      --fout=${maas_dir}maas2exvivo_fnirt_warp${warp}_reffwhm1-0_${interp}_fout \
      --verbose

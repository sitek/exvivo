#!/bin/bash

#SBATCH --time=2:00:00
#SBATCH --mem=100G

data_dir=/om2/user/ksitek/exvivo/data/
atlas_dir=/om2/user/ksitek/exvivo/atlas/

#input_image=${data_dir}S64520_m0_SLA.nii.gz
input_image=${atlas_dir}auditory_brainstem_nuclei_20180505.nii.gz
reference_image=${data_dir}Reg_S64550_nii_b0-slice.nii.gz
transform_file=${data_dir}diff2anatSLA_ants_Similarity_Affine_MI_16x8x4x20GenericAffine.mat
interp=Linear
output_image=${atlas_dir}auditory_brainstem_20180505_atlas2diff_Similarity_Affine_MI_16x8x4x2_${interp}.nii.gz

antsApplyTransforms \
  --input $input_image \
  --reference-image $reference_image \
  --output $output_image \
  --interpolation $interp \
  --transform [$transform_file, 1]

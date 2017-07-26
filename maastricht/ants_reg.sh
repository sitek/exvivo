#!/bin/bash

# nipype documentation example's command line output:
# http://nipype.readthedocs.io/en/latest/interfaces/generated/interfaces.ants/registration.html

#SBATCH --qos=gablab
#SBATCH --time=20:00:00
#SBATCH --mem=250G

mat=/om/user/ksitek/exvivo/maastricht/maas7t_flirt_exvivo-space.mat
fixed_img=/om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice_fslreorient2std.nii.gz
moving_img=/om/user/ksitek/maastricht/brainstem/fnirt_anat_siT1w_fslreorient2std.2.nii.gz
out_img=/om/user/ksitek/exvivo/maastricht/maas2exvivo_ants_warped_image.nii.gz

antsRegistration --collapse-output-transforms 0 --dimensionality 3 \
  --initial-moving-transform [ $mat, 0 ] --initialize-transforms-per-stage 0 \
  --interpolation Linear --output [ output_, out_img ]  --transform Affine[ 2.0 ] \
  --metric Mattes[ fixed_img, moving_img, 1, 32, Random, 0.05 ] \
  --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 \
  --use-estimate-learning-rate-once 1 --use-histogram-matching 1 \
  --transform SyN[ 0.25, 3.0, 0.0 ] \
  --metric Mattes[ fixed_img, moving_img, 1, 32 ] \
  --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 \
  --use-estimate-learning-rate-once 1 --use-histogram-matching 1 \
  --winsorize-image-intensities [ 0.0, 1.0 ]  --write-composite-transform 1

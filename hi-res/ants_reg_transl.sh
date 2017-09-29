#!/bin/bash

# from ants github wiki
# https://github.com/stnava/ANTs/wiki/Anatomy-of-an-antsRegistration-call

#SBATCH --qos=gablab
#SBATCH --time=24:00:00
#SBATCH --mem=250G

fixed_img=/om/user/ksitek/exvivo/data/S64520_m0.nii.gz
moving_img=/om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice_fslreorient2std.nii.gz
out_template=/om/user/ksitek/exvivo/data/Reg_S64550_to_S64520_ants

antsRegistration --dimensionality 3 --float 0 \
        --output [$out_template, ${out_template}Warped.nii.gz] \
        --interpolation Linear \
        --winsorize-image-intensities [0.005,0.995] \
        --use-histogram-matching 0 \
        --initial-moving-transform [$fixed_img, $moving_img, 0] \
        --transform Translation[0.1] \
        --metric MI[$fixed_img,$moving_img,1,32,Regular,0.25] \
        --convergence [1000x500x250x100,1e-6,10] \
        --shrink-factors 8x4x2x1 \
        --smoothing-sigmas 3x2x1x0vox

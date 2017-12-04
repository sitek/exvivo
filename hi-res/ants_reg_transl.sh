#!/bin/bash

# from ants github wiki
# https://github.com/stnava/ANTs/wiki/Anatomy-of-an-antsRegistration-call

#SBATCH --qos=gablab
#SBATCH --time=3:00:00
#SBATCH --mem=50G

moving_img=/om/user/ksitek/exvivo/data/S64520_m0_200um.nii.gz
fixed_img=/om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice_fslreorient2std.nii.gz
out_template=/om/user/ksitek/exvivo/data/Reg_S64520_200um_to_S64550_ants_Similarity_Affine_MI_16x8x4x2

antsRegistration --dimensionality 3 --float 0 \
        --output [$out_template, ${out_template}Warped.nii.gz] \
        --interpolation Linear \
        --winsorize-image-intensities [0.005,0.995] \
        --use-histogram-matching 0 \
        --initial-moving-transform [$fixed_img, $moving_img, 0] \
        --transform Similarity[0.1] \
        --metric MI[$fixed_img,$moving_img,1,32] \
        --convergence [1000x500x250x100,1e-6,10] \
        --shrink-factors 16x8x4x2 \
        --smoothing-sigmas 3x2x1x0vox  \
        --transform Affine[0.1] \
        --metric MI[$fixed_img,$moving_img,1,32] \
        --convergence [1000x500x250x100,1e-6,10] \
        --shrink-factors 16x8x4x2 \
        --smoothing-sigmas 3x2x1x0vox

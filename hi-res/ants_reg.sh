#!/bin/bash

# from ants github wiki
# https://github.com/stnava/ANTs/wiki/Anatomy-of-an-antsRegistration-call

#SBATCH --qos=gablab
#SBATCH --time=2-00:00:00
#SBATCH --mem=250G

fixed_base=S64520_m0_200um
fixed_img=/om2/user/ksitek/exvivo/data/${fixed_base}.nii.gz

#moving_img=/om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice_fslreorient2std.nii.gz
#out_template=/om2/user/ksitek/exvivo/data/Reg_S64550_to_S64520_ants
moving_img=/om2/user/ksitek/hcp_7t/data/100610/T1w/T1w_acpc_dc_bs-dc-thal.nii.gz
out_template=/om2/user/ksitek/exvivo/data/${fixed_base}_to_hcp100610_T1w

antsRegistration --dimensionality 3 --float 0 \
        --output [$out_template, ${out_template}Warped.nii.gz] \
        --interpolation Linear \
        --winsorize-image-intensities [0.005,0.995] \
        --use-histogram-matching 0 \
        --initial-moving-transform [$fixed_img,$moving_img,1] \
        --transform Rigid[0.1] \
        --metric MI[$fixed_img,$moving_img,1,32,Regular,0.25] \
        --convergence [1000x500x250x100,1e-6,10] \
        --shrink-factors 8x4x2x1 \
        --smoothing-sigmas 3x2x1x0vox \
        --transform Affine[0.1] \
        --metric MI[$fixed_img,$moving_img,1,32,Regular,0.25] \
        --convergence [1000x500x250x100,1e-6,10] \
        --shrink-factors 8x4x2x1 \
        --smoothing-sigmas 3x2x1x0vox \
        --transform SyN[0.1,3,0] \
        --metric CC[$fixed_img,$moving_img,1,4] \
        --convergence [100x70x50x20,1e-6,10] \
        --shrink-factors 8x4x2x1 \
        --smoothing-sigmas 3x2x1x0vox

#!/bin/bash

mrtrix_bin=/om/user/ksitek/scripts/mrtrix3/release/bin/
mrtrix_scripts=/om/user/ksitek/scripts/mrtrix3/scripts/

# already run 3/8/16
#${mrtrix_bin}mrconvert /om/user/ksitek/exvivo/data/Reg_S64550_nii4d.nii.gz \
#    /om/user/ksitek/exvivo/mrtrix/dwi.mif \
#    -fslgrad /om/user/ksitek/exvivo/data/camino_120_RAS_T.bvecs /om/user/ksitek/exvivo/data/camino_120_RAS_T.bvals

#${mrtrix_scripts}dwi2response tournier \
#    /om/user/ksitek/exvivo/mrtrix/dwi.mif \
#    /om/user/ksitek/exvivo/mrtrix/response.txt \
#    -shell 4000 -nthreads 4 -verbose \
#    -mask /om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice_mask.nii.gz \
#    -tempdir /om/user/ksitek/exvivo/mrtrix/workdir
#    -fslgrad /om/user/ksitek/exvivo/data/camino_120_RAS_T.bvecs /om/user/ksitek/exvivo/data/camino_120_RAS_T.bvals

${mrtrix_bin}dwi2fod csd \
    /om/user/ksitek/exvivo/mrtrix/dwi.mif \
    /om/user/ksitek/exvivo/mrtrix/response.txt \
    /om/user/ksitek/exvivo/mrtrix/fod_out.nii \
    -m /om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice_mask.nii.gz \
    -nthreads 4 \
    -fslgrad /om/user/ksitek/exvivo/data/camino_120_RAS_T.bvecs /om/user/ksitek/exvivo/data/camino_120_RAS_T.bvals
#    -tempdir /om/user/ksitek/exvivo/mrtrix/workdir -info

${mrtrix_bin}tckgen /om/user/ksitek/exvivo/mrtrix/fod_out.nii \
    /om/user/ksitek/exvivo/mrtrix/track_out.tck \
    -seed_image /om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice_mask.nii.gz \
    -number 1000000 -info

wait


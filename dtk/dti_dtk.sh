#!/bin/bash

#/om/user/ksitek/scripts/dtk/dti_recon /om/user/ksitek/exvivo/data/Reg_S64550_nii4d.nii.gz \
#    /om/user/ksitek/exvivo/dti -gm /om/user/ksitek/exvivo/data/bvecs/camino_120_RAS_corrected.txt \
#    -b 4000 -b0 1

/om/user/ksitek/scripts/dtk/dti_tracker /om/user/ksitek/exvivo/dtk_dti/dti \
    /om/user/ksitek/exvivo/dtk_dti/dti_recon -m /om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice_mask.nii.gz

wait

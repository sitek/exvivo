#!/bin/bash

DSI_PATH=/om/user/ksitek/scripts/dtk/matrices/

/om/user/ksitek/scripts/dtk/hardi_mat /om/user/ksitek/exvivo/data/camino_120_RAS.bvecs /om/user/ksitek/exvivo/dtk_odf/recon_mat.dat -ref "/Users/kevinsitek/Dropbox (Personal)/Sitek/Reg_S64550_nii4d.nii.gz" iop 1 0 0 0 1 0

/om/user/ksitek/scripts/dtk/odf_recon /om/user/ksitek/exvivo/data/Reg_S64550_nii4d.nii.gz \
    121 181 /om/user/ksitek/exvivo/dtk_odf/odf -b0 1 iop 1 0 0 0 1 0 \
    -mat /om/user/ksitek/exvivo/dtk_odf/recon_mat.dat -p 3 -sn 1 -ot nii 

wait

/om/user/ksitek/scripts/dtk/odf_tracker /om/user/ksitek/exvivo/dtk_odf/odf \
    /om/user/ksitek/exvivo/dtk_odf/odf_tracker -m /om/user/ksitek/exvivo/data/Reg_S64550_nii_b0-slice_mask.nii.gz

wait

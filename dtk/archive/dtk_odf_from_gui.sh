#!/bin/bash

dtk_dir=/om/user/ksitek/scripts/dtk/
set DSI_PATH=${dtk_dir}matrices/

${dtk_dir}hardi_mat "/om/user/ksitek/exvivo/data/camino_120_RAS.bvecs" "/om/user/ksitek/exvivo/dtk_odf/temp_mat.dat" \
    -ref "/om/user/ksitek/exvivo/data/Reg_S64550_nii4d.nii.gz" -iop 1 0 0 0 1 0 

${dtk_dir}odf_recon "/om/user/ksitek/exvivo/data/Reg_S64550_nii4d.nii.gz" 121 181 \
    "/om/user/ksitek/exvivo/dtk_odf/hardi" -b0 0 -iop 1 0 0 0 1 0  \
    -mat "/om/user/ksitek/exvivo/dtk_odf/temp_mat.dat" -p 3 -sn 1 -ot nii 

#${dtk_dir}odf_tracker "/om/user/ksitek/exvivo/dtk_odf/hardi" "/om/user/ksitek/exvivo/dtk_odf/track_tmp.trk" \
#    -at 35   -m "/om/user/ksitek/exvivo/dtk_odf/hardi_dwi.nii" -it nii
#
#${dtk_dir}spline_filter "/om/user/ksitek/exvivo/dtk_odf/track_tmp.trk" 1 "/om/user/ksitek/exvivo/dtk_odf/hardi.trk"
#
#${dtk_dir}trackvis "/om/user/ksitek/exvivo/dtk_odf/hardi.trk"


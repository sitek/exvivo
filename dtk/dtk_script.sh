#!/bin/bash

export DSI_PATH=/om/user/ksitek/scripts/dtk/matrices/

echo "running hardi_mat"
/om/user/ksitek/scripts/dtk/hardi_mat "/om/user/ksitek/exvivo/data/camino_120_RAS_flipped-yz.bvecs" \
    "/om/user/ksitek/scripts/dtk/matrices/exvivo_121_flipped-yz_mat.dat" \
    -ref "/om/user/ksitek/exvivo/data/Reg_S64550_nii4d.nii" \
    -iop 1 0 0 0 1 0 

echo "running odf_recon script"
/om/user/ksitek/scripts/dtk/odf_recon "/om/user/ksitek/exvivo/data/Reg_S64550_nii4d.nii" \
    121 181 "/om/user/ksitek/exvivo/dtk_odf/hardi" \
    -b0 1 -iop 1 0 0 0 1 0  \
    -mat "/om/user/ksitek/scripts/dtk/matrices/exvivo_121_flipped-yz_mat.dat" \
    -p 3 -sn 1 -ot nii 

echo "running odf_tracker"
/om/user/ksitek/scripts/dtk/odf_tracker "/om/user/ksitek/exvivo/dtk_odf/hardi" \
    "/om/user/ksitek/exvivo/dtk_odf/hardi_track_tmp.trk" \
    -at 35 -m "/om/user/ksitek/exvivo/dtk_odf/hardi_dwi.nii" \
     -it nii

echo "running spline_filter"
/om/user/ksitek/scripts/dtk/spline_filter "/om/user/ksitek/exvivo/dtk_odf/hardi_track_tmp.trk" \
    1 "/om/user/ksitek/exvivo/dtk_odf/hardi.trk"

echo "opening trackvis"
#/om/user/ksitek/scripts/trackvis "/om/user/ksitek/exvivo/dtk_odf/hardi.trk"

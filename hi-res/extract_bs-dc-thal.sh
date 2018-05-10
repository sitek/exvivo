#!/bin/bash

# extract relevant regions from T1w image with freesurfer aparc segmentation

fslmaths aparc.a2009s+aseg.nii.gz -thr 16 -uthr 16 aparc_brainstem.nii.gz
fslmaths aparc.a2009s+aseg.nii.gz -thr 28 -uthr 28 aparc_L-VentralDC.nii.gz
fslmaths aparc.a2009s+aseg.nii.gz -thr 60 -uthr 60 aparc_R-VentralDC.nii.gz
fslmaths aparc.a2009s+aseg.nii.gz -thr 10 -uthr 10 aparc_L-Thalamus.nii.gz
fslmaths aparc.a2009s+aseg.nii.gz -thr 49 -uthr 49 aparc_R-Thalamus.nii.gz
fslmaths aparc_brainstem.nii.gz -add aparc_L-VentralDC.nii.gz \
  -add aparc_R-VentralDC.nii.gz -add aparc_L-Thalamus.nii.gz \
  -add aparc_R-Thalamus.nii.gz \
  -bin aparc_bs-dc-thal.nii.gz
fslmaths T1w_acpc_dc_brain.nii.gz -mas aparc_bs-dc-thal.nii.gz \
  T1w_acpc_dc_bs-dc-thal.nii.gz

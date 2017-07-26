#!/bin/bash
#SBATCH --mem=100G
#SBATCH --time=2:00:00
#SBATCH --qos=gablab

fslmaths /om/user/ksitek/exvivo/data/Reg_S64550_nii4d.nii \
         -Tmean \
         /om/user/ksitek/exvivo/data/Reg_S64550_nii4d_mean.nii

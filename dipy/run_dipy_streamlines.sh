#!/bin/bash
#SBATCH --time=2:00:00
#SBATCH --mem=100GB
#SBATCH --cpus-per-task=10

script_dir=/om2/user/ksitek/exvivo/scripts/dipy/
python ${script_dir}dipy_atlas_target_life.py

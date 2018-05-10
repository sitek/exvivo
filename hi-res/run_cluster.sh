#!/bin/bash

#SBATCH --time=1:00:00
#SBATCH --mem=300G
#SBATCH --cpus-per-task=16

python clustering.py

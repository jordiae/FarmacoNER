#!/bin/bash
#SBATCH --job-name=16PN_PYAYGN
#SBATCH -D /gpfs/home/bsc88/bsc88251/CustomNeuroNERFinalCandidate1/src
#SBATCH --output=/gpfs/scratch/bsc88/bsc88251/experiments2/16PN_PYAYGN/16PN_PYAYGN.out
#SBATCH --error=/gpfs/scratch/bsc88/bsc88251/experiments2/16PN_PYAYGN/16PN_PYAYGN.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --time=18:00:00



module load gcc/7.2.0 impi/2018.1 mkl/2018.1
module load python/3.6.4_ML

source /gpfs/home/bsc88/bsc88251/CustomNeuroNERFinalCandidate1/bin/activate
python3 main.py --parameters_filepath /gpfs/scratch/bsc88/bsc88251/experiments2/16PN_PYAYGN/16PN_PYAYGN_parameters.ini

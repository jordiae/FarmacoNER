#!/bin/bash
#SBATCH --job-name=baseline_test
#SBATCH -D /gpfs/scratch/bsc88/bsc88251/NeuroNER/src
#SBATCH --output=baseline_test.out
#SBATCH --error=baseline_test.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=24:00:00
#SBATCH -gres=gpu:1

export PATH="/gpfs/home/bsc88/bsc88251/packages_power/bin:$PATH"
export PATH="/gpfs/home/bsc88/bsc88251:$PATH"
export LIBRARY_PATH="/gpfs/home/bsc88/bsc88251/packages_power/lib:$LIBRARY_PATH"
export LD_LIBRARY_PATH="/gpfs/home/bsc88/bsc88251/packages_power/lib:$LD_LIBRARY_PATH"
export CPATH="/gpfs/home/bsc88/bsc88251/packages_power/include:$CPATH"
export PATH="/gpfs/home/bsc88/bsc88251/packages_power/share:$PATH"

module load cudnn/7.1.3 atlas/3.10.3 scalapack/2.0.2 fftw/3.3.7 szip/2.1.1 opencv/3.4.1
module load python/3.6.5_ML

source /gpfs/scratch/bsc88/bsc88251/NeuroNER/bin/activate
python3 main.py --parameters_filepath /gpfs/scratch/bsc88/bsc88251/NeuroNERData/baseline/baseline_parameters.ini
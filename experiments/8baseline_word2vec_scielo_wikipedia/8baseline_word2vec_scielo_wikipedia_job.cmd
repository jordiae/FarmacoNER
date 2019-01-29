#!/bin/bash
#SBATCH --job-name=8baseline_word2vec_scielo_wikipedia
#SBATCH -D /gpfs/home/bsc88/bsc88251/CustomNeuroNER/src
#SBATCH --output=/gpfs/home/bsc88/bsc88251/experiments/8baseline_word2vec_scielo_wikipedia/8baseline_word2vec_scielo_wikipedia.out
#SBATCH --error=/gpfs/home/bsc88/bsc88251/experiments/8baseline_word2vec_scielo_wikipedia/8baseline_word2vec_scielo_wikipedia.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --time=2-00:00:00



module load gcc/7.2.0 impi/2018.1 mkl/2018.1
module load python/3.6.4_ML

source /gpfs/home/bsc88/bsc88251/CustomNeuroNER/bin/activate
python3 main.py --parameters_filepath /gpfs/home/bsc88/bsc88251/experiments/8baseline_word2vec_scielo_wikipedia/8baseline_word2vec_scielo_wikipedia_parameters.ini

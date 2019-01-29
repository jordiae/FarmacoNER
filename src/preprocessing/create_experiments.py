import collections
import os
def create_experiments():
    EXPERIMENTS_PATH = os.path.join('..','..','experiments')
    if not os.path.exists(EXPERIMENTS_PATH):
        os.makedirs(EXPERIMENTS_PATH)
    print('Creating experiments...')
    Experiment = collections.namedtuple('Experiment',['name','oversampling','delete','pos','augmentation','other','embedding','stratified'])
    def create_experiment(experiment):
        parameters = {'pretrained_model_folder':'../trained_models/conll_2003_en',
                      'dataset_text_folder':'../data/conll2003/en',
                      'character_embedding_dimension':25,
                      'character_lstm_hidden_state_dimension':25,
                      'check_for_digits_replaced_with_zeros':True,
                      'check_for_lowercase':True,
                      'debug':False,
                      'dropout_rate':0.5,
                      'experiment_name':experiment.name,
                      'freeze_token_embeddings':False,
                      'gradient_clipping_value':5.0,
                      'learning_rate':0.005,
                      'load_only_pretrained_token_embeddings':False,
                      'load_all_pretrained_token_embeddings':False,
                      'main_evaluation_mode':'conll',
                      'maximum_number_of_epochs':100,
                      'number_of_cpu_threads':8,
                      'number_of_gpus':0,
                      'optimizer':'sgd',
                      'output_folder':'../output',
                      'patience':10,
                      'plot_format':'pdf',
                      'reload_character_embeddings':True,
                      'reload_character_lstm':True,
                      'reload_crf':True,
                      'reload_feedforward':True,
                      'reload_token_embeddings':True,
                      'reload_token_lstm':True,
                      'remap_unknown_tokens_to_unk':True,
                      'spacylanguage':'es',
                      'tagging_format':'bioes',
                      'token_embedding_dimension':300,
                      'token_lstm_hidden_state_dimension':300,
                      'token_pretrained_embedding_filepath':experiment.embedding,
                      'tokenizer':'spacy',
                      'train_model':True,
                      'use_character_lstm':True,
                      'use_crf':True,
                      'use_pretrained_model':False,
                      'verbose':False,
                      'use_pos': False,
                      'freeze_pos': False}
        parameters_filepath = '/gpfs/home/bsc88/bsc88251/experiments/' + experiment.name + '/' + experiment.name + '_parameters.ini'
        output_folder = '/gpfs/home/bsc88/bsc88251/experiments/' + experiment.name + '/' + experiment.name + '_output'
        dataset_text_folder = '/gpfs/scratch/bsc88/bsc88251/data/' + experiment.name + '/farmacos-final-one'
        token_pretrained_embedding_filepath = '/gpfs/scratch/bsc88/bsc88251/data/word_vectors/' + experiment.embedding

        if experiment.stratified:
            dataset_text_folder += '-stratified-split'
        else:
            dataset_text_folder += '-simple-split'
        if experiment.oversampling:
            dataset_text_folder += '-oversampling'
            if experiment.delete:
                dataset_text_folder += '-delete'
        if experiment.augmentation:
            dataset_text_folder += '-augmented'
            if experiment.other:
                dataset_text_folder += '-other'
        if experiment.pos:
            parameters['use_pos'] = True
            dataset_text_folder += '-pos'

        parameters['parameters_filepath'] = parameters_filepath
        parameters['output_folder'] = output_folder
        parameters['dataset_text_folder'] = dataset_text_folder
        parameters['token_pretrained_embedding_filepath'] = token_pretrained_embedding_filepath
        parameter_template = '''

#----- Possible modes of operation -----------------------------------------------------------------------------------------------------------------#
# training mode (from scratch): set train_model to True, and use_pretrained_model to False (if training from scratch).                        #
#                               Must have train and valid sets in the dataset_text_folder, and test and deployment sets are optional.               #
# training mode (from pretrained model): set train_model to True, and use_pretrained_model to True (if training from a pretrained model).     #
#                                        Must have train and valid sets in the dataset_text_folder, and test and deployment sets are optional.      #
# prediction mode (using pretrained model): set train_model to False, and use_pretrained_model to True.                                       #
#                                           Must have either a test set or a deployment set.                                                        #
# NOTE: Whenever use_pretrained_model is set to True, pretrained_model_folder must be set to the folder containing the pretrained model to use, and #
#       model.ckpt, dataset.pickle and parameters.ini must exist in the same folder as the checkpoint file.                                         #
#---------------------------------------------------------------------------------------------------------------------------------------------------#

[mode]
# At least one of use_pretrained_model and train_model must be set to True.
train_model = {train_model}
use_pretrained_model = {use_pretrained_model}
pretrained_model_folder = {pretrained_model_folder}

[dataset]
dataset_text_folder = {dataset_text_folder}

# main_evaluation_mode should be either 'conll', 'bio', 'token', or 'binary'. ('conll' is entity-based)
# It determines which metric to use for early stopping, displaying during training, and plotting F1-score vs. epoch.
main_evaluation_mode = {main_evaluation_mode}

output_folder = {output_folder}

#---------------------------------------------------------------------------------------------------------------------#
# The parameters below are for advanced users. Their default values should yield good performance in most cases.      #
#---------------------------------------------------------------------------------------------------------------------#

[ann]
use_character_lstm = {use_character_lstm}
character_embedding_dimension = {character_embedding_dimension}
character_lstm_hidden_state_dimension = {character_lstm_hidden_state_dimension}

use_pos = {use_pos}

# In order to use random initialization instead, set token_pretrained_embedding_filepath to empty string, as below:
# token_pretrained_embedding_filepath =
token_pretrained_embedding_filepath = {token_pretrained_embedding_filepath}
token_embedding_dimension = {token_embedding_dimension}
token_lstm_hidden_state_dimension = {token_lstm_hidden_state_dimension}

use_crf = {use_crf}

[training]
patience = {patience}
maximum_number_of_epochs = {maximum_number_of_epochs}

# optimizer should be either 'sgd', 'adam', or 'adadelta'
optimizer = {optimizer}
learning_rate = {learning_rate}
# gradients will be clipped above |gradient_clipping_value| and below -|gradient_clipping_value|, if gradient_clipping_value is non-zero
# (set to 0 to disable gradient clipping)
gradient_clipping_value = {gradient_clipping_value}

# dropout_rate should be between 0 and 1
dropout_rate = {dropout_rate}

# Upper bound on the number of CPU threads NeuroNER will use
number_of_cpu_threads = {number_of_cpu_threads}

# Upper bound on the number of GPU NeuroNER will use
# If number_of_gpus > 0, you need to have installed tensorflow-gpu
number_of_gpus = {number_of_gpus}

[advanced]
experiment_name = {experiment_name}

# tagging_format should be either 'bioes' or 'bio'
tagging_format = {tagging_format}

# tokenizer should be either 'spacy' or 'stanford'. The tokenizer is only used when the original data is provided only in BRAT format.
# - 'spacy' refers to spaCy (https://spacy.io). To install spacy: pip install -U spacy
# - 'stanford' refers to Stanford CoreNLP (https://stanfordnlp.github.io/CoreNLP/). Stanford CoreNLP is written in Java: to use it one has to start a
#              Stanford CoreNLP server, which can tokenize sentences given on the fly. Stanford CoreNLP is portable, which means that it can be run
#              without any installation.
#              To download Stanford CoreNLP: https://stanfordnlp.github.io/CoreNLP/download.html
#              To run Stanford CoreNLP, execute in the terminal: `java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 50000`
#              By default Stanford CoreNLP is in English. To use it in other languages, see: https://stanfordnlp.github.io/CoreNLP/human-languages.html
#              Stanford CoreNLP 3.6.0 and higher requires Java 8. We have tested NeuroNER with Stanford CoreNLP 3.6.0.
tokenizer = {tokenizer}
# spacylanguage should be either 'de' (German), 'en' (English) or 'fr' (French). (https://spacy.io/docs/api/language-models)
# To install the spaCy language: `python -m spacy.de.download`; or `python -m spacy.en.download`; or `python -m spacy.fr.download`
spacylanguage = {spacylanguage}

# If remap_unknown_tokens is set to True, map to UNK any token that hasn't been seen in neither the training set nor the pre-trained token embeddings.
remap_unknown_tokens_to_unk = {remap_unknown_tokens_to_unk}

# If load_only_pretrained_token_embeddings is set to True, then token embeddings will only be loaded if it exists in token_pretrained_embedding_filepath
# or in pretrained_model_checkpoint_filepath, even for the training set.
load_only_pretrained_token_embeddings = {load_only_pretrained_token_embeddings}

# If load_all_pretrained_token_embeddings is set to True, then all pretrained token embeddings will be loaded even for the tokens that do not appear in the dataset.
load_all_pretrained_token_embeddings = {load_all_pretrained_token_embeddings}

# If check_for_lowercase is set to True, the lowercased version of each token will also be checked when loading the pretrained embeddings.
# For example, if the token 'Boston' does not exist in the pretrained embeddings, then it is mapped to the embedding of its lowercased version 'boston',
# if it exists among the pretrained embeddings.
check_for_lowercase = {check_for_lowercase}

# If check_for_digits_replaced_with_zeros is set to True, each token with digits replaced with zeros will also be checked when loading pretrained embeddings.
# For example, if the token '123-456-7890' does not exist in the pretrained embeddings, then it is mapped to the embedding of '000-000-0000',
# if it exists among the pretrained embeddings.
# If both check_for_lowercase and check_for_digits_replaced_with_zeros are set to True, then the lowercased version is checked before the digit-zeroed version.
check_for_digits_replaced_with_zeros = {check_for_digits_replaced_with_zeros}

# If freeze_token_embeddings is set to True, token embedding will remain frozen (not be trained).
freeze_token_embeddings = {freeze_token_embeddings}

freeze_pos = {freeze_pos}

# If debug is set to True, only 200 lines will be loaded for each split of the dataset.
debug = {debug}
verbose = {verbose}

# plot_format specifies the format of the plots generated by NeuroNER. It should be either 'png' or 'pdf'.
plot_format = {plot_format}

# specify which layers to reload from the pretrained model
reload_character_embeddings = {reload_character_embeddings}
reload_character_lstm = {reload_character_lstm}
reload_token_embeddings = {reload_token_embeddings}
reload_token_lstm = {reload_token_lstm}
reload_feedforward = {reload_feedforward}
reload_crf = {reload_crf}

parameters_filepath = {parameters_filepath}
'''.format(**parameters)
        script = {'jobname': 'conll2003_debug',
                'workdir': '/gpfs/home/bsc88/bsc88251/CustomNeuroNER/src',
                'output': '/gpfs/home/bsc88/bsc88251/ntest/conll2003_debug.out',
                'error': '/gpfs/home/bsc88/bsc88251/ntest/conll2003_debug.err',
                'ntasks': 1,
                'cpuspertask': 12,
                'time': '2-00:00:00',
                'debug': '#SBATCH --qos=debug',
                'parameters_filepath': parameters_filepath}
        script['debug'] = ''
        script['output'] = '/gpfs/home/bsc88/bsc88251/experiments/' + experiment.name + '/' + experiment.name + '.out'
        script['error'] = '/gpfs/home/bsc88/bsc88251/experiments/' + experiment.name + '/' + experiment.name + '.err'
        script['jobname'] = experiment.name

        job_template = '''#!/bin/bash
#SBATCH --job-name={jobname}
#SBATCH -D {workdir}
#SBATCH --output={output}
#SBATCH --error={error}
#SBATCH --ntasks={ntasks}
#SBATCH --cpus-per-task={cpuspertask}
#SBATCH --time={time}
{debug}


module load gcc/7.2.0 impi/2018.1 mkl/2018.1
module load python/3.6.4_ML

source /gpfs/home/bsc88/bsc88251/CustomNeuroNER/bin/activate
python3 main.py --parameters_filepath {parameters_filepath}
'''.format(**script)


        EXPERIMENTS_PATH = os.path.join('..','..','experiments')
        experiment_path = os.path.join(EXPERIMENTS_PATH,experiment.name)
        if os.path.exists(experiment_path):
            print('Experiment',experiment_path,'already exists!')
            exit()
        else:
            os.makedirs(experiment_path)

        with open(os.path.join(experiment_path,script['jobname'] + '_parameters.ini'), 'w') as f:
            f.write(parameter_template)
        with open(os.path.join(experiment_path,script['jobname'] + '_job.cmd'), 'w') as f:
            f.write(job_template)

        '''
        rsync_template = "rsync -auvh {0} bsc88251@dt01.bsc.es:/gpfs/home/bsc88/bsc88251/experiments/ " + script[job-name]
        with open(os.path.join(experiment_path,script[job-name] + '_rsync.sh')) as f:
            f.write(job_template)
        '''
        

    # embeddings
    create_experiment(Experiment(name = '1baseline_glove_original',oversampling = False, delete = False, pos = False, augmentation = False, \
        other = False, embedding = 'glove-sbwc.i25.vec', stratified = True))

    create_experiment(Experiment(name = '2baseline_fasttext_original',oversampling = False, delete = False, pos = False, augmentation = False, \
        other = False, embedding = 'fasttext-sbwc.vec', stratified = True))

    create_experiment(Experiment(name = '3baseline_fasttext_wikipedia',oversampling = False, delete = False, pos = False, augmentation = False, \
        other = False, embedding = 'Wikipedia_Fasttext.vec', stratified = True))

    create_experiment(Experiment(name = '4baseline_fasttext_scielo',oversampling = False, delete = False, pos = False, augmentation = False, \
        other = False, embedding = 'Scielo_Fasttext.vec', stratified = True))

    create_experiment(Experiment(name = '5baseline_fasttext_scielo_wikipedia',oversampling = False, delete = False, pos = False, augmentation = False, \
        other = False, embedding = 'Scielo_wiki_Fasttext.vec', stratified = True))

    create_experiment(Experiment(name = '6baseline_word2vec_wikipedia',oversampling = False, delete = False, pos = False, augmentation = False, \
        other = False, embedding = 'W2V_wiki_w10_c5_300_15epoch.txt', stratified = True))

    create_experiment(Experiment(name = '7baseline_word2vec_scielo',oversampling = False, delete = False, pos = False, augmentation = False, \
        other = False, embedding = 'W2V_scielo_w10_c5_300_15epoch.txt', stratified = True))

    create_experiment(Experiment(name = '8baseline_word2vec_scielo_wikipedia',oversampling = False, delete = False, pos = False, augmentation = False, \
        other = False, embedding = 'W2V_scielo_wiki_w10_c5_300_15epoch.txt', stratified = True))


def main():
    create_experiments()
if __name__ == "__main__":
    main()
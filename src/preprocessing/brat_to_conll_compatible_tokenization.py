# File based on NeuroNER brat_to_conll

# -*- coding: utf-8 -*-
import os
import glob
import codecs
import utils_nlp
import json
import sys
import ntpath


'''
def get_sentences_and_tokens_from_PlanTL(text, tag):
    parsed = tag.parse(text)
    while len(parsed) == 0:
        parsed = tag.parse(text)
    sentences = []
    start = 0
    end = 0 
    for sentence in parsed:
        sentence_tokens = []
        for element in sentence:
            token = element[0]
            start = end
            end = start + len(token)
            token_dict = {}
            token_dict['start'] = start
            token_dict['text'] = token
            token_dict['end'] = end
            if token_dict['text'].strip() in ['\n', '\t', ' ', '']:
                continue
            # Make sure that the token text does not contain any space
            if len(token_dict['text'].split(' ')) != 1:
                print("WARNING: the text of the token contains space character, replaced with hyphen\n\t{0}\n\t{1}".format(token_dict['text'], 
                                                                                                                           token_dict['text'].replace(' ', '-')))
                token_dict['text'] = token_dict['text'].replace(' ', '-')
            sentence_tokens.append(token_dict)
            end += 1
        sentences.append(sentence_tokens)
    return sentences
'''

def get_entities_from_brat(text_filepath, annotation_filepath, verbose=False):
    # load text
    with codecs.open(text_filepath, 'r', 'UTF-8') as f:
        text =f.read()
    if verbose: print("\ntext:\n{0}\n".format(text))

    # parse annotation file
    entities = []
    with codecs.open(annotation_filepath, 'r', 'UTF-8') as f:
        malformatted = False
        for line in f.read().splitlines():
            anno = line.split()
            id_anno = anno[0]
            # parse entity
            if id_anno[0] == 'T':
                entity = {}
                entity['id'] = id_anno
                entity['type'] = anno[1]
                entity['start'] = int(anno[2])
                entity['end'] = int(anno[3])
                entity['text'] = ' '.join(anno[4:])
                # WORKAROUND FOR WRONG ANNOTATIONS COMMING FROM UMLS/MANTRA:
                # The END offset should be -1 if the next char is puntuation sign.
                if ntpath.basename(annotation_filepath)[0] == 'd':
                    if entity['text'].strip() in ['\n', '\t', ' ', '']:
                        continue
                    if entity['end'] > len(text):
                        entity['end'] = len(text)
                    if text[entity['end']-1] == '.' and entity['end'] - entity['start'] > 1:
                        entity['end'] = entity['end']-1
                        if entity['text'][-1] == '.':
                            entity['text'] = entity['text'][:-1]
                if verbose:
                    print("entity: {0}".format(entity))
                # Check compatibility between brat text and anootation
                if utils_nlp.replace_unicode_whitespaces_with_ascii_whitespace(text[entity['start']:entity['end']]) != \
                    utils_nlp.replace_unicode_whitespaces_with_ascii_whitespace(entity['text']):
                    print("Warning: brat text and annotation do not match.")
                    print("\ttext: {0}".format(text[entity['start']:entity['end']]))
                    print("\tanno: {0}".format(entity['text']))
                    print("In:",annotation_filepath)
                    #exit()
                    input("Press Enter to continue...")
                    malformatted = True
                # add to entitys data
                entities.append(entity)
    if verbose: print("\n\n")
    return text, entities, malformatted

def get_pos_tags_from_brat(text,annotation_filepath2, verbose=False):
    # parse annotation file
    pos_tags = []
    with codecs.open(annotation_filepath2, 'r', 'UTF-8') as f:
        for line in f.read().splitlines():
            anno = line.split()
            id_anno = anno[0]
            # parse entity
            if id_anno[0] == 'T':
                pos_tag = {}
                pos_tag['id'] = id_anno
                pos_tag['type'] = anno[1] # tag
                pos_tag['start'] = int(anno[2])
                pos_tag['end'] = int(anno[3])
                pos_tag['text'] = ' '.join(anno[4:])
                if pos_tag['text'].strip() in ['\n', '\t', ' ', '']:
                    continue
                if verbose:
                    print("pos_tag: {0}".format(pos_tag))
                # Check compatibility between brat text and anootation
                if utils_nlp.replace_unicode_whitespaces_with_ascii_whitespace(text[pos_tag['start']:pos_tag['end']]) != \
                    utils_nlp.replace_unicode_whitespaces_with_ascii_whitespace(pos_tag['text']):
                    print("Warning: brat text and annotation do not match.")
                    print("\ttext: {0}".format(text[pos_tag['start']:pos_tag['end']]))
                    print("\tanno: {0}".format(pos_tag['text']))
                    print("In:",annotation_filepath2)
                    #exit()
                    input("Press Enter to continue...")
                # add to entitys data
                pos_tags.append(pos_tag['type'])
    if verbose: print("\n\n")
    return pos_tags


def get_sentences_from_pos_annotations(text,annotation_filepath2, verbose=False):
    # parse annotation file
    sentences = []
    sentence  = []
    with codecs.open(annotation_filepath2, 'r', 'UTF-8') as f:
        for line in f.read().splitlines():
            anno = line.split()
            id_anno = anno[0]
            if id_anno[0] == 'T':
                token_dict = {}
                token_dict['start'] = int(anno[2])
                token_dict['end'] = int(anno[3])
                token_dict['text'] = ' '.join(anno[4:])
                if token_dict['text'].strip() in ['\n', '\t', ' ', '']:
                    continue
                if verbose:
                    print("token_dict: {0}".format(token_dict))
                # Check compatibility between brat text and anootation
                if utils_nlp.replace_unicode_whitespaces_with_ascii_whitespace(text[token_dict['start']:token_dict['end']]) != \
                    utils_nlp.replace_unicode_whitespaces_with_ascii_whitespace(token_dict['text']):
                    print("Warning: brat text and annotation do not match.")
                    print("\ttext: {0}".format(text[token_dict['start']:token_dict['end']]))
                    print("\tanno: {0}".format(token_dict['text']))
                    print("In:",annotation_filepath2)
                    #exit()
                    input("Press Enter to continue...")
                # add to entitys data
                sentence.append(token_dict)
                if token_dict['text'] == '.':
                    sentences.append(sentence)
                    sentence = []
    if verbose: print("\n\n")
    return sentences


def brat_to_conll(input_folder, output_filepath, tag):
    '''
    Assumes '.txt' and '.ann' files are in the input_folder.
    Checks for the compatibility between .txt and .ann at the same time.
    '''
    verbose = False
    dataset_type =  os.path.basename(input_folder)
    print("Formatting {0} set from BRAT to CONLL... ".format(dataset_type), end='')
    text_filepaths = sorted(glob.glob(os.path.join(input_folder, '*.txt')))
    output_file = codecs.open(output_filepath, 'w', 'utf-8')
    bug_counter = 0
    for text_filepath in text_filepaths:
        base_filename = os.path.splitext(os.path.basename(text_filepath))[0]
        annotation_filepath = os.path.join(os.path.dirname(text_filepath), base_filename + '.ann')
        annotation_filepath2 = os.path.join(os.path.dirname(text_filepath), base_filename + '.ann2')
        # create annotation file if it does not exist
        if not os.path.exists(annotation_filepath):
            codecs.open(annotation_filepath, 'w', 'UTF-8').close()
        # create annotation file if it does not exist
        if not os.path.exists(annotation_filepath2):
            codecs.open(annotation_filepath2, 'w', 'UTF-8').close()

        text, entities,malformatted = get_entities_from_brat(text_filepath, annotation_filepath)
        if malformatted:
            bug_counter += 1
        pos_tags = get_pos_tags_from_brat(text,annotation_filepath2)
        entities = sorted(entities, key=lambda entity:entity["start"])
        
        sentences = get_sentences_from_pos_annotations(text,annotation_filepath2)
        
        token_counter = 0
        for sentence in sentences:
            inside = False
            previous_token_label = 'O'
            for token in sentence:
                token['label'] = 'O'
                for entity in entities:
                    if entity['start'] <= token['start'] < entity['end'] or \
                       entity['start'] < token['end'] <= entity['end'] or \
                       token['start'] < entity['start'] < entity['end'] < token['end']:

                        token['label'] = entity['type'].replace('-', '_') # Because the ANN doesn't support tag with '-' in it

                        break
                    elif token['end'] < entity['start']:
                        break
                        
                if len(entities) == 0:
                    entity={'end':0}
                if token['label'] == 'O':
                    gold_label = 'O'
                    inside = False
                elif inside and token['label'] == previous_token_label:
                    gold_label = 'I-{0}'.format(token['label'])
                else:
                    inside = True
                    gold_label = 'B-{0}'.format(token['label'])
                if token['end'] == entity['end']:
                    inside = False
                previous_token_label = token['label']
                pos_tag = pos_tags[token_counter]
                token_counter += 1
                if verbose: print('{0} {1} {2} {3} {4} {5}\n'.format(token['text'], base_filename, token['start'], token['end'],pos_tag,gold_label))
                output_file.write('{0} {1} {2} {3} {4} {5}\n'.format(token['text'], base_filename, token['start'], token['end'],pos_tag,gold_label))
            if verbose: print('\n')
            output_file.write('\n')
    print(bug_counter)
    output_file.close()
    print('Done.')

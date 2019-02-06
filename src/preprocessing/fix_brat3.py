# File based on NeuroNER brat_to_conll

# -*- coding: utf-8 -*-
import os
import glob
import codecs
import utils_nlp
import json
import sys
import ntpath
from shutil import copyfile



def bad_text(s):
    if not any(c.isalpha() for c in s):
        return True
    if len(s.split()) > 4:
        return True
    for c in ['\n', '\t', ' ', ',',';','(',')','.',':','?',"'",'"','/','\\','-','”','“']:
        if c in s:
            return True
    return False

def fix_one(text_filepath):
    # load text
    with codecs.open(text_filepath, 'r', 'UTF-8') as f:
        text =f.read()
    base_filename = os.path.splitext(os.path.basename(text_filepath))[0]
    annotation_filepath = os.path.join(os.path.dirname(text_filepath), base_filename + '.ann')
    ann = ''
    malformatted = False
    original = ''
    with codecs.open(annotation_filepath, 'r', 'UTF-8') as f:
        original = f.read()
        for line in original.splitlines():
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
                '''
                if ntpath.basename(base_filename)[0] == 'd':
                    if entity['text'].strip() in ['\n', '\t', ' ', '']:
                        empty = True
                        malformatted = True
                    if not empty and entity['end'] > len(text):
                        entity['end'] = len(text)
                        malformatted = True
                    if not empty and text[entity['end']-1] == '.' and entity['end'] - entity['start'] > 1:
                        entity['end'] = entity['end']-1
                        malformatted = True
                        if entity['text'][-1] == '.':
                            entity['text'] = entity['text'][:-1]
                    while not empty and entity['end'] < len(text) and text[entity['end']] not in ['\n', '\t', ' ', ',',';','(',')','.',':','?',"'",'"','/','\\','-','”','“']:
                        malformatted = True
                        entity['text'] = entity['text']+text[entity['end']]
                        entity['end'] += 1
                    while not empty and entity['start'] > 0 and text[entity['start']-1] not in ['\n', '\t', ' ', ',',';','(',')','.',':','?',"'",'"','/','\\','-','”','“']:
                        malformatted = True
                        entity['text'] = text[entity['start']-1]+entity['text']
                        entity['start'] = -1
                    if not any(c.isalpha() for c in entity['text']) or len(entity['text'].split()) > 3 or '/' in entity['text'] or '\\' in entity['text']:
                        malformatted = True
                        empty = True
                        print('hey')
                '''
                # Check compatibility between brat text and anootation
                if utils_nlp.replace_unicode_whitespaces_with_ascii_whitespace(text[entity['start']:entity['end']]) != \
                    utils_nlp.replace_unicode_whitespaces_with_ascii_whitespace(entity['text']):
                    malformatted = True
                    '''
                    print("Warning: brat text and annotation do not match.")
                    print("\ttext: {0}".format(text[entity['start']:entity['end']]))
                    print("\tanno: {0}".format(entity['text']))
                    print("In:",annotation_filepath)
                    '''
                    #exit()
                    #input("Press Enter to continue...")
                elif bad_text(text[entity['start']:entity['end']]):
                    malformatted = True
                    '''
                    print("Warning: Bad text")
                    print("\ttext: {0}".format(text[entity['start']:entity['end']]))
                    print("\tanno: {0}".format(entity['text']))
                    print("In:",annotation_filepath)
                    print('Text: ')
                    print(text)
                    print()
                    print('Original:')
                    print(original)
                    print()
                    '''
                    #exit()
                    #input("Press Enter to continue...")
                '''
                #elif False:#else:
                    print("OKAY")
                    print("\ttext: {0}".format(text[entity['start']:entity['end']]))
                    print("\tanno: {0}".format(entity['text']))
                    print("In:",annotation_filepath)
                    print('Text: ')
                    print(text)
                    print()
                    print('Original:')
                    print(original)
                    print()
                    #exit()
                    #input("Press Enter to continue...")
                '''
        return malformatted
        if malformatted and ann != '':
            print('FIXED a malformatted annotation: ', annotation_filepath)
            print('Text: ')
            print(text)
            print()
            print('Original:')
            print(original)
            print()
            print('Fixed:')
            print(ann)
            input('Press enter to continue')
            '''
            with codecs.open(annotation_filepath, 'w', 'UTF-8') as f:
                f.write(ann)
            '''
        elif malformatted:
            print('DELETED a malformatted annotation: ', annotation_filepath)
            print('Text: ')
            print(text)
            print()
            print('Original:')
            print(original)
            input('Press enter to continue')
        elif ann == '':
            print('EMPTY ANNOTATION found!', annotation_filepath)
            print('Text: ')
            print(text)
            print()
            print('Original:')
            print(original)
            input('Press enter to continue')
        
        '''
        with open(AUGMENTED_DATA_PATH + '/' + sentence.id + '.ann','w') as f:
            f.write(ann)
        '''
        return malformatted

def fix_malformatted_brat(path,dst):
    text_filepaths = sorted(glob.glob(os.path.join(path, '*.txt')))
    i = 0
    malcount = 0
    if not os.path.exists(dst):
        os.makedirs(dst)
    for text_filepath in text_filepaths:
        i += 1
        if i % 10 == 0:
            print('Fixing', i, 'of',len(text_filepaths))
        malformatted = fix_one(text_filepath)
        if malformatted:
            malcount += 1
        else:
            base_filename = os.path.splitext(os.path.basename(text_filepath))[0]
            annotation_filepath = os.path.join(os.path.dirname(text_filepath), base_filename + '.ann')
            annotation2_filepath = os.path.join(os.path.dirname(text_filepath), base_filename + '.ann2')
            src = text_filepath
            dest = os.path.join(dst,base_filename + '.txt')
            copyfile(src, dest)
            src = annotation_filepath
            dest = os.path.join(dst,base_filename + '.ann')
            copyfile(src, dest)
            src = annotation2_filepath
            dest = os.path.join(dst,base_filename + '.ann2')
            copyfile(src, dest)

    print('Malformatted =',malcount, 'Total=',len(text_filepaths), '%=', (malcount/len(text_filepaths))*100)
#DATA_PATH = os.path.join('..','..','data')
#AUGMENTED_NO_OTHER_DATA_PATH = os.path.join(DATA_PATH, 'augmentedDataNoOther')
#fix_malformatted_brat(AUGMENTED_NO_OTHER_DATA_PATH+'Fixed2')
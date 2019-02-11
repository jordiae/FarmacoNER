import dataset
import dataset as dat
import shutil
import os
import pandas as pd
import dataset as dat
from sqlalchemy import create_engine
import dataset
import xml.etree.ElementTree as ET
import ast
import collections
import math
from sklearn.model_selection import train_test_split
import sys
import random
from brat_to_conll_compatible_tokenization import brat_to_conll
import fix_brat3
import create_experiments
import math
import glob


SEED = 1234
DATA_PATH = os.path.join('..','..','data')
FARMACOS_PATH = os.path.join(DATA_PATH,'farmacos-final')
UMLS_PATH = os.path.join(DATA_PATH,'UMLS')
MRCONSO_PATH = os.path.join(UMLS_PATH,'MRCONSO.RRF')
MRSTY_PATH = os.path.join(UMLS_PATH,'MRSTY.RRF')
FILTERED_MRCONSO_PATH = os.path.join(UMLS_PATH,'filtered-mrconso.txt')
SQL_MRCONSO_PATH = os.path.join(UMLS_PATH,'mrconso.db')
SQL_MRSTY_PATH = os.path.join(UMLS_PATH,'mrsty.db')

MANTRA_XML_PATH = os.path.join(DATA_PATH,'EC21-v1','EC21.d')
MANTRA_XML_FILE_EMEA_PATH = os.path.join(MANTRA_XML_PATH,'EMEA_es_EC21_man.xml')
MANTRA_XML_FILE_MEDLINE_PATH =os.path.join(MANTRA_XML_PATH,'Medline_es_EC21_man.xml')

AUGMENTED_NO_OTHER_DATA_PATH = os.path.join(DATA_PATH, 'augmentedDataNoOther')
AUGMENTED_OTHER_DATA_PATH = os.path.join(DATA_PATH, 'augmentedDataOther')

AUGMENTED_DATA_PATH = ''

FARMACOS_STRATIFIED_PATH = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split')
FARMCOS_STRATIFIED_OVERSAMPLING_WITHOUT_DELETING_PATH = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split-oversampling')
FARMACOS_STRATIFIED_OVERSAMPLING_DELETING = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split-oversampling-deleting')
FARMACOS_STRATIFIED_AUGMENTED_NO_OTHER_PATH = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split-augmented-no-other')
FARMACOS_STRATIFIED_AUGMENTED_OTHER_PATH = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split-augmented-other')
FARMACOS_STRATIFIED_OVERSAMPLING_WITHOUT_DELETING_AUGMENTED_NO_OTHER_PATH  = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split-oversampling-augmented-no-other')
FARMACOS_STRATIFIED_OVERSAMPLING_WITHOUT_DELETING_AUGMENTED_OTHER_PATH  = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split-oversampling-augmented-other')
FARMACOS_STRATIFIED_OVERSAMPLING_DELETING_AUGMENTED_NO_OTHER_PATH  = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split-oversampling-deleting-augmented-no-other')
FARMACOS_STRATIFIED_OVERSAMPLING_DELETING_AUGMENTED_OTHER_PATH  = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split-oversampling-deleting-augmented-other')

FARMACOS_STRATIFIED_WITHOUT_UNCLEAR_AND_NO_NORM = FARMACOS_STRATIFIED_PATH + '-without-unclear-no-norm'

FARMACOS_STRATIFIED_WITHOUT_UNCLEAR_AND_NO_NORM_AUGMENTED_SUBSET = FARMACOS_STRATIFIED_WITHOUT_UNCLEAR_AND_NO_NORM + '-augmented-subset'

FARMACOS_STRATIFIED_ONLY_NO_NORM = FARMACOS_STRATIFIED_PATH + '-only-no-norm'

FARMACOS_STRATIFIED_ONLY_NO_NORM_LESS_SENTENCES = FARMACOS_STRATIFIED_ONLY_NO_NORM + '-less-sentences'

FARMACOS_STRATIFIED_ONLY_NO_NORM_AUGMENTED_SUBSET = FARMACOS_STRATIFIED_ONLY_NO_NORM + '-augmented-subset'

FARMACOS_STRATIFIED_ONLY_UNCLEAR = FARMACOS_STRATIFIED_PATH + '-only-unclear'

FARMACOS_STRATIFIED_ONLY_UNCLEAR_LESS_SENTENCES = FARMACOS_STRATIFIED_ONLY_UNCLEAR + '-less-sentences'

'''
TAGGER_PATH = 'PlanTL-SPACCC_POS-TAGGER-9b64add/Med_Tagger'
sys.path.append(TAGGER_PATH)

from Med_Tagger import Med_Tagger
#tag = Med_Tagger()
'''

EMBEDDINGS_PATH = os.path.join(DATA_PATH,'embeddings')

GAZETTEER_PATH = os.path.join(DATA_PATH,'gazetteer')
NOMENCLATOR_PATH = os.path.join(GAZETTEER_PATH,'20190130_Nomenclator_de_Facturacion.csv')

GAZETTEER_SET_PATH = os.path.join(GAZETTEER_PATH,'principio_activo_gazetteer.txt')

POS_TAGGER_URL = 'https://github.com/PlanTL/SPACCC_POS-TAGGER/archive/master.zip'
POS_TAGGER_ZIP_PATH = os.path.join(DATA_PATH,'master')
POS_TAGGER_PATH = os.path.join(DATA_PATH,'SPACCC_POS-TAGGER-master','SPACCC_POS-TAGGER-master','Med_Tagger')

AUGMENTED_FIXED_PATH =AUGMENTED_NO_OTHER_DATA_PATH+'Fixed2'

AUGMENTED_SUBSET_PATH = AUGMENTED_FIXED_PATH + 'Subset'

AUGMENTED_SUBSET_PATH_ONLY_NO_NORM = AUGMENTED_FIXED_PATH + 'Subset' + '-only-no-norm'


def get_data():
    print('Downloading data...')
    if not os.path.exists(EMBEDDINGS_PATH):
        os.makedirs(EMBEDDINGS_PATH)
    embeddings = ['http://dcc.uchile.cl/~jperez/word-embeddings/fasttext-sbwc.vec.gz', \
        'http://dcc.uchile.cl/~jperez/word-embeddings/glove-sbwc.i25.vec.gz', \
        'https://zenodo.org/record/2542722/files/Embeddings_2019-01-01.zip']
    for e in embeddings:
        os.system('wget ' + e + ' -P ' + EMBEDDINGS_PATH)
    MANTRA_URL = 'https://files.ifi.uzh.ch/cl/mantra/ssc/EC21-v1.zip'
    os.system('wget ' + MANTRA_URL + ' -P ' + DATA_PATH)
    UMLS_URL = 'https://s3.eu-west-3.amazonaws.com/bsc-corpus/UMLS.zip'
    os.system('wget ' + UMLS_URL + ' -P ' + DATA_PATH)
    os.system('unzip ' + os.path.join(EMBEDDINGS_PATH,'Embeddings_2019-01-01.zip') + ' -d ' + os.path.join(EMBEDDINGS_PATH,'Embeddings'))
    os.system('gzip -d ' + os.path.join(EMBEDDINGS_PATH,'fasttext-sbwc.vec.gz'))
    os.system('gzip -d ' + os.path.join(EMBEDDINGS_PATH,'glove-sbwc.i25.vec.gz'))

    os.system('unzip ' + os.path.join(DATA_PATH,'EC21-v1.zip')  + ' -d ' + os.path.join(DATA_PATH,'EC21-v1'))
    os.system('unzip ' + os.path.join(DATA_PATH,'UMLS.zip')  + ' -d ' + os.path.join(DATA_PATH,'UMLS'))

def organize_dir():
    print('Organizing dir...')
    source = FARMACOS_PATH
    dest = FARMACOS_PATH + '-one'

    if not os.path.exists(dest):
            os.makedirs(dest)

    subdirs = os.listdir(source)

    for subdir in subdirs:
        files = os.listdir(source+'/'+subdir+'/')
        for f in files:
            shutil.copy(source+'/'+subdir+'/'+f, dest)

def augment_data(other = False):
    print('Augmenting data...')
    os.system("cut -d '|' -f1,12 " + MRCONSO_PATH + " > " + FILTERED_MRCONSO_PATH)
    engine_mrconso = create_engine('sqlite:///' + SQL_MRCONSO_PATH, echo=False)
    print('Reading file...')
    with open(FILTERED_MRCONSO_PATH) as f:
        mrconsoDF = pd.read_csv(f, sep='|', header=None,lineterminator='\n',names=['cui','source'])# index_col=0,
    print('Processing table...')                          
    print(mrconsoDF.head(1))
    mrconsoDF.to_sql('mrconso', con=engine_mrconso)#, if_exists='append')
    del(engine_mrconso)
    del(mrconsoDF)

    engine_mrsty = create_engine('sqlite:///' + SQL_MRSTY_PATH, echo = False)
    print('Reading file...')
    with open(MRSTY_PATH) as f:
        mrstyDF= pd.read_csv(f, sep='|', header=None,lineterminator='\n',names=['cui','ts','as','names','a2s','num','extra'])# index_col=0,
    print('Processing table...')                          
    print(mrstyDF.head(6))
    mrstyDF.to_sql('mrsty', con=engine_mrsty)#, if_exists='append')
    del(engine_mrsty)
    del(mrstyDF)

    os.system('sqlite3 -line ' + SQL_MRCONSO_PATH + " 'CREATE INDEX cuis ON mrconso (cui);'")
    os.system('sqlite3 -line ' + SQL_MRSTY_PATH + " 'CREATE INDEX cuis ON mrsty (cui);'")

    Concept = collections.namedtuple('Concept',['cui','len','text','offset'])
    Sentence = collections.namedtuple('Sentence',['id','text','concepts'])
    Datum = collections.namedtuple('Datum',['id','txt','annotation'])
    Annotation = collections.namedtuple('Annotation',['t','type','offset1','offset2','name','numNote','cui'])
    AnnotationSet = collections.namedtuple('AnnotationSet',['annotations'])

    MRCONSO = dataset.connect('sqlite:///' + SQL_MRCONSO_PATH)
    MRSTY = dataset.connect('sqlite:///' + SQL_MRSTY_PATH)


    def getAllSentencesFromXML(filePath):
        print('Parsing XML',filePath,'...')
        tree = ET.parse(filePath)
        print('Processing XML...')
        root = tree.getroot()
        sentences = [] # array of: [title,text,[concenpts]]
        for document in root:
            maxUnits = 3
            unitIn = 0
            for unit in document:
                if len(unit) < 2:
                    continue
                es = unit[1:]
                # treat extra spaces, dots, commas. For the moment, only at the end.
                for e in es:
                    if e.text == None: # for Medline
                        continue
                    if e.text[-1] == ' ' or e.text[-1] == ',' or e.text[-1] == '.':
                        e.text = e.text[:-1]
                        e.attrib['len'] = str(int(e.attrib['len'])-1)
                # Add concepts:
                concepts = []
                for e in es:
                    if e.text == None: # for Medline
                        continue
                    concepts.append(Concept(cui = e.attrib['cui'], len = e.attrib['len'], text = e.text, offset = e.attrib['offset']))
                sentence = Sentence(id = unit.attrib['id'], text = unit[0].text, concepts = concepts)
                sentences.append(sentence)
                unitIn += 1
        return sentences

    def createAnnotation(T,label,offset,length,name,numNote,cui):
        return Annotation(t = 'T' + str(T), type = label, offset1 = offset, offset2 = str(int(offset) + int(length)), name = name, numNote = str(numNote), cui = cui)

    def createAnnotationSet(sentence):
        uniqueConcepts = []
        currentConceptOffset = sentence.concepts[0].offset
        uniqueConcepts = {sentence.concepts[0].offset:[sentence.concepts[0]]}
        for concept in sentence.concepts:
            if concept.offset != currentConceptOffset:
                uniqueConcepts[concept.offset] = [concept]
                currentConceptOffset = concept.offset
            else:
                uniqueConcepts[currentConceptOffset].append(concept)

        # compare semantic types etc
        '''
        T116,"Amino Acid, Peptide, or Protein"
        T126,Enzyme

        Chemical
        T109,Organic Chemical
        T103,Chemical
        T104,Chemical Viewed Structurally
        T121,Pharmacologic Substance
        T196,"Element, Ion, or Isotope"
        T197,Inorganic Chemical
        '''
        proteinsTs = set(['T116','T126'])
        chemicalTs = set(['T109','T103','T104','T121','T196','T197'])
        annotations = []
        numNotes = 0
        for uniqueConcept, concepts in uniqueConcepts.items():
            ts = set([])
            for concept in concepts:
                rows = MRSTY['mrsty'].find(cui = concept.cui)
                if rows != None:
                    empty = True
                    for tt in rows:
                        empty = False
                        ts.add(tt['ts'])
                    if empty:
                        print('Warning: CUI', concept.cui, 'was not found in UMLS')
                else:
                    print('Warning: CUI', concept.cui, 'was not found in UMLS')
            label = ''
            if len(ts.intersection(proteinsTs)) > 0 and len(ts.intersection(chemicalTs)) == 0:
                label = 'PROTEINAS'
            elif len(ts.intersection(proteinsTs)) == 0 and len(ts.intersection(chemicalTs)) > 0:
                row2 = MRCONSO['mrconso'].find_one(cui = concept.cui, source='SNOMEDCT_US')
                if row2 != None:
                    label = 'NORMALIZABLES'
                else:
                    label = 'NO_NORMALIZABLES'
            else:
                #print('WHAT TO DO HERE)')
                if other:
                    label = 'OTHER'
                else:
                    continue
            annotations.append(createAnnotation(T = numNotes+1,label = label,offset = uniqueConcepts[uniqueConcept][0].offset,\
                length = uniqueConcepts[uniqueConcept][0].len,name = uniqueConcepts[uniqueConcept][0].text,numNote = numNotes+1,cui=uniqueConcepts[uniqueConcept][0].cui))
            numNotes += 1
        if len(annotations) == 0:
            return None
        return AnnotationSet(annotations = annotations)


    def writePair(sentence,annotationSet):
        if annotationSet == None:
            return
        txt = sentence.text
        ann = ''
        for annotation in annotationSet.annotations:
            ann = ann + annotation.t + '\t' + annotation.type + ' ' + annotation.offset1 + ' ' + annotation.offset2  \
                   + '\t' + annotation.name + '\n' + '#' + annotation.numNote + '\tAnnotatorNotes ' +  annotation.t \
                   + '\t' + annotation.cui + '\n'
        with open(AUGMENTED_DATA_PATH + '/' + sentence.id + '.txt','w') as f:
            f.write(txt)
        with open(AUGMENTED_DATA_PATH + '/' + sentence.id + '.ann','w') as f:
            f.write(ann)

    
    if other:
        AUGMENTED_DATA_PATH = AUGMENTED_OTHER_DATA_PATH
    else:
        AUGMENTED_DATA_PATH = AUGMENTED_NO_OTHER_DATA_PATH
    if not os.path.exists(AUGMENTED_DATA_PATH):
        os.makedirs(AUGMENTED_DATA_PATH)

    sentences = getAllSentencesFromXML(MANTRA_XML_FILE_EMEA_PATH)
    for index,sentence in enumerate(sentences):
        print('Processing and writing sentence ', sentence.id, ' (',index,'/',len(sentences),') of', MANTRA_XML_FILE_EMEA_PATH)
        writePair(sentence,createAnnotationSet(sentence))
        
    sentences = getAllSentencesFromXML(MANTRA_XML_FILE_MEDLINE_PATH)
    for index,sentence in enumerate(sentences):
        print('Processing and writing sentence ', sentence.id, ' (',index,'/',len(sentences),') of', MANTRA_XML_FILE_MEDLINE_PATH)
        writePair(sentence,createAnnotationSet(sentence))

    #get_pos(AUGMENTED_DATA_PATH)


def stratified_split(oversampling,delete = False):
    source = FARMACOS_PATH + '-one'
    if not oversampling:
        dest = FARMACOS_STRATIFIED_PATH
    elif not delete:
        dest = FARMCOS_STRATIFIED_OVERSAMPLING_WITHOUT_DELETING_PATH
    else:
        dest = FARMACOS_STRATIFIED_OVERSAMPLING_DELETING
    if not os.path.exists(dest):
        os.makedirs(dest)

    def get_frequencies(annotation):
        content = ''
        freqs = {}
        with open(source+'/'+annotation+'.ann','r') as f:
            content = f.read()
        freqs['NORMALIZABLES'] = content.count('NORMALIZABLES') # beware: non-overlapping, but without spaces
        freqs['NO_NORMALIZABLES'] = content.count('NO_NORMALIZABLES')
        freqs['PROTEINAS'] = content.count('PROTEINAS')
        freqs['UNCLEAR'] = content.count('UNCLEAR')
        return freqs

    def assign_labels(data_array):
        labels = []
        for x in data_array:
            frequencies = get_frequencies(x)
            if frequencies['NO_NORMALIZABLES'] > 0:
                labels.append('NO_NORMALIZABLES')
            elif frequencies['UNCLEAR'] > 0:
                labels.append('UNCLEAR')
            elif frequencies['PROTEINAS'] >= frequencies['NORMALIZABLES']:
                labels.append('PROTEINAS')
            else:
                labels.append('NORMALIZABLES')
        return labels

    def concat(l):
        s = ''
        for x in l:
            s += x
        return s
    def duplicate_with_or_without_other_labels(annotation,label,delete):
        if not delete:
            content = ''
            with open(source+'/'+annotation+'.ann','r') as f:
                content = f.read()
            return content
        else:
            with open(source+'/'+annotation+'.ann','r') as f:
                lines = f.readlines()
            dup_lines = []
            for l in range(0, len(lines)-1, 2):
                if (label == 'NO_NORMALIZABLES' and lines[l].find('NO_NORMALIZABLES') != -1) or (label == 'UNCLEAR' and lines[l].find('UNCLEAR') != -1):
                    dup_lines.append(lines[l])
                    dup_lines.append(lines[l+1])
            return concat(dup_lines)


    files = os.listdir(source)
    annotations = []
    for f in files:
        if f.endswith(".ann"):
            annotations.append(f[:-4])
    labels = assign_labels(annotations)
    X = annotations
    y = labels
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, stratify = y, random_state=SEED)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1/(0.1+0.8), stratify = y_train, random_state=SEED)

    if not os.path.exists(dest+'/train'):
        os.makedirs(dest+'/train')
    if not os.path.exists(dest+'/valid'):
        os.makedirs(dest+'/valid')
    if not os.path.exists(dest+'/test'):
        os.makedirs(dest+'/test')
    print(len(X))
    print(len(X_train))
    print(len(X_val))
    print(len(X_test))
    for a, label in zip(X_train, y_train):
        if oversampling:
            # Oversampling of the minority classes
            if label == 'NO_NORMALIZABLES':
                dupli = duplicate_with_or_without_other_labels(a,label,delete)
                for i in range(0,29): # we want 30 of them, so 29 extra copies
                    with open(dest + '/' + 'train'+'/'+a+'_copy'+str(i+1) +'.ann','w') as f:
                        f.write(dupli)
                    shutil.copy(source+'/'+a+'.txt', dest + '/' + 'train'+'/'+a+'_copy'+str(i+1) +'.txt')
                    shutil.copy(source+'/'+a+'.ann2', dest + '/' + 'train'+'/'+a+'_copy'+str(i+1) +'.ann2')
            if label == 'UNCLEAR':
                dupli = duplicate_with_or_without_other_labels(a,label,delete)
                for i in range(0,19): # we want 20 of them, so 19 extra copies
                    with open(dest + '/' + 'train'+'/'+a+'_copy'+str(i+1) +'.ann','w') as f:
                        f.write(dupli)
                    shutil.copy(source+'/'+a+'.txt', dest + '/' + 'train'+'/'+a+'_copy'+str(i+1) +'.txt')
                    shutil.copy(source+'/'+a+'.ann2', dest + '/' + 'train'+'/'+a+'_copy'+str(i+1) +'.ann2')
        shutil.copy(source+'/'+a+'.ann', dest + '/' + 'train'+'/'+a+'.ann')
        shutil.copy(source+'/'+a+'.ann2', dest + '/' + 'train'+'/'+a+'.ann2')
        shutil.copy(source+'/'+a+'.txt', dest + '/' + 'train'+'/'+a+'.txt')

    for a in X_val:
        shutil.copy(source+'/'+a+'.ann', dest + '/' + 'valid'+'/'+a+'.ann')
        shutil.copy(source+'/'+a+'.ann2', dest + '/' + 'valid'+'/'+a+'.ann2')
        shutil.copy(source+'/'+a+'.txt', dest + '/' + 'valid'+'/'+a+'.txt')

    for a in X_test:
        shutil.copy(source+'/'+a+'.ann', dest + '/' + 'test'+'/'+a+'.ann')
        shutil.copy(source+'/'+a+'.ann2', dest + '/' + 'test'+'/'+a+'.ann2')
        shutil.copy(source+'/'+a+'.txt', dest + '/' + 'test'+'/'+a+'.txt')



def get_pos(path):
    sys.path.append(POS_TAGGER_PATH)
    from Med_Tagger import Med_Tagger
    tag = Med_Tagger()
    print('Getting POS of ' + path)
    files = os.listdir(path)
    import time
    time.sleep(50)

    for file in files:
        if file.endswith(".txt"):
            with open(path + '/' + file,'r') as f:
                content = f.read()
                parsed = tag.parse(content)
                while len(parsed) == 0:
                    parsed = tag.parse(content)
                tag.write_brat(content,parsed,path + '/' + file[:-4] + '.ann2')
    del(tag)
def generate_experiments():
    print('Creating experiments...')
    #create_experiments.create_experiments()
    #create_experiments.create_experiments2()
    #create_experiments.create_experiments3()
    create_experiments.create_experiments4()

'''
def simple_split():
    source = '../farmacos-final-One-POS2'
    dest = '../farmacos-final-Simple-Split-With-POS2'

    files = os.listdir(source)

    annotations = []
    pos_tags = []

    for f in files:
        if f.endswith(".ann"):
            annotations.append(f[:-4])

    random.shuffle(annotations)
    train = annotations[:math.floor(len(annotations)*0.8)]
    valid = annotations[math.floor(len(annotations)*0.8):math.floor(len(annotations)*0.9)]
    test = annotations[math.floor(len(annotations)*0.9):len(annotations)]

    if not os.path.exists(dest+'/train'):
        os.makedirs(dest+'/train')
    if not os.path.exists(dest+'/valid'):
        os.makedirs(dest+'/valid')
    if not os.path.exists(dest+'/test'):
        os.makedirs(dest+'/test')
    print(len(annotations))
    print(len(train))
    print(len(valid))
    print(len(test))
    for a in train:
        shutil.copy(source+'/'+a+'.ann', dest + '/' + 'train'+'/'+a+'.ann')
        shutil.copy(source+'/'+a+'.ann2', dest + '/' + 'train'+'/'+a+'.ann2')
        shutil.copy(source+'/'+a+'.txt', dest + '/' + 'train'+'/'+a+'.txt')

    for a in valid:
        shutil.copy(source+'/'+a+'.ann', dest + '/' + 'valid'+'/'+a+'.ann')
        shutil.copy(source+'/'+a+'.ann2', dest + '/' + 'valid'+'/'+a+'.ann2')
        shutil.copy(source+'/'+a+'.txt', dest + '/' + 'valid'+'/'+a+'.txt')

    for a in test:
        shutil.copy(source+'/'+a+'.ann', dest + '/' + 'test'+'/'+a+'.ann')
        shutil.copy(source+'/'+a+'.ann2', dest + '/' + 'test'+'/'+a+'.ann2')
        shutil.copy(source+'/'+a+'.txt', dest + '/' + 'test'+'/'+a+'.txt')
'''

def build_gazetteer():
    # Get CSV for building the Gazetteer: follwing URL (can't be easiliy downloaded by the script because the file is dynamically generated. A headless browser woould do tje job)
    # https://www.mscbs.gob.es/profesionales/nomenclator.do?fechabajahasta=&generico=&codnacional=&metodo=buscarProductos&metodo=buscarProductos&nomlab=&especialidad=&priact_dos=&d-4015021-e=1&priact_uno=&buscar=Buscar&fechaaltadesde=01%2F01%2F1980&fechaaltahasta=&estado=&priact_tres=&6578706f7274=1&ngenerico=&nomaport=&priact_cuatro=&fechabajadesde=
    'Building gazetteer...'
    df_nomenclator = pd.read_table(NOMENCLATOR_PATH,sep=',')
    l_nomenclator = df_nomenclator['Principio activo o asociación de principios activos'].tolist()
    # check if nan
    l_nomenclator_filtered = list(filter(lambda x: x == x,l_nomenclator))
    # remove final ','
    l_nomenclator_filtered = list(map(lambda x: x if str(x)[-1] != ',' else x[:-1],l_nomenclator_filtered))
    gaz_set = set([])
    for term in l_nomenclator_filtered:
        words = str(term).split()
        for word in words:
            for c in range(0,len(word)):
                if word[c] == ',':
                    word = word[0:c] + ' ' + word[c+1:len(word)]
                elif word[c] == '(' or word[c] == ')':
                    word = word[0:c] + ' ' + word[c+1:len(word)]
            for word2 in word.split():
                w = word2.lower()
                if w[0] == '-':
                    w = w[1:]
                if w[-1] == '-':
                    w = w[:-1]
                if not w.isdigit() and w not in ['de','por','para','a','te']:
                    gaz_set.add(w)
    with open(GAZETTEER_SET_PATH,'w') as f:
        f.writelines(["%s\n" % item  for item in gaz_set])


def get_pos_tagger():
    print('Getting POS Tagger...')
    os.system('wget ' + POS_TAGGER_URL + ' -P ' + DATA_PATH)
    os.system('unzip ' + POS_TAGGER_ZIP_PATH + ' -d ' + os.path.join(DATA_PATH,'SPACCC_POS-TAGGER-master'))
    os.system(os.path.join(DATA_PATH,'SPACCC_POS-TAGGER-master','SPACCC_POS-TAGGER-master','compila_freeling.sh'))

def add_augmented_data(oversampling, delete = False, other = False):
    print('Adding augmented data...')
    if other:
        source_augmented = AUGMENTED_OTHER_DATA_PATH
    else:
        source_augmented = AUGMENTED_NO_OTHER_DATA_PATH
    if oversampling:
        if delete:
            source_farmacos = FARMACOS_STRATIFIED_OVERSAMPLING_DELETING
        else:
            source_farmacos = FARMCOS_STRATIFIED_OVERSAMPLING_WITHOUT_DELETING_PATH
    else:
        source_farmacos = FARMACOS_STRATIFIED_PATH
    '''
    FARMACOS_STRATIFIED_AUGMENTED_NO_OTHER_PATH = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split-augmented-no-other')
FARMACOS_STRATIFIED_AUGMENTED_OTHER_PATH = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split-augmented-other')
FARMACOS_STRATIFIED_OVERSAMPLING_WITHOUT_DELETING_AUGMENTED_NO_OTHER_PATH  = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split-oversampling-augmented-no-other')
FARMACOS_STRATIFIED_OVERSAMPLING_WITHOUT_DELETING_AUGMENTED_OTHER_PATH  = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split-oversampling-augmented-other')
FARMACOS_STRATIFIED_OVERSAMPLING_DELETING_AUGMENTED_NO_OTHER_PATH  = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split-oversampling-deleting-augmented-no-other')
FARMACOS_STRATIFIED_OVERSAMPLING_DELETING_AUGMENTED_OTHER_PATH  = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split-oversampling-deleting-augmented-other')
'''
    if not oversampling:
        if not other:
            dest = FARMACOS_STRATIFIED_AUGMENTED_NO_OTHER_PATH
        else:
            dest = FARMACOS_STRATIFIED_AUGMENTED_OTHER_PATH
    else:
        if not delete:
            if not other:
                dest = FARMACOS_STRATIFIED_OVERSAMPLING_WITHOUT_DELETING_AUGMENTED_NO_OTHER_PATH
            else:
                dest = FARMACOS_STRATIFIED_OVERSAMPLING_WITHOUT_DELETING_AUGMENTED_OTHER_PATH
        else:
            if not other:
                dest = FARMACOS_STRATIFIED_OVERSAMPLING_DELETING_AUGMENTED_NO_OTHER_PATH
            else:
                dest = FARMACOS_STRATIFIED_OVERSAMPLING_DELETING_AUGMENTED_OTHER_PATH
    if not os.path.exists(dest):
        os.system('cp -r ' + source_farmacos + ' ' + dest)
        os.system('cp -rT ' + source_augmented + ' ' + os.path.join(dest,'train'))


def brat_to_conll_for_POS_and_augmented():
    sys.path.append(POS_TAGGER_PATH)
    from Med_Tagger import Med_Tagger
    tag = Med_Tagger()
    for path in [FARMACOS_STRATIFIED_PATH,FARMACOS_STRATIFIED_OVERSAMPLING_DELETING,FARMACOS_STRATIFIED_AUGMENTED_OTHER_PATH,\
        FARMACOS_STRATIFIED_AUGMENTED_NO_OTHER_PATH,FARMACOS_STRATIFIED_OVERSAMPLING_WITHOUT_DELETING_AUGMENTED_OTHER_PATH,\
        FARMACOS_STRATIFIED_OVERSAMPLING_DELETING_AUGMENTED_NO_OTHER_PATH,FARMACOS_STRATIFIED_OVERSAMPLING_WITHOUT_DELETING_AUGMENTED_NO_OTHER_PATH]:

        if not os.path.exists(path):
            continue
        if not os.path.exists(path + '-CONLL'):
            os.makedirs(path + '-CONLL')
        for dataset in ['train','valid','test']:
            brat_to_conll(input_folder = os.path.join(path,dataset), output_filepath = os.path.join(path + '-CONLL',dataset + '.txt'), tag = tag)
    del(tag)

def fix_augmented():
    fix_brat3.fix_malformatted_brat(AUGMENTED_NO_OTHER_DATA_PATH,AUGMENTED_FIXED_PATH)

def select_proportional_subset_of_augmented(source):
    print('Selecting proportional subset of',source)
    def get_frequencies(annotation_filepath):
        content = ''
        freqs = {}
        with open(annotation_filepath,'r') as f:
            content = f.read()
        freqs['NORMALIZABLES'] = content.count('NORMALIZABLES') # beware: non-overlapping, but without spaces
        freqs['NO_NORMALIZABLES'] = content.count('NO_NORMALIZABLES')
        freqs['PROTEINAS'] = content.count('PROTEINAS')
        freqs['UNCLEAR'] = content.count('UNCLEAR')
        return freqs
    dest = AUGMENTED_SUBSET_PATH
    if not os.path.exists(dest):
        os.makedirs(dest)
    nsamples = 10000
    proportion_normalizables_original = 4448/(3009+4448)
    proportion_proteinas_original = 3009/(3009+4448)
    num_normalizables = math.floor(nsamples*proportion_normalizables_original)
    num_proteinas = math.floor(nsamples*proportion_proteinas_original)
    path = os.path.join('..')
    text_filepaths = sorted(glob.glob(os.path.join(source, '*.txt')))
    normalizables = 0
    proteinas = 0
    random.seed = SEED
    random.shuffle(text_filepaths)
    for text_filepath in text_filepaths:
        if normalizables == num_normalizables and proteinas == num_proteinas:
            break
        base_filename = os.path.splitext(os.path.basename(text_filepath))[0]
        annotation_filepath = os.path.join(os.path.dirname(text_filepath), base_filename + '.ann')
        freqs = get_frequencies(annotation_filepath)
        if freqs['NO_NORMALIZABLES'] > 0:
            continue
        elif freqs['UNCLEAR'] > 0:
            continue
        elif normalizables < num_normalizables and freqs['NORMALIZABLES'] == 1 and freqs['PROTEINAS'] == 0:
            normalizables += 1
        elif proteinas < num_proteinas and freqs['NORMALIZABLES'] == 0 and freqs['PROTEINAS'] == 1:
            proteinas += 1
        else:
            continue
        shutil.copy(text_filepath, os.path.join(dest,base_filename+'.txt'))
        shutil.copy(annotation_filepath, os.path.join(dest,base_filename+'.ann'))
        annotation_filepath2 = annotation_filepath +'2'
        shutil.copy(annotation_filepath2, os.path.join(dest,base_filename+'.ann2'))
    print('Kept',normalizables,'normalizables and',proteinas,'proteinas')


def remove_labels(labels,src,dst):
    print('Removing labels',str(labels),'from',src,'(dst=',dst,')')
    if not os.path.exists(dst):
        os.makedirs(dst)
    for dataset in ['train','valid','test']:
        source = os.path.join(src,dataset)
        dest = os.path.join(dst,dataset)
        if not os.path.exists(dest):
            os.makedirs(dest)
        ann_filepaths = sorted(glob.glob(os.path.join(source, '*.ann')))
        for ann_filepath in ann_filepaths:
            with open(ann_filepath,'r') as f:
                lines = f.readlines()
            i = 0
            content = ''
            while i < len(lines):
                #print(i,len(lines),ann_filepath)
                to_remove = False
                for label in labels:
                     if lines[i].count(label) > 0:
                        if i+1 != len(lines) and lines[i+1][0] == '#':
                            i += 2
                        else:
                            i += 1
                        to_remove = True
                        break
                if to_remove:
                    continue
                '''
                if lines[i].count('NO_NORMALIZABLES') > 0 or lines[i].count('UNCLEAR') > 0:
                    i += 2 
                '''
                #else:
                
                if i+1 != len(lines) and lines[i+1][0] == '#':
                    #content = content + lines[i] + '\n' + lines[i+1] +'\n'
                    content = content + lines[i] + lines[i+1]
                    i += 2
                else:
                    content = content + lines[i] #+ '\n'
                    i += 1
            base_filename = os.path.splitext(os.path.basename(ann_filepath))[0]
            dest_ann_filepath = os.path.join(dest, base_filename + '.ann')
            with open(dest_ann_filepath,'w') as f:
                f.write(content)
            source_ann2_filepath = os.path.join(source, base_filename + '.ann2')
            dest_ann2_filepath = os.path.join(dest, base_filename + '.ann2')
            shutil.copy(source_ann2_filepath,dest_ann2_filepath)
            source_txt_filepath = os.path.join(source, base_filename + '.txt')
            dest_txt_filepath = os.path.join(dest, base_filename + '.txt')
            shutil.copy(source_txt_filepath,dest_txt_filepath)
        
def add_augmented_subset_data(farmacos, augmented, dest):
    if not os.path.exists(dest):
        #os.makedirs(dest)
        shutil.copytree(farmacos,dest)

    dest_train = os.path.join(dest,'train')
    text_filepaths = sorted(glob.glob(os.path.join(augmented, '*.txt')))
    i = 0
    for text_filepath in text_filepaths:
        i += 1
        print('Adding',i,'of',len(text_filepaths))
        base_filename = os.path.splitext(os.path.basename(text_filepath))[0]
        shutil.copy(text_filepath,os.path.join(dest_train,base_filename+'.txt'))
        shutil.copy(os.path.join(augmented,base_filename+'.ann'),os.path.join(dest_train,base_filename+'.ann'))
        shutil.copy(os.path.join(augmented,base_filename+'.ann2'),os.path.join(dest_train,base_filename+'.ann2'))

def select_subset_augmented_only_label(src, dst, label):
    source = src
    print('Selecting subset of',source,'with only',label,'and moving data to',dst)
    def get_frequencies(annotation_filepath):
        content = ''
        freqs = {}
        with open(annotation_filepath,'r') as f:
            content = f.read()
        freqs['NORMALIZABLES'] = content.count('\tNORMALIZABLES') # beware: non-overlapping, but without spaces
        freqs['NO_NORMALIZABLES'] = content.count('NO_NORMALIZABLES')
        freqs['PROTEINAS'] = content.count('PROTEINAS')
        freqs['UNCLEAR'] = content.count('UNCLEAR')
        return freqs
    dest = dst
    if not os.path.exists(dest):
        os.makedirs(dest)
    nsamples = 50
    path = os.path.join('..')
    text_filepaths = sorted(glob.glob(os.path.join(source, '*.txt')))
    counter = 0
    random.seed = SEED
    random.shuffle(text_filepaths)
    for text_filepath in text_filepaths:
        if counter >= nsamples:
            break
        base_filename = os.path.splitext(os.path.basename(text_filepath))[0]
        annotation_filepath = os.path.join(os.path.dirname(text_filepath), base_filename + '.ann')
        freqs = get_frequencies(annotation_filepath)
        skip = False
        for key, value in freqs.items():
            if key != label and value > 0:
                skip = True
                break
        if skip:
            continue
        if freqs[label] > 0:
            counter += 1
        else:
            continue
        shutil.copy(text_filepath, os.path.join(dest,base_filename+'.txt'))
        shutil.copy(annotation_filepath, os.path.join(dest,base_filename+'.ann'))
        annotation_filepath2 = annotation_filepath +'2'
        shutil.copy(annotation_filepath2, os.path.join(dest,base_filename+'.ann2'))
    print('Kept',counter,label)


def get_start_and_end_offset_of_token_from_spacy(token):
    start = token.idx
    end = start + len(token)
    return start, end

def get_sentences_and_tokens_from_spacy(text, spacy_nlp):
    document = spacy_nlp(text)
    # sentences
    sentences = []
    for span in document.sents:
        sentence = [document[i] for i in range(span.start, span.end)]
        sentence_tokens = []
        for token in sentence:
            token_dict = {}
            token_dict['start'], token_dict['end'] = get_start_and_end_offset_of_token_from_spacy(token)
            token_dict['text'] = text[token_dict['start']:token_dict['end']]
            if token_dict['text'].strip() in ['\n', '\t', ' ', '']:
                continue
            # Make sure that the token text does not contain any space
            if len(token_dict['text'].split(' ')) != 1:
                print("WARNING: the text of the token contains space character, replaced with hyphen\n\t{0}\n\t{1}".format(token_dict['text'], 
                                                                                                                           token_dict['text'].replace(' ', '-')))
                token_dict['text'] = token_dict['text'].replace(' ', '-')
            sentence_tokens.append(token_dict)
        sentences.append(sentence_tokens)
    return sentences

def remove_phrases_without_annotations_for_minority(source,dest):
    random.seed(SEED)
    import spacy
    shutil.copytree(source, dest)
    #subdirs = os.listdir(dest)
    #subdirs = ['train']
    subdirs = ['train','valid']
    for subdir in subdirs:
        #files = os.listdir(os.path.join(source,subdir))
        text_filepaths = sorted(glob.glob(os.path.join(dest,subdir, '*.txt')))
        i = 0
        for text_filepath in text_filepaths:
            i += 1
            #print(i,'of',len(text_filepaths))
            base_filename = os.path.splitext(os.path.basename(text_filepath))[0]
            annotation_filepath = os.path.join(os.path.dirname(text_filepath), base_filename + '.ann')
            annotation2_filepath = os.path.join(os.path.dirname(text_filepath), base_filename + '.ann2')
            with open(annotation_filepath,'r') as f_ann:
                content = f_ann.read()
                if len(content) == 0:
                    #print('empty')
                    os.unlink(text_filepath)
                    os.unlink(annotation_filepath)
                    os.unlink(annotation2_filepath)
                '''
                else:
                    annotations = []
                    for line in content.splitlines():
                        anno = line.split()
                        id_anno = anno[0]
                        # parse entity
                        if id_anno[0] == 'T':
                            entity = {}
                            entity['id'] = id_anno
                            entity['type'] = anno[1]
                            entity['start'] = int(anno[2])
                            entity['end'] = int(anno[3])
                            #entity['text'] = elimina_tildes(' '.join(anno[4:]))
                            entity['text'] = ' '.join(anno[4:])
                            annotations.append(tuple((entity['start'],entity['end'])))
                    #with open(text_filepath,'r+') as f_txt:
                    new_text = ''
                    with open(text_filepath,'r') as f_txt:
                        spacy_nlp = spacy.load('es')
                        text = f_txt.read()
                        new_text = text
                        sentences = get_sentences_and_tokens_from_spacy(text,spacy_nlp)
                        #new_text = ''
                        sentence_has_annotation_counter = 0
                        sentence_counter = 0
                        for sentence in sentences:    
                            token_start = sentence[0]['start']
                            token_end = sentence[len(sentence)-1]['end']
                            for annotation in annotations:
                                ann_start, ann_end = annotation
                                if ann_start >= token_start and ann_start < token_end:
                                    sentence_has_annotation_counter += 1
                            sentence_counter += 1
                        prop_to_keep = round(100*sentence_has_annotation_counter/sentence_counter)
                        #print(base_filename,prop_to_keep,sentence_has_annotation_counter,sentence_counter)
                        #print(text)
                        #print(content)
                        for sentence in sentences:
                            sentence_has_annotation = False
                            token_start = sentence[0]['start']
                            token_end = sentence[len(sentence)-1]['end']
                            for annotation in annotations:
                                ann_start, ann_end = annotation
                                if ann_start >= token_start and ann_start < token_end:
                                    sentence_has_annotation = True
                                    break
                            if sentence_has_annotation:
                                #new_text += text[token_start:token_end]
                                pass
                            else:
                                
                                kept = False
                                ran = random.randint(1,100)
                                if ran <= prop_to_keep:
                                    #new_text += text[token_start:token_end]
                                    kept = True
                                else:
                                    xx = len(new_text)
                                    new_text = new_text[0:token_start]+(len(text[token_start:token_end])*' ') + new_text[token_end:len(new_text)]
                                    yy = len(new_text)
                                    if xx != yy:
                                        input('hey')
                                #print(kept)
                                #print(prop_to_keep,ran,kept)
                    #print(new_text)
                    with open(text_filepath,'w') as f_txt:
                        f_txt.write(new_text)
                '''






def main():
    #get_data()
    #organize_dir()
    #get_pos_tagger()
    #get_pos(path = FARMACOS_PATH + '-one')
    #stratified_split(oversampling = False)
    #stratified_split(oversampling = True, delete = False)
    # Beware: some of the annotations of the augmented data are mal-formatted.
    # This is fixed with fix_augmented()
    #augment_data(other = False)
    #get_pos(AUGMENTED_NO_OTHER_DATA_PATH)
    #build_gazetteer()
    #add_augmented_data(oversampling = False, delete = False, other = False)
    #add_augmented_data(oversampling = True, delete = False, other = False)
    #brat_to_conll_for_POS_and_augmented()
    #fix_augmented()
    #select_proportional_subset_of_augmented(AUGMENTED_FIXED_PATH)
    #remove_labels(labels = ['UNCLEAR','NO_NORMALIZABLES'], src = FARMACOS_STRATIFIED_PATH, dst = FARMACOS_STRATIFIED_WITHOUT_UNCLEAR_AND_NO_NORM)
    #add_augmented_subset_data(farmacos = FARMACOS_STRATIFIED_WITHOUT_UNCLEAR_AND_NO_NORM, augmented = AUGMENTED_SUBSET_PATH, dest = FARMACOS_STRATIFIED_WITHOUT_UNCLEAR_AND_NO_NORM_AUGMENTED_SUBSET)
    
    #remove_labels(labels = ['UNCLEAR','PROTEINAS','\tNORMALIZABLES'], src = FARMACOS_STRATIFIED_PATH, dst = FARMACOS_STRATIFIED_ONLY_NO_NORM)
    #select_subset_augmented_only_label(src = AUGMENTED_FIXED_PATH, dst =AUGMENTED_SUBSET_PATH_ONLY_NO_NORM , label = 'NO_NORMALIZABLES')
    #add_augmented_subset_data(farmacos = FARMACOS_STRATIFIED_ONLY_NO_NORM, augmented = AUGMENTED_SUBSET_PATH_ONLY_NO_NORM, dest = FARMACOS_STRATIFIED_ONLY_NO_NORM_AUGMENTED_SUBSET)
    
    #remove_labels(labels = ['NO_NORMALIZABLES','PROTEINAS','\tNORMALIZABLES'], src = FARMACOS_STRATIFIED_PATH, dst = FARMACOS_STRATIFIED_ONLY_UNCLEAR)
    
    #remove_phrases_without_annotations_for_minority(source = FARMACOS_STRATIFIED_ONLY_NO_NORM, dest =FARMACOS_STRATIFIED_ONLY_NO_NORM_LESS_SENTENCES)
    remove_phrases_without_annotations_for_minority(source = FARMACOS_STRATIFIED_ONLY_UNCLEAR, dest =FARMACOS_STRATIFIED_ONLY_UNCLEAR_LESS_SENTENCES)

    generate_experiments()
if __name__ == "__main__":
    main()
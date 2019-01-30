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

FARMACOS_STRATIFIED_PATH = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split')
FARMCOS_STRATIFIED_OVERSAMPLING_WITHOUT_DELETING_PATH = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split-oversampling')
FARMACOS_STRATIFIED_OVERSAMPLING_DELETING = os.path.join(DATA_PATH,'farmacos-final-one-stratified-split-oversampling-deleting')

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

    get_pos(AUGMENTED_DATA_PATH)


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
def create_experiments():
    print('Creating experiments...')
    pass

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



def main():
    #get_data()
    #organize_dir()
    #get_pos_tagger()
    get_pos(path = FARMACOS_PATH + '-one')
    #stratified_split(oversampling = False)
    #stratified_split(oversampling = True, delete = False)
    #augment_data(other = False)
    # shouldn't we treat empty annotations, both ann and ann2? How? Removing them?
    #create_experiments()
    #build_gazetteer()
if __name__ == "__main__":
    main()
import dataset
import xml.etree.ElementTree as ET
import ast
import collections
MRCONSO = dataset.connect('sqlite:///../mrconso.db')
MRSTY = dataset.connect('sqlite:///../mrsty.db')

XML_PATH = '../EC21.d/'
XML_FILE_EMEA = XML_PATH + 'EMEA_es_EC21_man.xml'
XML_FILE_MEDLINE = XML_PATH + 'Medline_es_EC21_man.xml'

Concept = collections.namedtuple('Concept',['cui','len','text','offset'])
Sentence = collections.namedtuple('Sentence',['id','text','concepts'])
Datum = collections.namedtuple('Datum',['id','txt','annotation'])
Annotation = collections.namedtuple('Annotation',['t','type','offset1','offset2','name','numNote','cui'])
AnnotationSet = collections.namedtuple('AnnotationSet',['annotations'])
'''
T1  NORMALIZABLES 3688 3692 CDDP
#1  AnnotatorNotes T1   387318005
'''
AUGMENTED_DATA_PATH = '../augmentedData/'

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
            #sentence = []
            #sentence.append(unit.attrib['id'])
            #sentence.append(unit[0].text)
            #sentence = Sentence(id = unit.attrib['id'], text = unit[0].text, concepts = [])
            es = unit[1:]
            # treat extra spaces, dots, commas. For the moment, only at the end.
            for e in es:
                if e.text[-1] == ' ' or e.text[-1] == ',' or e.text[-1] == '.':
                    e.text = e.text[:-1]
                    e.attrib['len'] = str(int(e.attrib['len'])-1)
            # Add concepts:
            concepts = []
            for e in es:
                #concepts.append(ET.tostring(e, encoding='utf8', method='xml'))
                #concepts.append(tuple((e.attrib['cui'],e.attrib['len'],e.text)))
                concepts.append(Concept(cui = e.attrib['cui'], len = e.attrib['len'], text = e.text, offset = e.attrib['offset']))
            # compare concepts: TODO
            #sentence.append(concepts)
            #sentences.append(sentence)
            #sentence.concepts = concepts
            sentence = Sentence(id = unit.attrib['id'], text = unit[0].text, concepts = concepts)
            sentences.append(sentence)
            unitIn += 1
            '''
            if (unitIn > maxUnits):
                break
            '''
        #break
    return sentences

def createAnnotation(T,label,offset,length,name,numNote,cui):
    return Annotation(t = 'T' + str(T), type = label, offset1 = offset, offset2 = str(int(offset) + int(length) - 1), name = name, numNote = str(numNote), cui = cui)

def createAnnotationSet(sentence):
    # Annotation = collections.namedtuple('Annotation',['t','type','offset1','offset2','name','numNote','cui'])
    # Concept = collections.namedtuple('Concept',['cui','len','text','offset'])
    # MRCONSO, MRSTY
    uniqueConcepts = []
    currentConceptOffset = sentence.concepts[0].offset#currentConceptText = sentence.concepts[0].text
    #uniqueConcepts.append(sentence.concepts[0].text,[sentence.concepts[0]])
    #uniqueConcepts = {sentence.concepts[0].text:[sentence.concepts[0]]}
    uniqueConcepts = {sentence.concepts[0].offset:[sentence.concepts[0]]}
    for concept in sentence.concepts:
        if concept.offset != currentConceptOffset:#if concept.text != currentConceptText:
            #uniqueConcepts.append(concept.text,[])
            uniqueConcepts[concept.offset] = [concept]#uniqueConcepts[concept.text] = [concept]
            currentConceptOffset = concept.offset #currentConceptText = concept.text
        else:
            uniqueConcepts[currentConceptOffset].append(concept)#uniqueConcepts[currentConceptText].append(concept)

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
            #row = MRSTY['mrconso'].find_one(cui = concept.cui) # the table is named mrconso instead of mrsty
            rows = MRSTY['mrconso'].find(cui = concept.cui)
            if rows != None:
                empty = True
                for tt in rows:
                    empty = False
                    #ts.append(tt['ts'])
                    ts.add(tt['ts'])
                if empty:
                    print('Warning: CUI', concept.cui, 'was not found in UMLS')
            else:
                print('Warning: CUI', concept.cui, 'was not found in UMLS')
        #ts = set(ts)
        #print()
        #print(ts)
        label = ''
        if len(ts.intersection(proteinsTs)) > 0 and len(ts.intersection(chemicalTs)) == 0:
            label = 'PROTEINAS'
        elif len(ts.intersection(proteinsTs)) == 0 and len(ts.intersection(chemicalTs)) > 0:
            row2 = MRCONSO['mrconso'].find_one(cui = concept.cui, source='SNOMEDCT_US')
            if row2 != None:
                label = 'NORMALIZABLES'
            else:
                label = 'NO_NORMALIZABLES'
            '''
            if row2['source'] == 'SNOMEDCT_US':
                label = 'NORMALIZABLES'
            else:
                label = 'NO_NORMALIZABLES'
            '''
        else:
            #print('WHAT TO DO HERE)')
            label = 'OTHER'
        #print(label)
        annotations.append(createAnnotation(T = numNotes+1,label = label,offset = uniqueConcepts[uniqueConcept][0].offset,\
            length = uniqueConcepts[uniqueConcept][0].len,name = uniqueConcepts[uniqueConcept][0].text,numNote = numNotes+1,cui=uniqueConcepts[uniqueConcept][0].cui)) # T? cui?
       #print()
        numNotes += 1
    return AnnotationSet(annotations = annotations)


def writePair(sentence,annotationSet):
    #AUGMENTED_DATA_PATH
    # Annotation = collections.namedtuple('Annotation',['t','type','offset1','offset2','name','numNote','cui'])
    '''
    T1  NORMALIZABLES 3688 3692 CDDP
    #1  AnnotatorNotes T1   387318005
    '''
    txt = sentence.text
    ann = ''
    #print('Parell va:')
    #print(txt)
    #print(annotationSet.annotations)
    for annotation in annotationSet.annotations:
        #print('name', annotation.name)
        ann = ann + annotation.t + ' ' + annotation.type + ' ' + annotation.offset1 + ' ' + annotation.offset2  \
               + ' ' + annotation.name + '\n' + '#' + annotation.numNote + ' AnnotatorNotes ' +  annotation.t \
               + ' \t ' + annotation.cui + '\n'
        #print(ann)
    #print()
    #return None
    '''
    print(sentence.id + '.txt:')
    print(txt)
    print()
    print(sentence.id + '.ann:')
    print(ann)
    print()
    print()
    '''
    #print('Adding sentence ' + sentence.id)
    with open(AUGMENTED_DATA_PATH + sentence.id + '.txt','w') as f:
        f.write(txt)
    with open(AUGMENTED_DATA_PATH + sentence.id + '.ann','w') as f:
        f.write(ann)

def main():
    sentences = getAllSentencesFromXML(XML_FILE_EMEA)
    #annotations = []
    for index,sentence in enumerate(sentences):
        print('Processing and writing sentence ', sentence.id, ' (',index,'/',len(sentences),') of', XML_FILE_EMEA)
        writePair(sentence,createAnnotationSet(sentence))

    sentences = getAllSentencesFromXML(XML_FILE_MEDLINE)
    for index,sentence in enumerate(sentences):
        print('Processing and writing sentence ', sentence.id, ' (',index,'/',len(sentences),') of', XML_FILE_MEDLINE)
        writePair(sentence,createAnnotationSet(sentence))
        
    '''
    for index,sentence in enumerate(sentences):
        print('Processing sentence ', sentence.id, ' (',index,'/',len(sentences),') of', XML_FILE_EMEA)
        annotations.append(createAnnotationSet(sentence))
    for sentence,annotationSet in zip(sentences,annotations):
        print('Writing sentence', sentence.id)
        writePair(sentence,annotationSet)
    '''
if __name__ == "__main__":
    main()
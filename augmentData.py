import dataset
import xml.etree.ElementTree as ET
import ast
import collections
MRCONSO = dataset.connect('sqlite:///../mrconso.db')
MRSTY = dataset.connect('sqlite:///../mrsty.db')

XML_PATH = '../EC21.d/'
XML_FILE = XML_PATH + 'EMEA_es_EC21_man.xml'

Concept = collections.namedtuple('Concept',['cui','len','text','offset'])
Sentence = collections.namedtuple('Sentence',['id','text','concepts'])
Datum = collections.namedtuple('Datum',['id','txt','annotation'])
Annotation = collections.namedtuple('Annotation',['t','type','offset1','offset2','name','numNote','cui'])
'''
T1  NORMALIZABLES 3688 3692 CDDP
#1  AnnotatorNotes T1   387318005
'''
AUGMENTED_DATA_PATH = '../augmentedData/'

def getAllSentencesFromXML():
    print('Parsing XML',XML_FILE,'...')
    tree = ET.parse(XML_FILE)
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
            if (unitIn > maxUnits):
                break
        break
    return sentences

def createAnnotation(sentence):
    # Annotation = collections.namedtuple('Annotation',['t','type','offset1','offset2','name','numNote','cui'])
    # Concept = collections.namedtuple('Concept',['cui','len','text','offset'])
    # MRCONSO, MRSTY
    uniqueConcepts = []
    currentConceptText = sentence.concepts[0].text
    #uniqueConcepts.append(sentence.concepts[0].text,[sentence.concepts[0]])
    uniqueConcepts = {sentence.concepts[0].text:[sentence.concepts[0]]}
    for concept in sentence.concepts:
        if concept.text != currentConceptText:
            #uniqueConcepts.append(concept.text,[])
            uniqueConcepts[concept.text] = [concept]
            currentConceptText = concept.text
        else:
            uniqueConcepts[currentConceptText].append(concept)

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
    for uniqueConcept, concepts in uniqueConcepts.items():
        ts = []
        for concept in concepts:
            row = MRSTY['mrconso'].find_one(cui = concept.cui) # the table is named mrconso instead of mrsty
            ts.append(row['ts'])
        ts = set(ts)
        print()
        print(ts)
        if len(ts.intersection(proteinsTs)) > 0 and len(ts.intersection(chemicalTs)) == 0:
            print('PROTEINAS')
        elif len(ts.intersection(proteinsTs)) == 0 and len(ts.intersection(chemicalTs)) > 0:
            row2 = MRCONSO['mrconso'].find_one(cui = concept.cui)
            if row2['source'] == 'SNOMEDCT_US':
                print('NORMALIZABLES')
            else:
                print('NO_NORMALIZABLES')
        else:
            print('WHAT TO DO HERE, UNCLEAR?')
        print()
    annotation = None#Annotation()
    return annotation
def writePair(sentence,annotation):
    #AUGMENTED_DATA_PATH
    pass
def main():
    sentences = getAllSentencesFromXML()
    for sentence in sentences:
        print(sentence)
        print()
        print()
        '''
        print('TITLE',sentence[0])
        print('TEXT',sentence[1])
        print('ES')
        for concepts in sentence[2]:
            #print('CUI',concepts[0],'len',concepts[1],'text', "'"+concepts[2]+"'")
            print()
        print()
        print()
        '''
    annotations = []
    for sentence in sentences:
        annotations.append(createAnnotation(sentence))
    for sentence,annotation in zip(sentences,annotations):
        writePair(sentence,annotation)
if __name__ == "__main__":
    main()
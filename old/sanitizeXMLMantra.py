import xml.etree.ElementTree as ET
import ast
#import collections
PATH = '../EC21.d/'
FILE = PATH + 'EMEA_es_EC21_man.xml'


print('Parsing XML',FILE,'...')
tree = ET.parse(FILE)
print('Processing...')
root = tree.getroot()
#SentenceRecord = collections.namedtuple('title','text','concepts')
sentences = [] # array of: [title,text,[concenpts]]
for document in root:
    maxUnits = 3
    unitIn = 0
    for unit in document:
        if len(unit) < 2:
            continue
        sentence = []
        sentence.append(unit.attrib['id'])
        sentence.append(unit[0].text)
        es = unit[1:]
        # treat extra spaces, dots, commas. For the moment, only at the end.
        for e in es:
            if e.text[-1] == ' ' or e.text[-1] == ',' or e.text[-1] == '.':
                e.text = e.text[:-1]
                e.attrib['len'] = str(int(e.attrib['len'])-1)
        # treat repeated concepts
        '''
        i = 0
        while i < (len(es)-1):
            currentCUI = es[i].attrib['cui']
            j = 1
            nextCUI = es[i+j]
            while currentCUI == nextCUI and j < len(es):
                if type(es[i].attrib['cui']) == str:
                    es[i].attrib['cui'] = [es[i].attrib['cui'],es[i+j]]
                else:
                    es[i].attrib['cui'].append(es[i+j])
                j +=1
            i += 1
        '''
        '''
        i = 0
        while i < (len(es)-1):
            currentConcept = es[i].text
            j = 1
            nextConcept = es[i+j].text
            while currentConcept == nextConcept and j+i < len(es):
                #ast.literal_eval(q)
                if es[i].text[1] != '[':#type(es[i].text) == str:
                    es[i].text = str([es[i].text,es[i+j]])
                else:
                    es[i].text.append(es[i+j])
                j +=1
            i += 1
        '''
        # Add concepts:
        concepts = []
        for e in es:
            #concepts.append(ET.tostring(e, encoding='utf8', method='xml'))
            concepts.append(tuple((e.attrib['cui'],e.attrib['len'],e.text)))
        # compare concepts: TODO
        sentence.append(concepts)
        sentences.append(sentence)
        unitIn += 1
        if (unitIn > maxUnits):
            break
    break

for sentence in sentences:
    print('TITLE',sentence[0])
    print('TEXT',sentence[1])
    print('ES')
    for concepts in sentence[2]:
        print('CUI',concepts[0],'len',concepts[1],'text', "'"+concepts[2]+"'")
        print()
    print()
    print()

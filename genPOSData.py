import os
import sys

DATA_PATH = '../farmacos-final-One-POS2'
TAGGER_PATH = '../PlanTL-SPACCC_POS-TAGGER-9b64add/Med_Tagger'
sys.path.append(TAGGER_PATH)

from Med_Tagger import Med_Tagger
tag = Med_Tagger()

files = os.listdir(DATA_PATH)

for file in files:
    if file.endswith(".txt"):
        with open(DATA_PATH + '/' + file,'r') as f:
            parsed = tag.parse(f.read())
        tag.write_brat(parsed,DATA_PATH + '/' + file[:-4] + '.ann2')
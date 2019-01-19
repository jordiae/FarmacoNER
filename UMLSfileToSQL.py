import pandas as pd
import dataset as dat
from sqlalchemy import create_engine

engine = create_engine('sqlite:///../UMLS/mrconso.db', echo=False)


PATH = '../UMLS/'
MRCONSO = PATH+'filtered-mrconso.txt'#'MRCONSO.RRF'
#MRSTY = PATH+'MRSTY.RRF'
print('Reading file...')
with open(MRCONSO) as f:
    mrconsoDF= pd.read_csv(f, sep='|', header=None,lineterminator='\n',names=['cui','source'])# index_col=0,
print('Processing table...')                          
print(mrconsoDF.head(1))
mrconsoDF.to_sql('mrconso', con=engine)#, if_exists='append')






engine = create_engine('sqlite:///../UMLS/mrsty.db', echo=False)


PATH = '../UMLS/'
MRSTY = PATH+'MRSTY.RRF'
print('Reading file...')
with open(MRSTY) as f:
    mrstyDF= pd.read_csv(f, sep='|', header=None,lineterminator='\n',names=['cui','ts','as','names','a2s','num','extra'])# index_col=0,
print('Processing table...')                          
print(mrstyDF.head(6))
mrstyDF.to_sql('mrsty', con=engine)#, if_exists='append')


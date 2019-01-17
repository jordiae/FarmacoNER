import datas NO_NORMALIZABLES: precision:   0.00%; recall:   0.00%; FB1:   0.00  895
et

db = dataset.connect('sqlite:///../mrconso2.db')
table = db['mrconso']
print(table.columns)
print(table.count(source='SNOMEDCT_US'))
#table.delete(source = {'!=': 'SNOMEDCT_US'})
db.query("DELETE FROM mrconso WHERE mrconso.source != 'SNOMEDCT_US'")
db.commit()
print(table.count())
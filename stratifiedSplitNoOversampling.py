import shutil
import os
import random
import math

from sklearn.model_selection import train_test_split

source = '../farmacos-final-One'
dest = '../farmacos-final-One-stratified-split'

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
def duplicate_without_other_labels(annotation,label):
	with open(source+'/'+annotation+'.ann','r') as f:
		lines = f.readlines()
	dup_lines = []
	for l in range(0, len(lines)-1, 2):
		if (label == 'NO_NORMALIZABLES' and lines[l].find('NO_NORMALIZABLES') != -1) or (label == 'UNCLEAR' and lines[l].find('UNCLEAR') != -1):
			dup_lines.append(lines[l])
			dup_lines.append(lines[l+1])
	return concat(dup_lines)
def main():
	files = os.listdir(source)
	annotations = []
	for f in files:
		if f.endswith(".ann"):
			annotations.append(f[:-4])
	labels = assign_labels(annotations)
	X = annotations
	y = labels
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, stratify = y, random_state=1234)
	X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1/(0.1+0.8), stratify = y_train, random_state=1234)

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
		'''
		# Oversampling of the minority classes
		if label == 'NO_NORMALIZABLES':
			dupli = duplicate_without_other_labels(a,label)
			for i in range(0,29): # we want 30 of them, so 29 extra copies
				with open(source + '/' + 'train'+'/'+a+'_copy'+str(i+1) +'.ann','w') as f:
					f.write(dupli)
				shutil.copy(source+'/'+a+'.txt', source + '/' + 'train'+'/'+a+'_copy'+str(i+1) +'.txt')
		if label == 'UNCLEAR':
			dupli = duplicate_without_other_labels(a,label)
			for i in range(0,19): # we want 20 of them, so 19 extra copies
				with open(source + '/' + 'train'+'/'+a+'_copy'+str(i+1) +'.ann','w') as f:
					f.write(dupli)
				shutil.copy(source+'/'+a+'.txt', source + '/' + 'train'+'/'+a+'_copy'+str(i+1) +'.txt')
		'''
		shutil.copy(source+'/'+a+'.ann', dest + '/' + 'train'+'/'+a+'.ann')
		shutil.copy(source+'/'+a+'.txt', dest + '/' + 'train'+'/'+a+'.txt')

	for a in X_val:
		shutil.copy(source+'/'+a+'.ann', dest + '/' + 'valid'+'/'+a+'.ann')
		shutil.copy(source+'/'+a+'.txt', dest + '/' + 'valid'+'/'+a+'.txt')

	for a in X_test:
		shutil.copy(source+'/'+a+'.ann', dest + '/' + 'test'+'/'+a+'.ann')
		shutil.copy(source+'/'+a+'.txt', dest + '/' + 'test'+'/'+a+'.txt')

if __name__ == "__main__":
	main()
	



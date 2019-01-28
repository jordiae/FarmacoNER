import shutil
import os
import random
import math

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


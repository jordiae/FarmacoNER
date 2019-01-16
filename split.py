import shutil
import os
import random
import math

source = '../farmacosOne'

files = os.listdir(source)

annotations = []

for f in files:
	if f.endswith(".ann"):
		annotations.append(f[:-4])

random.shuffle(annotations)
train = annotations[:math.floor(len(annotations)*0.8)]
valid = annotations[math.floor(len(annotations)*0.8):math.floor(len(annotations)*0.9)]
test = annotations[math.floor(len(annotations)*0.9):len(annotations)]

if not os.path.exists(source+'/train'):
	os.makedirs(source+'/train')
if not os.path.exists(source+'/valid'):
	os.makedirs(source+'/valid')
if not os.path.exists(source+'/test'):
	os.makedirs(source+'/test')
print(len(annotations))
print(len(train))
print(len(valid))
print(len(test))
for a in train:
	shutil.move(source+'/'+a+'.ann', source + '/' + 'train'+'/'+a+'.ann')
	shutil.move(source+'/'+a+'.txt', source + '/' + 'train'+'/'+a+'.txt')

for a in valid:
	shutil.move(source+'/'+a+'.ann', source + '/' + 'valid'+'/'+a+'.ann')
	shutil.move(source+'/'+a+'.txt', source + '/' + 'valid'+'/'+a+'.txt')

for a in test:
	shutil.move(source+'/'+a+'.ann', source + '/' + 'test'+'/'+a+'.ann')
	shutil.move(source+'/'+a+'.txt', source + '/' + 'test'+'/'+a+'.txt')


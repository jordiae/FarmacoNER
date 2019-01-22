import shutil
import os

source = '../farmacos-final'
dest = '../farmacos-final-One'


if not os.path.exists(dest):
		os.makedirs(dest)

subdirs = os.listdir(source)

for subdir in subdirs:
	files = os.listdir(source+'/'+subdir+'/')
	for f in files:
		shutil.copy(source+'/'+subdir+'/'+f, dest)

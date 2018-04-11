# -*- coding: utf-8 -*-
import graphs,os,glob,shutil
from os import path, mkdir
from sys import argv
import numpy as np

# definitions
dataDir = "/home/tr332/scratch/functional"
diag = argv[1]

# make data diagnosis directory if required
if not path.exists(path.join(dataDir, diag)):
	mkdir(path.join(dataDir, diag))

ROInums = ["500"] #["100", "200", "300", "400", "500"]  #  "600", "1000", "100", "200","300" 
mainDir = os.getcwd()

# get directory names
dirNames = [v for v in glob.glob(path.join(dataDir, diag, '*', '*')) if not 'excluded' in v]
dirNames = [v for v in dirNames if path.isdir(v)]
print dirNames

# open log file
log = open("log.txt","w")

# iterate through subjects
for subj in dirNames:
	# define WBIC number
	WBICNum = path.basename(path.split(subj)[0])
	cond = path.basename(subj)
	print WBICNum
	print cond
	
	# iterate through parcel files
	for ROInum in ROInums:
		parcelFile = "sw"+WBICNum+"_functional_reordered_pp_cl"+ROInum+"_ts.txt" #'functional_reordered_pp_wpd_MNI'+ROInum+'_ts.txt'
		print subj + ' '+parcelFile
		
			
	# columnise timeseries
	ts = columnise(parcelFile)

	# perform wavelet analysis
	a = graphs.individual(ts)
	a.waveletDecomp()
	
	# return files to data
	if not path.exists(path.join(dataDir, diag, WBICNum, cond)):
		mkdir(path.join(dataDir, diag, 	WBICNum, cond))
	for f in glob.glob('wave*'):
		shutil.move(f, path.join(dataDir, diag, WBICNum, cond, f))
	os.remove(parcelFile)
	if path.exists(path.join(dataDir, diag, WBICNum, cond, ts)):
		os.remove(ts)
	else:
		shutil.move(ts, path.join(dataDir, diag, WBICNum, cond, ts))
	#shutil.move(parcelFile, path.join(dataDir, diag, WBICNum, parcelFile))		
	
	# return to original directory
	os.chdir(mainDir)
log.close()

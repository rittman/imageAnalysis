"""
This script is designed to submit analysis of functional images to the grid engine at the WBIC for preprocessing.

The main preprocessing function called is speedypp.py from the signal processing toolbox.
"""
import glob,os
from os import path

email="tr332@medschl.cam.ac.uk"

# define diagnostic groups here
diags = ["Control"] #"Control",

# Get the name of the current working directory
curDir = os.getcwd()

# Iterate through the diagnostic groups
for diag in diags:
	# get a list of all the directories (ie subjects) for each group
	dirs = [ v for v in glob.glob(path.join(curDir,diag,"*")) if path.isdir(v) ]
	
	# iterate through the subject directories
	for d in dirs:
		os.chdir(d)  # move in to subject's directory
		f = open("submitScript.sh","wb")  # open a script to submit the preprocessing
		f.writelines('\n'.join(["#!/bin/bash","#$ -cwd","#$ -l qname=clusterall.q","#$ -M "+email,"#$ -V"])) # headers required for the grid engine
		f.writelines("\nfslreorient2std functional.nii functional_reordered.nii\n") # reorientate the functional image so that it applies skull strip and displays correctly
		f.writelines("\nfslreorient2std structural.nii structural_reordered.nii\n") # reorientate structural image
		f.writelines("\n3dWarp -prefix structural_reordered_deob.nii -deoblique structural_reordered.nii\n") # deoblique the structural image
		
		# speedypp with options - these may need changing, see signal processing toolbox for details
		f.writelines("\n~/fmri_spt/speedypp.py -d functional_reordered.nii -a structural_reordered.nii -o -f 8mm --rall --skullstrip --atrophy --betthresh=0.2 --tpattern=seqminus --highpass=0.01 --despike --TR=2 --basetime=10 --OVERWRITE\n")
		f.close() # close submission file
		os.system("qsub submitScript.sh") # submit submision file to the grid engine
		os.chdir(curDir) # move back to the main directory

"""
This script is designed to submit analysis of functional images to the grid engine at the WBIC for preprocessing.

The main preprocessing function called is speedypp.py from the signal processing toolbox, which should be located
in your home directory as ~/fmri_spt
"""
import glob,os
from os import path

email="tr332@medschl.cam.ac.uk"

# define diagnostic groups here
diags = ["Control","PD"] #"Control",

# Get the name of the current working directory
curDir = os.getcwd()

# Iterate through the diagnostic groups
for diag in diags: 
	# get a list of all the directories (ie subjects) for each group
	dirs = [ v for v in glob.glob(path.join(curDir,diag,"*","*")) if path.isdir(v) ]
	
	# iterate through the subject directories
	for d in dirs:
		os.chdir(d)  # move in to subject's directory
		WBICNum = path.basename(path.split(d)[0])
		print WBICNum
		f = open("submitScript.sh","wb")  # open a script to submit the preprocessing
		f.writelines('\n'.join(["#!/bin/bash","#$ -cwd","#$ -l qname=clusterall.q","#$ -M "+email,"#$ -V"])) # headers required for the grid engine
		f.writelines("\nfslreorient2std "+WBICNum+"_functional.nii "+WBICNum+"_functional_reordered.nii.gz\n") # reorientate the functional image so that it applies skull strip and displays correctly
		f.writelines("\nfslreorient2std "+WBICNum+"_structural.nii "+WBICNum+"_structural_reordered.nii.gz\n") # reorientate structural image
		f.writelines("\n3dWarp -prefix "+WBICNum+"_structural_reordered_deob.nii.gz -deoblique "+WBICNum+"_structural_reordered.nii.gz\n") # deoblique the structural image
		
		# speedypp with options - these may need changing, see signal processing toolbox for details
#		f.writelines("\n~/fmri_spt/speedypp.py -d "+WBICNum+"_functional_reordered.nii.gz -a "+WBICNum+"_structural_reordered.nii.gz -o --rall --tpattern=seqminus --TR=2 --basetime=10 --OVERWRITE\n")
		
		# wavelet despiking


		# High pass filter


		f.close() # close submission file
		os.system("qsub submitScript.sh") # submit submision file to the grid engine
		os.chdir(curDir) # move back to the main directory

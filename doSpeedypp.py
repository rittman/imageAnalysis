import glob,os
from os import path

diags = ["Control"] #"Control",
curDir = os.getcwd()

for diag in diags:
	dirs = [ v for v in glob.glob(path.join(curDir,diag,"*")) if path.isdir(v) ]
	for d in dirs:
		os.chdir(d)
		f = open("submitScript.sh","wb")
		f.writelines('\n'.join(["#!/bin/bash","#$ -cwd","#$ -l qname=clusterall.q","#$ -M tr332@medschl.cam.ac.uk","#$ -V"]))
		f.writelines("\nfslreorient2std functional.nii functional_reordered.nii\n")
		f.writelines("\nfslreorient2std structural.nii structural_reordered.nii\n")
		f.writelines("\n3dWarp -prefix structural_reordered_deob.nii -deoblique structural_reordered.nii\n")
		f.writelines("\n~/fmri_spt/speedypp.py -d functional_reordered.nii -a structural_reordered.nii -o -f 8mm --rall --skullstrip --atrophy --betthresh=0.2 --tpattern=seqminus --highpass=0.01 --despike --TR=2 --basetime=10 --OVERWRITE\n")
		f.close()
		os.system("qsub submitScript.sh")
		os.chdir(curDir)

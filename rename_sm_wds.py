from os import system,path,getcwd,chdir,rename
from glob import glob,os
from string import split
import os,sys

SmWds = glob('*/*/*/*/*_functional_reordered_sm.nii.gz')

curDir = getcwd()

for original in SmWds:
#	try:
		chdir(path.split(original)[0])
		wbic = (split(path.basename(original),sep='_')[0])
		os.rename(original,wbic+'_functional_reordered_sm_beforeWDS.nii.gz')
		chdir(curDir)
#	except:
#		print 'File name belonging to patient with WBIC number '+wbic+' could not be renamed' 





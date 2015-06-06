# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 23:24:39 2012
File for creating a mean association matrix.

Instructions:
1. define the list of filenames on line 18
2. run this script
3. run doMean.py

@author: tim
"""

import numpy as np
import os,csv
from os import chdir,path,getcwd
from glob import glob
from shutil import rmtree


def meanMatrix(dg, nP, fNames=None):
    # define the list of association matrix files to use here
    if not fNames:
        fNames = glob(path.join(dg, "*/wave_cor_mat_level_2d_"+str(nP)+"_z.txt"))
    
    # iterate through each node setting up a directory
    for i in range(nP):
        if not path.exists("dir_"+str(i)):
            os.mkdir("dir_"+str(i))
        f = open(path.join("dir_"+str(i),"allValues.txt"), "wb")
        f.close()
    
    # iterate through subjects and extract data for each node
    for fName in fNames:
        print 'loading data from', fName
        # open file
        f = open(fName,"rb")
        reader = csv.reader(f, delimiter=" ")
      
        for i in range(nP):
            g = open(path.join("dir_"+str(i),"allValues.txt"), "ab")
            writer = csv.writer(g, delimiter=",")
            l = reader.next()
            line = [v if v not in ["NA", "NaN"] else 0 for v in l]
            writer.writerow(line)
        del(line)
        g.close()
        del(reader)
        f.close()
        
    mainDir = getcwd()
    
    for d in glob("dir*"):
      chdir(d)
      # load file
      arr = np.loadtxt("allValues.txt", delimiter=",")
    
      # calculate means
      meanarr = np.mean(arr, axis=0)
      np.savetxt("meanValues.txt", meanarr[None], delimiter=",")
      chdir(mainDir)
    
    # collate the matrices
    dirNames = ["dir_"+str(v) for v in range(nP)]
    
    f = open(path.join(dg,"mean_"+str(nP)+".txt"),"w")
    for dirName in dirNames:
        print dirName
        g = open(path.join(dirName,"meanValues.txt"))
        line = g.readlines()[0]
        f.writelines(line)
        g.close()
        rmtree(dirName)
        
    f.close()

nP=500
for dg in ["Control", "PD", "PSP", "CBS"]:
    meanMatrix(dg, nP=nP)
    
f = open("ControlLog.txt", "rb")
fNameDict = {l.split()[0]:[v.replace(str(500), str(nP)) for v in l.split()[1:]] for l in f.readlines()}
f.close()

for dg in fNameDict.keys():
    meanMatrix("Control"+dg, nP=nP, fNames = fNameDict[dg])

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

import os,glob,csv
from os import path

# define the list of association matrix files to use here
fNames = glob.glob("PD/*/wave_cor_mat_level_2d_500.txt")

# iterate through each node setting up a directory
for i in range(500):
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
  
    for i in range(500):
        g = open(path.join("dir_"+str(i),"allValues.txt"), "ab")
        writer = csv.writer(g, delimiter=",")
	l = reader.next()
        line = [v if v not in ["NA", "NaN"] else 0 for v in l]
        writer.writerow(line)
        del(line)
        g.close()
    del(reader)
    f.close()

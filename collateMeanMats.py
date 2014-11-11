# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 00:05:20 2012

@author: tim
"""

from os import path

dirNames = ["dir_"+str(v) for v in range(500)]

f = open("mean_500.txt","w")
for dirName in dirNames:
    print dirName
    g = open(path.join(dirName,"meanValues.txt"))
    line = g.readlines()[0]
    f.writelines(line)
    g.close()
    
f.close()

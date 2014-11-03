# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 19:29:00 2013

@author: tim
"""

from sys import argv
import glob
from os import path
import numpy as np
from scipy import stats,spatial

fdFile="functional_reordered_motion_fd.txt" #should this be the motion_1D.txt file?
corr="functional_reordered_pp_wpd_MNI500_ts_col_corr.txt" #this is the result from the parcellation - might have to rename
locs=argv[2] #"parcel_500_xyz_nolabels_mm.txt"     what is this?

dirName = argv[1]
subjs = [v for v in glob.glob(path.join(dirName,"*")) if path.isdir(v)]

meanFDs = []

# collate mean FD values for individuals
for subj in subjs:
    if path.exists(path.join(subj, fdFile)):
        print subj
        fdVals = np.loadtxt(path.join(subj, fdFile))
        fdVals = np.ma.array(fdVals, mask=np.isnan(fdVals))
        print subj + ' '+ str(np.mean(fdVals))
        meanFDs.append(np.mean(fdVals))
        
    else:
        print(subj + " " + fdFile + " doesn't exist")
        subjs.remove(subj)

FDfile = open(path.join(dirName, "meanFD.txt"),"w")
FDfile.writelines('\n'.join([str(v) for v in meanFDs]))
FDfile.close()

meanFDs = np.array(meanFDs)
print(meanFDs.size)
print(len(subjs))

# extract subject connectivity values by node pair
assocMat = np.memmap(path.join(dirName,"assocMatAll.txt"), mode="w+", shape=(500,500,len(subjs)), dtype='float32')
for subj in subjs:
    mat = np.loadtxt(path.join(subj,corr))
    if np.isnan(mat[0,0]):
    	print subj+ "has NA values"
    assocMat[:,:,subjs.index(subj)]=mat


# correlate FD and connectivity values
FDvsConnMat = np.zeros((500,500))

for x in range(len(FDvsConnMat[:,1])):
    for y in range(len(FDvsConnMat[1,:])):
        if x != y:
            FDvsConnMat[x,y] = stats.pearsonr(meanFDs, assocMat[x,y,:])[0]
del(assocMat)
np.savetxt(path.join(dirName, "FDvsConnMat.txt"), FDvsConnMat)

# plot vs distance
# create euclidean distance matrix
posArray = np.loadtxt(locs)
dists = spatial.distance.pdist(np.rot90(posArray,3), 'euclidean')
dists = spatial.distance.squareform(dists)

outmat = np.zeros(((500*499)/2,2))

count = 0
for x in range(len(FDvsConnMat[:,1])):
    for y in range(len(FDvsConnMat[1,:])):
        if x > y:
            outmat[count,0] = dists[x,y]
            outmat[count,1] = FDvsConnMat[x,y]
            count+=1

np.savetxt(path.join(dirName,"FDcorrConnVsDistance.txt"), outmat)

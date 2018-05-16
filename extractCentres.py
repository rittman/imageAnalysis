# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 19:37:17 2015

@author: tim
"""

import nibabel as nb
from numpy import newaxis
import numpy as np
import numpy.linalg as npl
import csv

# define input and output images - just change these to suit
inImage = "parcel_500.nii"
outROIs  = "parcel_500_xyz.txt"

# load image
f = nb.load(inImage)
fData = f.get_data()

# extract voxel coordinates
I,J,K=fData.shape
coords = np.zeros((I, J, K, 3))
coords[...,0] = np.arange(I)[:,newaxis,newaxis]
coords[...,1] = np.arange(J)[newaxis,:,newaxis]
coords[...,2] = np.arange(K)[newaxis,newaxis,:]

# convert voxel coordinates to mm values using affine values
M = f.affine[:3,:3]
abc = f.affine[:3,3]

for x in range(len(coords[:,0,0,0])):
    for y in range(len(coords[0,:,0,0])):
        for z in range(len(coords[0,0,:,0])):
            coords[x,y,z,:] = M.dot(coords[x,y,z,:]) + abc
            
# get unique values in the mask
valList = np.unique(fData)
valList = valList[valList!=0]

out = open(outROIs, "w")
writer = csv.DictWriter(out,
                        fieldnames = ["Node", "x", "y", "z"],
                        delimiter=" "
                        )

# write out the centrroids
for v in valList:
    tempArr = np.zeros((I, J, K, 3), dtype=bool)
    tfArray = fData==v
    tempArr[...,0] = tfArray
    tempArr[...,1] = tfArray
    tempArr[...,2] = tfArray
    
    tempArr = coords[tempArr]
    tempArr = np.mean(tempArr.reshape([int(tempArr.shape[0]/3),3]),axis=0)
    outList = [str(int(v))]
    outList.extend(["{:.2f}".format(x) for x in tempArr])
    outDict = dict(zip(writer.fieldnames,
                       outList))
    writer.writerow(outDict)
    
out.close()

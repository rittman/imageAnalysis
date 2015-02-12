# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 10:33:22 2014

@author: tim
"""

from maybrain import brainObjs as mbt
from maybrain import mbplot as mbp
from os import mkdir,path
from time import sleep
from numpy import power

# set the diagnosis and input files/delimiter
d = "Control"
assMat = "mean_500.txt"
delim = ","
spatFile = "parcel_500_xyz.txt"

# set output directory and create if necessary
outDir = "examplePics"
if not path.exists(outDir):
    mkdir(outDir)

# function to save brain images
def saveFig(brain, outFile, outDir = "brainPictures", fEnd=None, fType=".png"):
    if not path.exists(outDir):
        mkdir(outDir)
    
    if fEnd:
        outFile = outFile+fEnd
        
    # rotate the brain and save axial, sagittal and coronal images
    mbp.mlab.view(0, 90)
    sleep(2)
    mbp.mlab.savefig(path.join(outDir, outFile + "_sag_graph"+fType), size=(1200,1200), magnification=1)
    mbp.mlab.savefig(path.join(outDir, outFile + "_sag_graph"+fType), size=(1200,1200), magnification=1)
    mbp.mlab.view(0,180)
    sleep(2)
    mbp.mlab.savefig(path.join(outDir,outFile + "_ax_graph"+fType), size=(1200,1200), magnification=1)
    mbp.mlab.view(90,90)
    sleep(2)
    mbp.mlab.savefig(path.join(outDir,outFile + "_cor_graph"+fType), size=(1200,1200), magnification=1)
  
# use this as the percentage edge connectivity
edgePC = 3

# create a brain object, import an adjacency matrix and apply a threshold
a = mbt.brainObj()
a.importAdjFile(path.join(d, assMat), delimiter=delim)
#a.applyThreshold()

# apply a local threshold
a.localThresholding(edgePC=edgePC)
#weights = [weightDict[e]+1.0 for e in a.G.edges()]
#weights = [power(v,4)*v for v in weights]
a.removeUnconnectedNodes()

# get the connection strength 
cc = mbt.nx.clustering(a.G)  #mbt.nx.degree(a.G, weight='weight')
#weightDict = {e:a.G.edge[e[0]][e[1]]['weight'] for e in a.G.edges()}

# fudge the sizes a bit so there is more of a contrast, ie take the square
sizeList = [power(float(cc[v]),2) for v in a.G.nodes()]
print sizeList

# import the spatial file
a.importSpatialInfo(spatFile)

# import MNI space as a background brain
a.importBackground("avg152T1_brain.nii")

# create a plotting object
b = mbp.plotObj()

# plot the brain edges
b.plotBrainEdges(a, opacity=0.5, lw=3.) #, scalars=weights

#plot the brain nodes
b.plotBrainCoords(a, col=(0.,0.,1.), sizeList = sizeList, opacity=0.5) #, sf=4.

# plot the background MNI space
b.plotSkull(a, contourVals = [3000,9000])

#fEnd = "edgesOnly"
fEnd = None

saveFig(a, d, outDir, fEnd=fEnd, fType=".png")

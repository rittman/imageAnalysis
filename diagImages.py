# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 10:33:22 2014

@author: tim
"""

from maybrain import mayBrainTools as mbt
from maybrain import mbplot as mbp
from os import mkdir,path
from time import sleep
from numpy import power

d = "Control"
assMat = "mean_2d_500.txt"
delim = ","
spatFile = "parcel_500_xyz.txt"

outDir = "examplePics"
if not path.exists(outDir):
    mkdir(outDir)
    
def saveFig(brain, outFile, outDir = "brainPictures", fEnd=None, fType=".png"):
    if not path.exists(outDir):
        mkdir(outDir)
    
    if fEnd:
        outFile = outFile+fEnd
        
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
  
edgePC = 3

a = mbt.brainObj()
a.importAdjFile(path.join(d, assMat), delimiter=delim)
a.applyThreshold()
degs = mbt.nx.degree(a.G, weight='weight')
weightDict = {e:a.G.edge[e[0]][e[1]]['weight'] for e in a.G.edges()}


a.localThresholding(edgePC=edgePC)
#weights = [weightDict[e]+1.0 for e in a.G.edges()]
#weights = [power(v,4)*v for v in weights]

sizeList = [power(degs[v],2) for v in a.G.nodes()]


a.importSpatialInfo(spatFile)

#a.importBackground("/usr/share/data/fsl-mni152-templates/MNI152_T1_2mm_brain.nii.gz")


b = mbp.plotObj()

b.plotBrainEdges(a, opacity=0.7, lw=3.) #, scalars=weights

#b.plotBrainCoords(a, col=(0.,0.,1.), sizeList = sizeList, opacity=0.5, sf=4.)
#b.plotSkull(a, contourVals = [3000,9000])

fEnd = "edgesOnly"
saveFig(a, d, outDir, fEnd=fEnd, fType=".jpg")
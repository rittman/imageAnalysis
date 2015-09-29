# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 23:35:36 2014

@author: tim
"""

from maybrain import brainObjs as mbt 
from datetime import datetime
from metrics import metrics
from random import choice

startTime = datetime.now()
nodesToExclude = [28, 303, 355, 339, 131, 250, 491, 205, 423, 140, 434, 142, 235, 244, 493, 21, 26, 232, 76, 234, 422]

parcelFile = "parcel_500.txt"
degenName = "localSpread"
dVal = "2"
thresholdtype = "local"
am = "wave_cor_mat_level_"+dVal+"d_500_z.txt"

a = mbt.brainObj()
a.importAdjFile(am, exclnodes=nodesToExclude)
a.applyThreshold()
a.removeUnconnectedNodes()
a.importSpatialInfo(parcelFile)

# total weights
weights = [mbt.np.absolute(a.G.edge[v[0]][v[1]]['weight']) for v in a.G.edges() ]

T_start = mbt.np.sum(weights)
wtLossPC = 5.
wtLoss = T_start * (wtLossPC/100)

appVal = False

# identify degenerating nodes      
badNodes = [choice(a.G.nodes())]

for n in range(1,11):
    print "doing degenerative process"
    increment = wtLoss/10
    trackWtLoss = wtLoss
    while trackWtLoss>0.:  # just above 0 to cope with issues of defining 0
        a.degenerate(weightloss=0.05, weightLossLimit=increment, nodeList=badNodes)
        allNodes = [ v for v in a.G.nodes() if not v in badNodes ]
        badNodes.append(a.findSpatiallyNearest(badNodes))
        trackWtLoss-=increment
    
    a.reconstructAdjMat()
    print "getting metrics"

    metrics(a, appVal, degenName, pcLoss=str(wtLossPC))
    appVal = True
    
# total weights
weights = [mbt.np.absolute(a.G.edge[v[0]][v[1]]['weight']) for v in a.G.edges() ]
T_final = mbt.np.sum(weights)
print T_final

print(datetime.now()-startTime)

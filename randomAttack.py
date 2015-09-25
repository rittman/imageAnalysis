# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 23:35:36 2014

@author: tim
"""

from maybrain import brainObjs as mbt 
from maybrain import extraFns as extras
from datetime import datetime
import bct
from metrics import metrics

startTime = datetime.now()
nodesToExclude = [28, 303, 355, 339, 131, 250, 491, 205, 423, 140, 434, 142, 235, 244, 493, 21, 26, 232, 76, 234, 422]

parcelFile = "parcel_500.txt"
degenName = "randomAttack"
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
print T_start
wtLoss = T_start * 0.001

appVal = False

for n in range(1,11):
    print "doing degenerative process"
    a.degenerate(weightloss=0.05, weightLossLimit=wtLoss)
    a.reconstructAdjMat()
    print "getting metrics"
    metrics(a, appVal, degenName, pcLoss=str(n*5))  # something in the metrics is reinstating too many edges, including node 0 connected to everything
    appVal = True
    
# total weights
weights = [mbt.np.absolute(a.G.edge[v[0]][v[1]]['weight']) for v in a.G.edges() ]
T_final = mbt.np.sum(weights)
print T_final

print(datetime.now()-startTime)

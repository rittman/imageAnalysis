# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 23:35:36 2014
A script for applying a random attack model to a graph.
Updates on 12th June to tidy the script up and add comments.
@author: tim
"""

from maybrain import brainObjs as mbt 
from datetime import datetime

startTime = datetime.now()		# record the starting time

# define some variables
parcelFile = "parcel_500.txt"			# the file containing the spatial position of nodes in the brain
degenName = "randomAttack"			# name of the degenerative model
dVal = "2"					# this refers to the wavelet scale used to construct the association matrix
thresholdtype = "local"				# the type of thresholding to use
am = "mean_500.txt"				# the association matrix
nodesToExclude = [28, 303, 355, 339, 131, 250, 491, 205, 423, 140, 434, 142, 235, 244, 493, 21, 26, 232, 76, 234, 422]  # a list of nodes that are not covered in most/all subjects on the imaging

a = mbt.brainObj()				# create a brain object
a.importAdjFile(am, exclnodes=nodesToExclude, delimiter=",")	# import the association matrix
a.localThresholding(edgePC=3)			# apply local thresholding with 3 percent of all possible connections retained
a.removeUnconnectedNodes()			# remove any unconnected nodes
a.importSpatialInfo(parcelFile)			# import the spatial information

## total weights
weights = [mbt.np.absolute(a.G.edge[v[0]][v[1]]['weight']) for v in a.G.edges() ]	# list all the weights in the graph

T_start = mbt.np.sum(weights)			# starting sum of all graph weights
print T_start					# record the starting time
wtLossPC = 5. 					# five percent loss of connections at each iteration
wtLoss = T_start * (wtLossPC/100)		# calculate 5% of the connections

for n in range(3,4):
    print "doing degenerative process"
    a.degenerate(weightloss=0.05, weightLossLimit=wtLoss)	# applying the degenerative model
    #a.reconstructAdjMat()					# not sure whether this is required or not - may have been needed to fix a bug
    
# total weights
weights = [mbt.np.absolute(a.G.edge[v[0]][v[1]]['weight']) for v in a.G.edges() ]	# measure the weight of edges at the end
T_final = mbt.np.sum(weights)			# sum of all edge weights
print T_final

print(datetime.now()-startTime)			# and that took how long?

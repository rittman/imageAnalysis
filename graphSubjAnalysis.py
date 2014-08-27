# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 00:18:58 2012

@author: tim
"""

from maybrain import mayBrainTools as mbt
from maybrain import mayBrainExtraFns as extras
import bct
import numpy as np

edgePCCons = [v for v in range(1,11)]
excludedNodes = [28, 303, 355, 339, 131, 250, 491, 205, 423, 140, 434, 142, 235,
                 244, 493, 21, 26, 232, 76, 234, 422]
parcelFile = "parcel_500_xyz.txt"
thresholdtype = "local"
dVal = "2"
adjMatFile = "wave_cor_mat_level_"+dVal+"d_500.txt" #  =  "mean_2d_500.txt"
delim=" "

a = mbt.brainObj()
appVal = False

# unweighted measures
for e in edgePCCons:
    ofb = '_'.join(["brain", thresholdtype, str(e), "d"+dVal+"_"])
    propDict = {"edgePC":str(e)}

    a.importAdjFile(adjMatFile, delimiter=delim, excludedNodes=excludedNodes)
    a.localThresholding(edgePC=e)
    a.removeUnconnectedNodes()
    
    degs = a.G.degree(weight='weight')
    extras.writeResults(degs, "degreeWt", ofb, append=appVal)

    a.binarise()
    a.importSpatialInfo(parcelFile)  # read spatial information
    a.weightToDistance()
    a.makebctmat()    
   
    #### small worldness metrics ####
    degs = mbt.nx.degree(a.G)
    extras.writeResults(degs, "degree", ofb, propDict=propDict, append=appVal)
        
    clustCoeff = mbt.nx.average_clustering(a.G)
    extras.writeResults(clustCoeff, "clusterCoeff", ofb, propDict=propDict, append=appVal)
    del(clustCoeff)
    
    pl = mbt.nx.average_shortest_path_length(a.G)
    extras.writeResults(pl, "pl", ofb, propDict=propDict, append=appVal)
    del(pl)
    
    ge = extras.globalefficiency(a.G)
    extras.writeResults(ge, "ge", ofb, propDict=propDict, append=appVal)
    del(ge)
    
    le = extras.localefficiency(a.G)
    extras.writeResults(le, "le", ofb, propDict=propDict, append=appVal)
    del(le)

    # hub metrics
    betCent = mbt.nx.centrality.betweenness_centrality(a.G)
    extras.writeResults(betCent, "betCent", ofb, propDict=propDict, append=appVal)
    
    closeCent = mbt.nx.centrality.closeness_centrality(a.G)
    extras.writeResults(closeCent, "closeCent", ofb, propDict=propDict, append=appVal)
     
#    hs = extras.hubscore(a.G, bc=betCent, cc=closeCent, degs=degs, weighted=False)
#    extras.writeResults(hs, "hs", ofb, propDict=propDict, append=appVal)
#    del(hs, betCent, closeCent, degs)
     
    try:
        eigCent = mbt.nx.centrality.eigenvector_centrality_numpy(a.G)
    except:
        eigCent = dict(zip(a.G.nodes(), ['NA' for n in a.G.nodes()]))
    extras.writeResults(eigCent, "eigCentNP", ofb, propDict=propDict, append=appVal)
    del(eigCent)
    
    eln = extras.edgeLengths(a.G, nodeWise=True)
    extras.writeResults(eln, "eln", ofb, propDict=propDict, append=appVal)
    del(eln)
    
    el = extras.edgeLengths(a.G)
    meanEL = np.mean(np.array((el.values()), dtype=float))
    extras.writeResults(meanEL, "meanEL", ofb, propDict=propDict, append=appVal)

    medianEL = np.median(np.array((el.values()), dtype=float))
    extras.writeResults(medianEL, "medianEL", ofb, propDict=propDict, append=appVal)

    del(el, meanEL, medianEL)
    
    # modularity metrics
    ci = bct.modularity_louvain_und(a.bctmat)
    Q = ci[1]
    ciN = a.assignbctResult(ci[0])
    extras.writeResults(Q, "Q", ofb, propDict=propDict, append=appVal)
    extras.writeResults(ciN, "ci", ofb , propDict=propDict, append=appVal)  
    
    pcCent = bct.participation_coef(a.bctmat,ci[0])
    pcCent = a.assignbctResult(pcCent)
    extras.writeResults(pcCent, "pcCent", ofb, propDict=propDict, append=appVal)
    del pcCent
    
    wmd = extras.withinModuleDegree(a.G, ciN)
    extras.writeResults(wmd, "wmd", ofb, append=appVal)
    del wmd    
    
    nM = len(np.unique(ci[0]))
    extras.writeResults(nM, "nM", ofb, propDict=propDict, append=appVal)
    del(nM)
    del(ci, ciN, Q)
    
    # rich club measures
    rc = mbt.nx.rich_club_coefficient(a.G, normalized=False)
    extras.writeResults(rc, "rcCoeff", ofb, propDict=propDict, append=appVal)
    del(rc)
    # robustness
    rbt = a.robustness()
    extras.writeResults(rbt, "robustness", ofb, propDict=propDict, append=False)

    # append any further iterations
    appVal = True

# weighted measures
a.importAdjFile(adjMatFile, delimiter=delim, excludedNodes=excludedNodes)
a.applyThreshold()
a.removeUnconnectedNodes()

##a.adjMatThresholding(MST=False)
a.weightToDistance()
ofb = '_'.join(["brain", "d"+dVal+"_"])
appVal = False
a.importSpatialInfo(parcelFile)  # read spatial information
a.makebctmat()

# weighted hub metrics
degs = a.G.degree(weight='weight')
extras.writeResults(degs, "degree_wt", ofb, append=appVal)

betCent = mbt.nx.centrality.betweenness_centrality(a.G, weight='distance')
extras.writeResults(betCent, "betCent_wt", ofb, append=appVal)

closeCent = mbt.nx.centrality.closeness_centrality(a.G, distance='distance')
extras.writeResults(closeCent, "closeCent_wt", ofb, append=appVal)

#hs = extras.hubscore(a.G, bc=betCent, cc=closeCent, degs=degs, weighted=True)
#extras.writeResults(hs, "hubscores_wt", ofb, append=appVal)
#del(hs, betCent)

eigCent = mbt.nx.centrality.eigenvector_centrality_numpy(a.G)
extras.writeResults(eigCent, "eigCentNP_wt", ofb, append=appVal)
del(eigCent)

# weighted modularity metrics
ci = bct.modularity_louvain_und_sign(a.bctmat)
Q = ci[1]
ciN = a.assignbctResult(ci[0])
extras.writeResults(Q, "Q_wt", ofb, append=appVal)
extras.writeResults(ciN, "ci_wt", ofb, append=appVal)  

nM = len(np.unique(ci[0]))
extras.writeResults(nM, "nM_wt", ofb, append=appVal)
del(nM)

wmd = extras.withinModuleDegree(a.G, ciN, weight='weight')
extras.writeResults(wmd, "wmd", ofb, append=appVal)
del wmd

clustCoeff = mbt.nx.average_clustering(a.G, weight="weight")
extras.writeResults(clustCoeff, "clusterCoeff_wt", ofb, append=appVal)
del(clustCoeff)

pl = mbt.nx.average_shortest_path_length(a.G, weight="distance")
extras.writeResults(pl, "pl_wt", ofb, append=appVal)
del(pl)

ge = extras.globalefficiency(a.G, weight="distance")
extras.writeResults(ge, "ge_wt", ofb, append=appVal)
del(ge)

le = extras.localefficiency(a.G, weight="distance")
extras.writeResults(le, "leN_wt", ofb, append=appVal)
del(le)

pcCent = np.zeros((len(a.G.nodes()), 10))
betCentT = np.zeros((len(a.G.nodes()), 10))
nM = np.zeros((10))
wmd = np.zeros((len(a.G.nodes()), 10))
Q = np.zeros((10))

appValT=False
#
for n,i in enumerate([v for v in range(1,11)]):
    a.localThresholding(edgePC=i)
    a.removeUnconnectedNodes()
    a.makebctmat()
    a.weightToDistance()
    ofbT = '_'.join(["brain", thresholdtype, str(i), "d"+dVal+"_"])
    propDict = {"edgePC":a.edgePC}
    
    # weighted modularity metrics
    ci = bct.modularity_louvain_und_sign(a.bctmat)
    QWt = ci[1]
    Q[n] = QWt
    ciN = a.assignbctResult(ci[0])
    extras.writeResults(QWt, "QWt", ofbT, propDict=propDict, append=appValT)
    extras.writeResults(ciN, "ciWt", ofbT, propDict=propDict, append=appValT)
    del QWt
    
    nMWt = len(np.unique(ci[0]))
    nM[n] = nMWt
    extras.writeResults(nMWt, "nMWt", ofbT, propDict=propDict, append=appValT)
    del(nMWt)

    wmdWt = extras.withinModuleDegree(a.G, ciN, weight='weight')
    wmd[:,n] = [wmdWt[v] for v in a.G.nodes()]
    extras.writeResults(wmdWt, "wmdWt", ofbT, propDict=propDict, append=appValT)
    del wmdWt
    
    pcCentWt = bct.participation_coef_sign(a.bctmat,ci[0])
    pcCent[:,n] = pcCentWt
    pcCentWt = a.assignbctResult(pcCentWt)
    extras.writeResults(pcCentWt, "pcCentWt", ofbT, propDict=propDict, append=appValT)
    
    bcT = mbt.nx.centrality.betweenness_centrality(a.G, weight='distance')    
    betCentT[:,n] = [bcT[v] for v in a.G.nodes()]
    appValT=True
    
    
Q = np.mean(Q)
extras.writeResults(Q, "QWt_wt", ofb, append=appVal)
del(Q)

pcCent = a.assignbctResult(np.mean(pcCent, axis=1))
extras.writeResults(pcCent, "pcCentWt_wt", ofb, append=appVal)
del(pcCent,ci)

betCentT = a.assignbctResult(np.mean(betCentT, axis=1))
extras.writeResults(betCentT, "betCentWtT_wt", ofb, append=appVal)

nM = np.mean(nM)
extras.writeResults(nM, "nMWt_wt", ofb, append=appVal)
del(nM)

wmd = a.assignbctResult(np.mean(wmd, axis=1))
extras.writeResults(wmd, "wmdWt_wt", ofb, append=appVal)
del(wmd)


#hs = extras.hubscore(a.G, bc=betCentT, cc=closeCent, degs=degs, weighted=True)
#extras.writeResults(hs, "hsT_wt", ofb, append=appVal)
#del(hs, betCentT)


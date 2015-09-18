# -*- coding: utf-8 -*-
"""
@author: tim
"""

from maybrain import brainObjs as mbt 
from maybrain import extraFns as extras
import bct

edgePCCons = [v for v in range(1,11)]
def metrics(a,
            appVal,
            degenName,
            pcLoss,
            edgePCCons = [v*0.01 for v in range(1,11)],
            dVal = "2",
            thresholdtype = "local"
            ):
    appValW = appVal
    appValT = appVal


    # prepare matrices for weighted measures
#    pcCent = mbt.np.zeros((len(a.G.nodes()), 10))
    betCentT = mbt.np.zeros((len(a.G.nodes()), 10))
#    nM = mbt.np.zeros((10))
#    wmd = mbt.np.zeros((len(a.G.nodes()), 10))
                 
#    pcCentNm = mbt.np.zeros((len(a.G.nodes()), 10))
#    nMNm = mbt.np.zeros((10))
#    wmdNm = mbt.np.zeros((len(a.G.nodes()), 10))    
#    QNm = mbt.np.zeros((10))

    # unweighted measures
    for n,e in enumerate(edgePCCons):
        ofb = '_'.join(["brain", degenName, thresholdtype, str(e), "d"+dVal+"_"])

        a.localThresholding(edgePC=e)
        a.removeUnconnectedNodes()
        a.makebctmat()
        a.weightToDistance()

        propDict = {"edgePC":str(a.edgePC),
                    "pcLoss":pcLoss}
        degs = a.G.degree(weight='weight')
        extras.writeResults(degs, "degreeWt", ofb, propDict=propDict,
                            append=appVal)

	# weighted betweenness centrality
        bcT = mbt.centrality.betweenness_centrality(a.G, weight='distance')    
        betCentT[:,n] = [bcT[v] for v in a.G.nodes()]

#        # weighted modularity metrics
#        ci = bct.modularity_louvain_und_sign(a.bctmat)
#        Q = ci[1]
#        ciN = a.assignbctResult(ci[0])
#        extras.writeResults(Q, "QWt", ofb, propDict=propDict, append=appValT)
#        extras.writeResults(ciN, "ciWt", ofb, propDict=propDict, append=appValT)  
#        
#        nMWt = len(mbt.np.unique(ci[0]))
#        nM[n] = nMWt
#        extras.writeResults(nMWt, "nMWt", ofb, propDict=propDict, append=appValT)
#        del(nMWt)
#    
#        wmdWt = extras.withinModuleDegree(a.G, ciN, weight='weight')
#        wmd[:,n] = [wmdWt[v] for v in a.G.nodes()]
#        extras.writeResults(wmdWt, "wmdWt", ofb, propDict=propDict, append=appValT)
#        del wmdWt
#        
#        pcCentWt = bct.participation_coef_sign(a.bctmat,ci[0])
#        pcCent[:,n] = pcCentWt
#        pcCentWt = a.assignbctResult(pcCentWt)
#        extras.writeResults(pcCentWt, "pcCentWt", ofb, propDict=propDict, append=appValT)
#        
#        # Newman partitioning
#        ciNm = bct.modularity_und(a.bctmat)
#        QNmWt = ciNm[1]
#        QNm[n] = QNmWt
#        ciNNm = a.assignbctResult(ciNm[0])
#        extras.writeResults(QNmWt, "QNmWt", ofb, propDict=propDict, append=appValT)
#        extras.writeResults(ciNNm, "ciNmWt", ofb, propDict=propDict, append=appValT)  
#        
#        nMNmWt = len(mbt.np.unique(ciNm[0]))
#        nMNm[n] = nMNmWt
#        extras.writeResults(nMNmWt, "nMNmWt", ofb, propDict=propDict, append=appValT)
#        del(nMNmWt)
#    
#        pcCentNmWt = bct.participation_coef_sign(a.bctmat,ciNm[0])
#        pcCentNm[:,n] = pcCentNmWt
#        pcCentNmWt = a.assignbctResult(pcCentNmWt)
#        extras.writeResults(pcCentNmWt, "pcCentNmWt", ofb, propDict=propDict, append=appValT)
#        
#        wmdNmWt = extras.withinModuleDegree(a.G, ciNNm, weight='weight')
#        wmdNm[:,n] = [wmdNmWt[v] for v in a.G.nodes()]
#        extras.writeResults(wmdNmWt, "wmdNmWt", ofb, propDict=propDict, append=appValT)
#        del wmdNmWt

        appValT=True

	# now to collect measures in a binary graph
        a.binarise()

        a.weightToDistance()
        a.makebctmat()
        
        #### small worldness metrics ####
        degs = mbt.nx.degree(a.G)
        extras.writeResults(degs, "degree", ofb, propDict=propDict, append=appVal)
    
        degsNorm = extras.normaliseNodeWise(a.G, mbt.nx.degree, inVal=degs)
        extras.writeResults(degsNorm, "degreeNorm", ofb, propDict=propDict, append=appVal)

        cc = mbt.nx.clustering(a.G)
        extras.writeResults(cc, "cc", ofb, propDict=propDict, append=appVal)
            
        ccNorm = extras.normaliseNodeWise(a.G, mbt.nx.clustering, inVal=cc)
        extras.writeResults(ccNorm, "ccNorm", ofb, propDict=propDict, append=appVal)

        clustCoeff = np.mean(cc.values())
        extras.writeResults(clustCoeff, "clusterCoeff", ofb, propDict=propDict, append=appVal)

        clustCoeffNorm = np.mean(ccNorm.values())
        extras.writeResults(clustCoeffNorm, "clusterCoeffNorm", ofb, propDict=propDict, append=appVal)
            del(clustCoeff)
        del(clustCoeffNorm)
            del(cc)
        del(ccNorm)
        
        pl = mbt.nx.average_shortest_path_length(a.G)
        extras.writeResults(pl, "pl", ofb, propDict=propDict, append=appVal)

        plNorm = extras.normalise(a.G, mbt.nx.average_shortest_path_length, inVal=pl)
        extras.writeResults(plNorm, "plNorm", ofb, propDict=propDict, append=appVal)
            del(pl)
        del(plNorm)
        
        ge = extras.globalefficiency(a.G)
        extras.writeResults(ge, "ge", ofb, propDict=propDict, append=appVal)

        geNorm = extras.normalise(a.G, extras.globalefficiency, inVal=ge)
        extras.writeResults(geNorm, "geNorm", ofb, propDict=propDict, append=appVal)
            del(ge)
        del(geNorm)
        
        le = extras.localefficiency(a.G)
        extras.writeResults(le, "le", ofb, propDict=propDict, append=appVal)

        leNorm = extras.normaliseNodeWise(a.G, extras.localefficiency, inVal=le)
        extras.writeResults(leNorm, "leNorm", ofb, propDict=propDict, append=appVal)
            del(le)
        del(leNorm)
    
        # hub metrics
        betCent = mbt.nx.centrality.betweenness_centrality(a.G)
        extras.writeResults(betCent, "betCent", ofb, propDict=propDict, append=appVal)
            
        betCentNorm = extras.normaliseNodeWise(a.G, mbt.nx.centrality.betweenness_centrality, inVal=betCent)
        extras.writeResults(betCentNorm, "betCentNorm", ofb, propDict=propDict, append=appVal)
        del(betCent, betCentNorm)
    
        closeCent = mbt.nx.centrality.closeness_centrality(a.G)
        extras.writeResults(closeCent, "closeCent", ofb, propDict=propDict, append=appVal)
         
        closeCentNorm = extras.normaliseNodeWise(a.G, mbt.nx.centrality.closeness_centrality, inVal=closeCent)
        extras.writeResults(closeCentNorm, "closeCentNorm", ofb, propDict=propDict, append=appVal)
        del(closeCent, closeCentNorm)
         
        try:
            eigCent = mbt.nx.centrality.eigenvector_centrality_numpy(a.G)
        except:
            eigCent = dict(zip(a.G.nodes(), ['NA' for n in a.G.nodes()]))
        extras.writeResults(eigCent, "eigCentNP", ofb, propDict=propDict, append=appVal)
    
        try:
            eigCentNorm = extras.normaliseNodeWise(a.G, mbt.nx.centrality.eigenvector_centrality_numpy, inVal=eigCent)
        except:
            eigCentNorm = dict(zip(a.G.nodes(), ['NA' for n in a.G.nodes()]))
        extras.writeResults(eigCentNorm, "eigCentNorm", ofb, propDict=propDict, append=appVal)
        del(eigCent, eigCentNorm)
        
        eln = extras.edgeLengths(a.G, nodeWise=True)
        extras.writeResults(eln, "eln", ofb, propDict=propDict, append=appVal)

        elnNorm = {v:[] for v in a.G.nodes()}
        for i in range(500):
            rand = mbt.nx.configuration_model(a.G.degree().values())
            rand = mbt.nx.Graph(rand) # convert to simple graph from multigraph
            mbt.nx.set_node_attributes(rand, 'xyz', {rn:a.G.node[v]['xyz'] for rn,v in enumerate(a.G.nodes())}) # copy across spatial information
            res = extras.edgeLengths(rand, nodeWise=True)
            
            for x,node in enumerate(elnNorm):
                elnNorm[node].append(res[x])

        for node in elnNorm:
            elnNorm[node] = eln[node]/np.mean(elnNorm[node])
        
        
        extras.writeResults(elnNorm, "elnNorm", ofb, propDict=propDict, append=appVal)
        del(eln, elnNorm)
        
        el = extras.edgeLengths(a.G)
        meanEL = mbt.np.mean(mbt.np.array((el.values()), dtype=float))
        extras.writeResults(meanEL, "meanEL", ofb, propDict=propDict,
                            append=appVal)
    
        elNorm = []
    
        for i in range(500):
            rand = mbt.nx.configuration_model(a.G.degree().values())
            rand = mbt.nx.Graph(rand) # convert to simple graph from multigraph
            mbt.nx.set_node_attributes(rand, 'xyz', {rn:a.G.node[v]['xyz'] for rn,v in enumerate(a.G.nodes())}) # copy across spatial information
            elNorm.extend([v for v in extras.edgeLengths(rand).values()])
    
        meanEL = np.mean(np.array((el.values()), dtype=float))
        meanELNorm = np.mean(np.array((elNorm), dtype=float))
        extras.writeResults(meanEL, "meanEL", ofb, propDict=propDict, append=appVal)
        extras.writeResults(meanELNorm, "meanELNorm", ofb, propDict=propDict, append=appVal)
    
        medianEL = np.median(np.array((el.values()), dtype=float))
        medianELNorm = np.median(np.array((elNorm), dtype=float))
        extras.writeResults(medianEL, "medianEL", ofb, propDict=propDict, append=appVal)
        extras.writeResults(medianELNorm, "medianELNorm", ofb, propDict=propDict, append=appVal)
        
        del(el, elNorm, meanEL, meanELNorm, medianEL, medianELNorm)
        
#        # modularity metrics
#        ci = bct.modularity_louvain_und(a.bctmat)
#        Q = ci[1]
#        ciN = a.assignbctResult(ci[0])
#        extras.writeResults(Q, "Q", ofb, propDict=propDict, append=appVal)
#        extras.writeResults(ciN, "ci", ofb , propDict=propDict, append=appVal)  
#        
#        pcCent = bct.participation_coef(a.bctmat,ci[0])
#        pcCent = a.assignbctResult(pcCent)
#        extras.writeResults(pcCent, "pcCent", ofb, propDict=propDict,
#                            append=appVal)
#        del pcCent
#        
#        wmd = extras.withinModuleDegree(a.G, ciN)
#        extras.writeResults(wmd, "wmd", ofb, propDict=propDict, append=appVal)
#        del wmd    
#        
#        nM = len(mbt.np.unique(ci[0]))
#        extras.writeResults(nM, "nM", ofb, propDict=propDict, append=appVal)
#        del(nM)
#        del(ci, ciN, Q)
#        
#        # rich club measures
#        rc = mbt.nx.rich_club_coefficient(a.G, normalized=False)
#        extras.writeResults(rc, "rcCoeff", ofb, propDict=propDict, append=appVal)
#        del(rc)
#        # robustness
#        rbt = a.robustness()
#        extras.writeResults(rbt, "robustness", ofb, propDict=propDict,
#                            append=appVal)
#
#        # Newman partitioning
#        ciNm = bct.modularity_und(a.bctmat)
#        QNm= ciNm[1]
#        ciNNm = a.assignbctResult(ciNm[0])
#        extras.writeResults(QNm, "QNm", ofb, propDict=propDict, append=appValT)
#        extras.writeResults(ciNNm, "ciNm", ofb, propDict=propDict, append=appValT)
#        del QNm
#        
#        nMNm = len(mbt.np.unique(ciNm[0]))
#        extras.writeResults(nMNm, "nMNm", ofb, propDict=propDict, append=appValT)
#        del nMNm
#    
#        pcCentNm = bct.participation_coef_sign(a.bctmat,ciNm[0])
#        pcCentNm = a.assignbctResult(pcCentNm)
#        extras.writeResults(pcCentNm, "pcCentNm", ofb, propDict=propDict, append=appValT)
#        del pcCentNm
#        
#        wmdNm = extras.withinModuleDegree(a.G, ciNNm, weight='weight')
#        extras.writeResults(wmdNm, "wmdNm", ofb, propDict=propDict, append=appValT)
#        del(wmdNm,ciNNm,ciNm)

        # append any further iterations
        appVal = True
    
    propDict = {"pcLoss":pcLoss}
    # weighted measures

    a.weightToDistance()
    ofb = '_'.join(["brain", degenName, "d"+dVal+"_"])
    a.makebctmat()
    
    # weighted hub metrics
    degs = a.G.degree(weight='weight')
    extras.writeResults(degs, "degree_wt", ofb, propDict=propDict, append=appValW)
    
    betCent = mbt.centrality.betweenness_centrality(a.G, weight='distance')
    extras.writeResults(betCent, "betCent_wt", ofb, propDict=propDict, append=appValW)
    
    closeCent = mbt.centrality.closeness_centrality(a.G, distance='distance')
    extras.writeResults(closeCent, "closeCent_wt", ofb, propDict=propDict, append=appValW)
    
    eigCent = mbt.centrality.eigenvector_centrality_numpy(a.G)
    extras.writeResults(eigCent, "eigCentNP_wt", ofb, propDict=propDict, append=appValW)
    del(eigCent)
    
#    # weighted modularity metrics
#    ci = bct.modularity_louvain_und_sign(a.bctmat)
#    Q = ci[1]
#    ciN = a.assignbctResult(ci[0])
#    extras.writeResults(Q, "Q_wt", ofb, propDict=propDict, append=appValW)
#    extras.writeResults(ciN, "ci_wt", ofb, propDict=propDict, append=appValW)  
#    
#    nM = len(mbt.np.unique(ci[0]))
#    extras.writeResults(nM, "nM_wt", ofb, propDict=propDict, append=appValW)
#    del(nM)
#    
#    wmd = extras.withinModuleDegree(a.G, ciN, weight='weight')
#    extras.writeResults(wmd, "wmd_wt", ofb, propDict=propDict, append=appValW)
#    del wmd
#        
#pl = mbt.nx.average_shortest_path_length(a.G, weight="distance")
#extras.writeResults(pl, "pl_wt", ofb, append=appVal)
#del(pl)
#
#ge = extras.globalefficiency(a.G, weight="distance")
#extras.writeResults(ge, "ge_wt", ofb, append=appVal)
#del(ge)
#
#le = extras.localefficiency(a.G, weight="distance")
#extras.writeResults(le, "le_wt", ofb, append=appVal)
#del(le)
#
#pcCent = np.zeros((len(a.G.nodes()), 10))
#betCentT = np.zeros((len(a.G.nodes()), 10))
#cc = np.zeros((len(a.G.nodes()), 10))
#
#nM = np.zeros((10))
##clustCoeff = np.zeros((10))
#wmd = np.zeros((len(a.G.nodes()), 10))
#Q = np.zeros((10))
#
#pcCentIM = np.zeros((len(a.G.nodes()), 10))
#nMIM = np.zeros((10))
#wmdIM = np.zeros((len(a.G.nodes()), 10))
#QIM = np.zeros((10))
#
#pcCentNm = np.zeros((len(a.G.nodes()), 10))
#nMNm = np.zeros((10))
#wmdNm = np.zeros((len(a.G.nodes()), 10))    
#QNm = np.zeros((10))
#
#appValT=False
#
#for n,i in enumerate([v for v in range(1,11)]):
#    a.localThresholding(edgePC=i)
#    a.removeUnconnectedNodes()
#    a.makebctmat()
#    a.weightToDistance()
#    ofbT = '_'.join(["brain", thresholdtype, str(i), "d"+dVal+"_"])
#    propDict = {"edgePC":a.edgePC}
#    
#    # weighted modularity metrics
#    ci = bct.modularity_louvain_und_sign(a.bctmat)
#    QWt = ci[1]
#    Q[n] = QWt
#    ciN = a.assignbctResult(ci[0])
#    extras.writeResults(QWt, "QWt", ofbT, propDict=propDict, append=appValT)
#    extras.writeResults(ciN, "ciWt", ofbT, propDict=propDict, append=appValT)
#    del QWt
#    
#    nMWt = len(np.unique(ci[0]))
#    nM[n] = nMWt
#    extras.writeResults(nMWt, "nMWt", ofbT, propDict=propDict, append=appValT)
#    del(nMWt)
#
#    wmdWt = extras.withinModuleDegree(a.G, ciN, weight='weight')
#    wmd[:,n] = [wmdWt[v] for v in a.G.nodes()]
#    extras.writeResults(wmdWt, "wmdWt", ofbT, propDict=propDict, append=appValT)
#    del wmdWt
#    
#    pcCentWt = bct.participation_coef_sign(a.bctmat,ci[0])
#    pcCent[:,n] = pcCentWt
#    pcCentWt = a.assignbctResult(pcCentWt)
#    extras.writeResults(pcCentWt, "pcCentWt", ofbT, propDict=propDict, append=appValT)
#    
#    # infomap partitioning
#    bIM = infomap.nx2infomap(a.G)
#    del(bIM)
#    f = open("nxdigraph.clu", "r") # recapture results from output file
#    modules = mbt.np.array([int(v.strip('\n')) for v in f.readlines()[1:]])
#    f.close()
#    remove("nxdigraph.clu")
#    
#    ciNIM = a.assignbctResult(modules)
#    QIMWt = community.modularity(ciNIM, a.G)
#    QIM[n] = QIMWt
#    extras.writeResults(QIMWt, "QIMWt", ofbT, propDict=propDict,append=appValT)
#    extras.writeResults(ciNIM, "ciIMWt", ofbT, propDict=propDict, append=appValT)
#    del(QIMWt)
#    
#    nMIMWt = len(np.unique(modules))
#    nMIM[n] = nMIMWt
#    extras.writeResults(nMIMWt, "nMIMWt", ofbT, propDict=propDict, append=appValT)
#    del(nMIMWt)
#    
#    pcCentIMWt = bct.participation_coef_sign(a.bctmat, modules)
#    pcCentIM[:,n] = pcCentIMWt
#    pcCentIMWt = a.assignbctResult(pcCentIMWt)
#    extras.writeResults(pcCentIMWt, "pcCentIMWt", ofbT, propDict=propDict, append=appValT)
#    del(pcCentIMWt)
#    
#    wmdIMWt = extras.withinModuleDegree(a.G, ciNIM, weight='weight')
#    wmdIM[:,n] = [wmdIMWt[v] for v in a.G.nodes()]
#    extras.writeResults(wmdIMWt, "wmdIMWt", ofbT, propDict=propDict, append=appValT)
#    del wmdIMWt
#
#    # Newman partitioning
#    ciNm = bct.modularity_und(a.bctmat)
#    QNmWt = ciNm[1]
#    QNm[n] = QNmWt
#    ciNNm = a.assignbctResult(ciNm[0])
#    extras.writeResults(QNmWt, "QNmWt", ofbT, propDict=propDict, append=appValT)
#    extras.writeResults(ciNNm, "ciNmWt", ofbT, propDict=propDict, append=appValT)  
#    
#    nMNmWt = len(np.unique(ciNm[0]))
#    nMNm[n] = nMNmWt
#    extras.writeResults(nMNmWt, "nMNmWt", ofbT, propDict=propDict, append=appValT)
#    del(nMNmWt)
#
#    pcCentNmWt = bct.participation_coef_sign(a.bctmat,ciNm[0])
#    pcCentNm[:,n] = pcCentNmWt
#    pcCentNmWt = a.assignbctResult(pcCentNmWt)
#    extras.writeResults(pcCentNmWt, "pcCentNmWt", ofbT, propDict=propDict, append=appValT)
#    
#    wmdNmWt = extras.withinModuleDegree(a.G, ciNNm, weight='weight')
#    wmdNm[:,n] = [wmdNmWt[v] for v in a.G.nodes()]
#    extras.writeResults(wmdNmWt, "wmdNmWt", ofbT, propDict=propDict, append=appValT)
#    del wmdNmWt
#
#    ccWt = mbt.nx.clustering(a.G, weight="weight")
#    cc[:,n]  = [ccWt[v] for v in a.G.nodes()]
#    extras.writeResults(ccWt, "ccWt", ofbT, propDict=propDict, append=appValT)
#    
#    clustCoeffWt = np.average(ccWt.values())
#    clustCoeff[n] = clustCoeffWt
#    extras.writeResults(clustCoeffWt, "clustCoeffWt", ofbT, propDict=propDict, append=appValT)
#    del(clustCoeffWt)
#    del(ccWt)
#
#    bcT = mbt.nx.centrality.betweenness_centrality(a.G, weight='distance')    
#    betCentT[:,n] = [bcT[v] for v in a.G.nodes()]
#    appValT=True
#    
#    
#Q = np.mean(Q)
#extras.writeResults(Q, "QWt_wt", ofb, append=appVal)
#del(Q)
#
#pcCent = a.assignbctResult(np.mean(pcCent, axis=1))
#extras.writeResults(pcCent, "pcCentWt_wt", ofb, append=appVal)
#    del(pcCent,ci)
#    
    betCentT = a.assignbctResult(mbt.np.mean(betCentT, axis=1))
    extras.writeResults(betCentT, "betCentWtT_wt", ofb, propDict=propDict, append=appValW)
#    
#    nM = mbt.np.mean(nM)
#    extras.writeResults(nM, "nMWt_wt", ofb, propDict=propDict, append=appValW)
#    del(nM)
#    
#    wmd = a.assignbctResult(mbt.np.mean(wmd, axis=1))
#    extras.writeResults(wmd, "wmdWt_wt", ofb, propDict=propDict, append=appValW)
#    del(wmd)
#    
#    # Newman
#    QNm = mbt.np.mean(QNm)
#    extras.writeResults(QNm, "QNmWt_wt", ofb, append=appValW)
#    del(QNm)
#    
#    pcCentNm = a.assignbctResult(mbt.np.mean(pcCentNm, axis=1))
#    extras.writeResults(pcCentNm, "pcCentNmWt_wt", ofb, append=appValW)
#    del(pcCentNm)
#     
#    wmdNm = a.assignbctResult(mbt.np.mean(wmdNm, axis=1))
#    extras.writeResults(wmdNm, "wmdNmWt_wt", ofb, append=appValW)
#    del(wmdNm)
#    
#    nMNm = mbt.np.mean(nMNm)
#    extras.writeResults(nMNm, "nMNmWt_wt", ofb, append=appValW)
#    del(nMNm)
    a.adjMatThresholding(MST=False)

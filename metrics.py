from maybrain import mayBrainTools as mbt
from maybrain import mayBrainExtraFns as extras
import bct

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


#    # prepare matrices for weighted measures
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
        extras.writeResults(degs, "degree", ofb, propDict=propDict,
                            append=appVal)
        
        clustCoeff = mbt.nx.average_clustering(a.G)
        extras.writeResults(clustCoeff, "clusterCoeff", ofb, propDict=propDict,
                            append=appVal)
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
        betCent = mbt.centrality.betweenness_centrality(a.G)
        extras.writeResults(betCent, "betCent", ofb, propDict=propDict,
                            append=appVal)
        
        closeCent = mbt.centrality.closeness_centrality(a.G)
        extras.writeResults(closeCent, "closeCent", ofb, propDict=propDict,
                            append=appVal)
         
        hs = extras.hubscore(a.G, bc=betCent, cc=closeCent, degs=degs,
                             weighted=False)
        extras.writeResults(hs, "hs", ofb, propDict=propDict, append=appVal)
        del(hs, betCent, closeCent, degs)
         
        try:
            eigCent = mbt.centrality.eigenvector_centrality_numpy(a.G)
        except:
            eigCent = dict(zip(a.G.nodes(), ['NA' for n in a.G.nodes()]))
        extras.writeResults(eigCent, "eigCentNP", ofb, propDict=propDict,
                            append=appVal)
        del(eigCent)
        
        eln = extras.edgeLengths(a.G, nodeWise=True)
        extras.writeResults(eln, "eln", ofb, propDict=propDict, append=appVal)
        del(eln)
        
        el = extras.edgeLengths(a.G)
        meanEL = mbt.np.mean(mbt.np.array((el.values()), dtype=float))
        extras.writeResults(meanEL, "meanEL", ofb, propDict=propDict,
                            append=appVal)
    
        medianEL = mbt.np.median(mbt.np.array((el.values()), dtype=float))
        extras.writeResults(medianEL, "medianEL", ofb, propDict=propDict,
                            append=appVal)
    
        del(el, meanEL, medianEL)
        
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
    a.adjMatThresholding(MST=False)
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
    appValT=False
        
#    pcCent = a.assignbctResult(mbt.np.mean(pcCent, axis=1))
#    extras.writeResults(pcCent, "pcCentWt_wt", ofb, propDict=propDict, append=appValW)
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

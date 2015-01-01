# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 13:30:05 2013

@author: tim
"""
from os import path
from glob import glob
from string import split
from numpy import mean,nan,isnan
import csv

# class definition

class metricObj:
    def __init__(self, dVal, diag, cond=None):
        # define wavelet scale
        self.dVal = "d"+str(dVal)
        
        # define diagnosis list
        self.diag = diag
        self.cond = cond        
        
        # get subject list
        if self.cond:
            self.subjList = [ v for v in glob(path.join(diag, "*", cond)) if path.isdir(v) ]
        else:
            self.subjList = [ v for v in glob(path.join(diag, "*")) if path.isdir(v) ]
            
        self.subjList = [ v for v in self.subjList if not 'excluded' in v ]
        
    def collate(self,
                metricroot,
                eVals = [str(v) for v in range(1,11)],
                thresholdtype="local"):
                
        # prepare output file
        if self.cond:
            outFile = path.join(self.diag, '_'.join([self.cond, self.dVal, metricroot, thresholdtype]))
        else:
            outFile = path.join(self.diag, '_'.join([self.dVal, metricroot, thresholdtype]))

        out = open(outFile, "wb")
        
        o = csv.DictWriter(out, fieldnames=None ,delimiter=" ")

        # get file list
        if eVals:
            fNames = ['_'.join(["brain", thresholdtype, e, self.dVal, metricroot+'.txt']) for e in eVals]
        
        else:
            fNames =  ['_'.join(["brain", self.dVal, metricroot+'.txt'])]
            eH = 'weighted'
            
        # iterate through files
        for subj in self.subjList:
            for fName in fNames:
                try:
                    f = open(path.join(subj, fName))
                    reader = csv.DictReader(f, delimiter=" ")
                    
                    if eVals:
                        eH = split(fName, sep="_")[2]
                                    
                    # assign values to output dictionary
                    for l in reader:
                        l["edgePC"] = eH
                        l["wbic"] = path.basename(subj)
                        if not o.fieldnames:
                            headers = ["wbic"]
                            headers.extend(reader.fieldnames)
                            if not 'edgePC' in headers:
                                headers.insert(0, 'edgePC')
                            
                            
                            if len(headers) > 3:
                                headers = headers[:headers.index('0')]
                                headers.extend([str(v) for v in range(500)])
                            
                            o.fieldnames = headers
                            o.writeheader()
                        for h in headers:
                            if not h in l.keys():
                                l[h] = "NA"
                        o.writerow(l)
                    f.close()
                except IOError:
                    print ' '.join([subj, fName])

        out.close()
            
diags = ["Control", "PD"]
conds = ["placebo", "atomoxetine", "citalopram"]

for d in range(2,3):
    for thresholdtype in ["local"]:
        for diag in diags:
            for cond in conds:
                print diag
                
                a = metricObj(d, diag, cond)
                
                # get list of graph metrics
                mList = None
                while not mList:
                    for sn,subj in enumerate([v for v in glob(path.join(diag, "*")) if all([path.isdir(v), path.basename(v)!=diag])]):
                        subjOne = [v for v in glob(path.join(diag, "*")) if path.isdir(v)][sn]
                        print subjOne
                        mList = [split(path.basename(v), sep="_")[-1][:-4] for v in glob(path.join(subjOne, "brain*")) if not 'wt' in v]
                        mList.extend(  ['_'.join(split(path.basename(v), sep="_")[-2:])[:-4] for v in glob(path.join(subjOne, "brain*")) if 'wt' in v] )
                        mList = [v for v in mList if all([not '.old' in v, not '.txt' in v])]
    
                        mList = set(mList)
                        print mList
                        
                for metric in mList:
                    if 'wt' in metric:
                        print metric
                        a.collate(metric, eVals=None)
                    else:
                        print metric
                        a.collate(metric)


# split control metrics
# get list of subjects
f = open("ControlLog.txt", "rb")
subjDict = {l.split()[0]:[split(v,'/')[1] for v in l.split()[1:]] for l in f.readlines()}
f.close()

# get list of metrics
metrics = [v for v in glob("Control/d2_*local")]
#metrics.remove("Control/d2_eigCent_local")
#metrics.remove("Control/d2_hs_local")

# split metrics
for m in metrics:
    print m
    f = open(m, "rb")
    reader = csv.DictReader(f, delimiter=" ")
    
    outFilesOpenDict= {}
    outFileDict = {}
    for s in subjDict.keys():
        outFilesOpenDict[s] = open(path.join("Control"+s,path.basename(m)),"wb")
        outFileDict[s] = csv.DictWriter(outFilesOpenDict[s], fieldnames=reader.fieldnames, delimiter=" ")
        outFileDict[s].writeheader()
    
    for l in reader:
        for s,t in subjDict.iteritems():
            if l['wbic'] in t:
                outFileDict[s].writerow(l)
                break
            else:
                pass
    f.close()
    for s in subjDict.keys():
         outFilesOpenDict[s].close()

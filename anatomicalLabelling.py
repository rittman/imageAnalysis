# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 00:34:37 2016
The aim of this script is to assign anatomical labels to nodes that can be
added to a maybrain object. This depends on a list of anatomical labels from
the AAL atlas, then overlaying this on to a parcellation scheme.
@author: tim
"""

import numpy as np
import csv
import nibabel as nb

parcelFile = "parcels/parcel_500.nii"
AALFile = "aal/ROI_MNI_V5.nii"
AALtext = "aal/ROI_MNI_V5.txt"
lobeFile = "aal/lobeList.csv"
outFile = parcelFile.replace(".nii","_lobe_data.txt")

def match(region,AALData,pData,AALlabels):
    """
    returns the anatomical location of the MRI region by finding the AAL region
    that it most overlaps with
    """
    intArr = np.where(pData==region, AALData, 0.) # mask the AAL data by the fMRI region
    intUnique = np.unique(intArr) # get the unique AAL regions within the fMRI region
    if intUnique.any():
        intUnique = intUnique[intUnique!=0.] # remove zeros
        intDict = {v:len(intArr[intArr==v]) for v in intUnique} # dictionary of the size of each AAL region
        v = intUnique[0]
        for i in intDict.keys():
            if intDict[i] > intDict[v]:
                v=i
        return(AALlabels[str(int(i))]['Anatomical label']) # look up the AAL region in the anatomical labels dictionary
    else:
        return('None')
            

# import parcellation file and extract data as a matrix
pScan = nb.load(parcelFile)
pData = pScan.get_data()

# import AAL file and extract data as a matrix
AALScan = nb.load(AALFile)
AALData = AALScan.get_data()

# import text file containing AAL node numbers and anatomical labels as a dictionary
fields = ["Code","Anatomical label","Region"]
with open(AALtext) as f:
    reader = csv.DictReader(f,
                            fieldnames = ["Code","Anatomical label","Region"], 
                            delimiter="\t")
    AALlabels = {v["Region"]:{k:v[k] for k in fields} for v in reader}
f.close()

# get unique parcel values
pData_unique = np.unique(pData)
pData_unique = [x for x in pData_unique[1:]]# # removes the zero which we're not interested in and converts to a list

# get matching lobe definitions for anatomical areas
f = open(lobeFile, "r")
reader = csv.DictReader(f, delimiter="\t")
lobeDict = {}
for r in reader:
    lobeDict[r["Region"]]=r["Lobe"]
f.close()

outDict = {str(int(v)):match(v,AALData,pData,AALlabels) for v in pData_unique} # create dictionary of nodes and anatomical labels

# now write the final file with node, anatomical label and lobe designation
outHeaders = ["Node", "AnatLabel", "Lobe"]
with open(outFile,"w") as out:
    outWriter = csv.DictWriter(out, outHeaders, delimiter="\t")
    outWriter.writeheader()
    for i in outDict.keys():
        outWriter.writerow({"Node":i,
                            "AnatLabel":outDict[i],
                            "Lobe":lobeDict[outDict[i]]})
out.close()

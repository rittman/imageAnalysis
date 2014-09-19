#The purpose of this script is to calculate the number of participants/scans which remain after excluding scans which have a median spike percentage above a specific value. Ameera recommends this threshold to be around 5%. For this study it will probably be around 10% to avoid having to exclude the majority of the data. As a reminder, spike percentage is the percentage of all voxels in a frame which contain a spike. The median spike percentage is taking the media of the spike percentages from each frame across a scan. 

from string import split

SPmedian = open('/scratch/rb729/PDStudy/SP_median.txt','r')

lines = SPmedian.readlines()

wDict = {}
for l in lines[1:]:
	bits = split(l,sep="\t")
	if bits[1] == "PD":
		if not bits[0] in wDict.keys():
			wDict[bits[0]] = []
		if float(bits[5].rstrip('\n')) < 5.:    #the value here is referring to the threshold which is being defined so later on all the output values will be based on a percentage threshold defined by this value. 5% is the percent ameera recommended but we will probably use 10%, otherwise we'd have to cut out a lo to four data. 
			wDict[bits[0]].append(bits[3])  # append the condition

lAll = len(wDict.keys())
lThree = len([v for v in wDict.keys() if len(wDict[v])==3])
print "Total no of PD subjects: "+str(lAll) 
print "No subjects with all three scans surviving the motion threshold: "+str(lThree)
print "Proportion with all three scans surviving the motion threshold:"
print (float(lThree)/lAll) * 100


nPlac = [v for v in wDict.keys() if "placebo" in wDict[v]]
nCit = [v for v in wDict.keys() if "citalopram" in wDict[v]]
nAto = [v for v in wDict.keys() if "atomoxetine" in wDict[v]]

print "Number of placebo scans surviving motion threshold: "+str(len(nPlac))
print "Number of citalopram scans surviving motion threshold: "+str(len(nCit))
print "Number of atomoxetine scans surviving motion threshold: "+str(len(nAto))

lPlacAto = [v for v in nPlac if v in nAto]
lPlacCit = [v for v in nPlac if v in nCit]

print "Number with both placebo and atomoxetine scans: " + str(len(lPlacAto))
print "Number with both placebo and citalopram scans: " + str(len(lPlacCit))
SPmedian.close()


# the purpose of this script is to calculate the median spike percentage of each scan. spike percentage is the percentage of all voxels in each frame of a scan which contain spikes, however we want to calculate the media spike percentage across all frames for a scan and this is what this scan is doing. then finally with this median spike percentage we can decide which scans to exclude due to excessive presence of motion artefacts. 



from os import chdir,getcwd,listdir,path #this imports chdir, whic is the equivalent of cd as well as getcwd which is the equivalent of pwd
from numpy import median,array
import os

diagList = ["Control", "PD"]

list = [] #creating an empty list here which we are going to use later in the script. 
mainDir = getcwd()
SPmedian = open('spikePercentages.txt','w') #this is creating a new text file which we will use to write the output of the script to. 'w' stands for 'write' because we are going to be writing to this file as opposed to reading from it.   

SPmedian.writelines('\t'.join(["WBIC", "Diagnosis", "Condition", "median\n"])) #here, we are writing these strings into our empty SPmedian text file. These will be the titles of the columns and the data will fall in rows underneath these column headers. 
for d in diagList: #for loop for d. d is either control or PD as a result.
	#print d
	directory = listdir(d) #listdir(path3) is a function to list path3, in this case the list only consists of the 'Control' folder and the 'PD' folder so our variable 'directory' pretty much defines these two folders. 
	
	for WBIC in directory: #now we move one folder deeper to the WBIC number. 'WBIC' here represents all the wbic numbers in this for loop. 
		#print WBIC
		path1 = path.join(d,WBIC) #this tells us where to find the WBIC folders
		subdirectory = listdir(path1) #again, here we are making a variable which is defined by the list of all the WBIC folders. 

		for condition in subdirectory: #now we're going into the condition folder where ultimately we'll be able to find the original spike percentage text which tells us the spike percentage for each frame of the scan. There shouldn't be more than one folder per subject though
			try:
				chdir(path.join(mainDir, d, WBIC, condition, 'preprocessing'))
				SP = open('FUNCTIONAL_SP.txt','r') #this is opening the text file with the spike percentage information for each frame. 'r' means that we're reading from the file as oppossed to writing to it as we are doing with the SPmedian text file. 	
				SPlist = [float(v.rstrip('\n')) for v in SP.readlines()]
				mu = median(SPlist) #this is calculating the median of spike percentages for each frame in the scan
				list.append(mu) #we are appending the median value to the list which we created earlier, so each time it goes through this loop with different scans it always adds the median to the end of the list. 
# get proportion surviving
								
				SPmedian.writelines('\t'.join([WBIC,d,condition,str(mu)+'\n'])) #this writes each rowe of our new SPmedian text file. first column wbic number, then tab, then condition, then tab, then median, then new line which is indicated with '\n'. 
			except: #this is here because some participants have folders for a specific scan condition however the functional data isn't there so we obviously don't have the spike percentage data for them. if this is the case, the following error message will appear:
				print 'something is wrong with this participant - potentially no functional scan'
		chdir(mainDir)
	arr = array(list)
	print d + ": spike threshold of 10%"
	print (float(len(arr[arr>10])) / len(arr)) * 100
	print d + ": spike threshold of 5%"
	print (float(len(arr[arr>5])) / len(arr)) * 100


SPmedian.close()

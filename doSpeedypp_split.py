from os import system,path,getcwd,chdir
from glob import glob

speedyoriglist = glob('*/*/*/_spp_*_functional_reordered.sh') #this creates a list of all the bash scripts for each participant

curDir = getcwd() #this defines curDir as the current directory which should be /scratch/rb729/PDStudy

for speedyorig in speedyoriglist: #iterating through the list of the bash scripts
	orig = open(speedyorig, 'r') #opening the original bash script
	chdir(path.split(speedyorig)[0]) #this splits the path of speedyorig so that it only takes the path and not the actual file name. This is achieved using [0]. 
	speedybeforeWD = open('speedybeforeWD.sh','w') #create the new speedy script which will be used before despiking - w for write
	speedyafterWD = open('speedyafterWD.sh','w') #create the new speedz script which will be used after despiking - w for write
	lines = orig.readlines() #lines is now a variable for each line within the bash script
	for n,line in enumerate(lines):
		if '0.020000 99 ' in line:
			print n #print n, the number of the line which contains 0.0200...  this is where we want to cut the script
			speedybeforeWD.writelines(lines[:n]) #write the lines up to n in our new before spiking speedy script
			speedyafterWD.writelines(lines[n:]) #write the lines from n to the end in our new after spiking speedy script
			break #stop iterating through script (to save time)
	speedybeforeWD.close() #close the files of course...
	speedyafterWD.close()
	orig.close()
	system('qsub bash '+path.basename(speedybeforeWD)) #run the new speedy before despiking script straight from here

	chdir(curDir) #return back to /scratch/rb729/PDStudy for the iteration through the next participant

d=$1 # Diagnosis

mainDir=`pwd`
dataDir=/data/tr332/preprocessing_20130531/
graphDir=/data/tr332/graphs_20130531
func=functional_reordered_pp_wpd_MNI.nii
mot=functional_reordered_motion.1D
ts=functional_reordered_pp_wpd_MNI500_ts.txt
tsCol=functional_reordered_pp_wpd_MNI500_ts_col.txt

for ih in ${d}/*/*
do
#	echo ${ih}
#	cp ${dataDir}/${ih}/${mot} ${ih}/${mot}
	
	echo "Running motion check"
	./runMotionCheck.sh ${ih} $mainDir functional_reordered parcel_500_xyz_nolabels_mm.txt
	#echo "Moving scans back"
	
#	# make graph directory diagnosis subdirectory if necessary
#	if [ ! -d ${graphDir}/${d} ]
#	then
#		mkdir ${graphDir}/${d}
#	fi
#	
#	# make graph directory subject directory if necessary
#	i [ ! -d ${graphDir}/${ih} ]
#	then
#		mkdir ${graphDir}/${ih}
#	fi
#	
#	# Move everything to the data graph directory
#	mv ${ih}/* ${graphDir}/${ih}
#	rmdir ${ih}
done

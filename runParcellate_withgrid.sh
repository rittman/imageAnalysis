#!/bin/bash
# Run this script specifying the diagnosis, eg runParcellate_withgrid Control
# definitions
diag=$1
baseDir=`pwd`
dataDir=/data/tr332/preprocessing_20130531
func=functional_reordered_pp.nii   # functional file warped to study specific template
struc=structural_reordered_ns.nii  # structural file warped to study specific template
subfile=submitfile.sh
tsScript=/home/tr332/jobs/tsExtractorScript.py
#warp=${baseDir}/${diag}toMNI.nii
#MNISpace=${baseDir}/MNI152_T1_2mm_brain.nii.gz

# Check if diagnosis directory exists, and create if necessary
if [ ! -d $diag ]
then
  mkdir $diag
fi

for i in ${dataDir}/${diag}/*/* # adjusted to search subdirectories, eg placebo/citalopram
do
  # check if data directory exists 
  if [ -d $i ]
  then  
    # define local directory
    i=${diag}/${i##*$diag\/} 
    
    # check if structural file exists
    if [ -e $dataDir/${i}/${struc} ]
    then
      # make local directory if it doesn't exit
      echo $i
      if [ ! -d $i ]
      then
        mkdir $i
      fi
      
      # switch to subject directory
      cd $i
      
      # copy files from data to scratch 
      cp $dataDir/${i}/${struc} .
      cp $dataDir/${i}/${func} .
      
      ### write functions to submit script ###
      echo -e "#!/bin/bash\n#$ -cwd\n#$ -l qname=clusterall.q\n#$ -V\n" > $subfile      
      
#      # warp functional scan to MNI space, take mean across time and create mask
#      echo -e "applywarp -i ${func} -o ${func/.nii/_MNI.nii} -r $MNISpace -w $warp" >> $subfile
      echo -e "fslmaths ${func} -Tmean ${func/.nii.gz/_mean.nii.gz}" >> $subfile
      echo -e "fslmaths ${func/.nii.gz/_mean.nii.gz} -mul ${func/.nii.gz/_mean.nii.gz} -bin ${func/.nii.gz/_mask.nii.gz}" >> $subfile
#      
      # warp structural scan to MNI space, threshold and create mask
#      echo -e "applywarp -i $struc -o ${struc/.nii/_MNI.nii} -r $MNISpace -w $warp" >> $subfile
      echo -e "fslmaths ${struc/.nii/_MNI.nii} -thr 50 -bin ${struc/.nii/_mask.nii}" >> $subfile

      for x in 100 200 300 400 500
      do
        parcel=parcel_${x}.nii
        echo -e "python $tsScript ${func/.nii/_MNI.nii} ${struc/.nii/_mask.nii} ${func/.nii/_mask.nii} ${x}" >> $subfile
      done
      
      # submit to grid engine
      qsub $subfile
      
      # return to original directory
      cd $baseDir
      fi
      
    else
      # if structural scan not present, make a note in the log
      echo -e "$i $dataDir/${i}/${struc}\n" >> ${diag}_log.txt
    fi
done

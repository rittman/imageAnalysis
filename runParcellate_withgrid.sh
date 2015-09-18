#!/bin/bash
# Run this script specifying the diagnosis, eg runParcellate_withgrid Control
# definitions
baseDir=`pwd`
dataDir=/data/tr332/GENFI_20150525
funcT=functional_reordered_pp_thld10_wds_corr.nii.gz # functional file warped to study specific template
strucT=structural_struc_brain.nii.gz # structural file warped to study specific template
subfile=submitfile.sh
tsScript=/home/tr332/pythonLib/imageAnalysis/tsExtractorScript.py
#warp=${baseDir}/${diag}toMNI.nii
#MNISpace=${baseDir}/MNI152_T1_2mm_brain.nii.gz

for i in ${dataDir}/* # 
do
  # check if data directory exists 
  if [ -d $i ]
  then  

    # define local directory
    i=${i##*\/} 
    echo $i
    
    # get WBIC number
    w=$i
    func=${funcT}
    struc=${strucT}
    echo $func

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

      echo `ls`
      
      ### write functions to submit script ###
      echo -e "#!/bin/bash\n#$ -cwd\n#$ -l qname=clusterall.q\n#$ -V\n" > $subfile      
      
#      # warp functional scan to MNI space, take mean across time and create mask
#      echo -e "applywarp -i ${func} -o ${func/.nii/_MNI.nii} -r $MNISpace -w $warp" >> $subfile
      echo -e "${FSL_BIN}/fslmaths ${func} -Tmean ${func/.nii.gz/_mean.nii.gz}" >> $subfile
      echo -e "${FSL_BIN}/fslmaths ${func/.nii.gz/_mean.nii.gz} -mul ${func/.nii.gz/_mean.nii.gz} -bin ${func/.nii.gz/_mask.nii.gz}" >> $subfile
#      
      # warp structural scan to MNI space, threshold and create mask
#      echo -e "applywarp -i $struc -o ${struc/.nii/_MNI.nii} -r $MNISpace -w $warp" >> $subfile
      echo -e "${FSL_BIN}/fslmaths ${struc} -thr 50 -bin ${struc/.nii.gz/_mask.nii.gz}" >> $subfile

      for x in 100 200 300 400 500
      do
        parcel=parcel_${x}.nii
        echo -e "python $tsScript ${func} ${struc/.nii.gz/_mask.nii.gz} ${func/.nii.gz/_mask.nii.gz} ${x}" >> $subfile
      done
      
      # submit to grid engine
      qsub $subfile
      
      # return to original directory
      cd $baseDir
    
    else
      # if structural scan not present, make a note in the log
      echo -e "$i $dataDir/${i}/${struc}\n" >> log.txt
    fi
  fi
done

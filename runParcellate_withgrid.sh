#!/bin/bash
# Run this script specifying the diagnosis, eg runParcellate_withgrid Control
# definitions
diag=$1 #what does this mean?
baseDir=`pwd`
dataDir=/data/tr332/graphs_20130531
outdataDir=/data/tr332/graphs_aal_20150212
subfile=submitfile.sh
tsScript=/home/tr332/pythonLib/imageAnalysis/tsExtractorScript.py
parcel=aaltoMNI.nii.gz #AAL90_cortonly.nii
warp=${baseDir}/${diag}toMNI.nii.gz
MNISpace=${baseDir}/MNI152_T1_1mm_brain.nii.gz
x=116 # number of parcels in AAL template

# Check if diagnosis directory exists, and create if necessary
if [ ! -d $diag ]
then
  mkdir $diag
fi

if [ ! -d ${outdataDir}/${diag} ]
then
  mkdir ${outdataDir}/${diag}
fi

# search for subject directories
for i in ${dataDir}/${diag}/*
do
  echo $i
  # check if data directory exists 
  if [ -d $i ]
  then  

    # define local directory
    i=${diag}/${i##*$diag\/} 
    
    # get WBIC number
    w=${i##$diag\/} 

    func=functional_reordered_pp_wpd.nii # functional file warped to study specific template
    struc=structural_reordered_ns_wpd.nii #structural_reordered_ns_wpd.nii.gz # structural file warped to study specific template

    # check if structural file exists
    if [[ -e $dataDir/${i}/${struc} || -e $dataDir/${i}/${struc}.gz ]] ; then
     if [[ ! -e ${i}/${struc}  && ! -e ${i}/${struc}.gz ]] ; then
      # make local directory if it doesn't exit
      echo $i
      if [ ! -d $i ]
      then
        mkdir -p $i
      fi
       
      # switch to subject directory
      cd $i

      if  [[ -e $dataDir/${i}/${struc}.gz ]] ; then
       struc=${struc}.gz
       func=${func}.gz
       
       # copy files from data to scratch 
       cp $dataDir/${i}/${struc} .
       cp $dataDir/${i}/${func} .

      elif [[ -e $dataDir/${i}/${struc} ]] ; then
       # copy files from data to scratch 
       cp $dataDir/${i}/${struc} .
       cp $dataDir/${i}/${func} .
 
       # change file type
       fslchfiletype NIFTI_GZ ${struc}
       struc=${struc}.gz
       fslchfiletype NIFTI_GZ ${func}
       func=${func}.gz
       echo `ls`
       
      fi

      ### write functions to submit script ###
      echo -e "#!/bin/bash\n#$ -cwd\n#$ -l qname=clusterall.q\n#$ -V\n" > $subfile      
      
      # warp functional scan to MNI space, take mean across time and create mask
      echo -e "applywarp -i ${func} -o ${func/.nii/_MNI.nii} -r $MNISpace -w $warp" >> $subfile
      func=${func/.nii/_MNI.nii}
      echo -e "${FSL_BIN}/fslmaths ${func} -Tmean ${func/.nii.gz/_mean.nii.gz}" >> $subfile
      echo -e "${FSL_BIN}/fslmaths ${func/.nii.gz/_mean.nii.gz} -mul ${func/.nii.gz/_mean.nii.gz} -bin ${func/.nii.gz/_mask.nii.gz}" >> $subfile
#      
      # warp structural scan to MNI space, threshold and create mask
      echo -e "applywarp -i $struc -o ${struc/.nii/_MNI.nii} -r $MNISpace -w $warp" >> $subfile
      struc=${struc/.nii/_MNI.nii}
      echo -e "${FSL_BIN}/fslmaths ${struc} -thr 50 -bin ${struc/.nii.gz/_mask.nii.gz}" >> $subfile

      echo -e "python $tsScript ${func} ${struc/.nii.gz/_mask.nii.gz} ${func/.nii.gz/_mask.nii.gz} ${x}" >> $subfile
      echo "cd $baseDir" >> $subfile
      echo "mv $i $outdataDir" >> $subfile

      # submit to grid engine
      qsub $subfile
      
      # return to original directory
      cd $baseDir
    
    else
      # if structural scan not present, make a note in the log
      echo -e "$i $dataDir/${i}/${struc}\n" >> ${diag}_log.txt
    fi
   fi
  fi
done

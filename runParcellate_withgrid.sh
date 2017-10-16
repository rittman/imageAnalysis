#!/bin/bash
# Run this script specifying the diagnosis, eg runParcellate_withgrid Control
# definitions
baseDir=`pwd`
func=FUNCTIONAL_ppm_std.nii # functional file warped to MNI space 
struc=DATA_do_std.nii # structural file warped to study specific template
subfile=submitfile.sh
tsScript=/home/tr332/imageAnalysis/tsExtractorScript.py

for i in */*/*/preprocessing # get a list of all subject preprocessing directories
do
  # check if data directory exists 
  if [ -d $i ]
  then  
    cd $i

    # check if structural file exists
    if [ -e $struc ]
    then
      ### write functions to submit script ###
      # create functional mask in case voxels in the template lie outside the are covered by the functional image. Note the functional image has already been masked by the structural image, so no strutural masking is required.
      echo -e "${FSL_BIN}/fslmaths ${func} -Tmean ${func/.nii.gz/_mean.nii.gz}" >> $subfile
      echo -e "${FSL_BIN}/fslmaths ${func/.nii.gz/_mean.nii.gz} -mul ${func/.nii.gz/_mean.nii.gz} -bin ${func/.nii.gz/_mask.nii.gz}" >> $subfile

      # run the parcellation script for each of 5 templates
      for x in 100 200 300 400 500
      do
        parcel=parcel_${x}.nii
        echo -e "python $tsScript ${func} ${func/.nii.gz/_mask.nii.gz} ${x}" >> $subfile
      done
      
      # submit to grid engine
      sbatch $subfile
      
    else
      # if structural scan not present, make a note in the log
      echo -e "$i $dataDir/${i}/${struc}\n" >> log.txt
    fi
    # return to original directory
    cd $baseDir
  fi
done

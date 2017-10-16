#!/bin/bash
func=FUNCTIONAL_ppm_std.nii # functional file warped to MNI space 
struc=DATA_do_std.nii # structural file warped to study specific template
subfile=submitfile.sh
tsScript=/home/tr332/imageAnalysis/tsExtractorScript.py

fslmaths ${func} -Tmean ${func/.nii.gz/_mean.nii.gz}
fslmaths ${func/.nii.gz/_mean.nii.gz} -mul ${func/.nii.gz/_mean.nii.gz} -bin ${func/.nii.gz/_mask.nii.gz}
for x in 100 200 300 400 500
do
 parcel=parcel_${x}.nii
 python $tsScript ${func} ${func/.nii.gz/_mask.nii.gz} ${x}
done


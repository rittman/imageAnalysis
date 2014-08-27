wd=$1
mainDir=$2
func=$3
loc=$4


cd ${mainDir}/${wd}

# switch to cluster4-0 for a bit
ssh -x tr332@cluster4-0 << EOI
cd ${mainDir}/${wd}
echo `pwd`

# get framewise displacement and BOLD variability
fd.sh -i ${func}_motion.1D
dvars.sh -i ${func}_pp_wpd_MNI.nii

# Change timeseries to columns 
python ${mainDir}/colAndReplaceNAs.py ${func}_pp_wpd_MNI500_ts.txt

# get BOLD changes from timeseries
dbold.sh -i ${func}_pp_wpd_MNI500_ts_col.txt
exit
EOI

# back on local server
cd ${mainDir}/${wd}

# get values for Loess plot
loess.sh -f ${func}_motion_fd.txt -d ${func}_pp_wpd_MNI500_ts_col_dbold.txt
# plot Loess plot in R
R --vanilla --slave --args $* < ${mainDir}/plotLoess.R

# do scrubbing
scrub.sh -i ${func}_pp_wpd_MNI500_ts_col.txt -f ${func}_motion_fd.txt -d ${func}_pp_wpd_MNI_dvars.txt

# do Wavelet correlations for cloud plot
###### These lines have been changed to do wavelet rather than pearson corellation ##########
correlate_wavelets.sh ${func}_pp_wpd_MNI500_ts_col.txt
correlate_wavelets.sh ${func}_pp_wpd_MNI500_ts_col_scrub.txt

# get values for Cloud plot
cloud.sh -i ${func}_pp_wpd_MNI500_ts_col_corr.txt -s ${func}_pp_wpd_MNI500_ts_col_scrub_corr.txt -c ${mainDir}/${loc}.txt -o cloud
# plot Cloud plot in R
R --vanilla --slave --args $* < ${mainDir}/plotCloud.R

# get correlation values for Quality Control checking
R --vanilla --slave --args $* < ${mainDir}/corrLoess.R
R --vanilla --slave --args $* < ${mainDir}/corrPower.R
cd $mainDir

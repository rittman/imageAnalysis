# set variables
mbt=`readlink -f ../maybrain.tgz`
p=`readlink -f ../parcel_100.txt`
nx=`readlink -f ../networkx.tgz`
w=`readlink -f wrapper.sh`
psa=`readlink -f ../graphSubjAnalysis.py`
bct=`readlink -f ../bct.tgz`
cm=`readlink -f ../community.tgz`

curDir=`pwd`

# iterate through subjects
for i in *
do
  if [ -d $i ]
  then
    cd $i
    # make symbolic links
    for f in $mbt $psa $w $p $nx $dFile $am $bct $cm
    do
      ln -s $f ${newDir}
    done
    cd $curDir
  fi
done

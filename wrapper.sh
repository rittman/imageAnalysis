#!/bin/bash

for entry in `/bin/ls`
do
  suff=${entry##*.}

  if [[ "$suff" == "py" ]]; then
    chmod +x $entry
    echo $entry
  elif [[ "$suff" == "gz" ]]; then
    gunzip $entry
  elif [[ "$suff" == "tgz" ]]; then
    tar zxf $entry
  fi
done

export PATH="/usr/bin:/bin:/usr/local/bin:."
export PYTHONPATH="."
export ETS_TOOLKIT='null'
export HOME=`/bin/pwd`
python graphSubjAnalysis.py
rm networkx.tgz
rm maybrain.tgz

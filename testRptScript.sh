line="1 2 3 4 5 6 7 8 9"

echo $line
#set -- $line
#len=${#line[@]}
len=`wc -w <<< $line`

echo $len
echo $line

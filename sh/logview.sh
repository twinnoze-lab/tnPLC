#!/bin/bash
waittime=1
if [ $# = 1 ]; then
    waittime=$1
fi

while :
do
    clear
    echo '=== tnPLC processing infomation view ==='
    while read line
    do
        echo $line
    done < ./procinfo.log
    sleep $waittime
done
exit 0

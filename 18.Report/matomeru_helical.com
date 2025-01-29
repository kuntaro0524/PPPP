#!/bin/sh

test $(date "+%m") -lt 8 && AorB=A || AorB=B
prefix=`date "+%y%m%d"`-`date "+%H%M"`
echo $prefix

yamtbx.python ~/PPPP/11.ClusterAnalysis/find_correctlp_and_summarize.py

# $1 : a path for data processing
# $2 : a prefix for an output .tgz

find ./$1 -name 'report.html' > list0

find ./$1 -name 'ccp4' > list2
find ./$1 -name 'CORRECT.LP' >> list2
find ./$1 -name 'XDS_ASCII.HKL' >> list2
find ./$1 -name 'aniso.log' >> list2

grep -v core list2 > list4

# For automatic merging results
pwd > ./pwd.txt
echo "./pwd.txt" >> list4
echo "./correct.txt" >> list4

cat list00 list4 | xargs tar cvfz ${prefix}_${2}.tgz

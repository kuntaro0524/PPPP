#!/bin/sh

test $(date "+%m") -lt 8 && AorB=A || AorB=B
prefix=`date "+%y%m%d"`-`date "+%H%M"`
echo $prefix

# $1 : a path for data processing
# $2 : a prefix for an output .tgz

find ./$1 -name 'report.html' > list0

find ./$1 -name 'ccp4' > list2
find ./$1 -name 'CORRECT.LP' >> list2
find ./$1 -name 'XSCALE.LP' >> list2
find ./$1 -name 'XSCALE.INP' >> list2
find ./$1 -name 'aniso.log' >> list2

grep -v core list2 > list4

# For normal merging
# grep run_03 list4 > list5

# For automatic merging results
grep final list0 > list00
grep run_03 list4| grep final > list5
pwd > ./pwd.txt
echo "./pwd.txt" >> list5

cat list00 list5 | xargs tar cvfz ${prefix}_${2}.tgz

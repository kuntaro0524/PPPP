#!/bin/sh
for d in $(ls):
do
ppp=$(pwd)
 if [ -d $d ] ; then
# Processing Started
cd $d
yamtbx.python ~/PPPP/DirectoryProc.py . cry00_000.log 7.67E11
cd $ppp
# Processing Done
 fi
done


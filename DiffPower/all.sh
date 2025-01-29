#!/bin/bash
dlist=$(find . -maxdepth 1 -type d | sort -k1)

ndat=0
for dir in $dlist; do
#echo $dir
python ~/PPPP/DiffPower/XDSascii.py $dir/XDS_ASCII_fullres.HKL
done

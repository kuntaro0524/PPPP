#!/bin/bash
logname=dnum_xdsi.dat

dlist=$(find . -maxdepth 1 -type d | sort -k1)
ndat=1

echo "" > $logname

for dir in $dlist; do
#echo "DIR=" $dir
if [ $dir = "." ]; then
continue
fi

#echo $dir
logstr=$(python ~/PPPP/DiffPower/XDSascii.py $dir/XDS_ASCII_fullres.HKL)
printf "%10d %20s %30s\n" $ndat $logstr $dir >> $logname
let ++ndat
done

# yamtbx.python ~/PPPP/analyze_helical_dose.py ./dnum_xdsi.dat ../../../tln-hel-2x18um-5-CPS0389-16/data/cry00_007.log 8e11

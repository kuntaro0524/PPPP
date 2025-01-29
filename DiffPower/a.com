#!/bin/bash

dlist=$(find . -maxdepth 1 -type d | sort -k1)

for xdir in $dlist; do
pwd=$(pwd)
cd $xdir/
logstr=$(grep SPACE XDS.INP)

echo $logstr
# split log str
set -- $logstr

# Space group number is the 2nd column
spgnum=$2

# making shell for qsub
echo "#!/bin/sh" >> x.sh
echo "#$ -cwd" >> x.sh
echo "#$ -S /bin/bash" >> x.sh
echo "xds_par" >> x.sh
chmod 744 x.sh
qsub x.sh
cd $pwd
done

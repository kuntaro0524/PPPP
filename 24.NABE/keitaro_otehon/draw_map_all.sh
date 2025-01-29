#for d in $PWD/*/cluster_*/run_03/ccp4/refine0
#for d in $PWD/*3.4*/cluster_*/run_03/ccp4/refine0
for d in $PWD/*3.5*/cluster_*/run_03/ccp4/refine0
do
 echo $d
 qsub -S /bin/bash -V -wd $d -j y <<+
pymol -cpqk < $PWD/draw_map.pml
+
done

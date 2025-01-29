#!/bin/bash
for d in $PWD/

do
 echo $d
 qsub -S /bin/bash -V -wd $d -j y <<+
/isilon/users/target/target/pymol/pymol -cpqk < $PWD/draw_map.pml
+
done


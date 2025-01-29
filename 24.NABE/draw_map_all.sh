#!/bin/bash
for d in $PWD/Data*/

do
 echo $d
 qsub -S /bin/bash -V -wd $d -j y <<+

/isilon/BL32XU/BLsoft/PPPP/24.NABE/pymol/pymol -cpqk < $PWD/draw_map.pml
+
done


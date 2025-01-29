#!/bin/csh
set OUTDIR="/isilon/BL32XU/TMP/190618-xiangyu/"
set OD = $PWD

foreach DIR (merge_blend_FLAAT/ merge_blend_Neb_Nb60/ merge_blend_SX/ merge_blend_T18_Nb60/ merge_ccc_FLAAT/ merge_ccc_Neb_Nb60/ merge_ccc_SX/ merge_ccc_T18_Nb60/)
cd $DIR/
python ~/PPPP/18.Report/MakeReporKAMO.py ./ /isilon/BL32XU/TMP/190618-xiangyu/
cd $OD
end

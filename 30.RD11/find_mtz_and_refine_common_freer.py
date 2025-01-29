import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/11.ClusterAnalysis")

import glob,numpy
import DirectoryProc
import ComRefine

# 
symm="C2221"
ref_dmin=3.5

# Finding xscale.mtz
dp=DirectoryProc.DirectoryProc(os.environ["PWD"])
xscale_list,path_list=dp.findTarget("xscale.mtz")

# Model PDB
model="/isilon/users/target/target/Iwata/180522BL32XU/_kamoproc/merge_zenbunose/blend_3.3A_framecc_b+B_selected/at2r_iso.pdb"

# Free-R flags common
refmtz="/isilon/users/target/target/Iwata/180522BL32XU/_kamoproc/merge_zenbunose/blend_3.3A_framecc_b+B_selected/cluster_0540/run_03/ccp4/at2_anti_refine_001.mtz"

# find xscale.mtz and refine  with REFMAC JellyBody and phenix.refine
for proc_path in path_list:
    comrefine=ComRefine.ComRefine(proc_path)
    #comname=comrefine.refine_common_free(refmtz,"xscale.mtz",symm,3.5,model,"refine",hkl_sort="l,h,k")
    #comname=comrefine.refine_common_free(refmtz,"xscale.mtz",symm,ref_dmin,model,"refine")
    comname=comrefine.refine_compare_cluster_lowreso(refmtz,"xscale.mtz",symm,ref_dmin,model,"refine")
    #print comname
    os.system("qsub %s"%comname)

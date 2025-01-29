import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/11.ClusterAnalysis/")
import glob,numpy
import DirectoryProc
import ComRefine

# MTZ file
mtzname="xscale.mtz"

# Finding xscale.mtz
dp=DirectoryProc.DirectoryProc(os.environ["PWD"])
xscale_list,path_list=dp.findTarget(mtzname)

# MTZ file list for refinement
symm="P21212"
dmin=3.0

# Symm
hkl_sort="k,l,h"

# Keyword selection
############################################
keys=["run_03","final"]

# Keyword selection
proc_xscale_list=[]
proc_path_list=[]

for xscale_mtz,path in zip(xscale_list,path_list):
        good_count=0
        for key in keys:
            if xscale_mtz.rfind(key)!=-1:
                good_count+=1
        if good_count==len(keys):
            proc_xscale_list.append(xscale_mtz)
            proc_path_list.append(path)
            cnt+=1

# Model PDB
model="/isilon/users/target/target/AutoUsers/190122/Toma/_kamoproc/model.pdb"

# Free-R flags common
refmtz="/isilon/users/target/target/AutoUsers/190122/Toma/_kamoproc/merge_cc_pattern2_ligand1/cc_3.00A_final/cluster_0065/otehon/ccp4/otehon_free.mtz"

# find xscale.mtz and refine  with REFMAC JellyBody and phenix.refine
for proc_path in proc_path_list:
    comrefine=ComRefine.ComRefine(proc_path)
    # Extract Free-R flag columns
    free_column=comrefine.extractFreeR(refmtz)
    comname=comrefine.mr_refine_common_free(refmtz,mtzname,symm,dmin,model,"refine",hkl_sort=hkl_sort,free_column=free_column,nmon=1)
    os.system("chmod 744 %s"%(comname))
    os.system("qsub %s"%comname)

import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/Libs")
import glob,numpy
import DirectoryProc
import ComRefine
import Subprocess
import ResolutionFromXscaleHKL

# Finding xscale.hkl
dp=DirectoryProc.DirectoryProc(os.environ["PWD"])
xscale_list,path_list=dp.findTarget("xscale.hkl")

subproc=Subprocess.Subprocess()

# Symm
symm="P212121"
hkl_sort="h,k,l"

# Model PDB
model="/isilon/target_backup/UserData/2019B/AutoUsers/191121/ohto/_kamoproc/merge_blend_2.3S_b/blend_2.67A_final/model.pdb"

# Free-R flags common
refmtz="/isilon/target_backup/UserData/2019B/AutoUsers/191121/ohto/_kamoproc/merge_blend_2.3S_b/blend_2.67A_final/ref_for_freer.mtz"

# find xscale.mtz and refine  with REFMAC JellyBody and phenix.refine
for xscale_hkl, proc_path in zip(xscale_list,path_list):

    # ccp4 directory
    ccp4_dir = os.path.join(proc_path,"ccp4")
    comrefine=ComRefine.ComRefine(ccp4_dir)

    # Extract Free-R flag columns
    free_column=comrefine.extractFreeR(refmtz)

    # Resolution estimation
    resol_calculator = ResolutionFromXscaleHKL.ResolutionFromXscaleHKL(xscale_hkl)
    dmin = resol_calculator.get_resolution()

    print "dmin estimation has been finished."

    comname=comrefine.mr_refine_common_free(refmtz,"xscale.mtz",symm,dmin,model,"refine",free_column=free_column,nmon=1)
    os.system("chmod 744 %s"%(comname))
    os.system("qsub %s"%comname)

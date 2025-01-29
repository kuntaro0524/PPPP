import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/Libs")

import ResolutionFromXscaleHKL

import glob,numpy
import DirectoryProc
import ComRefine
import Subprocess
import AnaXSCALE
import LibSPG

# Setting
ref_mtz = "/isilon/BL32XU/BLsoft/PPPP/31.DIMPLE/toma_free.mtz"
model_pdb = "/isilon/BL32XU/BLsoft/PPPP/31.DIMPLE/C11MRmodel.pdb"
dimple_dir = "00.DIMPLE/"
proj_name = "toma"
symm = "C2"

# Finding xscale.mtz
dp=DirectoryProc.DirectoryProc(os.environ["PWD"])
xscale_list,path_list=dp.findTarget("xscale.hkl")

subproc=Subprocess.Subprocess()

# Bad reflection file
bad_files = []

# find xscale.mtz and refine  with REFMAC JellyBody and phenix.refine
for xscale_path, proc_path in zip(xscale_list,path_list):
    print "Processing %s " % proc_path

    resol_calculator = ResolutionFromXscaleHKL.ResolutionFromXscaleHKL(xscale_path)
    dmin = resol_calculator.get_resolution()

    print "resolution limit = ", dmin

    xscalelp_path = os.path.join(proc_path, "XSCALE.LP")
    ac=AnaXSCALE.AnaXSCALE(xscalelp_path)
    cells = ac.getCellParm()
    spg_num = ac.getFinalSPG()
    libspg = LibSPG.LibSPG()
    spg_xscale = libspg.search_spgnum(spg_num)

    # CCP4 directory
    ccp4_dir = os.path.join(proc_path, "ccp4")

    if os.path.exists(ccp4_dir) != True:
        logstr = "CCP4 directory does not exit: %s" % proc_path
        bad_files.append(logstr)
    else:
        mtz_file = os.path.join(ccp4_dir, "xscale.mtz")

    if spg_xscale.lower() == symm.lower():
        print "this is under consideration"
    else:
        print "this is not so good"
        bad_files.append(xscale_path)
        continue

    comf = ComRefine.ComRefine(ccp4_dir)
    comname = comf.dimple_common_free(ref_mtz, "xscale.mtz",spg_xscale,dmin,model_pdb,"toma")
    os.system("qsub %s" % comname)

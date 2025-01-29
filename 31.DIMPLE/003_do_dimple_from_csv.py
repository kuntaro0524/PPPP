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
ref_mtz = "/isilon/users/target/target/AutoUsers/200408/ono/_kamo_30deg/merge_blend_1.5S_GC-024-01-mg/blend_1.85A_final/cluster_0022/run_03/ccp4/free.mtz"
proj_name = "ono"

bad_files = []

# Read file information 
lines = open(sys.argv[1],"r").readlines()

for line in lines:
    xscale_mtz_path, model_pdb, symm, sample_name = line.split(",")
    print xscale_mtz_path, model_pdb, symm
    # Checking  the file path
    if os.path.exists(xscale_mtz_path) == False:
        print "%s does not exist" % xscale_mtz_path
    if os.path.exists(model_pdb) == False:
        print "%s does not exist" % model_pdb

    ccp4_path = xscale_mtz_path[:xscale_mtz_path.rfind("/")]
    xscalehkl_path = os.path.join(ccp4_path, "../xscale.hkl")
    xscale_proc_path = os.path.join(ccp4_path, "../")
    print xscalehkl_path
    print "Processing %s " % ccp4_path

    resol_calculator = ResolutionFromXscaleHKL.ResolutionFromXscaleHKL(xscalehkl_path)
    dmin = resol_calculator.get_resolution()
    print "resolution limit = ", dmin

    comf = ComRefine.ComRefine(ccp4_path)
    comname = comf.dimple_common_free(ref_mtz, "xscale.mtz",symm,dmin,model_pdb,sample_name)
    os.system("qsub %s" % comname)

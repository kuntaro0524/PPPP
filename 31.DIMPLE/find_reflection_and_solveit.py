import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/Libs")

import ResolutionFromXscaleHKL

import glob,numpy
import DirectoryProc
import ComRefine
import Subprocess
import AnaXSCALE

# Setting
dimple_dir = "00.DIMPLE/"
proj_name = "toma"
symm = "C2"
dmax = 25
n_shelxd = 1000
n_site = 12
anom_atom = "S"
solcon = 0.40
n_dm = 50
n_residue = 118
n_automodel = 5

# Finding xscale.mtz
dp=DirectoryProc.DirectoryProc(os.environ["PWD"])
xscale_list,path_list=dp.findTarget("xscale.hkl")

subproc=Subprocess.Subprocess()

# find xscale.mtz and refine  with REFMAC JellyBody and phenix.refine
for xscale_path, proc_path in zip(xscale_list,path_list):
    print "Processing %s " % proc_path
    solve_path = os.path.join(proc_path, solve_dir)

    # making directory
    if os.path.exists(solve_path) == False:
        os.makedirs(solve_path)

    resol_calculator = ResolutionFromXscaleHKL.ResolutionFromXscaleHKL(xscale_path)
    dmin = resol_calculator.get_resolution()

    xscalelp_path = os.path.join(proc_path, "XSCALE.LP")
    ac=AnaXSCALE.AnaXSCALE(xscalelp_path)
    cells = ac.getCellParm()

    xscale_rel_path = os.path.relpath(xscale_path, solve_path)
    comf = ComRefine.ComRefine(solve_path)
    comname = comf.solve_sad(symm, proj_name, dmax, n_shelxd, n_site, anom_atom, solcon, n_dm, n_residue, xscale_rel_path, dmin, "lys.pir", n_automodel, cells)
    os.system("chmod a+x %s" % comname)
    os.system("qsub %s" % comname)

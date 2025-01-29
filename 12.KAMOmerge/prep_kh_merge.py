import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import glob,numpy
import DirectoryProc

# Finding xscale.mtz
dp=DirectoryProc.DirectoryProc(os.environ["PWD"])
xscale_lp_list,path_list=dp.findTarget("XDS_ASCII.HKL")

# find xscale.mtz and refine  with REFMAC JellyBody and phenix.refine
for pathh in path_list:
    print "xdsdir=%s \\"%pathh

print "workdir=./test/"

import h5py,glob, sys
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp
from PIL import Image
import PIL.ImageOps 
import numpy,os

from libtbx import easy_mp

sys.path.append("/isilon/BL32XU/BLsoft/PPPP/Libs")
import MergeH5

if __name__ == "__main__":

    print len(sys.argv)

    if len(sys.argv) != 6:
        print "Usage: progname INPUTDIR OUTDIR OUT_PREFIX STARTNUM ENDNUM"
        sys.exit()

    indir = sys.argv[1]
    outdir = sys.argv[2]
    outprefix = sys.argv[3]
    startnum = int(sys.argv[4])
    endnum = int(sys.argv[5])

    # the number of frames to be summed along rotation axis
    # if you'd like to sumup 0.1 deg x 10 = 1.0 deg, you should input 10 here.
    n_sum_along_rotation = 1

    mh5 = MergeH5.MergeH5()
    mh5.setNproc(8)

    rot_start = 0.0
    osc_width = 0.1

    master_files = glob.glob("%s/*master.h5" % indir)

    if os.path.exists(outdir) == False:
        os.makedirs(outdir)

    # MergeH5.sumUpList(param_list)
    # masterfile, sumnum_list, outdir, outprefix, out_imgnum, start_phi, osc_phi = param_list

    proc_list = []
    for imgnum in range(startnum, endnum+1):
        param_list = []
        master_info_list = []

        for master_file in master_files:
            master_info_list.append((master_file, imgnum, imgnum))

        start_phi = rot_start + float(imgnum) * osc_width
        param_list = master_info_list, outdir, outprefix, imgnum, rot_start, osc_width
        print "Process list:", param_list
        # mh5.sumUpSimpleList(param_list)
        proc_list.append(param_list)

    easy_mp.pool_map(fixed_func=lambda n: mh5.sumUpSimpleList(n), args=proc_list, processes=56)

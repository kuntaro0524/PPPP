import h5py,glob, sys
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp
from PIL import Image
import PIL.ImageOps 
import numpy,os
import glob

sys.path.append("/isilon/BL32XU/BLsoft/PPPP/Libs")
import MergeH5

if __name__ == "__main__":
    master_file = sys.argv[1]
    n_sumup = int(sys.argv[2])
    nimg_per_data = int(sys.argv[3])
    outprefix = sys.argv[4]

    mh5 = MergeH5.MergeH5()
    #nimg_per_data = 100
    nsum_rotation = 10

    mh5.setNproc(int(sys.argv[5]))
    mh5.sumDoseSlicingPhiSlicing(master_file, n_sumup, nsum_rotation, nimg_per_data, outprefix)

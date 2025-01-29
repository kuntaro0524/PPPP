#!/usr/bin/env yamtbx.python

"""
(c) RIKEN 2015. All rights reserved. 
Author: Keitaro Yamashita

This software is released under the new BSD License; see LICENSE.
"""

from yamtbx.dataproc import cbf
import numpy,scipy
from PIL import Image

def run(cbfin, jpegfile):
    # This function only returns signed int.
    arr, ndimfast, ndimmid = cbf.load_minicbf_as_numpy(cbfin, quiet=False)
    print len(arr)
    # 3110 x 3269
    y=arr.reshape(3110,3269)
    #Image.fromarray(y).save(jpegfile)
    Image.fromarray(numpy.uint8(y)).save(jpegfile)
# run()

if __name__ == "__main__":
    import sys
    import os

    cbfin = sys.argv[1]
    if len(sys.argv) > 2:
        jpegfile = sys.argv[2]
    else:
        jpegfile = os.path.basename(cbfin) + ".jpeg"

    run(cbfin, jpegfile)

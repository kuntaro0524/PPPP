import os
import sys
import math
# from  pylab import *
import pylab
import numpy
from File import *
# from numpy import *
from pylab import *
# from scipy.interpolate import splprep,splev

from AnalyzeData import *

if __name__ == "__main__":

    f = File("./")
    flist = f.listSuffix("gonioz.drv")

    for file in flist:
        print file

        ana = AnalyzeData(file)

        # extract information from derivative file
        ana.storeData(0, 1)
        xdat, ydat = ana.getData()
        # convert array to pylab-array
        px, py = ana.getPylabArray(xdat, ydat)
        # smoothing the pylab data
        newy = ana.smooth(py)
        # plot raw data
        ana.gFit(px, newy)

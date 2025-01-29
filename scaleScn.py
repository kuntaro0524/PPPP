import os
import sys
import math
import pylab
import scipy
import numpy
from pylab import *
from scipy.interpolate import splrep,splev,interp1d,splprep
from AnalyzePeak import *

if __name__=="__main__":
		ana=AnalyzePeak(sys.argv[1])

		xdat,ydat,junk=ana.prepData3(1,2,1)
		mini,maxi=ana.findMinMax(ydat)

		norm_factor=1.0/ydat[maxi]

		ydash=ana.scaleY(ydat,norm_factor)

		for i in range(0,len(ydat)):
			print "%8.3f %8.3f "%(xdat[i],ydash[i])

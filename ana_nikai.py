import os
import sys
import math
#from  pylab import * 
import socket
import pylab
import scipy
import numpy
#from numpy import *
from pylab import *
from scipy.interpolate import splrep,splev,interp1d,splprep
from MyException import *
import AnalyzePeak

if __name__=="__main__":
		ana=AnalyzePeak.AnalyzePeak(sys.argv[1])
		xdat,ydat,junk=ana.prepData3(0,2,1)

		dx,dy=ana.derivative(xdat,ydat)
		ddx,ddy=ana.derivative(dx,dy)

		print "# Derivative"
		for idx in range(0,len(dy)):
			print dx[idx],dy[idx]

		print "# DDerivative"
		for idx in range(0,len(ddy)):
			print ddx[idx],ddy[idx]

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
from AnalyzePeak import *

if __name__=="__main__":
	ana=AnalyzePeak(sys.argv[1])
	#px,py=ana.prepData2(4,6)
	
	#for x,y in zip(px,py):
		#print x,y

	x,y=ana.analyzeAll2("T","P","test.png",4,6,"TEST","OBS","FCEN")
	#x,y=ana.analyzeAll("T","P","test.png","TEST","OBS","FCEN")

	#print ana.newFWHM2(px,py)

	#xdat,y1dat,y2dat=self.prepData3(1,2,3)
	#px,py1,py2=self.prepPylabArray(xdat,y1dat,y2dat)


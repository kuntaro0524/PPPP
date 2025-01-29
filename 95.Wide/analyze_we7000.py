import os
import sys
import math
import  pylab
import numpy
from File import *
from pylab import *

from AnalyzeData import *

if __name__=="__main__":

		ana=AnalyzeData(sys.argv[1])

	# extract information from derivative file
		ana.storeData(0,4)
		xdat,ydat=ana.getData()

	# convert array to pylab-array
               	px,py=ana.getPylabArray(xdat,ydat)

	# average value
		ave=average(py)
	# std value
		std_value=std(py)

	# calculate PV value
		pv=py.max()-py.min()
		pv_per=pv/ave*100
		print py.min(),py.max()
		print "STD:%12.5f\n"%std_value

		print "PV = %12.5f"%pv_per

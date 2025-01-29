import os
import sys
import math
#from  pylab import *
from  AnalyzeData import *

if __name__=="__main__":

	ana=AnalyzeData(sys.argv[1])

	ana.storeData(0,5)

	xdat,ydat=ana.getData()
	#dx,dy=ana.derivative(xdat,ydat)

	xave,yave=ana.averageData(50)
	ave_dx,ave_dy=ana.derivative(xave,yave)

	ave_dxx,ave_dyy=ana.derivative(ave_dx,ave_dy)

	#ana.writeData("out.drv",dx,dy)
	ana.writeData("out.scn",xdat,ydat)
	ana.writeData("out.ave",xave,yave)
	ana.writeData("out.drv",ave_dx,ave_dy)
	ana.writeData("out.dxx",ave_dxx,ave_dyy)


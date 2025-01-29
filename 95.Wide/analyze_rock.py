import os
import sys
import math
import  pylab
import numpy
from File import *
from pylab import *

from AnalyzePeak import *

if __name__=="__main__":

	ana=AnalyzePeak(sys.argv[1])

	perc=100.0-float(sys.argv[2])

        xdat,ydat,junk=ana.prepData3(1,2,1)

        # Swap for splined curve fitting
        if xdat[0]>xdat[1]:
                xdat.reverse()
                ydat.reverse()

        px,py,junk2=ana.prepPylabArray(xdat,ydat,junk)

        minx=px.min()
        maxx=px.max()
	miny=py.min()
	maxy=py.max()

	# test 
	newpy=py/maxy*100.0
	maxo=ana.getXinY(px,py,maxy)

        ## preparation of spline curve fitting
        step_int=(maxx-minx)/100000.0

        ## Spline fitting
        tck=splrep(px,newpy)
        newx=arange(minx,maxx,step_int)
        newy=splev(newx,tck,der=0)

	maxyyy=newy.max()
        maxx_smooth=ana.getXinY(newx,newy,maxyyy)

	#pylab.plot(newx,newy)
	#pylab.show()

	# Loading a raw data
	for i in range(1,len(newx)):
		if newy[i] > perc and newy[i-1] < perc :
			position=(newx[i]+newx[i-1])/2.0
			break

	diff=maxx_smooth-position

	print "Observed Max Dtheta1: %12.3f "% maxo,
	print "Smoothed Max Dtheta1: %12.3f\n"% maxx_smooth,
	print "Offset corresponding to %5.2f percent intensity: %12.3f\n" % ((100.0-perc),position),
	print "Difference of them %8.4f [pulse]=%8.4f[arcsec]=%8.4f[urad]" % (diff,diff/100.0,diff/100.0*4.848136812)

import os
import sys
import  pylab
from AnalyzePeak import *
from File import *
from scipy.interpolate import splrep,splev

if __name__=="__main__":

		if len(sys.argv)!=2:
			print "Usage: PROGRAM SCANFILE"
			sys.exit(1)

                host = '172.24.242.41'
                port = 10101
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host,port))

		ana=AnalyzePeak(sys.argv[1])

		f=File("./")

		# Energy scan file
		x1,y1,y2=ana.prepData3(1,2,3)
		norm=ana.divide(y1,y2)
		dx,dy=ana.derivative(x1,norm)

		# PYLAB ARRAY
		prx,pry=ana.convertArray(x1,norm)
                tck=splrep(prx,pry,s=0)

		ddx,ddy=ana.derivative(dx,dy)

		pylab.plot(dx,dy,ddx,ddy)

		# convert pylab array
		pdx,pdy=ana.convertArray(dx,dy)

		pylab.plot(pdx,pdy)
		pylab.show()
		minx=pdx.min()
		maxx=pdx.max()
		
		print "Min:%8.5f Max:%8.5f\n"%(minx,maxx)

                # Spline (1-D) sine curve
                #tck=splrep(pdx,pdy,s=3)
                #tck=splrep(pdx,pdy,s=0)
                tck=splrep(pdx,pdy,s=0)

                # making narrow step profile from a splined curve
                newx=arange(minx,maxx,0.001)
                newy=splev(newx,tck,der=0)

		pylab.plot(dx,dy,newx,newy)
		pylab.show()

                #comment=AxesInfo(s).getLeastInfo()
                #fwhm,center=ana.analyzeKnife("Energy[keV]","Intensity","drv.scn","drv.png",comment)

		#test.writeData("test.dat",dx,dy)

import numpy
import matplotlib.pyplot as plt
import pylab
import re
import os

class FittingNumpy:
	def __init__(self,xd,yd,nfit):
		self.xd=xd
		self.yd=yd
		self.nfit=nfit
		self.isInit=False

	def init(self):
		self.xa=numpy.array(self.xd)
		self.ya=numpy.array(self.yd)
		self.isInit=True

	def linearFit(self):
    		x = numpy.array(x)
    		y = numpy.array(y)
    		A = numpy.vstack([x, numpy.ones(len(x))]).T
    		m, c = numpy.linalg.lstsq(A, y)[0]
    		return m , c

	def polyFit(self):
		if self.isInit==False:
			self.init()
		self.fitted_curve=numpy.poly1d(numpy.polyfit(self.xa,self.ya,self.nfit))

	def estimatePolyFit(self,xstart,ystart,ndata):
		xp=numpy.linspace(xstart,ystart,ndata)
		pylab.plot(self.xa,self.ya,'o',xp,self.fitted_curve(xp),'--')
		pylab.savefig('polyfit.png')

if __name__ == "__main__":
    import sys

    lines=open(sys.argv[1],"r").readlines()
	
    xd=[]
    yd=[]
    for line in lines:
	    print line
            cols=line.split()
            en=float(cols[0])
            dose_per_1E8=float(cols[1])
            xd.append(en)
            yd.append(dose_per_1E8)

    ft=FittingNumpy(xd,yd,30)
    d=ft.polyFit()
    ft.estimatePolyFit(8,18,100)

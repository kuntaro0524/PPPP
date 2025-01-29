import os
import sys
from pylab import *
from scipy import *
import numpy
import scipy
import math

# FWHMs of RD profiles
#  1.0um  2.8 um
#  5.0um  7.8 um
# 10.0um 12.8 um
# Fitting line of (FWHM of RD profile)=1.106*beamsize+1.898 @ 12.3984 keV

class Gauss:
	def __init__(self,fwhm,A):
		# beam_fwhm [um]
		self.fwhm=fwhm
		self.sigma=fwhm/2.35
		self.mu=0.0
		self.A=A
		self.isInit=False

	def setA(self,A):
		self.A=A

	def gaussian(self,x):
		#x = position
		gauss=self.A*numpy.exp(-(((x-self.mu)/self.sigma)**2))
		return gauss

	def plotProfile(self):
		# each width from center of Gaussian function
		each_width=self.fwhm
		
		# Plot step
		# FWHM roughly ranges from 1 to 300 um
		# 1/10 x FWHM is set to step to plot the function
		step=0.1*self.fwhm

		for x in arange(-each_width,each_width+0.1,step):
			print x,self.gaussian(x)

	def getArea(self):
		# Area = Amplitude * sigma * PI
		area=self.A*self.sigma*math.sqrt(numpy.pi)
		return area

	def allSum(self):
		edge=100.0
		step=0.001
		self.allsum=0.0
		for x in arange(-edge,edge,step):
			value=self.calcAmpl(x)
			self.allsum+=value
		self.isInit=True
		print "ALLSUM=%8.5f\n"%self.allsum
		return self.allsum

	def normVal(self,x):
		if self.isInit==False:
			self.allSum()
		return self.calcAmpl(x)/self.allsum

	def integrate(self,x1,x2,width):
		whole_width=x2-x1
		#print "WIDTH plot=",whole_width

		if whole_width < 0.0:
			print "Range setting error"
			sys.exit()

		npoints=int(float(whole_width)/width)+1

		#print "POINTS=",npoints

		sumi=0.0
		for idx in range(0,npoints):
			xstart=x1+float(idx)*width
			xend  =x1+float(idx+1)*width
			ystart=self.gaussian(xstart)
			yend  =self.gaussian(xend)

			# DEBUG
			# print "XSTART,XEND,YSTART,YEND=",xstart,xend,ystart,yend
			small_area=width*(ystart+yend)/2.0
			sumi+=small_area

		self.area=sumi
		return sumi
	
	def getSig(self):
		return self.sigma

if __name__=="__main__":
	g=Gauss(10,1.0)
	g.plotProfile()
	a1=g.getArea()
	a2=g.integrate(-100,100,0.1)

	print a1,a2,a1/a2

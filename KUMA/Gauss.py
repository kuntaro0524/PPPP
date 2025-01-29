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
	def __init__(self,sigma,mu):
		self.sigma=float(sigma)
		self.mu=float(mu)
		self.isInit=False
		self.scale=1.0

	def getSig(self):
		return self.sigma

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

	def integrate(self,x1,x2):
		width=x2-x1
		if width<0.0:
			print "fatal error"
			sys.exit()

		# number of sampling points
		#step=self.sigma/200.0
		#step=self.sigma/100.0
		step=self.sigma/50.0
		np=float(width)/step

		sumi=0.0
		for x in arange(x1,x2,step):
			#print x
			value=self.calc(x)
			sn=step*value
			#print sn
			sumi+=sn

		return sumi

	def integrate2(self,x1,x2,step):
		width=x2-x1
		if width < 0.0:
			print "Range setting error"
			sys.exit()

		npoints=int(float(width)/step)+1

		sumi=0.0
		for idx in range(0,npoints):
			xstart=x1+float(idx)*step
			xend  =x1+float(idx+1)*step
			y=step*(self.calc(xstart)+self.calc(xend))/2.0
			#print idx,xstart,xend,y
			sumi+=y

		return sumi
	
	def calc(self,x):
		#print "### MU %8.5f\n"%self.mu
		#print "### SIG %8.5f\n"%self.sigma
		kakko=(float(x)-self.mu)
		kakko2=kakko*kakko
		sig2=self.sigma*self.sigma
		daikakko=-kakko2/(2.0*sig2)
		expo=math.exp(daikakko)
		mae=(1.0/math.sqrt(2.0*math.pi))/self.sigma*self.scale
		value=mae*expo

		if value < 1e-8:
			value=0.0

		return value

	def getGauss(self):
		x=[]
		y=[]
		start=-self.sigma*3.0
		end=self.sigma*3.0
		step=0.1

		for tx in arange(start,end+step,step):
			x.append(tx)
			y.append(self.calc(tx))

		idx=0
		sum=0.0
		for dat in x:
			#print x[idx],y[idx]
			print "GAUSS: %8.5f %8.5f"%(x[idx],y[idx])
			idx+=1

		return x,y

	def setMu(self,mu):
		self.mu=mu

	def setSigmaFromFWHM(self,fwhm):
		self.sigma=fwhm/2.35
		#print self.sigma

	def setTotalArea(self,area):
		self.scale=area

if __name__=="__main__":
	g=Gauss(0.425,0.0)

	bs_list=[1.0,5.0,10.0,50]
	hs_list=[0.5,1.0,5,10]

	# Gauss function
	g.setSigmaFromFWHM(10.0)
	g.setTotalArea(10.0)
	g.getGauss()
	print "AREA %12.5f"%g.integrate2(-10,10,0.01)

	# Gauss function
	g.setSigmaFromFWHM(1.0)
	g.setTotalArea(1.0)
	g.getGauss()
	print "AREA %12.5f"%g.integrate2(-10,10,0.01)

"""
	for beamsize in bs_list:
		# RD propagation FWHM
		rd_fwhm=1.106*beamsize+1.898 # see above
		print "## Beamsize: %5.2f,RD_FWHM=%8.5f\n"%(beamsize,rd_fwhm),

		# RD propagation gaussian function
		gauss_rd=Gauss(20.0,0.0)
		gauss_rd.setSigmaFromFWHM(rd_fwhm)

		# integration range 
		# 3*sigma covers 99.7% in gaussian distribution
		# Observed area(crystal volume) is -3sigma <= x <= +3sigma
		# origin is set to 0.0
		# IMPORTANT: this should be independent from the 
		# RD propagation gaussian function because volume illuminated
		# by the beam is not determined by RDP
		# Only to see the crystal region to be exposed at the
		# REAL exposure
		sigma=beamsize/2.35
		three_sigma=sigma*3.0
		intstart=-three_sigma
		intend=three_sigma 
		#print "SIGMA:",intstart,intend

		for hstep in hs_list: # helical step [um]
			# Beam movements in helical data collection
			hstart=-200*hstep
			hend=0.0
			#print "HRANGE:",hstart,hend
			sum=0.0
			for offset in arange(hstart,hend,hstep):
				g.setMu(offset)
				value=g.integrate(intstart,intend)
				sum+=value
				#print "PLOT:",offset,value,sum
			sum+=1.0
			print "%8.5f, %8.5f" %(hstep,sum)

		print "\n\n"
"""

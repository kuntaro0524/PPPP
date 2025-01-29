import os 
import sys
import math
from  numpy import *

class RDprop:

	def __init_(self):

	def gauss(height,sigma,center,x):
		#kake=height/math.sqrt(math.pi*2.0)/sigma
		kake=1.0
		expo=math.exp(-1.0*math.pow(x-center,2.0)/2.0/sigma/sigma)
		return kake*expo

	def getRDfwhm(self,beamsize):
		# FWHMs of RD profiles
		#  1.0um  2.8 um
		#  5.0um  7.8 um
		# 10.0um 12.8 um
		# Fitting line of (FWHM of RD profile)=1.106*beamsize+1.898 @ 12.3984 keV
		rtnvalue=1.106*beamsize+1.898 # see above
		
		return rtnvalue

	def writeData(self,dplot,dtable):
		center=0.0
		
		sum=0.0
		#step_list=[0.5,1.0,2.0,5.0,10.0]
		beamsize_list=arange(1.0,11.0,1.0)
		step_list=arange(0.5,10.1,0.1)

		oplot=open(dplot,"w")
		otable=open(dtable,"w")

		all_data=[]

		for beamsize in beamsize_list:
			rd_fwhm=self.getRDfwhm(beamsize)
			sigma=rd_fwhm/2.35
			bslist=[]
			for step in step_list:
				trange=step*1000.0
				for center in arange(-trange,trange,step):
					#print center
					#for x in arange(-10,10,0.1):
					zero_gauss=gauss(1.0,sigma,center,0)
					if zero_gauss>=1.0:
						#print 0,1.0
						break
					else:
						sum+=zero_gauss
						#print 0,gauss(1.0,sigma,center,0)
			
				accumulated_rd=sum+1.0
				bslist.append(accumulated_rd)
				oplot.write("beamsize %8.2f step %5.2f accumulated effect:%8.3f\n"%(beamsize,step,sum+1.0))
				#print "\n\n"
				sum=0.0
			oplot.write("\n\n")
			# storage
			tmp=beamsize,bslist
			all_data.append(tmp)
			bslist=[]
		
		for each in all_data:
			print "##############"
			print each[0]
			print "##############"
			dlist=each[1]
			nlist=len(dlist)
			for j in range(0,nlist):
				print "%5.2f"%dlist[j],
			print "\n"
		
		oplot.close()
		otable.close()

if __name__=="__main__":
	rdd=RDprop()
	rdd.writeData("test.plt","test.tbl")

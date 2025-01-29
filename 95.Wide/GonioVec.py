import numpy
import scipy
import sys
import os
from MyException import *
from numpy import *

class GonioVec:

	def __init__(self):
		self.test=1
		self.vertVec=numpy.array((0,0,0))
		self.horiVec=numpy.array((0,0,0))
		self.origVec=numpy.array((0,0,0))

	def setVertVec(self,x,y,z):
		vec=numpy.array((x,y,z))
		self.vertVec=vec

	def setHoriVec(self,x,y,z):
		vec=numpy.array((x,y,z))
		self.horiVec=vec

	def getHoriLen(self):
		dist=self.calcDist(self.ori_hori)
		return dist

	def setOrigVec(self,x,y,z):
		vec=numpy.array((x,y,z))
		self.origVec=vec

	def calcDist(self,vec):
		return numpy.linalg.norm(vec)

	def makePlane(self,vstep,hstep):
		self.ori_vert=self.vertVec-self.origVec
		self.ori_hori=self.horiVec-self.origVec

		#print self.calcDist(self.ori_vert)
		#print self.calcDist(self.ori_hori)

		# div step
		div_vert=self.ori_vert/float(vstep-1)
		div_hori=self.ori_hori/float(hstep-1)

		if self.calcDist(div_vert) < 0.0005 or self.calcDist(div_hori) < 0.0005:
			raise MyException("Scan step should be greater than 0.5um!")

		start_points=[]
		end_points=[]
		for i in range(0,vstep):
			vert_origin=self.origVec+div_vert*float(i)
			hori_end=vert_origin+self.ori_hori

			start_points.append(vert_origin)
			end_points.append(hori_end)

		dv=self.calcDist(div_vert)
		dh=self.calcDist(div_hori)
		print "DIV: %8.4f %8.4f [mm]" % (dv,dh)

		return start_points,end_points,dv,dh

	def getXYZ(self,vec):
		print vec[0],vec[1],vec[2]

if __name__=="__main__":

	vecg=GonioVector()
	vecg.setOrigVec(0,0,0)
	vecg.setVertVec(0,100,0)
	vecg.setHoriVec(10,0,0)

	start_points,end_points=vecg.makePlane(10,10)

	print start_points
	print end_points

	for i in range(0,len(start_points)):
		print start_points[i],end_points[i]

	#try:
		#start_points,end_points=vecg.makePlane(ori,v1,v2,5)
	#except MyException,e:
		#print e.args[0]
		#sys.exit(1)

import numpy
import scipy
import sys
import os
from MyException import *
from numpy import *


class VectorGonio:

	def __init__(self):
		self.vec_list=[]

	def setVertVec(self,x,y,z):
		vec=numpy.array((x,y,z))
		self.vertVec=vec

	def setHoriVec(self,x,y,z):
		vec=numpy.array((x,y,z))
		self.horiVec=vec

	def setVertVec(self,x,y,z):
		vec=numpy.array((x,y,z))
		self.vertVec=vec

	def setOrigVec(self,x,y,z):
		vec=numpy.array((x,y,z))
		self.origVec=vec

	def set

	def setVector(self,vec):
		self.vec_list.append(vec)

	def isExist(self,index):
		length=len(self.vec_list)

		if index<0:
			return False
		if length<index+1:
			return False
		else:
			return True

	def calcDist(self,vector):
		dist=linalg.norm(vector)
		return dist

	def getVector(self,index1):
		if self.isExist(index1):
			return self.vec_list[index1]

	####
	## vec(index1) -> vec(index2) : origin=index1
	####
	def makeVector(self,index1,index2):
		if self.isExist(index1) and self.isExist(index2):
			return self.vec_list[index2]-self.vec_list[index1]

	def getCode(self,vec):
		if len(vec)!=3:
			raise MyException("Vector length should be 3D")
		else :
			return vec[0],vec[1],vec[2]

	def divVector(self,vec,ndiv):
		tmpvec=vec/float(ndiv)
		return tmpvec

	def addVector(self,x,y,z):
		vec=numpy.array((x,y,z))
		self.vec_list.append(vec)
		print self.vec_list

	def makePlaneCode(self,hori_vec,vert_vec,step1,step2):
		hori_stepv=self.divVector(vert_vec,step1)
		vert_steph=self.divVector(hori_vec,step2)

		coord=[]

		for i in range(0,step1+1):
			for j in range(0,step2+1):
				vec=hori_stepv*float(i)+vert_steph*float(j)
				coord.append(vec)
		return coord

	def makePlane(self,orig_v,vert_v,hori_v,v_step,h_step):
		#################################
		#      vertical vector (end:orig_v+vert_v)
		#     /
		#    /
		#   /
		#  /
		# ----------> horizontal vector (end:orig_v+hori_v)
		#################################
	
		vert_stepv=self.divVector(vec2,v_step)

		if self.calcDist(vert_stepv) < 0.5:
			raise MyException("Scan step should be greater than 0.5um!")

		start_points=[]
		end_points=[]

		for i in range(0,step+1):
			vert_origin=orig+vert_stepv*float(i)
			hori_end=vert_origin+vec3
			print vert_origin,hori_end

			start_points.append(vert_origin)
			end_points.append(hori_end)

		return start_points,end_points

if __name__=="__main__":

	vecg=VectorGonio()

	vecg.addVector(0,0,0)
	vecg.addVector(0,30,0)
	vecg.addVector(20,0,0)

	ori=vecg.getVector(0)
	v1=vecg.makeVector(0,1)
	v2=vecg.makeVector(0,2)
	print vecg.calcDist(v1)
	print vecg.calcDist(v2)

	try:
		start_points,end_points=vecg.makePlane(ori,v1,v2,5)
	except MyException,e:
		print e.args[0]
		sys.exit(1)

	print end_points


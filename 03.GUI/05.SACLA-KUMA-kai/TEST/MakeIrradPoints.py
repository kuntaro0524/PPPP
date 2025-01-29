import numpy as np
import os,sys,time,datetime
import CoaxPlaneTraj 

class MakeIrradPoints():
	def __init__(self,startvec,endvec):
		# Numpy array vectors unit[mm]
		self.svec=startvec
		self.evec=endvec
		self.vect=self.evec-self.svec

	def getDist(self):
		dist=np.linalg.norm(self.vect)
		return dist

	def getUnitVector(self):
		dist=self.getDist()
		uvec=self.vect/dist
		return uvec

	def countNtrans(self,vecdist,step):
		shou,amari=divmod(vecdist,step)
		#print shou,amari
		# Concept B
		ntrans=int(shou)+1
		return ntrans

	def calcIrradPoints(self,step_mm,phi):
		traj=CoaxPlaneTraj.CoaxPlaneTraj()
		# Length of a step vector on the current vector
		step_mod_mm=traj.calcStepLengthOnVector(self.vect,phi,step_mm)
		# Number of irradiation points
		vec_len=self.getDist()
		npoints=self.countNtrans(vec_len,step_mod_mm) # irradiation points
		n_trans=npoints-1 # times of translation to make end vector
		# 1 um vector of this vector
		uvec=self.getUnitVector()
		start_vector=self.svec

		irrad_points=[]
		for i in range(0,npoints):
			vvv=self.svec+i*step_mod_mm*uvec
			irrad_points.append(vvv)
			#print "%5d %8.5f %8.5f %8.5f"%(i,vvv[0],vvv[1],vvv[2])
		return irrad_points

	def calcIrradStartEndVector(self,step_mm,phi):
		traj=CoaxPlaneTraj.CoaxPlaneTraj()
		# Length of a step vector on the current vector
		step_mod_mm=traj.calcStepLengthOnVector(self.vect,phi,step_mm)
		# Number of irradiation points
		vec_len=self.getDist()
		npoints=self.countNtrans(vec_len,step_mod_mm) # irradiation points
		n_trans=npoints-1 # times of translation to make end vector
		# 1 um vector of this vector
		uvec=self.getUnitVector()
		start_vector=self.svec
		end_vector=self.svec+n_trans*step_mod_mm*uvec
		print "START/END=",self.svec,self.evec
		return start_vector,end_vector

if __name__ == "__main__":
	avec=np.array([0.2490,0.9194,0.1427])
	bvec=np.array([0.3190,1.2203,0.4627])

	vect=bvec-avec
	
	phi=45.0
	step_mm=0.03

	traj=CoaxPlaneTraj.CoaxPlaneTraj()
	mip=MakeIrradPoints(avec,bvec)

	step_mod=traj.calcStepLengthOnVector(vect,phi,step_mm)
	length=mip.getDist()
	print "Length of 3D vector",length
	print "mod step ",step_mod

	nstep=mip.countNtrans(length,step_mod)
	print "N times step",nstep

	uvec=mip.getUnitVector() # length 1 um
	mip.calcIrradPoint(nstep,step_mod)
	svec,evec=mip.calcIrradStartEndVector(step_mm,phi)
	print svec
	print evec

	#Ang=traj.calcAngleVecAndCoaxPlane(ovec,phi)
	#lonvec=traj.calcStepLengthOnVector(ovec,phi,30.0)

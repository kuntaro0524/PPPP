import sys,os,math
import numpy as nm

class CoaxPlaneTraj():
	def __init__(self):
		self.isGotHousen=False
		self.phi=0.0

	def calcHousen(self):
		hx=nm.cos(nm.radians(self.phi))
		hy=0.0
		hz=nm.sin(nm.radians(self.phi))
		self.norm_vec=nm.array([hx,hy,hz])
		self.isGotHousen=True

	def calcAngleVecAndHousen(self,vector):
		if self.isGotHousen==False:
			self.calcHousen()
		# ovec and hou_vec angle
		len_houvec=nm.linalg.norm(self.norm_vec)
		len_vector=nm.linalg.norm(vector)
		psi=nm.arccos(nm.dot(vector,self.norm_vec)/(len_houvec*len_vector))
		psi_deg=nm.degrees(psi)

		return psi_deg

	def calcAngleVecAndCoaxPlane(self,vector,phi):
		self.phi=phi
		self.calcHousen()
		psi_deg=self.calcAngleVecAndHousen(vector)
		kusai_deg=90-psi_deg

		return kusai_deg

	def calcTrajectedLength(self,vector,phi):
		self.phi=phi
		self.calcHousen()
		kusai_deg=self.calcAngleVecAndCoaxPlane(vector,phi)
		kusai=nm.radians(kusai_deg)

		len_vector=nm.linalg.norm(vector)
		Lnew=nm.fabs(len_vector*nm.cos(kusai))
		#print "H: %5.2f %12.5f %12.5f"%(phi,len_vector,Lnew)
		return Lnew

	def calcStepLengthOnVector(self,vector,phi,step):
		kusai_deg=self.calcAngleVecAndCoaxPlane(vector,phi)
		kusai=nm.radians(kusai_deg)

		step_mod=step/nm.cos(kusai)
		#print "STEP %5.2f %5.2f"%(step,step_mod)
		return step_mod

if __name__ == '__main__':
	avec=nm.array([0.2490,0.9194,0.1427])
	bvec=nm.array([0.3190,1.2203,0.4627])

	#avec=nm.array([-0.6270, -0.9194, 0.5557])
	#bvec=nm.array([-0.3560,-1.1694,0.5457])

	ovec=avec-bvec

	traj=CoaxPlaneTraj()
	for phi in nm.arange(0,365,5):
		Lnew=traj.calcTrajectedLength(ovec,phi)
		Ang=traj.calcAngleVecAndCoaxPlane(ovec,phi)
		lonvec=traj.calcStepLengthOnVector(ovec,phi,30.0)
		print "%5.2f %12.5f %5.2f STEPLEN %8.3f"%(phi,Lnew,Ang,lonvec)

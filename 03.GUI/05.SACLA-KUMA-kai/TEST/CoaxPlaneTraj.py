import sys,os,math
import numpy as nm

class CoaxPlaneTraj():
	def __init__(self):
		self.isGotHousen=False
		self.phi_gonio=0.0
		self.rotation_dire=1.0
		self.phi=0.0
	
		self.DEBUG=False

	def calcHousen(self):
		self.phi=self.phi_gonio*self.rotation_dire

		hx=nm.cos(nm.radians(self.phi))
		hy=0.0
		hz=nm.sin(nm.radians(self.phi))
		if self.DEBUG:
			print "calcHousen: ",self.phi,hx,hy,hz
		# normal vector
		self.norm_vec=nm.array([hx,hy,hz])
		self.isGotHousen=True

	def calcAngleVecAndHousen(self,vector,phi_gonio):
		self.phi_gonio=phi_gonio
		self.calcHousen()
		# ovec and hou_vec angle
		len_houvec=nm.linalg.norm(self.norm_vec)
		len_vector=nm.linalg.norm(vector)
		psi=nm.arccos(nm.dot(vector,self.norm_vec)/(len_houvec*len_vector))
		psi_deg=nm.degrees(psi)

		return psi_deg

	def calcAngleVecAndCoaxPlane(self,vector,phi_gonio):
		psi_deg=self.calcAngleVecAndHousen(vector,phi_gonio)
		print "PSI:",psi_deg
		kusai_deg=90-psi_deg
		#if psi_deg > 90.0:
			#kusai_deg=180.0-psi_deg
		#else:
			#kusai_deg=90.0-psi_deg

		return kusai_deg

	def calcTrajectedLength(self,vector,phi_gonio):
		kusai_deg=self.calcAngleVecAndCoaxPlane(vector,phi_gonio)
		kusai=nm.radians(kusai_deg)

		len_vector=nm.linalg.norm(vector)
		Lnew=nm.fabs(len_vector*nm.cos(kusai))
		if self.DEBUG:
			print "H: %5.2f %12.5f %12.5f"%(phi_gonio,len_vector,Lnew)
		return Lnew

	def calcStepLengthOnVector(self,vector,phi_gonio,step):
		kusai_deg=self.calcAngleVecAndCoaxPlane(vector,phi_gonio)
		kusai=nm.radians(kusai_deg)

		step_mod=step/nm.cos(kusai)
		#print "STEP %5.2f %5.2f"%(step,step_mod)
		return step_mod,kusai_deg

	def calcDistFromPlane(self,vec,phi_gonio):
		self.phi_gonio=phi_gonio
		self.calcHousen()

		# Vector coordinate
		x,y,z=vec[0],vec[1],vec[2]

		# Normal vector
		a,b,c=self.norm_vec[0],self.norm_vec[1],self.norm_vec[2]

		#########################
		# Equation
		# Dist=|a*x+b*y+c*z+d|/sqrt(a**2+b**2+c**2)
		#########################
		bunshi=(a*x+b*y+c*z)
		bunbo=nm.sqrt(a*a+b*b+c*c)

		dist=-bunshi/bunbo
		return dist

	# vector: numpy 3D array
	def unitVec(self,vector):
		dist=nm.linalg.norm(vector)
		unit_vec=vector/dist
		#print unit_vec
		return unit_vec

	def getTrajectedVector(self,vector,phi_gonio):
		# Calc housen-vector at this PHI
		self.phi_gonio=phi_gonio
		self.calcHousen()
		if self.DEBUG:
			print "getTrajectedVector: housen",self.norm_vec
		
		# distance of startvec to Coax-plane
		length=self.calcDistFromPlane(vector,phi_gonio)
		if self.DEBUG:
			print "LENGTH:",length

		# unit vector of normal vector
		norm_unit=self.unitVec(self.norm_vec)
		if self.DEBUG:
			print "NORM_UNIT=",norm_unit

		# Crosspoint vector of suisen and startvec
		_vector=vector+length*norm_unit
		
		return _vector

	def getDist(self,vector):
		len=nm.linalg.norm(vector)
		return len

	def printVec(self,vector,comment="VEC:"):
		print "%s %12.5f %12.5f %12.5f"%(comment,vector[0],vector[1],vector[2])

if __name__ == '__main__':
	avec=nm.array([0.2490,0.9194,0.1427])
	bvec=nm.array([0.3190,1.2203,0.4627])

	#avec=nm.array([-0.6270, -0.9194, 0.5557])
	#bvec=nm.array([-0.3560,-1.1694,0.5457])

	ovec=avec-bvec

	phi=30.0

	traj=CoaxPlaneTraj()

	for phi in nm.arange(0,360,5):
		sd=traj.getTrajectedVector(avec,phi)
		ed=traj.getTrajectedVector(bvec,phi)
		dvec=ed-sd

		traj.printVec(ovec,"ORIG: ")
		traj.printVec(dvec,"VECT: ")

		print ""
		print ""
		#print phi,diss
	"""
	for phi in nm.arange(0,365,5):
		Lnew=traj.calcTrajectedLength(ovec,phi)
		Ang=traj.calcAngleVecAndCoaxPlane(ovec,phi)
		lonvec=traj.calcStepLengthOnVector(ovec,phi,30.0)
		print "%5.2f %12.5f %5.2f STEPLEN %8.3f"%(phi,Lnew,Ang,lonvec)
	for phi in nm.arange(0,365,5):
	"""

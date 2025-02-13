import os,sys
import numpy as np
import CoaxPlaneTraj

class All():
	# vectors a,b,c,d as numpy 3D array
	def __init__(self,a,b,c,d,phic,step,phistep):
		self.a=a
		self.b=b
		self.c=c
		self.d=d
		self.phic=phic
		self.vector_sequence="AB"
		self.mode="Horizontal"
		self.traj=CoaxPlaneTraj.CoaxPlaneTraj()
		self.phistep=phistep
		self.step=step #[mm]

	def setStep(self,step):
		self.step=step

	def setPhic(self,phic):
		self.phic=phic

	def setMode(self,mode="Vertical"):
		self.mode=mode

	# Trajected vectors on Coax-plane at phi
	def calcTrajVecs(self,phi):
		self._a=self.traj.getTrajectedVector(self.a,phi)
		self._b=self.traj.getTrajectedVector(self.b,phi)
		self._c=self.traj.getTrajectedVector(self.c,phi)
		self._d=self.traj.getTrajectedVector(self.d,phi)

	def calcShapeVecs(self):
		self.ab=self.b-self.a
		self.bc=self.c-self.b
		self.dc=self.c-self.d
		self.ad=self.d-self.a
		self.da=-self.ad
		self.cb=-self.bc

	def calcTrajectedShapeVecs(self,phi):
		# Trajected vectors onto Micro scope plane
		self.calcTrajVecs(phi)

		self._ab=self._b-self._a
		self._bc=self._c-self._b
		self._dc=self._c-self._d
		self._ad=self._d-self._a
		self._da=-self._ad
		self._cb=-self._bc

	def resetShapeVecs(self):
		if self.vector_sequence=="AB":
			self.s1=self.a,self.b
			self.s2=self.d,self.c
			self.f1=self.a,self.d
			self.f2=self.b,self.c
			self._s1=self._a,self._b
			self._s2=self._d,self._c
			self._f1=self._a,self._d
			self._f2=self._b,self._c

		elif self.vector_sequence=="DC":
			self.s1=self.d,self.c
			self.s2=self.a,self.b
			self.f1=self.d,self.a
			self.f2=self.c,self.b
			self._s1=self._d,self._c
			self._s2=self._a,self._b
			self._f1=self._d,self._a

		return True

	# only for horizontal data collection
	# phi : unit [degrees]
	def setSlowFastVectorsHori(self,phi):
		# Real shape vectors
		self.calcShapeVecs()
		self.calcTrajectedShapeVecs(phi)

		# Slow1 & Slow2 vectors
		# |s1| >= |s2|
		# check distance of _ab and _dc
		l_ab=self.calcDist(self._ab)
		l_dc=self.calcDist(self._dc)
		#print "len(AB), len(DC)=",l_ab,l_dc

		if l_ab >= l_dc:
			self.vector_sequence="AB"
		else:
			self.vector_sequence="DC"

		self.resetShapeVecs()
		return True

	# Return [degs]
	def calcAngle(self,vec1,vec2):
		naiseki=np.dot(vec1,vec2)
		dist1=self.calcDist(vec1)
		dist2=self.calcDist(vec2)
		cosang=naiseki/(dist1*dist2)
		angle=np.arccos(cosang)

		# unit is 'dgrees'
		return np.degrees(angle)

	def getDist(self,vec):
		dist=np.linalg.norm(vec)
		return dist

	def getUnitVector(self,vec):
		dist=self.getDist(vec)
		uvec=vec/dist
		return uvec

	def countNtrans(self,vecdist,step):
		shou,amari=divmod(vecdist,step)
		#print shou,amari
		# Concept B
		ntrans=int(shou)+1
		return ntrans

	def distIrradPoints(self,vecs,phi):
		svec,evec=vecs
		#print svec,evec
		vec=evec-svec
		mod_step,kusai=self.traj.calcStepLengthOnVector(vec,phi,self.step)
		total_len=self.getDist(vec)
		shou,amari=divmod(total_len,mod_step)
		print "MOD_STEP",mod_step
		# Number of translation
		ntrans=int(shou)

		# 1 um vector of this vector
		uvec=self.getUnitVector(vec)
		real_end_vec=svec+ntrans*mod_step*uvec

		#print "REAL S/E=",svec,real_end_vec
		#print "ORIG S/E=",svec,evec

		irrad_points=[]
		for i in range(0,ntrans+1):
			phi_current=phi+i*self.phistep
			vvv=svec+i*mod_step*uvec
			irrad_points.append(vvv)
			print "PLOT %8.5f %8.5f %8.5f %5.1f"%(vvv[0],vvv[1],vvv[2],phi_current)
			#return irrad_points
		print "PLOT"
		print "PLOT"
		phi_next=phi_current+self.phistep
		return ntrans,phi_next,mod_step

	def calcStepOnSlowVector(self,phi):
		# Vector
		#-----------------------
		# \ _| <- angle(alpha)
		#  \
		#   \
		#    \
		sa,sb=self._s1
		fa,fb=self._f1
		#vec1=sa-sb
		#vec2=fa-fb
		vec1=sb-sa
		vec2=fb-fa
		_alpha=self.calcAngle(vec1,vec2)
		print "Angle of fast/slow vectors on Coax-plane:",_alpha

		# Step length viewed in Coax-plane
		if _alpha <= 90.0:
			_alpha_rad=np.radians(90-_alpha)
			slow_step_traj=self.step/np.cos(_alpha_rad)
		elif _alpha > 90.0:
			_alpha_rad=np.radians(_alpha-90)
			slow_step_traj=self.step/np.cos(_alpha_rad)

		print "Step length in Coax-plane:",slow_step_traj," [mm]"
		ss,se=self.s1
		real_slow_vec=se-ss
		real_len,kusai_deg=self.traj.calcStepLengthOnVector(real_slow_vec,phi,slow_step_traj)
		print "KUSAI:",kusai_deg
		return real_len,kusai_deg

	# prev_svec: start vector of the previous irrad line
	# step_slow: step length on the real 'slow vector'
	def calcNextStartPoint(self,prev_svec,step_slow):
		# Current start vector
		t1,t2=self.s1
		slow_uvec=self.getUnitVector(t2-t1)
		curr_svec=prev_svec+step_slow*slow_uvec
		return curr_svec

	def calcCrossPoint(self,v1s,v1e,v2s,v2e):
		# direction of moving vector 
		nv=self.getUnitVector(v1e-v1s)
		# Direction of target vector
		mv=self.getUnitVector(v2e-v2s)
		# Point to Point vector (cross link of two vectors)
		vvv=v2s-v1s

		# WORK
		work1=np.dot(nv,mv)
		work2=1-work1*work1

		if work2==0.0:
			return np.array([-999,0,0])

		d1=(np.dot(nv,vvv)-work1*np.dot(mv,vvv))/work2
		d2=(work1*np.dot(nv,vvv)-np.dot(mv,vvv))/work2
		print d1,d2
		
		# cross point
		xyz1=v1s+d1*nv
		xyz2=v2s+d2*mv

		#print "%12.5f %12.5f %12.5f"%(xyz1[0],xyz1[1],xyz1[2])
		#print "%12.5f %12.5f %12.5f"%(xyz2[0],xyz2[1],xyz2[2])
		
		return xyz1
		#print xyz1,xyz2
	
	# Now Only for Horizontal type
	def horizontalType(self,phistart):
		self.setSlowFastVectorsHori(phistart)
		total_frame=0
		# For this vector 
		npoints,phi_next,adv_step=self.distIrradPoints(self.f1,phistart)
		total_frame+=npoints
		#print total_frame
		#print phi_next
		# Saving previous vector
		prev_svec,prev_evec=self.f1

		self.veclist=[]
		vecset=prev_svec,prev_evec,adv_step,npoints,phistart
		self.veclist.append(vecset)

		while(1):
			print "NEXT CALCULATION %5.1f deg"%phi_next
			# Trajected vectors onto Coax-Plane
			self.calcTrajectedShapeVecs(phi_next)
			self.resetShapeVecs()
			# Moving to the next starting point
			step_slow,kusai=self.calcStepOnSlowVector(phi_next)
			#print "STEP_SLOW",step_slow
			startvec=self.calcNextStartPoint(prev_svec,step_slow)

			# Check if this is over the total length of self.s1
			t1,t2=self.s1
			total_len=self.calcDist(t2-t1)
			this_len=self.calcDist(startvec-t1)
			#print "Total_len/this_len:",total_len,this_len
			if this_len > total_len:
				break
			
			# direction vector of 'fast axis'
			dire_vec=self.getUnitVector(prev_evec-prev_svec)
			# tempolary end point vector for calculating the crosspoint
			# Here, 2 possible cross points are calculated
			# vector1: direction vector (paralell to 'fast axis' and
			# start/end point is 'startvec'/'end_point')
			end_point=startvec+dire_vec
			# vector2-1: 'slow2 vector'
			slow2_s,slow2_e=self.s2
			crosspoint1=self.calcCrossPoint(startvec,end_point,slow2_s,slow2_e)
			# vector2-2: 'fast2 vector'
			fast2_s,fast2_e=self.f2
			crosspoint2=self.calcCrossPoint(startvec,end_point,fast2_s,fast2_e)
	
			# The nearst vector should be selected (length of the vector compared)
			if crosspoint1[0]==-999 and crosspoint2[0]!=-999:
				endvec=crosspoint2
			elif crosspoint1[0]!=-999 and crosspoint2[0]==-999:
				endvec=crosspoint1
			elif crosspoint1[0]!=-999 and crosspoint2[0]!=-999:
				cand1=crosspoint1-startvec
				cand2=crosspoint2-startvec
				len1=self.calcDist(cand1)
				len2=self.calcDist(cand2)
				if len1 <= len2:
					endvec=crosspoint1
				else:
					endvec=crosspoint2
			else: 
				print "hoizontalType: something wrong in vector settings"
				return False
			# Vector length
			#self.printVec("START:",startvec)
			#self.printVec("END:",endvec)
			vector_set=startvec,endvec
			#npoints,phi_next=self.distIrradPoints(vector_set,phi_next)
			curr_phi=phi_next
			npoints,phi_next,adv_step=self.distIrradPoints(vector_set,phi_next)
			if phi_next > 85.0:
				break
			prev_svec=startvec
			prev_evec=endvec
			vecset=prev_svec,prev_evec,adv_step,npoints,curr_phi
			self.veclist.append(vecset)
			#print npoints,phi_next

		#for vecs in self.veclist:
			#svec,evec=vecs
			#print "VEC %12.5f %12.5f %12.5f"%(svec[0],svec[1],svec[2])
			#print "VEC %12.5f %12.5f %12.5f"%(evec[0],evec[1],evec[2])
			#print ""
			#print ""
		return self.veclist

	def calcDist(self,vector):
		dist=np.linalg.norm(vector)
		return dist

	def printVec(self,comment,vec):
		print "%s %12.5f %12.5f %12.5f"%(comment,vec[0],vec[1],vec[2])

if __name__ == '__main__':
	# Normal square
	a=np.array([0.0,  0.1,  0.3])
	b=np.array([0.0,  0.1,  0.0])
	c=np.array([0.0,  0.0,  0.0])
	d=np.array([0.0,  0.0,  0.3])

	# Normal square (Large)
	a=np.array([0.0,  0.5,  0.5])
	b=np.array([0.0,  0.5,  0.0])
	c=np.array([0.0,  0.0,  0.0])
	d=np.array([0.0,  0.0,  0.5])

	# Normal square 
	a=np.array([0.0,  0.5,  0.2])
	b=np.array([0.0,  0.5,  0.00])
	c=np.array([0.1,  0.0,  0.00])
	d=np.array([0.1,  0.0,  0.2])

	print "O: %12.5f %12.5f %12.5f"%(a[0],a[1],a[2])
	print "O: %12.5f %12.5f %12.5f"%(b[0],b[1],b[2])
	print "O: %12.5f %12.5f %12.5f"%(c[0],c[1],c[2])
	print "O: %12.5f %12.5f %12.5f"%(d[0],d[1],d[2])
	print ""
	print ""

	phi=0.0
	all=All(a,b,c,d,phi,0.05,1.0)
	all.horizontalType(0.0)

import sys,os,math
import numpy as nm
import CoaxPlaneTraj

if __name__ == '__main__':

	a=nm.array([-0.3232,  0.8799,  0.3143])
	b=nm.array([-0.6091,  0.8030,  0.8093])
	c=nm.array([-0.4532,  0.2520,  0.8173])
	d=nm.array([-0.1822,  0.3320,  0.3473])

	ab=b-a
	bc=c-b
	cd=d-c
	da=a-d

	traj=CoaxPlaneTraj.CoaxPlaneTraj()

	for phi in nm.arange(0,360,5):
		ab_d=traj.getTrajectedVector(ab,phi)
		bc_d=traj.getTrajectedVector(bc,phi)
		cd_d=traj.getTrajectedVector(cd,phi)
		da_d=traj.getTrajectedVector(da,phi)

		traj.printVec(ab_d,"AB: ")
		traj.printVec(bc_d,"BC: ")
		traj.printVec(cd_d,"CD: ")
		traj.printVec(da_d,"DA: ")
		traj.printVec(ab,"AB: ")
		traj.printVec(bc,"BC: ")
		traj.printVec(cd,"CD: ")
		traj.printVec(da,"DA: ")

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

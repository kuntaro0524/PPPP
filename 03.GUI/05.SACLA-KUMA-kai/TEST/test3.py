import sys,os,math
import numpy as nm
import CoaxPlaneTraj

if __name__ == '__main__':

	a=nm.array([-0.3232,  0.8799,  0.3143])
	b=nm.array([-0.6091,  0.8030,  0.8093])
	c=nm.array([-0.4532,  0.2520,  0.8173])
	d=nm.array([-0.1822,  0.3320,  0.3473])

	traj=CoaxPlaneTraj.CoaxPlaneTraj()

	for phi in nm.arange(0,360,5):
		_a=traj.getTrajectedVector(a,phi)
		_b=traj.getTrajectedVector(b,phi)
		_c=traj.getTrajectedVector(c,phi)
		_d=traj.getTrajectedVector(d,phi)

		print "#### %8.2f ####"%phi
		traj.printVec(_a,"AB: ")
		traj.printVec(_b,"BC: ")
		traj.printVec(_c,"CD: ")
		traj.printVec(_d,"DA: ")
		traj.printVec(a,"AB: ")
		traj.printVec(b,"BC: ")
		traj.printVec(c,"CD: ")
		traj.printVec(d,"DA: ")

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

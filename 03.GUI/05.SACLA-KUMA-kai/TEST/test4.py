import sys,os,math
import numpy as nm
import CoaxPlaneTraj

if __name__ == '__main__':

	a=nm.array([-1.0,3.0,3.0])
	b=nm.array([-1.0,3.0,1.0])

	traj=CoaxPlaneTraj.CoaxPlaneTraj()

	for phi in nm.arange(0,360,5):
		_a=traj.getTrajectedVector(a,phi)
		_b=traj.getTrajectedVector(b,phi)

		print "#### %8.2f ####"%phi
		traj.printVec(_a,"Ad: ")
		traj.printVec(_b,"Bd: ")
		traj.printVec(a,"A: ")
		traj.printVec(b,"B: ")

		print ""
		print ""

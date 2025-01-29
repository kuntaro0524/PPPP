import sys,os,math
import numpy as nm
import CoaxPlaneTraj

if __name__ == '__main__':

	a=nm.array([-1.0,1.0,3.0])
	b=nm.array([-1.0,1.0,1.0])
	c=nm.array([-1.0,3.0,1.0])
	d=nm.array([-1.0,3.0,3.0])

	a=nm.array([-0.3232,  0.8799,  0.3143])
	b=nm.array([-0.6091,  0.8030,  0.8093])
	c=nm.array([-0.4532,  0.2520,  0.8173])
	d=nm.array([-0.1822,  0.3320,  0.3473])

	traj=CoaxPlaneTraj.CoaxPlaneTraj()

	for phi in nm.arange(0,360,5):
		print "#######################"
		print "PHI %8.2f"%(phi)
		print "#######################"
		_a=traj.getTrajectedVector(a,phi)
		_b=traj.getTrajectedVector(b,phi)
		_c=traj.getTrajectedVector(c,phi)
		_d=traj.getTrajectedVector(d,phi)

		print "A' %12.5f %12.5f %12.5f"%(_a[0],_a[1],_a[2])
		print "B' %12.5f %12.5f %12.5f"%(_b[0],_b[1],_b[2])
		print "C' %12.5f %12.5f %12.5f"%(_c[0],_c[1],_c[2])
		print "D' %12.5f %12.5f %12.5f"%(_d[0],_d[1],_d[2])

		# Vector length
		_ab=_b-_a
		_bc=_c-_b

		dist1=traj.getDist(_ab)
		dist2=traj.getDist(_bc)
		print "ABd %12.5f %12.5f %12.5f"%(_ab[0],_ab[1],_ab[2])
		print "BCd %12.5f %12.5f %12.5f"%(_bc[0],_bc[1],_bc[2])

		menseki=dist1*dist2
		print "#######################"
		print "DIST %5.2f %12.5f %12.5f %12.5f"%(phi,dist1,dist2,menseki)
		print "#######################"

		#print ""
		#print ""

import math, numpy
L=4000

step=50.0

V=1000.0

nv=int(V/step)
nh_ideal=4000.0/step
ideal_hit=nv*nh_ideal

for phi in numpy.arange(10,60,1.0):
	phi_rad=numpy.radians(phi)
	Lnew=L*numpy.cos(phi_rad)
	nh=int(Lnew/step)
	current_hit=nh*nv
	hit_rate=float(current_hit)/float(ideal_hit)
	
	print "PHI %5.2f,%10.1f,%10.2f,%8d,%8d,%8.2f"%(phi,Lnew,Lnew/L,ideal_hit,current_hit,hit_rate)

import sys,os,math
import numpy as nm

x=0.2490
y=-0.9194
z=0.1427

x2=0.3190
y2=-1.2203
z2=0.4627

for phi in nm.arange(0,365,5.0):
	vecA=nm.array([x,y,z])
	vecB=nm.array([x2,y2,z2])

	ovec=vecA-vecB

	# housen-vector of a view-point of coax-camera
	hx=nm.cos(nm.radians(phi))
	hy=0.0
	hz=nm.sin(nm.radians(phi))
	
	hou_vec=nm.array([hx,hy,hz])
	
	#print hou_vec
	# ovec and hou_vec angle
	len_houvec=nm.linalg.norm(hou_vec)
	len_ovec=nm.linalg.norm(ovec)
	psi=nm.arccos(nm.dot(ovec,hou_vec)/(len_houvec*len_ovec))
	psi_deg=nm.degrees(psi)

	if psi_deg <= 90.0:
		kusai_deg=90-psi_deg
	elif psi_deg > 90.0 and psi_deg <= 360.0:
		kusai_deg=psi_deg-270.0

	kusai=nm.radians(kusai_deg)

	#print nm.degrees(psi)
	Lnew=len_ovec*nm.cos(kusai)
	#print "PLOT: ",phi,Lnew
	print "H: %5.2f %12.5f %12.5f %12.5f"%(phi,hx,hy,hz)
	#print "%5.2f %12.5f %5.2f %5.2f"%(phi,Lnew,psi_deg,kusai_deg)

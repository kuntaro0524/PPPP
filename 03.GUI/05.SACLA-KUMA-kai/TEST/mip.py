import numpy as np
import os,sys,time,datetime,socket
import CoaxPlaneTraj 
import MakeIrradPoints
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/03.GUI/04.SACLA-KUMA/Libs")
from Gonio import *

if __name__ == "__main__":
	ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ms.connect(("192.168.163.1", 10101))

	gonio=Gonio(ms)

	#avec=np.array([     0.3861,   -1.1153,    0.3495])
	#bvec=np.array([     0.4391,   -0.8383,    0.1595])
	avec=np.array([     0.3516,   -1.3757,    0.5453])
	bvec=np.array([     0.4304,   -0.8337,    0.1535])

	#avec=np.array([0.2490,0.9194,0.1427])
	#bvec=np.array([0.3190,1.2203,0.4627])

	vect=bvec-avec
	
	phi=0.0
	step_mm=0.1

	traj=CoaxPlaneTraj.CoaxPlaneTraj()
	kusai_deg=traj.calcAngleVecAndCoaxPlane(vect,phi)
	print "kusai_deg=",kusai_deg

	mip=MakeIrradPoints.MakeIrradPoints(avec,bvec)

	# Vector list
        veclist=mip.calcIrradPoints(step_mm,phi)
	print len(veclist),veclist

	gonio.rotatePhi(phi)
	for vec in veclist:
		x,y,z=vec
		gonio.moveXYZmm(x,y,z)
		time.sleep(10.0)
		print "Next point!"

	svec,evec=mip.calcIrradStartEndVector(step_mm,phi)
	#print "kusai_deg=",kusai_deg
	#jjj=iii*np.cos(np.radians(kusai_deg))
	#print "MODOSHITA=",jjj

	# Start & End vector
	#x0,y0,z0=svec
	#x1,y1,z1=evec
	#gonio.moveXYZmm(x0,y0,z0)
	#time.sleep(5.0)
	#gonio.moveXYZmm(x1,y1,z1)

	ms.close()

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
	
	step_mm=0.1
	mip=MakeIrradPoints.MakeIrradPoints(avec,bvec)

	for phi in arange(0,360,10):
		traj=CoaxPlaneTraj.CoaxPlaneTraj()
		kusai_deg=traj.calcAngleVecAndCoaxPlane(vect,phi)
		lenlen=traj.calcTrajectedLength(vect,phi)
		step_mod_mm=traj.calcStepLengthOnVector(vect,phi,step_mm)
		#print "kusai_deg=",kusai_deg
		# Vector list
        	veclist=mip.calcIrradPoints(step_mm,phi)
		print " %5.2f  %5d KUSAI= %5.2f LEN= %8.3f STEP= %8.3f"%(phi,len(veclist),kusai_deg,lenlen,step_mod_mm)

	"""
	gonio.rotatePhi(phi)
	for vec in veclist:
		x,y,z=vec
		gonio.moveXYZmm(x,y,z)
		time.sleep(10.0)
		print "Next point!"
	"""

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

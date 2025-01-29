import socket
import time
import datetime

# My library
from Morning import Morning

if __name__=="__main__":
	mng=Morning("./")

	ox=-0.0984
	oy=1.9381
	oz=0.9201
	
	# Evacuate needle
	#sx,sy,sz=mng.evacNeedle(15)
	#mng.prepBC()
	#mng.prepExposure()
	#time.sleep(60.0)
	mng.doCapAna("captest")
	#mng.finishBC()
	#mng.finishExposure()
	# Move to the save position
	#mng.moveXYZmm(ox,oy,oz)
	mng.allFin()

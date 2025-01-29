import socket
import time
import datetime

# My library
import Morning

if __name__=="__main__":
	mng=Morning.Morning("./")

	mng.prepBC()
	starttime=datetime.datetime.now()
	mng.prepScan()

       	prefix="captest"
	ofile=open("cap.dat","w")
	#mng.tuneAttThick()

	for i in range(0,10):
		y,z=mng.doCapAna(prefix,thicktune=False)
		now=datetime.datetime.now()
		difftime=float((now-starttime).seconds)
		ofile.write("%12.2f %8.5f %8.5f\n"%(difftime,y,z))
		time.sleep(10)

	mng.finishBC()
	mng.finishExposure()

	mng.allFin()

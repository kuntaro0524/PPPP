from RotationCenter import *
from File import *
from Gonio import *
from Capture import *
from Light import *
import math
from Zoom import *
import datetime

if __name__=="__main__":

	rc=RotationCenter()

	starttime=datetime.datetime.now()

### PORT
	#host = '192.168.163.1'
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
### PORT
	gonio=Gonio(s)
	f=File("./")

	sx,sy,sz=gonio.getXYZmm()

	# Initialization of flags
	isOkay1=False
	isOkay2=False
	isOkay3=False
	ntimes=0

	while(1):
		ntimes+=1
		if isOkay1==False:
			print " 0-180 deg"
			d1,c1=rc.tuneGonioAve(0,180)
		if isOkay2==False:
			print " 90-270 deg"
			d2,c2=rc.tuneGonioAve(90,270)
		if isOkay3==False:
			print " 45-225 deg"
			d3,c3=rc.tuneGonioAve(45,225)
		if fabs(d1)<0.3:
			isOkay1=True
		if fabs(d2)<0.3:
			isOkay2=True
		if fabs(d3)<0.3:
			isOkay3=True
		if isOkay1==True and isOkay2==True and isOkay3==True:
			break

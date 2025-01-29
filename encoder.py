import sys
import socket
import time
import datetime
from Received import *
from Motor import *
from Enc import *
from File import *

total_seconds = lambda td: (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1E6

if __name__=="__main__":
	enc=Enc()
	enc.openPort()
	f=File("./")
	
	filename="%03d_enc.dat"%(f.getNewIdx3())
	ofile=open(filename,"w")
	starttime=datetime.datetime.now()

	while (1):
		d=datetime.datetime.now()
		x=enc.getX()
		y=enc.getY()
		z=enc.getZ()

		ttime=total_seconds(d-starttime)

		#ofile.write("%8.2f %15s %10.4f %10.4f %10.4f\n"%(t,d,x,y,z))
		ofile.write("%8.2f %10.4f %10.4f %10.4f\n"%(ttime,x,y,z))
		ofile.flush()
		#print d,x,y,z
		if ttime>35000:
			break
		time.sleep(0.05)

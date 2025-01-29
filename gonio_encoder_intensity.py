import sys
import socket
import time
import math
from pylab import *
import datetime

# My library
from AnalyzePeak import *
from File import *
from Enc import *
from Gonio import *

if __name__=="__main__":
	#host = '192.168.163.1'
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	counter=Count(s,3,0)

	gonio=Gonio(s)
	f=File("./")

	# Counter time[sec]
	ctime=1.0

	# File name
	fname="%03d_gonio_enc.scn"%(f.getNewIdx3())
	ofile=open(fname,"w")

	while(1):
		ti=datetime.datetime.now()
		values=counter.getCount(ctime)
		i0,i1=int(values[0]),int(values[1])
		ex,ey,ez=gonio.getEnc()
		print ex,ey,ez,i0,i1
		ofile.write("%20s %12.5f %12.5f %12.5f %10d %10d\n"%(ti,ex,ey,ez,i0,i1))
		ofile.flush()

	ofile.close()
	s.close()

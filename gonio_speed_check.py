import sys
import socket
import time
import math
from pylab import *

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

	gonio=Gonio(s)
	f=File("./")

	# Counter time[sec]
	ctime=0.2

	# File name
	fname="%03d_gonio_enc.scn"%(f.getNewIdx3())
	ofile=open(fname,"w")

	sx,sy,sz=gonio.getXYZmm()

	for idx in arange(0,10,1):
		gonio.moveTrans(1000)
		px,py,pz=gonio.getXYZmm()
		ex,ey,ez=gonio.getEnc()
		ofile.write("GOGO:%12.5f %12.5f %12.5f Enc:%12.5f %12.5f %12.5f\n"%(px,py,pz,ex,ey,ez))

		gonio.moveTrans(-1000)
		px,py,pz=gonio.getXYZmm()
		ex,ey,ez=gonio.getEnc()
		ofile.write("BACK:%12.5f %12.5f %12.5f Enc:%12.5f %12.5f %12.5f\n"%(px,py,pz,ex,ey,ez))

	ofile.close()
	gonio.moveXYZmm(sx,sy,sz)

	s.close()

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
	ex,ey,ez=gonio.getEnc()
	ofile.write("Pulse:%12.5f %12.5f %12.5f Enc:%12.5f %12.5f %12.5f\n"%(sx,sy,sz,ex,ey,ez))
	ofile.flush()
	gonio.moveXYZmm(0.0,sy,sz)
	px,py,pz=gonio.getXYZmm()
	ex,ey,ez=gonio.getEnc()
	ofile.write("Pulse:%12.5f %12.5f %12.5f Enc:%12.5f %12.5f %12.5f\n"%(px,py,pz,ex,ey,ez))
	ofile.flush()

	#gonio.prepScan()
	for idx in arange(0,200,1):
		gonio.moveUpDown(4000)
		px,py,pz=gonio.getXYZmm()
		ex,ey,ez=gonio.getEnc()
		ofile.write("Pulse:%12.5f %12.5f %12.5f Enc:%12.5f %12.5f %12.5f\n"%(px,py,pz,ex,ey,ez))
		print idx
		ofile.flush()
		gonio.moveUpDown(-8000)
		px,py,pz=gonio.getXYZmm()
		ex,ey,ez=gonio.getEnc()
		ofile.write("Pulse:%12.5f %12.5f %12.5f Enc:%12.5f %12.5f %12.5f\n"%(px,py,pz,ex,ey,ez))
		print idx
		ofile.flush()
		gonio.moveUpDown(4000)
		px,py,pz=gonio.getXYZmm()
		ex,ey,ez=gonio.getEnc()
		ofile.write("Pulse:%12.5f %12.5f %12.5f Enc:%12.5f %12.5f %12.5f\n"%(px,py,pz,ex,ey,ez))
		print idx
		ofile.flush()

	ofile.close()
	gonio.moveXYZmm(sx,sy,sz)

	s.close()

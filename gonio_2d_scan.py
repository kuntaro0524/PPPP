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
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	gonio=Gonio(s)
	f=File("./")

	# Gonio set position [mm]
	sx=-0.0001
	sy=-14.6901
	sz=0.1060

	# Step size[mm]
	vstep=0.01
	hstep=0.01

	# Step num
	nv=11
	nh=11

	# Counter time[sec]
	ctime=0.2

	# range of V
	vstart=sz-(nv-1)/2*vstep
	vend=sz+(nv-1)/2*vstep+vstep*0.9

	# range of H
	hstart=sy-(nh-1)/2*hstep
	hend=sy+(nh-1)/2*hstep+hstep*0.9

	# PIN photo
	counter_pin=Count(s,3,0)

	# File name
	fname="%03d_g_2d.scn"%(f.getNewIdx3())
	ofile=open(fname,"w")

	for v in arange(vstart,vend,vstep):
		for h in arange(hstart,hend,hstep):
			gonio.moveXYZmm(sx,h,v)
        		cvalue=int(counter_pin.getCount(ctime)[0])
			ofile.write("%12.5f %12.5f %12.5f %d\n"%(sx,h,v,cvalue))

	ofile.close()
	gonio.moveXYZmm(sx,sy,sz)

	s.close()

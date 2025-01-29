import sys
import socket
import time
import math
from pylab import *

# My library
from File import *
from Gonio import *
from Motor import *

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

	sx,sy,sz=gonio.getXYZmm()

	# To pulse
	px=int(sx*1000.0*10.0)
	py=int(sy*1000.0*10.0)
	pz=int(sz*1000.0*10.0)

	print "Current pulse",px,py,pz

	# Encoder values
	ex,ey,ez=gonio.getEnc()
	
	# Convertion
	pe_x=int(ex*1000.0*10.0)
	pe_y=int(ey*1000.0*10.0)
	pe_z=int(ez*1000.0*10.0)
	print "Current encodeer:",pe_x,pe_y,pe_z
	#print pe_x,pe_y,pe_z

	diff_x=pe_x-px
	diff_y=pe_y-py
	diff_z=pe_z-pz
	print "diff_z,y,x=", diff_z, diff_y, diff_x

	# 30um difference is detected
	diff_thresh=50
	if abs(diff_z) > diff_thresh:
		# Preparation of gonioz preset
		print "Presetting Z"
		gonioz=Motor(s,"bl_32in_st2_gonio_1_z","pulse")
		gonioz.preset(pe_z)
	if abs(diff_y) > diff_thresh:
		print "Presetting Y"
		gonioy=Motor(s,"bl_32in_st2_gonio_1_y","pulse")
		gonioy.preset(pe_y)
	if abs(diff_x) > diff_thresh:
		print "Presetting X"
		goniox=Motor(s,"bl_32in_st2_gonio_1_x","pulse")
		goniox.preset(pe_x)
	s.close()

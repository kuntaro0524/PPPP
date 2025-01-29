import sys
import socket
import time
import math
from pylab import *

# My library
from Gonio import *
from ExSlit1 import *
from Shutter import *
from Light import *

def scanV(start,end,step):
	save=float(counter.getCount(0.1)[0])
	print "SAVE:%8.3f\n"%save

	for i in arange(start,end,step):
		gonio.moveUpDown(step)
		x2,y2,z2=gonio.getXYZmm()
		pincnt=float(counter.getCount(0.1)[0])
		print x2,y2,z2,pincnt,save

		if pincnt<(save/2.0):
			print "FIND!!: %8.5f\n"%pincnt
			break
		#else:
			#save=pincnt
	return x2,y2,z2

def scanH(start,end,step):
	save=float(counter.getCount(0.1)[0])
	print "SAVE:%8.3f\n"%save

	for i in arange(start,end,step):
		gonio.moveTrans(step)
		x2,y2,z2=gonio.getXYZmm()
		pincnt=float(counter.getCount(0.1)[0])
		print x2,y2,z2,pincnt,save

		if pincnt<(save/2.0):
			print "FIND!!: %8.5f\n"%pincnt
			break
		#else:
			#save=pincnt
	return x2,y2,z2

if __name__=="__main__":

        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	# Initialization
	gonio=Gonio(s)
        counter=Count(s,3,0)
        exs1=ExSlit1(s)
        shutter=Shutter(s)
        light=Light(s)

        exs1.openV()
        light.off()
        shutter.open()

	# current position
	x,y,z=gonio.getXYZmm()

	# here
	x2,y2,z2=scanV(0,200,10.0)

	gonio.moveUpDown(-100)
	x3,y3,z3=scanV(0,100,5.0)
	print gonio.getXYZmm()

	gonio.moveUpDown(-20)
	x4,y4,z4=scanV(0,50,2.0)
	print gonio.getXYZmm()

	gonio.moveUpDown(-10)
	x5,y5,z5=scanV(0,20,1.0)
	print gonio.getXYZmm()
	
	save_z=z5

#	Reset position
	gonio.moveXYZmm(x,y,z)

###	Horizontal
	x1,y1,z1=scanH(0,200,10.0)

	gonio.moveTrans(-100)
	x2,y2,z2=scanH(0,100,5.0)

	gonio.moveTrans(-50)
	x2,y2,z2=scanH(0,50,2.0)

	gonio.moveTrans(-20)
	x2,y2,z2=scanH(0,20,1.0)

	save_y=y2

	gonio.moveXYZmm(x,y,z)

	print save_z,save_y

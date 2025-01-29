#!/bin/env python 
import sys
import socket
import time
import datetime

# My library
from Mono import *
from FES import *
from ID import *
from TCS import *
from ExSlit1 import *
from AxesInfo import *
from File import *
from FixedPoint import  *
from Att import *
from SPACE import *
from MyException import *
from BM import *
from BS import *
from Stage import *
from Shutter import *
from Capture import *
from Gonio import *
from Colli import *
from Cryo import *
from CenteringNeedle import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:

	# Devices
	id=ID(s)
	mono=Mono(s)
	tcs=TCS(s)
	axes=AxesInfo(s)
	f=File("./")
	fixedp=FixedPoint(s)
	att=Att(s)
	space=SPACE()
	bm=BM(s)
	stage=Stage(s)
	shutter=Shutter(s)
	cap=Capture()
	colli=Colli(s)
	bs=BS(s)
	gonio=Gonio(s)
	cryo=Cryo(s)
	cn=CenteringNeedle(s)

	# current directory
	curr_dir=f.getAbsolutePath()

##################################
	# dtheta1 tune
##################################
	try :
		prefix="%03d"%f.getNewIdx3()
		mono.scanDt1PeakConfig(prefix,"DTSCAN_AUTOTUNE")

	except MyException,ttt:
		print "Dtheta1 tune failed."
		print ttt.args[1]
		sys.exit(1)

##################################
	# Mount centering pin
##################################
	# Evacuate devices
	colli.off()
	bs.off()
	cryo.off()

	# Gonio mount position
	gonio.moveXYZmm(0.050,-12.991,0.7717)
	gonio.rotatePhi(0.0)

	# Mount pin for centering
    	try :
		space.mountSample(1,1)

        except MyException,ttt:
		print "PIN mount failed"
		print ttt.args[1]

	# Pin rough centering
	gonio.moveXYZmm(-0.4846,-13.3307,0.3431)

	# Pin centering
	cn.centeringLow()
	cn.centeringHigh()

	# Dismount pin for centering
    	try :
		space.dismountSample(1,1)

        except MyException,ttt:
		print "PIN mount failed"
		print ttt.args[1]

	# Pin dismount
	# Monitor in
	#bm.relmove(-200)

	sys.exit(1)
	
#############################################
	# Automatic stage tune #
#############################################
	# Capture
	ceny=341
	cenz=232

	# Monitor out
	bm.set(0)

	print ceny,cenz

	for i in range(0,3):
        	print stage.getZmm(), stage.getYmm()
		# caputure
		filename="%s/test_%03d.ppm"%(curr_dir,f.getNewIdx3())
		y,z=cap.captureBM(filename)

		# diff x,y
		dy=y-ceny
		dz=z-cenz

		# pixel to micron [um/pixel] in high zoom
		p2u_z=7.1385E-2
		p2u_y=9.770E-2

		z_move=-dz*p2u_z
		y_move=dy*p2u_y

		print "Z: %8.4f [um]"%z_move
		print "Y: %8.4f [um]"%y_move

		#print z_move
		stage.moveZum(z_move)
		stage.moveYum(y_move)

	# Monitor out
	bm.set(-75000)

    	s.close()

	break

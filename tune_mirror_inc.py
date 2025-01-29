#!/bin/env python 
import sys
import socket
import time
import math
from pylab import *

# My library
from Gonio import *
from ID import *
from Mono import *
from Mirror import *
from TCS import *
from ConfigFile import *
from ExSlit1 import *

while True:
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

##	Device definition
	id=ID(s)
	mono=Mono(s)
	gonio=Gonio(s)
	tcs=TCS(s)
	conf=ConfigFile()
	slit1=ExSlit1(s)
	f=File("./")
	mirror=Mirror(s)

## 	Default position
	sx=3.5100
	sy=-13.0210
	sz=-0.4870

##	Counter channel
	cnt_ch1=3
	cnt_ch2=0

## 	Preparing gonio information (reset encoder)
	gonio.prepScan()

## 	Save current mirror position
	save_mv_ty=mirror.getVFMin()
	save_mh_tz=mirror.getHFMin()

## 	Scan flag
	dtheta_tune=False
	h_mirror=False
	v_mirror=True

##	dtheta
	if dtheta_tune:
        	prefix="%03d"%f.getNewIdx3()
        	mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)

	tcs.setApert(0.026,0.040)
	if v_mirror:
	# Preparation for vertical mirror refinement
		gonio.moveXYZmm(sx,sy,sz)
		gstep=0.1 # um
	## 	Log file
		logf=open("vert.log","w")
		for di in arange(0,1000,100):
			# changing incident angle
			print "VFM-tz %5d pls shifting...."%di
			mirror.setVFMinRelative(di)

			# rough scan Z
			newx1,newz1=gonio.wireRoughZ(3)
			print newx1,newz1

			if newx1==0.0 and newz1==0.0:
				print "Not found"
				break
	
			# set position to default
			gonio.moveXYZmm(sx,sy,sz)
	
			# Start position
			zstart=newz1*1000.0-10.0
			zend=newz1*1000.0+10.0

			print zstart,zend

        		prefix="%03d_mv_%dpls"%(f.getNewIdx3(),di)
       			zwidth,zcenter=gonio.scanZenc(prefix,zstart,zend,gstep,cnt_ch1,cnt_ch2,1.0)
	
			# set Mirror to the save position
			mirror.setVFMin(save_mv_ty)
	
			logf.write("%8d,%8.3f,%8.3f\n"%(di,zwidth,zcenter))
			logf.flush()
		logf.close()

		## Closing Slit1 V
	break


s.close()

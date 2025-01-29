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
from TCS import *
from ConfigFile import *

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
	f=File("./")

## 	Gonio set position [mm]
	#sx=-0.7009 #110410 13:00
	#sy=-14.4094 #110410 13:00
	#sz=1.1790 #110410 13:00
	sx=-0.7005
	sy=-14.4124
	sz=1.1756

## 	Gonio rough position (FWHM center) [um]
	default_y=-14412
	default_z=1173

## 	TCS aperture list
	tcs_list=[(0.026,0.04,0.2),(0.1,0.1,0.2),(0.2,0.2,0.5),(0.3,0.3,0.5),(0.4,0.4,0.5),(0.5,0.5,1.0),(1.0,1.0,1.0)]
	#tcs_list=[(1.0,1.0,1)]

## 	Needle y position list
	y_list=[0.0,100,200,300,500,1000,2000]

## 	Log file
	logf=open("needle_center.log","w")

##	Counter channel
	cnt_ch1=3
	cnt_ch2=0

## 	Preparing gonio information (reset encoder)
	gonio.prepScan()

## 	Wire scan
	step_num=50 # 

#dtheta1 tune
       	#prefix="%03d_dtheta1"%f.getNewIdx3()
        #mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)

	phi_list=[0,180]

	for phi in phi_list:
		gonio.rotatePhi(phi)
		phitxt="%fdeg"%phi

		for needle_y in y_list:
			gstep=5.0 # [um]
	
			# needle initial Y str
			nstr="%05.2f"%(needle_y)
	
			# PREFIX
       			prefix="%03d_%s_%s"%(f.getNewIdx3(),nstr,phitxt)
	
			# Gonio Y position at this condition
			ystart=(default_y-needle_y)/1000.0
	
			# set position
			gonio.moveXYZmm(sx,ystart,sz)

			# Gonio Z scan range
			zstart=default_z-float(step_num)*gstep
			zend=default_z+float(step_num)*gstep
	
       			gonio.scanZencNoAna(prefix,zstart,zend,gstep,cnt_ch1,cnt_ch2,0.2)
	
	logf.close()

	break

s.close()

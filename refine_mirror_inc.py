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
	sx=3.690
	sy=-13.0664
	sz=-0.8330

##      Gonio rough position (FWHM center) [um]
        default_y=-12932
        default_z=-532

##      scan range
        ystart=default_y-30
        yend=default_y+30
        zstart=default_z-30
        zend=default_z+30

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

## 	Relative inclination of the mirror[pls]
	#rrange=[-100,0,100]

##	dtheta
	if dtheta_tune:
        	prefix="%03d"%f.getNewIdx3()
        	mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)

	if h_mirror:
	# Preparation for horizontal mirror refinement
		step_num=50
		gstep=0.2 # um
	## 	Log file
		logf=open("hori.log","w")
		for di in arange(-100,0,100):
			tcs.setApert(0.026,0.040)
	
			# changing incident angle
			print "HFM-tz %5d pls shifting...."%di
			mirror.setHFMinRelative(di)
	
			# a change of incident angle
			# empirical um/pls coefficient = -0.04910 [um/pls]
			ddist=-0.04910*di
			
			# a center of new y
			newy=default_y+ddist
	
			# range
			ystart=newy-float(step_num)*gstep
			yend=newy+float(step_num)*gstep
	
			# set position to default
			gonio.moveXYZmm(sx,sy,sz)
	
        		prefix="%03d_mh_%dpls"%(f.getNewIdx3(),di)
       			ywidth,ycenter=gonio.scanYenc(prefix,ystart,yend,gstep,cnt_ch1,cnt_ch2,0.2)
	
			# set Mirror to the save position
			mirror.setHFMin(save_mh_tz)
	
			logf.write("%8d,%8.3f,%8.3f\n"%(di,ywidth,ycenter))
			logf.flush()
		logf.close()

	if v_mirror:
	# Preparation for vertical mirror refinement
		gonio.moveXYZmm(sx,sy,sz)
		step_num=100
		gstep=0.2 # um
	## 	Log file
		logf=open("vert.log","w")
		for di in arange(0,1800,100):
		##########
		# original
		#for di in arange(-500,550,50):
			tcs.setApert(0.026,0.040)
	
			# changing incident angle
			print "VFM-tz %5d pls shifting...."%di
			mirror.setVFMinRelative(di)
	
			# a change of incident angle
			#dangle=di/30.00 # urad
			# observed um/pls coefficient = 0.0393 [um/pls]
			#ddist=0.0393*di

			# 110614 Z(center)=0.074*di-541.4
			# a center of new Z
			newz=0.074*float(di)-541.4
	
			# range
			width=float(step_num)*gstep
			zstart=newz-width
			zend=newz+width
	
			# set position to default
			gonio.moveXYZmm(sx,sy,sz)
	
        		prefix="%03d_mv_%dpls"%(f.getNewIdx3(),di)
       			zwidth,zcenter=gonio.scanZenc(prefix,zstart,zend,gstep,cnt_ch1,cnt_ch2,1.0)
	
			# set Mirror to the save position
			mirror.setVFMin(save_mv_ty)
	
			logf.write("%8d,%8.3f,%8.3f\n"%(di,zwidth,zcenter))
			logf.flush()
		logf.close()

		## Closing Slit1 V
		slit1.closeV()

	break


s.close()

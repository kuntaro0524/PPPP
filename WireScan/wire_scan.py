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
from Count import *
from ExSlit1 import *
from Colli import *
from Shutter import *

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
	colli=Colli(s)
	f=File("./")
	exs1=ExSlit1(s)
	shutter=Shutter(s)

## 	Gonio set position [mm]
	sx=0.6700
	sy=-12.3028
	sz=0.5171
#	sx=-0.7000
#	sy=-15.0815
#	sz=0.3598

## 	Energy list
	#enlist=[18.5,17.5,16.5,15.5,14.5,13.5,12.3984,11.5,10.5,9.5,8.5]
	#enlist=[12.3984,18.0,15.5,10.5,8.5]
	enlist=[12.3984]

## 	TCS aperture list
	# Itsumono
	#tcs_list=[(0.026,0.040,0.1),(0.1220,0.216,0.5),(0.2450,0.50,1.0)]
	# 1x1um 5x5um 10x10um 1x10um
	#tcs_list=[(0.026,0.040),(0.175,0.201),(0.402,0.500),(0.402,0.040)]
	# 1x1um 2x4um 10x10um Max 1x10um
	#tcs_list=[(0.026,0.040),(0.1,0.1),(0.500,0.500),(1.0,1.0),(0.500,0.040)]
	# 1.66x1.0um 2x2um 5x5um 10x10um 13x10um 13x1um 120702
	#tcs_list=[(0.026,0.040),(0.042,0.069),(0.122,0.181),(0.256,0.500),(0.500,0.500),(0.500,0.040)]
	# 1.66x1.0um 2x2um 5x5um 10x10um 13x10um 10x1um 120717
	tcs_list=[(0.026,0.040),(0.042,0.069),(0.122,0.181),(0.256,0.500),(0.500,0.500),(0.256,0.040)]
	# 1x1um 5x5um 10x10um 1x10um
	#tcs_list=[(0.210,0.201)]

	# 1x1um 2x2 5x5um 8x8um 10x10um 1x10um
	#tcs_list=[(0.026,0.040),(0.052,0.08),(0.13,0.20),(0.208,0.32),(0.26,0.40),(0.5,0.5),(0.5,0.040)]

	# 1x10um beam
	#tcs_list=[(0.026,0.040),(0.5,0.5),(0.5,0.040)]

	# 120608
	#tcs_list=[(0.5,0.040),(0.5,0.08),(0.5,0.20),(0.5,1.0)]

## 	Log file
        logname="%03d_wire.log"%(f.getNewIdx3())
	logf=open(logname,"w")

##	Counter channel
	cnt_ch1=3
	cnt_ch2=0

## 	Preparing gonio information (reset encoder)
	gonio.prepScan()

## 	Counter
        counter_pin=Count(s,cnt_ch1,cnt_ch2)

#	Dtheta tune
	dthetaTuneFlag=True

## 	Wire scan
	for en in enlist:
		# Energy change
		mono.changeE(en)
		id.moveE(en)
		# Prefix of prefix
		prepre="e%07.3f"%en
		
		if dthetaTuneFlag:
			# 8.5keV 15min for thermal equilibrium
			if en<=10.0:
				time.sleep(900)
	
			if en > 10.0:
        			prefix="%03d_%s"%(f.getNewIdx3(),prepre)
        			mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)
			elif en <= 10.0:
        			prefix="%03d_%s"%(f.getNewIdx3(),prepre)
        			mono.scanDt1PeakConfig(prefix,"DTSCAN_LOWENERGY",tcs)
		## Collimator scan
		## evacuation of a wire
		gonio.moveXYZmm(sx,sy,sz)
        	prefix="%03d_colli"%(f.getNewIdx3())
		colli_y,colli_z=colli.scan(prefix,3) #PIN after sample position
                cntstr_colli=counter_pin.getPIN(3)

		## Wire rough scan
		xp,zp=gonio.wireRoughZ(3)
		yp=gonio.wireRoughY(3)

		# mm -> um
		xp=xp*1000.0
		yp=yp*1000.0
		zp=zp*1000.0

		print "##### Wire Rough %8.5f %8.5f %8.5f\n"%(xp,yp,zp)

		for tcs_param in tcs_list:
			# TCS aparture
			tcsv=float(tcs_param[0])
			tcsh=float(tcs_param[1])
	
			# TCS set aperture
			tcs.setApert(tcsv,tcsh)
	
			# TCS str
			tcsstr="%4.3fx%4.3f"%(tcsv,tcsh)
	
			# PREFIX
       			prefix="%03d_%s_%s"%(f.getNewIdx3(),prepre,tcsstr)

			# Check TCS aperture Horizontal
			if tcsh < 0.1:
				gstep_y=0.1
				ssec_y=1.0
				nstep_y=100 # 
			elif tcsh < 0.4:
				gstep_y=0.5
				ssec_y=1.0
				nstep_y=25 # 
			else :
				gstep_y=1.0
				ssec_y=0.2
				nstep_y=20 # 

			# Check TCS aperture Vertical
			if tcsv < 0.07:
				gstep_z=0.1
				ssec_z=1.0
				nstep_z=100 # 
			elif tcsv < 0.26:
				gstep_z=0.2
				ssec_z=1.0
				nstep_z=50 # 
			elif tcsv < 5.0:
				gstep_z=0.5
				ssec_z=1.0
				nstep_z=50 # 
	
			# range
			ystart=yp-float(nstep_y)*gstep_y
			yend=yp+float(nstep_y)*gstep_y
			zstart=zp-float(nstep_z)*gstep_z
			zend=zp+float(nstep_z)*gstep_z
	
			# set position
			gonio.moveXYZmm(sx,sy,sz)
       			ywidth,ycenter=gonio.scanYenc(prefix,ystart,yend,gstep_y,cnt_ch1,cnt_ch2,ssec_y)

			gonio.moveXYZmm(sx,sy,sz)
       			zwidth,zcenter=gonio.scanZenc(prefix,zstart,zend,gstep_z,cnt_ch1,cnt_ch2,ssec_z)

			# Flux measurements
                	# PIN counter
			gonio.moveXYZmm(sx,sy,sz)
                	cntstr=counter_pin.getPIN(3)

			logf.write("%8.4f %5.1f %5.1f %5.3f %5.3f %8.3f %8.3f %8.3f %8.3f %s (colli: %s)\n"%(en,colli_y,colli_z,tcsv,tcsh,zwidth,zcenter,ywidth,ycenter,cntstr,cntstr_colli))
			logf.flush()
	logf.close()#
	exs1.closeV()

	break

s.close()

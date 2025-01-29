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

## 	Energy list
	#enlist=[12.3984,18.5,17.5,16.5,15.5,14.5,13.5,11.5,10.5,9.5,8.5] # 121118
	enlist=[7.5] # 121118-low
	#enlist=[12.3984]

## 	TCS aperture list
	# Itsumono
	tcs_list=[(0.026,0.040),(0.043,0.040),(0.126,0.040),(0.263,0.040),(0.043,0.100),(0.126,0.100),(0.263,0.100),(0.126,0.273),(0.263,0.273),(0.263,0.389),(0.400,0.042),(0.400,0.100),(0.400,0.273),(0.500,0.500),(0.100,0.100)]

## 	Log file
        logname="%03d_flux.log"%(f.getNewIdx3())
	logf=open(logname,"w")

##	Counter channel
	cnt_ch1=3
	cnt_ch2=0

## 	Counter
        counter_pin=Count(s,cnt_ch1,cnt_ch2)

#	Dtheta tune
	dthetaTuneFlag=True

	for i in range(0,10):

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
					#time.sleep(900)
					time.sleep(30)
		
				if en > 10.0:
        				prefix="%03d_%s"%(f.getNewIdx3(),prepre)
        				mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)
				elif en <= 10.0:
        				prefix="%03d_%s"%(f.getNewIdx3(),prepre)
        				mono.scanDt1PeakConfig(prefix,"DTSCAN_LOWENERGY",tcs)
			## Collimator scan
			## evacuation of a wire
        		prefix="%03d_colli"%(f.getNewIdx3())
			colli_y,colli_z=colli.scan(prefix,3) #PIN after sample position
                	cntstr_colli=counter_pin.getPIN(3)
	
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
                		cntstr=counter_pin.getPIN(3)
	
				logf.write("%8.4f %5.1f %5.1f %5.3f %5.3f %s (colli: %s)\n"%(en,colli_y,colli_z,tcsv,tcsh,cntstr,cntstr_colli))
				logf.flush()
	break
	logf.close()#
	exs1.closeV()
s.close()

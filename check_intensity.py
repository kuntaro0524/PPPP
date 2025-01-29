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
	f=File("./")
	exs1=ExSlit1(s)
	shutter=Shutter(s)

## 	Energy list
	enlist=[12.3984,8.5,18.0]

## 	TCS position list
	# 110706
	ty1_tcsv_tcsh_list=[(3328,1.7234,0.1468),(3296,1.7204,0.1336)]
        tcs_list=[(0.1,0.1,0.2),(0.3,0.3,1.0),(0.5,0.5,1.0),(1.0,1.0,1.0)]

## 	Log file
	logf=open("check_intensity.log","w")

##	Counter channel
	cnt_ch1=3
	cnt_ch2=0

	for en in enlist:
		# Energy change
		mono.changeE(en)
		id.moveE(en)
		ty1_idx=0
                counter_pin=Count(s,cnt_ch1,cnt_ch2)

		for param1 in ty1_tcsv_tcsh_list:
			# Ty1
			ty1=param1[0]
			tcs_v=param1[1]
			tcs_h=param1[2]
                	# Setting Ty1
                	mono.moveTy1(ty1)
			# set TCS position
			tcs.setPosition(tcs_v,tcs_h)
			
			# Prefix of prefix
			prepre="e%05.2f_%05d"%(en,ty1)
			##	dtheta
        		prefix="%03d_%s"%(f.getNewIdx3(),prepre)
        		mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)

			# Slit shutter open
			exs1.openV()
			shutter.open()

			for tcs_param in tcs_list:
				tcs_height=float(tcs_param[0])
				tcs_width=float(tcs_param[1])
	                        tcs.setApert(tcs_height,tcs_width)

                		cntstr=counter_pin.getPIN(3)

				logf.write("%8.2f %8d %5.3f %5.3f %8.3f %8.3f %s\n"%(en,ty1,tcs_v,tcs_h,tcs_height,tcs_width,cntstr))
				logf.flush()

			# Slit shutter open
			exs1.closeV()
			shutter.close()
	break

s.close()

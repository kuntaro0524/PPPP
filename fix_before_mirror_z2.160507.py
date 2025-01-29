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

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

# insert by YK at 140929 for restart script
#time.sleep(600)

while True:

# Conditions
    #en_list=[10.0,12.3984,18.0] # /isilon/users/target/target/Staff/2015B/150916/04.MakeTableTy1Z2/
    en_list=[8.5,9.5,10.1,12.3984,15.0,18.0]
    ty1_list=[2568,2768,2968]
    z2_list=[0,3000,6000]

# TCS scan range 110406
    scan_step=0.05
    scan_time=0.2

# St2Slit1 knife edge scan
    slit1_start=18000
    slit1_end=100
    slit1_step=-100
    slit1_ch0=3
    slit1_ch1=0

# Devices
    id=ID(s)
    mono=Mono(s)
    tcs=TCS(s)
    exs=ExSlit1(s)
    axes=AxesInfo(s)
    f=File("./")

# Counter
    counter=Count(s,0,3)

    # Log file
    logf=open("table_z2.log","w")
    logf.write("Gap[mm],Energy[kev],Dtheta1[pulse],Ty1[pulse],TCS_v,TCS_h,ESlit1_v\n")
    logf.flush()

    for en in en_list :
	# Axes information 
	prefix="%03d"%f.getNewIdx3()
	enstr="%fkev"%en
	ofile=prefix+"_"+enstr+"_axes.dat"
	axes.all(ofile)

	# Changing Energy
    	id.moveE(en)
    	mono.changeE(en)

	time.sleep(300)

	for ty1 in ty1_list:
		# Setting Ty1
		mono.moveTy1(ty1)

		for z2 in z2_list:
			# Z2 move
			mono.moveZ2(z2)

			# slit1 full open
			exs.fullOpen()

			## Dtheta1
			if en >= 10.0:
				prefix="%03d_tcs_fo"%f.getNewIdx3()
				dt1_fwhm,dt1_center=mono.scanDt1PeakConfig(prefix,"DTSCAN_FULLOPEN",tcs)
			elif en < 10.0:
				prefix="%03d_tcs_fo"%f.getNewIdx3()
				dt1_fwhm,dt1_center=mono.scanDt1PeakConfig(prefix,"DTSCAN_FULLOPEN_LE",tcs)

			# Slit1 vertical scan
    			prefix="%03d"%f.getNewIdx3()
			slit1_vfwhm,slit1_vcenter=exs.scanV(prefix,-slit1_start,-slit1_end,-slit1_step,slit1_ch0,slit1_ch1,0.5)

			# Intensity counter
			# This is required to judge whether this position is suitable for user operation
			# Sometimes, beam intensity is very very weak because the collimator pin hole on the 
			# beamline obstacles the beam path.
			ch1,ch2=counter.getCount(1.0)

			# LOG STRINGS
			logstr="%8.3f, %8.3f, %8d, %8d, %8d, %9.1f, %12d, %12d"%(id.getE(en),en,dt1_center,ty1,z2,slit1_vcenter,ch1,ch2)
			logf.write("%s\n"%logstr)
			logf.flush()

			# Axes information 
			prefix="%03d_final"%f.getNewIdx3()
			ofile=prefix+"_axes.dat"
			axes.all(ofile)
    logf.close()
    break
s.close()

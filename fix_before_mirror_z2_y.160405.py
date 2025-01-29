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
    en_list=[8.5,12.3984,18.0]
    ty1_list=[2550,2750,2950]
    z2_list=[3000,5000,7000]

# TCS scan range 110406
    scan_step=0.05
    scan_time=0.2

# St2Slit1 knife edge scan
    slit1_start=18000
    slit1_end=100
    slit1_step=-100
    slit1_ch0=3
    slit1_ch1=0

# Detector number
    cnt_ch1=3
    cnt_ch2=0

# Devices
    id=ID(s)
    mono=Mono(s)
    tcs=TCS(s)
    exs=ExSlit1(s)
    axes=AxesInfo(s)
    f=File("./")


    # Log file
    logf=open("table_ty1_z2_test.log","w")
    logf.write("Gap[mm],Energy[kev],Dtheta1[pulse],Ty1[pulse],TCS_v,TCS_h,ESlit1_v,Eslit1_h\n")
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
	time.sleep(600)

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

			# TCS vertical & horizontal scan x 1times
    			#prefix="%03d_tcs"%f.getNewIdx3()
    			#vcenter1,tmp=tcs.scanVrel(prefix,0.05,0.5,1.6,scan_step,cnt_ch2,cnt_ch1,scan_time)
    			#hcenter1,tmp=tcs.scanHrel(prefix,0.50,0.05,1.6,scan_step,cnt_ch2,cnt_ch1,scan_time)

			# TCS aperture 0.1x0.1mm
			#tcs.setApert(0.1,0.1)

			# Slit1 vertical & horizontal scan
    			prefix="%03d"%f.getNewIdx3()

			slit1_vfwhm,slit1_vcenter=exs.scanV(prefix,-slit1_start,-slit1_end,-slit1_step,slit1_ch0,slit1_ch1,0.5)
			slit1_hfwhm,slit1_hcenter=exs.scanH(prefix,-slit1_start,-slit1_end,-slit1_step,slit1_ch0,slit1_ch1,0.5)

			# LOG STRINGS
			#logstr="%8.3f,%8.3f,%8d,%8d,%8d,%7.4f,%7.4f,%8.1f,%8.1f"%(id.getE(en),en,dt1_center,ty1,z2,vcenter1,hcenter1,slit1_vcenter,slit1_hcenter)
			logstr="%8.3f, %8.3f, %8d, %8d, %8d, %9.1f, %9.1f"%(id.getE(en),en,dt1_center,ty1,z2,slit1_vcenter,slit1_hcenter)
			logf.write("%s\n"%logstr)
			logf.flush()

			# Axes information 
			prefix="%03d_final"%f.getNewIdx3()
			ofile=prefix+"_axes.dat"
			axes.all(ofile)
    logf.close()
    break
s.close()

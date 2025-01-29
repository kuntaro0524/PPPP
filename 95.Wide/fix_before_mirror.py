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

while True:

# Conditions
##    en_list=[8.5,20.0]
##    ty1_list=[-2100,-1300]
##    en_list=[8.5,12.398,18.0,10.0,14.0,16.0,20.0]
##    ty1_list=[-2100,-1900,-1700,-1500,-1300]
#   en_list=[12.398,8.5,10.0, 16.0,18.0,20.0]    ##hashi 100615 for test_scan
#   en_list=[8.5,10.0, 16.0,18.0,20.0]    ##hashi 100615 for test_scan
#   en_list=[8.5,10.0,12.398, 16.0,18.0,20.0]    ##kh 101007
    en_list=[12.398,8.5,10.0,16.0,18.0,20.0]    ##kh 101017

#    ty1_list=[-1900,-1700,-1500] ## KH 100629
#    ty1_list=[-1675]                                 ##hashi 100615 for test_scan
#    ty1_list=[-1500,-2071,-2500] ## KH 100629
#   ty1_list=[-4650,-4850,-5050,-4450,-4250] ## KH 101007
    ty1_list=[-4650,-4950,-4350,-5250,-4050] ## KH 101016

# Dtheta scan range
    scan_dt1_start=-99000
    scan_dt1_end=-95000
    scan_dt1_step=20 # honmono
    scan_dt1_time=0.2

# TCS scan range 100712
    scan_apert=0.05
    scan_another_apert=0.5
    scan_start=-0.5
    scan_end=1.5
    scan_step=0.05
    scan_time=0.2

# St2Slit1 knife edge scan
    slit1_start=18010
    slit1_end=10
    slit1_step=-100
    slit1_ch0=0
    slit1_ch1=3

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

    index=0
    sizei=0

    # Log file
    logf=open("fix.log","w")
    logf.write("Gap[mm],Energy[kev],Dtheta1[pulse],Ty1[pulse],TCS_v,TCS_h,ESlit1_v,Eslit1_h\n")

    for en in en_list :
	# Axes information 
	prefix="%03d"%f.getNewIdx3()
	enstr="%fkev"%en
	ofile=prefix+"_"+enstr+"_axes.dat"
	axes.all(ofile)

	# Changing Energy
	if en==8.5:
		id.move(7.62)
	else:
    		id.moveE(en)

    	mono.changeE(en)

	# Waiting for a thermal equilibrium
	if en<12.398:
		time.sleep(1800)

	for ty1 in ty1_list:
		# slit1 full open
		exs.fullOpen()

		# Setting Ty1
		mono.moveTy1(ty1)

		##  dtheta1 tune @ TCS 3.0mm x 3.0mm
		tcs.setApert(3.0,3.0)

		## Dtheta1
		prefix="%03d_tcs_fo"%f.getNewIdx3()
		dt1_fwhm,dt1_center=mono.scanDt1Peak(prefix,scan_dt1_start,scan_dt1_end,scan_dt1_step,cnt_ch1,cnt_ch2,scan_dt1_time) #hashi 100615 dtheta1 tune with back lash

		# TCS vertical & horizontal scan x 2times
    		prefix="%03d_1st"%f.getNewIdx3()
    		vcenter1,hcenter1=tcs.scanBoth(prefix,scan_apert,scan_another_apert,scan_start,scan_end,scan_step,cnt_ch2,cnt_ch1,scan_time)

    		prefix="%03d_2nd"%f.getNewIdx3()
    		vcenter2,hcenter2=tcs.scanBoth(prefix,scan_apert,scan_another_apert,scan_start,scan_end,scan_step,cnt_ch2,cnt_ch1,scan_time)

		# TCS aperture 0.1x0.1mm
		tcs.setApert(0.1,0.1)

		# Slit1 vertical & horizontal scan
    		prefix="%03d"%f.getNewIdx3()
		exs.fullOpen()

		slit1_vfwhm,slit1_vcenter=exs.scanV(prefix,slit1_start,slit1_end,slit1_step,slit1_ch0,slit1_ch1,1.0)
		slit1_hfwhm,slit1_hcenter=exs.scanH(prefix,-slit1_start,-slit1_end,-slit1_step,slit1_ch0,slit1_ch1,0.5)

		# Log string
		#("Gap[mm],Energy[kev],Dtheta1[pulse],Ty1[pulse],TCS_v,TCS_h,ESlit1_v,Eslit1_h")
		logstr="%8.3f,%8.3f,%8.1f,%8d,%7.4f,%7.4f,%8.1f,%8.1f"%(id.getE(en),en,dt1_center,ty1,vcenter2,hcenter2,slit1_vcenter,slit1_hcenter)
		logf.write("%s\n"%logstr)
		logf.flush()

		# Axes information 
		prefix="%03d_final"%f.getNewIdx3()
		ofile=prefix+"_axes.dat"
		axes.all(ofile)

    logf.close()
    s.close()

    break

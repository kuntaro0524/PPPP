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
    en_list=[8.5,10.0,12.398,14.0, 16.0, 18.0,20]

# Dtheta scan range
    dtstart=-92000
    dtend=-88000
    dtstep=20

# Detector number
    cnt_ch1=0
    cnt_ch2=1

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

    for en in en_list :
	# Axes information 
	prefix="%02d"%f.getNewIdx("scn")
	enstr="%fkev"%en
	ofile=prefix+"_"+enstr+"_axes.dat"
	axes.all(ofile)

	# Changing Energy
	if en==8.5:
		id.move(7.62)
	else:
    		id.moveE(en)

    	mono.changeE(en)

	# slit1 full open
	exs.fullOpen()

	##  dtheta1 tune @ TCS 3.0mm x 3.0mm
	tcs.setApert(3.0,3.0)

	## Dtheta1
	prefix="%02d"%f.getNewIdx("scn")
	dt1_center=mono.scanDt1(prefix,dtstart,dtend,dtstep,cnt_ch1,cnt_ch2,0.2)

	# TCS vertical & horizontal scan x 2times
    	prefix="%02d"%f.getNewIdx("scn")
    	vcenter1,hcenter1=tcs.scanBoth(prefix,0.05,1.0,-1.0,1.0,0.05,cnt_ch1,cnt_ch2,0.2)

    	prefix="%02d"%f.getNewIdx("scn")
    	vcenter2,hcenter2=tcs.scanBoth(prefix,0.05,1.0,-1.0,1.0,0.05,cnt_ch1,cnt_ch2,0.2)

	# TCS aperture 0.1x0.1mm
	tcs.setApert(0.1,0.1)

	# Slit1 vertical & horizontal scan
    	prefix="%02d"%f.getNewIdx("scn")
	exs.fullOpen()
	slit1_vcenter=exs.scanV(prefix,18010,10,-100,0,1,0.2)
	slit1_hcenter=exs.scanH(prefix,-18010,-10,100,0,1,0.2)

	# log file
	logf.write("%8.2f keV Dtheta1=%8d TCS(V,H)=(%8.4f,%8.4f) Exslit1(V,H)=(%8d,%8d)\n"%(en,int(dt1_center),vcenter2,hcenter2,int(slit1_vcenter),int(slit1_hcenter)))
	logf.flush()

	# Axes information 
	prefix="%02d_final"%f.getNewIdx("scn")
	ofile=prefix+"_axes.dat"
	axes.all(ofile)

    logf.close()
    s.close()

    break

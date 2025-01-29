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
    dtend=-86000
    dtstep=100

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
    logf=open("dtheta.log","w")

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

	##  dtheta1 tune @ TCS 3.0mm x 3.0mm
	tcs.setApert(5.0,5.0)

	## Dtheta1
	prefix="%02d_%-4.2fkev"%(f.getNewIdx("scn"),en)
	dt1_center=mono.scanDt1(prefix,dtstart,dtend,dtstep,cnt_ch1,cnt_ch2,0.2)

	# log file
	logf.write("%8.2f keV Dtheta1=%8d \n"%(en,int(dt1_center)))
	logf.flush()

	# Axes information 
	prefix="%02d_final"%f.getNewIdx("scn")
	ofile=prefix+"_axes.dat"
	axes.all(ofile)

    logf.close()
    s.close()

    break

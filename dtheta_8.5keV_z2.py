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
    z2_list=[500,1000,1500,2000,2500]

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

    # Changing Energy
    id.move(7.62)
    mono.changeE(8.5)

    for z2 in z2_list :
	# Move z2
	mono.moveZ2(z2)
	# Axes information 
	prefix="%02d"%f.getNewIdx("scn")
	z2str="%dpulse"%z2
	ofile=prefix+"_"+z2str+"_axes.dat"
	axes.all(ofile)

	##  dtheta1 tune @ TCS 3.0mm x 3.0mm
	tcs.setApert(5.0,5.0)

	## Dtheta1
	prefix="%02d_%s"%(f.getNewIdx("scn"),z2str)
	dt1_center=mono.scanDt1(prefix,dtstart,dtend,dtstep,cnt_ch1,cnt_ch2,0.2)

	# log file
	logf.write("Z2=%8d pulse, Dtheta1=%8d \n"%(z2,int(dt1_center)))
	logf.flush()

	# Axes information 
	prefix="%02d_final"%f.getNewIdx("scn")
	ofile=prefix+"_axes.dat"
	axes.all(ofile)

    logf.close()
    s.close()

    break

#!/bin/env python 
import sys
import socket
import datetime
import time

# My library
from Received import *
from Organizer import *

from Dtheta import *
from FES import *
from ID import *
from TCS import *
from ExSlit1 import *
from AxesInfo import *


# Waiting the previous run
#time.sleep(2400)

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:
# List
    energy_list=[8.3, 10.0, 12.398, 14.0, 16.0,18.0,20.0]

# Observation time for each energy
    obstime=3600
# Interval time (sec)
    interval=10

# Counter
    ch_pin=2
    ch_ic=1

# Constructor
    stmono=Organizer(s,"bl_32in","tc1_stmono_1","")
    tcs=TCS(s)
    id=ID(s)
    dtune=DthetaTune(s)
    ex2slit=ExSlit(s)
    axes=AxesInfo(s)

# Initialization
    tcs.setApert(3.0,3.0)
    ex2slit.fullOpen()

# Output file open
    of=open("fixed.dat","w")
# Setting
    data_index=0
    for e in energy_list:
	data_index+=1
# energy string
	en_str="%-8.3f"%float(e)
# Prefix setting
	prefix="%02d_mono_%skeV" % (data_index,en_str.strip())
# Storing axes information
	tmp=prefix+"_axes.dat"
	axes.all(tmp)
# Moving monochro 
	stmono.move(e,"kev")
# Moving ID
	id.moveE(e)
# Dtheta1 tune
	dtune.do(prefix,ch_pin,ch_ic)
# Counter
	ntime=int(obstime/interval)
	for sec in range(0,ntime):
		tmpcnt=stmono.getCount(ch_pin,1.0)
		timestr="%s"%datetime.datetime.now()
		of.write("%s %s %12d\n"%(prefix,timestr,tmpcnt))
		time.sleep(interval)

    of.close()

    break

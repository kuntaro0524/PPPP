#!/bin/env python
import sys
import socket
import time
import datetime
import math
from pylab import *

# My library
from ExSlit1 import *
from Shutter import *
from Light import *
from CCDlen import *
from Cover import *
from CMOS import *
from File import *
from Gonio import *
from Att import *
from Colli import *
from TCS import *


while True:
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

##      Device definition
        exs1=ExSlit1(s)
        shutter=Shutter(s)
        light=Light(s)
        clen=CCDlen(s)
        covz=Cover(s)
        cmos=CMOS(s)
	gonio=Gonio(s)
	att=Att(s)
	f=File("./")
	colli=Colli(s)
	tcs=TCS(s)

##	Gonio meter evacuation
	sx,sy,sz=gonio.getXYZmm()

##	Crystal evacuation
	gonio.moveTrans(1000.0)

        ## CMOS off
        cmos.off()
        clen.evac()

        ## Cover on
        covz.on()
        print "CCD cover was closed"
        ## Cover check
        if covz.isCover():
                exs1.openV()
                print "Slit1 lower blade opened"
                light.off()
                print "Light went down"
                shutter.open()
                print "Shutter on diffractometer was opened"

	# Attenuator off
        att.att0um()

	# collimator in
	colli.on()

	# TCS 1x10um beam (height,width)=(0.5,0.040)
        tcs.setApert(0.5,0.040)

	prefix="%03d"%(f.getNewIdx3())
	ofile="%s_count.dat"%prefix
	outf=open(ofile,"w")
	
	counter=Count(s,3,0)

	currtime=datetime.datetime.now()
	ch1,ch2=counter.getCount(1.0)
	str=counter.getPIN(3)
	datestr=datetime.datetime.now()
	outf.write("%s %s ch3: %10d  ch0:%10d %s\n"%(datestr,currtime,ch1,ch2,str))

	shutter.close()
	exs1.closeV()
	outf.close()

	gonio.moveXYZmm(sx,sy,sz)

	colli.off()
        ## Cover on
        covz.off()

	s.close()
        break

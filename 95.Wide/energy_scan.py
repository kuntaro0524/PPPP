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
import  pylab
from AnalyzePeak import *


host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:

# IC number
#	cnt_ch1=0
#	cnt_ch2=1
        cnt_ch1=3 #hashi 
        cnt_ch2=0 #hashi at stage

# Energy setting [keV] [Ni]
	#edge=	8.330
	#start=	8.360 #
	#end=	8.310 #8.310
	#step=	-0.001
	#gap=7.4

# Energy setting [keV] [Zr]
	edge=	18.0000
	start=	18.0800
	end=	17.9800
	step=	-0.001

# Energy setting [keV] [Cu]
        #edge=   8.9800
        #start=  9.0200
        #end=    8.8000
        #step=   -0.001

# Energy setting [keV] [Zn]
        #edge=   9.6610
        #start=  9.6800
        #end=    9.6400
        #step=   -0.001

# Energy setting [keV] [Au]
	#edge=	11.9000
	#start=	11.960
	#end=	11.880
	#step=	-0.001

# Energy setting [keV] [Pb]
        #edge=   13.040
        #start=  13.100
        #end=    12.980
        #step=   -0.001


# Devices
	id=ID(s)
	mono=Mono(s)
	tcs=TCS(s)
	axes=AxesInfo(s)
	f=File("./")

	# Set edge energy
	mono.changeE(edge)
	id.moveE(edge)
	
	# Dtheta1 scan
	tcs.setApert(3.0,3.0)
	prefix="%03d"%f.getNewIdx3()
#    	mono.scanDt1Peak(prefix,-90000,-85000,50,cnt_ch1,cnt_ch2,0.2)
#       mono.scanDt1Peak(prefix,-87000,-82000,50,cnt_ch1,cnt_ch2,0.2)
#        mono.scanDt1Peak(prefix,-95000,-90000,50,cnt_ch1,cnt_ch2,0.2) ## 100629 hashi
#        mono.scanDt1Peak(prefix,-96500,-92500,50,cnt_ch1,cnt_ch2,0.2) ## 100714 hashi


	# Energy scan
	prefix="%03d"%f.getNewIdx3()
#        mono.scanEnergy(prefix,start,end,step,cnt_ch2,cnt_ch1,0.2)
        mono.scanEnergy(prefix,start,end,step,cnt_ch2,cnt_ch1,1.0)

	ofile=prefix+"_escan.scn"

	# derivative file
        ana=AnalyzePeak(ofile)
        f=File("./")

        # Energy scan file
	# normalize peak
        x1,y1,y2=ana.prepData3(1,2,3)
        norm=ana.divide(y1,y2)

        # derivative of normalized intensity
        dx,dy=ana.derivative(x1,norm)

        # convert dx,dy to Pylab array
        pdx,pdy=ana.convertArray(dx,dy)

        # File output
        newfile=ofile.replace(".scn","_drv.scn")
        ofile=open(newfile,"w")

        for i in range(0,len(pdx)):
                ofile.write("12345 %8.5f %8.5f 12345\n"%(pdx[i],pdy[i]))
        ofile.close()

	s.close()

	break

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
from FixedPoint import  *
from Att import *
from SPACE import *
from MyException import *
from BM import *
from Stage import *
from Shutter import *
from Capture import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:

	# Devices
	id=ID(s)
	mono=Mono(s)
	tcs=TCS(s)
	axes=AxesInfo(s)
	f=File("./")
	fixedp=FixedPoint(s)
	att=Att(s)
	space=SPACE()
	bm=BM(s)
	stage=Stage(s)
	shutter=Shutter(s)
	cap=Capture()

	# current directory
	curr_dir=f.getAbsolutePath()

	# Capture
	cenx=341
	ceny=232

	#filename="%s/test_%02d.ppm"%(curr_dir,f.getNewIdx3())
	#x,y=cap.captureBM(filename)

	ofile=open("test.log","w")
	# Gravity calculation
	for i in range(0,5):
		print i
        	stage.moveYum(1.0)
		filename="%s/test_%02d.ppm"%(curr_dir,f.getNewIdx3())
		x,y=cap.captureBM(filename)
		ofile.write("%5d %5d %8.4f %8.4f\n"%(x,y,stage.getZmm(),stage.getYmm()))

	# Monitor out
	ofile.close()
    	s.close()

	break

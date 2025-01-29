#!/bin/env python 
import sys
import socket
import time
import math
from pylab import *

# My library
from ExSlit1 import *
from Shutter import *
from Light import *
from CCDlen import *
from Cover import *

while True:
	#host = '192.168.163.1'
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

##	Device definition
	exs1=ExSlit1(s)
	shutter=Shutter(s)
	light=Light(s)
	clen=CCDlen(s)
	covz=Cover(s)

	# Shutter close
	shutter.close()
	print "Shutter on Diffractometer was closed"

	# Slit close
	exs1.closeV()
	print "Slit lower blade was closed"

	# CCD evacuate
	if clen.getLen() < 300.0:
		clen.evac()

	if clen.getLen() < 110.0:
		print "CCD is near!!!\n"
		sys.exit(1)

	## Cover check
	if covz.isCover()==True:
		covz.off()
		print "Cover was opened."

	print "Start diffraction experiments!"
	light.on()
	break

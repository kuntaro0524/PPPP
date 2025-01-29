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
from CMOS import *

while True:
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
	cmos=CMOS(s)

	## CMOS off
	cmos.off()

	clen.moveCL(500)
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
	break

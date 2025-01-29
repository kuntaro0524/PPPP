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

	# Backlight Off
	light.off()

	# Shutter close
	shutter.open()
	print "Shutter on Diffractometer was opened"

	# Slit close
	exs1.openV()
	print "Slit lower blade was opened"

	break

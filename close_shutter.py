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
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

##	Device definition
	exs1=ExSlit1(s)
	shutter=Shutter(s)

	# Shutter close
	shutter.close()
	print "Shutter on Diffractometer was closed"

	# Slit close
	exs1.closeV()
	print "Slit lower blade was closed"

	break

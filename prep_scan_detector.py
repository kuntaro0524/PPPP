#!/bin/env python 
import sys
import socket
import time
import math
from pylab import *

# My library
from CCDlen import *
from Cover import *

from Morning import q315r_workaround

while True:
	#host = '192.168.163.1'
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

##	Device definition
	clen=CCDlen(s)
	covz=Cover(s)

	clen.evac()
	covz.on()

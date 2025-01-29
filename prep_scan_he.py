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
from BM import *
from BS import *
from Cryo import *

while True:
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

##	Device definition
	exs1=ExSlit1(s)
	shutter=Shutter(s)
	light=Light(s)
	bm=BM(s)
	bs=BS(s)
	cryo=Cryo(s)
	
	## BS on
	bs.on()

	# Cryo Z
	cryo.moveTo(2000)

	## BM on between sample and BS
	bm.onXYZ()

	## Cover check
	exs1.openV()
	light.off()
	shutter.open()
	break

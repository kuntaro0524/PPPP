#!/bin/env python 
import sys
import socket
import time
import math
from pylab import *

# My library
from Gonio import *

while True:
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

##	Device definition
	gonio=Gonio(s)

## 	Gonio set position [mm]
	sx=3.69000
	sy=-13.0621
	sz=-0.7430

	gonio.moveXYZmm(sx,sy,sz)

	break

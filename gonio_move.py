#!/bin/env python 
import sys
import socket
import time
import math
from pylab import *
from Gonio import *

if __name__=="__main__":
	#host = '192.168.163.1'
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	gonio=Gonio(s)

	x,y,z,phi=float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])

	print x,y,z,phi
	gonio.moveXYZmm(x,y,z)
	gonio.rotatePhi(phi)
	print x,y,z,phi

	s.close()

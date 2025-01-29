#!/bin/env python 
import sys
import socket
import time
import math
from pylab import *

# My library
from Gonio import *

if __name__=="__main__":
	#host = '192.168.163.1'
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	comment=sys.argv[1]

	gonio=Gonio(s)

	xyz=gonio.getXYZmm()
	phi=gonio.getPhi()
	#print phi

	p=float(phi)
	
	print "%12.4f %12.4f %12.4f %12.4f  %s"%(xyz[0],xyz[1],xyz[2],p,comment)

	s.close()

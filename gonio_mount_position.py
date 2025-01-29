#!/bin/env python 
import sys
import socket
import time
import math
from pylab import *

# My library
from Gonio import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	gonio=Gonio(s)

	#while(1):
	#gonio.moveXYZ(-130,137500,4373)
	time.sleep(10)
	#gonio.moveXYZ(320,117852,4668)
	#time.sleep(10)

	s.close()

#!/bin/env python 
import sys
import socket
import time
from  File import *
from  Mono import *
from TCS import *

# My library
from Motor import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	f=File("./")
	prefix="%03d"%f.getNewIdx3()

	ch1=int(sys.argv[1])
	ch2=int(sys.argv[2])
	step=int(sys.argv[3])
	
	mono=Mono(s)
	tcs=TCS(s)
	tcs.setAperture(0.1,0.1)
    	mono.scanDt1(prefix,-88000,-83000,step,ch1,ch2,0.2)

	s.close()

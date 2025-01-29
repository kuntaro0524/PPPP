#!/bin/env python 
import sys
import socket
import time
from  File import *
from  Mono import *

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
	bl=int(sys.argv[4])
	
	mono=Mono(s)
    	maxx=mono.scanDt1PeakBackLash(prefix,-88000,-84000,step,ch1,ch2,0.2,bl)
	print maxx

	s.close()

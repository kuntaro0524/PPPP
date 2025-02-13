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
	
	tcs=TCS(s)
	mono=Mono(s)

        tcs.setApert(0.1,0.1) #before energy_scan.py by hashi 100614
    	mono.scanDt1Peak(prefix,-95000,-87000,step,ch1,ch2,0.2)
	s.close()

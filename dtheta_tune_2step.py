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
	
	mono=Mono(s)
    	current_max=mono.scanDt1Peak(prefix,-88000,-83000,100,ch1,ch2,0.2)[1]

	start2=current_max-30
	end2=current_max+30
	prefix="%03d"%f.getNewIdx3()
    	mono.scanDt1Peak(prefix,start2,end2,2,ch1,ch2,0.2)

	s.close()

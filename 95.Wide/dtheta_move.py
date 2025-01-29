#!/bin/env python 
import sys
import socket
import time

# My library
from Mono import *
  
if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	
	mono=Mono(s)
	dtheta1=int(raw_input())
    	mono.moveDt1(dtheta1)

	s.close()

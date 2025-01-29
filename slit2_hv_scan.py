#!/bin/env python 
import sys
import socket
import time

# My library
from ExSlit2 import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	slit2=ExSlit2(s)

	#print slit2.scanV("test",-200,0,5,3,0,1.0)
	print slit2.scanH("test",-500,500,20,3,0,1.0)

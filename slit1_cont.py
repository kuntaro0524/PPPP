#!/bin/env python 
import sys
import socket
import time

# My library
from ExSlit1 import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	test=ExSlit1(s)

	opt1=sys.argv[1]
	if sys.argv[1]=="open":
		test.openV()
	elif sys.argv[1]=="close":
		test.closeV()

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

	exs2=ExSlit2(s)

	v_apert=float(sys.argv[1])
	h_apert=float(sys.argv[2])
	exs2.setSize(v_apert,h_apert)

	s.close()

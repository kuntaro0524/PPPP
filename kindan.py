#!/bin/env python 
import sys
import socket
import time
import datetime 

from Colli import *
from Light import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	light=Light(s)
	coli=Colli(s)

	#coli.goOff()
	light.on()
	s.close()

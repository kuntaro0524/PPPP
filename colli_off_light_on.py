#!/bin/env python 
import sys
import socket
import time
import datetime 

import Colli
import Light

if __name__=="__main__":
	#host = '192.168.163.1'
	host = '172.24.242.41'
	port = 10101

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	coli=Colli.Colli(s)
	light=Light.Light(s)
	coli.off()
	light.on()
	s.close()

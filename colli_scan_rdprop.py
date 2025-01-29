#!/bin/env python 
import sys
import socket
import time
import datetime 

# My library
from Received import *
from Motor import *
from BSSconfig import *
from Colli import *
from File import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101

	f=File("./")

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

        prefix="%03d"%f.getNewIdx3()
	coli=Colli(s)
	coli.scan(prefix,3)
	trans=coli.compareOnOff(3)
	print "Transmission %5.2f percent\n"%trans

	s.close()

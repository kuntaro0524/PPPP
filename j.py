#!/bin/env python 
import sys
import socket
import time
import datetime

# My library
from Mono import *
from FES import *
from ID import *
from TCS import *
from ExSlit1 import *
from AxesInfo import *
from File import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

# insert by YK at 140929 for restart script
#time.sleep(600)

while True:
	counter=Count(s,0,3)
	ch1,ch2=counter.getCount(1.0)
	logstr="%12d"%(ch1)
	print logstr
	break

s.close()

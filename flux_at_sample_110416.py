#!/bin/env python 
import sys
import socket
import time
import datetime
from ExSlit1 import *
from Shutter import *
from Count import *
from BS import *
from ID import *

# My library

if __name__=="__main__":
	host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	count=Count(s,3,0)

	shutter=Shutter(s)
	slit1=ExSlit1(s)
	bs=BS(s)
	id=ID(s)

	bs.off()
	print count.getPIN(3)

	slit1.openV()
	shutter.open()

	print "gap:"
	gap=float(raw_input())
	id.move(gap)
	cnt=count.getPIN(3)

	print cnt

	#id.move(initID)
	shutter.close()
	slit1.closeV()

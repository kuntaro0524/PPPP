#!/bin/env python 
import sys
import socket
import time
import math
from pylab import *

# My library
from ExSlit1 import *
from Shutter import *
from Light import *
from Colli import *
from Count import *
from BS import *

while True:
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

##	Device definition
	exs1=ExSlit1(s)
	coli=Colli(s)
	shutter=Shutter(s)
        counter=Count(s,3,0)
	light=Light(s)
	bs=BS(s)

## 	Prep scan
	light.off()
	exs1.openV()
	shutter.open()

## 	Colli out
	coli.off()
        out1,ch2=counter.getCount(1)

	coli.on()
        out2,ch2=counter.getCount(1)

	perc=float(out2)/float(out1)*100.0
	print out1/1.0E3,out2/1.0E3,perc

##	BS on
	bs.on()
	print "Please set gain 1E-10 and press enter"
	raw_input()

        bsout,ch2=counter.getCount(1)

	print "After BS: %8.5f pA"%(float(bsout)/1.0E3)

	break

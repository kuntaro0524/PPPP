#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Motor import *
from ID import *
from TCS import *
from AxesInfo import *
from Dtheta import *
from ExSlit1 import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:
    print "Input index [example. 00, 01,...]:"
    data_index = int(raw_input())
 
    energy_list=[8.3, 12.398, 20.0]
    ty1_list=[-1500,-1600,-1700,-1800]

# Constructer
    stmono=Mono(s)
    tcs=TCS(s)
    id=ID(s)
    ex2slit=ExSlit1(s)
    axes=AxesInfo(s)

# Intensity monitor channels
    ch_pin=2
    ch_ic=1

# Initialize HW
    ex2slit.fullOpen()
    tcs.setApert(1.0,1.0)
    cnt_ch1=0
    cnt_ch2=1

# Setting TCS aperture
    for e in energy_list:
	for curr_ty1 in ty1_list:
	# energy string
		en_str="%-8.3f"%float(e)
	# Prefix setting
		prefix="%02d_mono_%skeV_ty1_%s" % (data_index,en_str.strip(),str(curr_ty1))
	# Storing axes information
		tmp=prefix+"_axes.dat"
		axes.all(tmp)
	# Moving monochro 
		stmono.changeE(e)
	# Moving ID
		id.moveE(e)
	# Moving Ty1
    		stmono.moveTy1(curr_ty1)
	# Tuning dtheta1
		tcs.setApert(1.0,1.0)
		stmono.scanDt1(prefix,-89000,-87000,20,cnt_ch1,cnt_ch2,0.2)
	# TCS scan
		tcs.scanBoth(prefix,0.05,1.0,-1,1,0.05,cnt_ch1,cnt_ch2,0.2)
	# TCS aperture 0.1mm square
		tcs.setApert(0.1,0.1)
	# Knife edge scan before mirror chamber
		ex2slit.scanBoth(prefix,ch_pin)
		data_index+=1
    s.close()

    break

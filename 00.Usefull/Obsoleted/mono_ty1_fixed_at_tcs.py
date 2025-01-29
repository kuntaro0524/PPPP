#!/bin/env python 
import sys
import socket
import time
import datetime

# My library
from Received import *
from Organizer import *
from Dtheta import *
from FES import *
from ID import *
from TCS import *
from ExSlit1 import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:

# scan energy list
    en_list=[8.3,10.0,12.4,14.0,18.0,20.0]

# Counter channel
    cnt_ch1=1
    cnt_ch2=2

# Slit size list(Height,Width)
    dtheta_width=[1.00,1.00]

# ty1 parameter list
    ty1_list=[-2000,-1500,-1200,-1000,-500,0,200]
    #ty1_list=[-1435]

# fes
    fes=FES(s)
    fes.moveInit()

# Devices
    stmono=Organizer(s,"bl_32in","tc1_stmono_1","")
    mono_ty1=Organizer(s,"bl_32in","tc1_stmono_1","thetay1")
    id=ID(s)
    dt=DthetaTune(s)
    tcs=TCS(s)

    index=0
    sizei=0

    print ("Input the first index:")
    index=int(raw_input())

    for en in en_list :
	for curr_ty1 in ty1_list:
		# file prefix
		prefix="%02d_%skev_ty1_%spulse"%(index,en,curr_ty1)
	
		#moving the fisrt position
    		stmono.move(en,"kev")
    		id.moveE(en)
		mono_ty1.move(int(curr_ty1),"pulse")

		## Dtheta tune
		tcs.setApert(dtheta_width[0],dtheta_width[1])
    		dt.do(prefix,cnt_ch1,cnt_ch2)

		## Horizontal & vertical TCS scan
		tcs.scan(prefix,cnt_ch1,cnt_ch2)

		index+=1
	
    s.close()

    break

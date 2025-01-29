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
from FixedPoint import  *
from Att import *
from SPACE import *
from MyException import *
from BM import *
from BS import *
from Stage import *
from Shutter import *
from Capture import *
from Gonio import *
from Colli import *
from Cryo import *
from CenteringNeedle import *
from StageTune import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:

	# Devices
	id=ID(s)
	mono=Mono(s)
	tcs=TCS(s)
	axes=AxesInfo(s)
	f=File("./")
	fixedp=FixedPoint(s)
	att=Att(s)
	space=SPACE()
	bm=BM(s)
	stage=Stage(s)
	shutter=Shutter(s)
	cap=Capture()
	colli=Colli(s)
	bs=BS(s)
	gonio=Gonio(s)
	cryo=Cryo(s)
	#cn=CenteringNeedle(s)

	# current directory
	curr_dir=f.getAbsolutePath()

#############################################
	# Automatic stage tune #
#############################################
	st=StageTune(stage,cap,bm)

        filename="%s/test_%03d.ppm"%(curr_dir,f.getNewIdx3())
	st.doAutomatic(filename)
    	s.close()

	break

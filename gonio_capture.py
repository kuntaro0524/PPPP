#!/bin/env python 
import sys
import socket
import time
import datetime
import os
import time

# My library
from BeamCenter import *
from Gonio import *
from Capture import *
from File import *

if __name__=="__main__":
        #host = '192.168.163.1'
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	cap=Capture()
	cap.capture("/tmp/junk",500)
	cap.setShutterSpeed(300)

	gonio=Gonio(s)
	gonio.rotatePhi(40.0)
	f=File("./")

	curr_dir=f.getAbsolutePath()

	# preparation for tuning binning mode
	time.sleep(5.0)

	iii=0
	for i in range(0,36):
		gonio.rotatePhiRelative(10.0)
		phi=gonio.getPhi()
		capfile="%s/%03d_%05.1f.ppm"%(curr_dir,iii,phi)
		cap.capture(capfile,500)
		iii+=1

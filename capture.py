#!/bin/env python 
import sys
import socket
import time
import datetime
import os

from Capture import *
from Light import *
from File import *

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	cap=Capture()
	file=File("./")

	while(1):
		filename="%03d_capture.ppm"%(file.getNewIdx3())
		abspath=os.path.abspath("./")
		fullfile="%s/%s"%(abspath,filename)
		# Capture
		cap.capture(fullfile)
		time.sleep(60)

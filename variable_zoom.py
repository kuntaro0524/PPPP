#!/bin/env python 
import sys
import socket
import time

from Zoom import *
from Capture import *
from File import *
from Gonio import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	f=File("./")
	zoom=Zoom(s)
        cap=Capture()
        cap.capture("/isilon/BL32XU/BLsoft/PPPP/ppp.ppm")

	abspath=f.getAbsolutePath()

	#list=[-48000,-33100,-13500,-6400,0]

	# zoom x1
	prefix="zoom_x_1"
	zoom.move(-48000)
	file="%s_orig.ppm"%prefix
	ofile=abspath+"/"+file
        cap.capture(ofile)

	# zoom x2
	prefix="zoom_x_2"
	zoom.move(-33100)
	file="%s_orig.ppm"%prefix
	ofile=abspath+"/"+file
        cap.capture(ofile)

	# zoom x5
	prefix="zoom_x_5"
	zoom.move(-13500)
	file="%s_orig.ppm"%prefix
	ofile=abspath+"/"+file
        cap.capture(ofile)

	# zoom x7
	prefix="zoom_x_7"
	zoom.move(-6400)
	file="%s_orig.ppm"%prefix
	ofile=abspath+"/"+file
        cap.capture(ofile)

	# zoom x10
	prefix="zoom_x_10"
	zoom.move(0)
	file="%s_orig.ppm"%prefix
	ofile=abspath+"/"+file
        cap.capture(ofile)

	s.close()

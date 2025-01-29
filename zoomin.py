#!/bin/env python 
import sys
import socket
import time

import Zoom

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	zoom=Zoom.Zoom(s)

	start=zoom.getPosition()
	print start

	#zoom.zoomOut()
	zoom.zoomIn()
	end=zoom.getPosition()
	print end

	#start=zoom.getPosition()
	#print start
#
	s.close()

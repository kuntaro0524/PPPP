import sys
import socket
import time
import datetime
from Shutter import *
from ExSlit1 import *

if __name__=="__main__":
	#host = '192.168.163.1'
	host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	shutter=Shutter(s)

	# Slit open
	ex1=ExSlit1(s)
	print ex1.getVpos()
	ex1.openV()
	print ex1.getVpos()
	
	# Shutter open
	#shutter.open()
	shutter.close()

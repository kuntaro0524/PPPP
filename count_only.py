import sys
import socket
import time
import datetime
import math
import timeit

from Received import *
from File import *
from AnalyzePeak import *
from Count import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	
	f=File("./")
	counter=Count(s,0,3)

	logf=open("beam_intensity.dat","w")

	while(1):
		timestr=datetime.datetime.now()
		ic,pin=counter.getCount(0.1)
		ic=float(ic)/10.0
		pin=float(pin)/10.0
		str=" %s : %8.3f [nA], %8.3f [uA]\n"% (timestr,ic,pin)
		print str,
		logf.write(str)
		time.sleep(1.0)
	s.close()


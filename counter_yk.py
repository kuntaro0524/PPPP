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
	
	while(1):
		counter=Count(s,0,3)
		ch0,ch3=counter.getCount(1.0)
		counter=Count(s,1,2)
		ch1,ch2=counter.getCount(1.0)
		print "counter ch0= %7d, ch1= %7d, ch2= %7d, ch3= %7d"%(ch0, ch1, ch2, ch3)
	s.close()

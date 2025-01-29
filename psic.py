import sys
import socket
import time
import datetime
import math
import timeit

from File import *
from Count import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	def cal(count):
		# for 1sec integration
		val=count/100.0
		# position [um]
		pos=val*37/75
		return pos
	
	while(1):
		counter=Count(s,1,0)
		c1,c2=counter.getCount(1.0)
		print cal(c1)
	s.close()

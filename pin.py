import sys
import socket
import time
import datetime
import math
import timeit

from Received import *
from TCS import *
from File import *
from AnalyzePeak import *
from Count import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	# Usage
	print "input a PIN channel:"
	ch=int(raw_input())

	tcs=TCS(s)
	counter=Count(s,ch,0)
	f=File("./")

	str=counter.getPIN(3)
	print"12345 %s\n" %(str)

	#of.close()
	s.close()


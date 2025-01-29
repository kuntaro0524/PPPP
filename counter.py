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
		counter=Count(s,1,0)
		print counter.getCount(1.0)
	s.close()

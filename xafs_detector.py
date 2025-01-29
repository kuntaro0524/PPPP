import sys
import socket
import time
import datetime
import math
import timeit

from Received import *
from File import *
from Count import *
from PlateYZ import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	
	counter=Count(s,4,5)
	plate=PlateYZ(s)
	save=int(plate.getZ()[0])

	for z in arange(6500,26500,1000):
		plate.moveZ(z)
		i4,i5=counter.getCount(0.5)
		i4=int(i4)
		i5=int(i5)
		diff= i4-i5
		print "%10d %10d"%(z,diff)

	s.close()
"""
	for y in arange(5000,35000,1000):
		plate.moveY(y)
		i4,i5=counter.getCount(0.5)
		i4=int(i4)
		i5=int(i5)
		diff= i4-i5
		print y,diff

	plate.moveY(save)
"""

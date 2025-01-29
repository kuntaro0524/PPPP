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
from Att import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	# Usage
	att=Att(s)
	counter=Count(s,3,0)

	# ofile
	of=open("att_fac.scn","w")

	idx=0
	for pls in arange(2800,3600,40):
		att.move(pls)
		str=counter.getPIN(5)
		of.write("%5d, %5d, %s\n"%(idx,pls,str))

		idx+=1

	of.close()
	s.close()


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

	tcs=TCS(s)
	counter=Count(s,2,0)
	f=File("./")

	# TCS aparture list
	tcs_list=[3.0, 0.5, 0.4, 0.3, 0.2, 0.1]

	# output file
       	prefix="%03d"%f.getNewIdx3()
	ofilename="%s_flux.scn"%prefix
	of=open(ofilename,"w")
	of.write("# TCS apeture is set to ? mm square\n")

	# TCS
	for tcs_size in tcs_list:
		# TCS size 
		tcs.setApert(tcs_size,tcs_size)

		# initialization
		str=counter.getPIN(3,2)
		of.write("12345 %8.4f %s\n" %(tcs_size,str))
	of.close()
	s.close()


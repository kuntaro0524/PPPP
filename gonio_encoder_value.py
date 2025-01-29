import sys
import socket
import time
import math
from pylab import *

# My library
from AnalyzePeak import *
from File import *
from Enc import *
from Gonio import *

if __name__=="__main__":
	#host = '192.168.163.1'
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	gonio=Gonio(s)
	f=File("./")

	# Counter time[sec]
	ctime=0.2

	sx,sy,sz=gonio.getXYZmm()
	ex,ey,ez=gonio.getEnc()
	print "Pulse:%12.5f %12.5f %12.5f Enc:%12.5f %12.5f %12.5f\n"%(sx,sy,sz,ex,ey,ez)

	s.close()

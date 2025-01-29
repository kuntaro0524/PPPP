import sys
import socket
import time
import math
from pylab import *
import numpy

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
	f=File("./")


	gonio=Gonio(s)

	# wait time
	wait=1.0

	fname="%03d_gonio_enc.scn"%(f.getNewIdx3())
	ofile=open(fname,"w")
	for i in arange(1,100):
		ex,ey,ez=gonio.getEnc()
		ofile.write("ENC: %12.5f %12.5f %12.5f\n"%(ex,ey,ez))
		ofile.flush()
		time.sleep(wait)
	s.close()

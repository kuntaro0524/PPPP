import sys
import socket
import time
import math
from pylab import *

# My library
from File import *
from Gonio import *
from Motor import *

if __name__=="__main__":
	#host = '192.168.163.1'
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	gonio=Gonio(s)
	gonio.resetPulseWithEncValue()
	s.close()

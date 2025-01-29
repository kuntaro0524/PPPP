import sys
import socket
import time
import math
from pylab import *

# My library
from Gonio import *

if __name__=="__main__":

        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	# Initialization
	gonio=Gonio(s)

	#print gonio.wireRoughScan(3)
	#print gonio.wireRoughZ(3)
	print gonio.wireRoughY(3)

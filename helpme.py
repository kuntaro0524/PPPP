import sys
import socket
import time
import math
from Att import *

# My library
from Motor import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	att=Att(s)
	
	thickness=float(sys.argv[1])
	flux=float(sys.argv[2])

	attfac=att.calcAttFac(1.0,thickness)

	total_flux=flux*attfac
	print "%8.3e"%total_flux

	s.close()

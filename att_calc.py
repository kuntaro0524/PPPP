import sys
import socket
import time
import math
import numpy 
import AttFactor

if __name__=="__main__":
	att=AttFactor.AttFactor()
	wl=float(sys.argv[1])
	thick=float(sys.argv[2])
	print att.calcAttFac(wl,thick)

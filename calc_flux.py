import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP")
import socket
import time
import math
import numpy 
import AttFactor

if __name__=="__main__":
	att=AttFactor.AttFactor()
	wl=float(sys.argv[1])
	thick=float(sys.argv[2])
	exptime=float(sys.argv[3])
	flux=float(sys.argv[4])
	print "%e"%(att.calcAttFac(wl,thick)*exptime*flux)

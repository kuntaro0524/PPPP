import os
import sys
import math
import socket
import  pylab
import scipy
import numpy

from AxesInfo import *
from pylab import *
from scipy.interpolate import splrep,splev,interp1d
from Gonio import *

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	if len(sys.argv)<4:
		print "Usage: program X Y Z [mm]\n"
		sys.exit(1)

        gonio=Gonio(s)

	# Position to move
        x=float(sys.argv[1])
        y=float(sys.argv[2])
        z=float(sys.argv[3])

        print "your input: %8.4f %8.4f %8.4f\n"%(x,y,z)

        px=int(x*10000)
        py=-int(y*10000)
        pz=int(z*10000)

        gonio.move(px,py,pz)

        curr_x= gonio.getX()[0]/10000.0
        curr_y=-gonio.getY()[0]/10000.0
        curr_z= gonio.getZ()[0]/10000.0

        print "final %8.4f %8.4f %8.4f\n"%(curr_x,curr_y,curr_z)

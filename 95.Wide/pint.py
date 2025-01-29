import os
import sys
import math
import socket
import  pylab
import scipy
import numpy

from Gonio import *

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        gonio=Gonio(s)

	um_value=float(sys.argv[1])
        gonio.movePint(um_value)

#!/bin/env python 
import sys
import socket
import time
import datetime
import os

# My library
from BeamCenter import *
from Capture import *

if __name__=="__main__":
	cap=Capture()


        # pixel to micron [um/pixel] in high zoom
        p2u_z=7.1385E-2
        p2u_y=9.770E-2

	ofile="test.log"
	of=open(ofile,"w")
	idx=0
	for i in range(0,100):
		filename="/isilon/users/target/target/Staff/101202/06.BeamPosition/%03d_cap.ppm"%i
		x,y=cap.captureFast(filename)
		of.write("%8.4f,%8.4f\n"%( float(x)*p2u_z,float(y)*p2u_y))
		of.flush()

import sys
import socket
import time
import datetime
import math
import timeit

from Procedure import *
from File import *
from AttFactor import *
from ConfigFile import *
from TCS import *
from Mono import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	
	proc=Procedure(s)
	attfac=AttFactor()
	f=File("./")
        conf=ConfigFile()
        tcs=TCS(s)
        mono=Mono(s)

	###
	##  Energy
	###
	en=12.3984
	first_wl=12.3984/en
	third_wl=12.3984/(en*3.0)

	#####
	## Set energy & dtheta1 determination
	#####
	attlist=[0,200,400,600,1200,1800,3000,6000]
	detune_list=[0,-50,-100,-150]

        prefix="%03d"%(f.getNewIdx3())
       	ofilename="%s_condition.dat"%prefix
       	of=open(ofilename,"w")

	for detune in detune_list:
        	prefix="%03d_%05dpls"%(f.getNewIdx3(),detune)
        	mono.scanDt1PeakConfigExceptForDetune(prefix,"DTSCAN_NORMAL",tcs,detune)
		for thick in attlist:
			print "Att thick = %8.1f [um]"%thick
			att1=attfac.calcAttFac(first_wl,thick)
			att3=attfac.calcAttFac(third_wl,thick)
			
			# Set attenuator
			proc.setAtt(thick)

        		ave3,ave4=proc.simpleCountBack(3,1,1.0,10)
			ave3=float(ave3)
			ave4=float(ave4)
			of.write("%10d %8.2f %8.5f %8.5f %8.5f %8.5f %12.1f %12.1f\n"%(detune,thick,first_wl,third_wl,att1,att3,ave3,ave4))
			of.flush()

	s.close()
	of.close()

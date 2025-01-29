#!/bin/env python 
import sys
import socket
import time
import datetime
import Enc
import BS

# My library
from Cover import *

# My library
from Received import *
from Motor import *

if __name__=="__main__":
	enc=Enc.Enc()
	enc.openPort()

	#host = '192.168.163.1'
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))


	# Beam stopper
	cover=Cover(s)
        bs=BS.BS(s)
	counter=Count(s,3,0)

        #bs.on()
        bs.off()

# Data collection
	starttime=datetime.datetime.now()
	ndata=0
	# Kurikaeshi time
	total_time=float(sys.argv[1]) # sec
	time_HWlimit=0.05 # sec
	n_limit=int(total_time/time_HWlimit)

	print "%d times"%n_limit

	# List
	t_list=[]
	d_list=[]

	for i in range(n_limit):
		t_list.append(datetime.datetime.now())
		x=enc.getX()
		y=enc.getY()
		z=enc.getZ()
		count_value=counter.getCountMsec(5)[0]
		d_list.append((x,y,z,count_value))

	print "Measurement finished!"
	print "Writing file...."

	ofile=open("enc.dat","w")
	for i in range(n_limit):
		t=t_list[i]
		time_from_start=t-starttime
		sec_part=float(time_from_start.seconds)
		sec_shousu=float(time_from_start.microseconds/1000000.0)
		dtime=sec_part+sec_shousu

		(x,y,z,count_value)=d_list[i]
		ofile.write("%8.5f %8.5f %8.5f %8.5f %5d\n"%(dtime,x,y,z,count_value))

	ofile.close()
	s.close()

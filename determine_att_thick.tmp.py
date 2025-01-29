import sys
import socket
import time
import datetime
import math

from Count import *
from Att import *
from AttFactor import *
from Procedure import *
from Mono import *
from File import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	# Usage
	mono=Mono(s)
	att=Att(s)
	counter=Count(s,3,0)
	proc=Procedure(s)
	attfac=AttFactor()
	f=File("./")

	# Condition
	energy=mono.getE()
	wave=12.3984/energy

	# Full flux count
	print "Attenuator is set to 0 pulse"
	att.move(0)
	ch0,ch1=proc.simpleCountBack(3,0,1.0,10)
	maxI=float(ch0)

	idx=0
	filename="%03d_attenuator.dat"%(f.getNewIdx3())
	ofile=open(filename,"w")
	for pls in arange(2800,3500,100):
		print "Att %5d pls"%pls
		att.move(pls)
		ch0,ch1=proc.simpleCountBack(3,0,1.0,10)
		value=float(ch0)
		trans=value/maxI
		thick=attfac.calcThickness(wave,trans)
		ofile.write("%5d %10.5f %10.1f\n"%(pls,trans,thick))
		ofile.flush()
		idx+=1

	ofile.close()
	s.close()


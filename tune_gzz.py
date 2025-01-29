import sys
import socket
import time
import math
from pylab import *

# My library
from Gonio import *
from ID import *
from Mono import *
from TCS import *
from ConfigFile import *

while True:
	#host = '192.168.163.1'
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

##	Device definition
	gonio=Gonio(s)
	f=File("./")

##	Counter channel
	cnt_ch1=3
	cnt_ch2=0
	counter=Count(s,cnt_ch1,cnt_ch2)

## 	Wire scan
       	oname="%03d_zz.dat"%(f.getNewIdx3())
	ofile=open(oname,"w")

	gonio.moveZZpulse(4538)

	savep=gonio.getZZ()
	print savep

	max=-99999.99999
	for rel in arange(-50,50,2):
		target=savep+rel
		gonio.moveZZpulse(target)
		cnt=counter.getCount(0.1)[0]
		ofile.write("1245 %10d %10d 1245\n"%(target,cnt))
		print "ZZ=%5d CPS=%5d"%(target,cnt*10)
		ofile.flush()

	gonio.moveZZpulse(savep)
	ofile.close()

	# Analyze
	ana=AnalyzePeak(oname)
       	outfig="%03d_zz.png"%(f.getNewIdx3())
	comment="GONIO V SCAN"
	fwhm,center=ana.analyzeAll("gonioV[mm]","Intensity",outfig,comment,"OBS","FCEN")
	print "FWHM = %8.5f CENTER=%8.5f "%(fwhm,center)

	# Move
	# 1um down Y.Kawano's result on 2014/05/28
	# gonioZZ 0.5 um/pls
	move_pos=int(center)-2
	gonio.moveZZpulse(move_pos)
	print "Final position=",gonio.getZZ()

	break

s.close()

import sys
import socket
import time
import datetime
import math
import timeit

from Count import *
from Gonio import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

        counter=Count(s,3,0)
	gonio=Gonio(s)
        f=File("./")
		
	ofile="%03d_count.scn"%(f.getNewIdx3())
	fff=open(ofile,"w")

	## save & evacuate gonio
	sx,sy,sz=gonio.getXYZmm()

	## 500um evacuation
	gonio.moveTrans(500)

	idx=0
        while(1):
                ti=datetime.datetime.now()
                ch1,ch2=counter.getCountMsec(50)
		fff.write("%20s %8d %8d\n"%(ti,ch1,ch2))
		idx+=1

		if idx>1200:
			break

	## save & evacuate gonio
	gonio.moveXYZmm(sx,sy,sz)

        s.close()

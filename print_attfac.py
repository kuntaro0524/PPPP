import sys
import socket
import time
import datetime
import math
import timeit
from numpy import *

from AttFactor import *

if __name__=="__main__":
        att=AttFactor()
	flux=1E10

	energy_list=[8.5,10.5,12.4,15.0,18.0]
	trans_list=[0.01]
	wave_list=[]

	for e in energy_list:
		wave=12.3984/e
		wave_list.append(wave)

	print len(wave_list)

        for w in wave_list:
		for t in trans_list:
        		print "%8.5f %10.3f %10.1f"%(w,t,att.calcThickness(w,t))
		print " "

	thick=110.0
	w= wave_list[2]
        print "%8.5f %10.3f %10.5f"%(w,thick,att.calcAttFac(w,thick))

import os
import sys
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
from Date import *

ifile=open(sys.argv[1],"r")

offsettime=float(sys.argv[2])

lines=ifile.readlines()

date=Date()

for i in range(0,len(lines)):
	idx=len(lines)-i-1
	#print len(lines)-i-1
	cols=lines[idx].split()
	time="%s %s"%(cols[0],cols[1])
	tmptime= date.getOkutsuTime(time)
	tempe=float(cols[2])
	if i==0:	
		starttime=tmptime

	diffsec=date.getDiffSec(starttime,tmptime)
	print diffsec,tempe

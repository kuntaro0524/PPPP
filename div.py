import os,sys

from AnalyzePeak import *

ana=AnalyzePeak(sys.argv[1])

xdat,ydat=ana.storeData(0,5)
dx,dy=ana.calcDrv()

idx=0
for x in xdat:
	print "%8.5f %8.2f\n"%(xdat[idx],ydat[idx]),
	idx+=1

print "\n\n"

idx=0
for x in dx:
	print "%8.5f %8.2f\n"%(dx[idx],-dy[idx]),
	idx+=1



import os,sys
import pylab
from numpy import r_, sin
from scipy.signal import cspline1d, cspline1d_eval

sys.path.append("/isilon/BL32XU/BLsoft/PPPP/") 
from AnalyzePeak import *

ana=AnalyzePeak(sys.argv[1])

xdat,ydat=ana.storeData(0,5)


#print type(xdat)

max=max(ydat)
threshold=max*0.8

idx=0
for x in xdat:
	if ydat[idx]<threshold:
		ydat[idx]=0
	idx+=1

dx,dy=ana.derivative(xdat,ydat)

idx=0

"""
for x in xdat:
	print "%8.5f %8.2f\n"%(xdat[idx],ydat[idx]),
	idx+=1

print "\n\n"
"""

idx=0
save=0
avelist=[]
for x in dx:
	if dy[idx] > 400:
		sflag=True
		sx=x
		#print "TWIDTH: %8.3f %8.3f %8.3f"%(sx-save,save,(sx+save)/2.0)
		avetime=(sx+save)/2.0
		avelist.append(avetime)
		#print "AVE %8.3f"%avetime
		save=x
	idx+=1


otime,encx=ana.prepData2(0,1)
ency,encz=ana.prepData2(2,3)
shutter,junk=ana.prepData2(4,0)

flag=False
idx=0
for t in shutter:
	#print t
	if t == 1 and flag==False:
		open_t=otime[idx]
		flag=True
	if flag==True and t==0:
		close_t=otime[idx]
		break
	idx+=1

print "OPEN %8.5f CLOSE %8.5f"%(open_t,close_t)
		

#ttime,newencx=ana.inter1dline(otime,encx,1.0)
ylist=ana.inter1dline(otime,ency,avelist)
#ttime,newencz=ana.inter1dline(otime,encz,1.0)


idx=0
for x in avelist:
	if x<=close_t and x>=open_t:
		print "%12.5f %12.5f"%(avelist[idx],ylist[idx])
	idx+=1

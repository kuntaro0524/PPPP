import os,sys
from AnalyzePeak import *

if __name__=="__main__":

	ana=AnalyzePeak(sys.argv[1])
	col1=int(sys.argv[2])
	col2=int(sys.argv[3])

	x,y=ana.prepData2(col1,col2)

	idx=0
	print "Average col (%5d,%5d)= %12.5f %12.5f"%(col1,col2,x.mean(),y.mean())
	print "STD     col (%5d,%5d)= %8.5f %8.5f"%(col1,col2,x.std(),y.std())

	#for xdat in x:
		#print x[idx],y[idx]
		#idx+=1

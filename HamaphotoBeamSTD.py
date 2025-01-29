import numpy 
import sys
from numpy import *
ifile=open(sys.argv[1],"r")

lines=ifile.readlines()

xa=[]
ya=[]

for line in lines:
	cols=line.split()
	x=float(cols[0])
	y=float(cols[1])
	xa.append(x)
	ya.append(y)

nxa=numpy.array(xa)
nya=numpy.array(ya)

xstd=nxa.std()
ystd=nya.std()

print "Average position: %8.2f %8.2f"%(nxa.mean(),nya.mean())
print "STD of  position: %8.2f %8.2f"%(xstd,ystd)

ifile.close()

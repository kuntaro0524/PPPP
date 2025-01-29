import numpy
import scipy
from numpy import *

x1=-0.4642
y1=-12.8603
z1=0.1880

x2=-0.4453
y2=-12.8053
z2=0.1970

point1=numpy.array((x1,y1,z1))
point2=numpy.array((x2,y2,z2))

print "POINT1"
print point1
print "POINT2"
print point2

### exp vector
ev1=point1-point2
tot_len=linalg.norm(ev1)
print ev1
print "Total length:%8.4f mm"%tot_len

### Step vector
step=5 # [um]
nstep=int(tot_len*1000/step)
stepvec=ev1*float(nstep)

print stepvec

for i in range(0,nstep):
	newpos=point1+float(i)*stepvec
	print i,newpos

## step
#nstep1=10
#nstep2=5

#ev1_step=ev1/float(nstep1)
#
#print linalg.norm(ev1_step)*1000
#print linalg.norm(ev2_step)*1000

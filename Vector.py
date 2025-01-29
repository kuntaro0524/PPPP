import numpy
import scipy
from numpy import *

x1=0.3333
y1=0.8333
z1=0.5333

x2=-0.5333
y2=-0.3333
z2=-1.2333

x3=-0.1035
y3=-0.2223
z3=-1.1113

origin=numpy.array((x1,y1,z1))
fast=numpy.array((x2,y2,z2))
slow=numpy.array((x3,y3,z3))

### exp vector
ev1=fast-origin
ev2=slow-origin

#print ev1,ev2

## step
nstep1=10
nstep2=5

ev1_step=ev1/float(nstep1)
ev2_step=ev2/float(nstep2)

print linalg.norm(ev1_step)*1000
print linalg.norm(ev2_step)*1000
	

print "#### AB ####"
print ev1_step
print "#### AC ####"
print ev2_step

print "#### O,F,S ####"
print origin
print fast
print slow

print "#### #### ####"
for i in range(0,nstep2+1):
	print "Line %5d"%i
	for j in range(0,nstep1+1):
		vec=origin+ev1_step*float(j)+ev2_step*float(i)
		#print linalg.norm(vec)

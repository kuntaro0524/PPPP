import numpy
import scipy
import math
from numpy import *

x1=0.050
y1=-12.991
z1=0.7717

x2=-0.2891
y2=-13.0229
z2=0.4535

origin=numpy.array((x1,y1,z1))
sample=numpy.array((x2,y2,z2))

### exp vector
ev1=sample-origin

print ev1[0],ev1[1],ev1[2]

dist=math.sqrt(ev1[0]**2+ev1[1]**2+ev1[2]**2)
print dist

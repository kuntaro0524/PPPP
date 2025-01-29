from AnalyzePeak import *

# file open
ana=AnalyzePeak("1000_time.scn")
x,y1,y2=ana.prepData3(1,2,3)

py1=ana.getPylabArray(y1)
py2=ana.getPylabArray(y2)

mean1=py1.mean()
mean2=py2.mean()
std1=py1.std()
std2=py2.std()

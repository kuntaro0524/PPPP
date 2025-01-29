import os,sys
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp
import glob
import datetime

def myfunc(x):
	rtn=x*x
	return rtn

def myfunc2(compo):
	filename,ddd=compo
	print filename,ddd,

renren=range(1,100)
print renren

processing_list=[]

for i in range(1,100):
	filename="file_%05d.dat"%i
	ddd=[(i,i+5)]
	processing_list.append((filename,ddd))

starttime=datetime.datetime.now()
easy_mp.pool_map(fixed_func=lambda n: myfunc2(n), args=processing_list, processes=8)
endtime=datetime.datetime.now()
print "%5.3f"%(endtime-starttime).seconds

print "\n"

starttime=datetime.datetime.now()
for c in processing_list:
	myfunc2(c)
endtime=datetime.datetime.now()
print "%5.3f"%(endtime-starttime).seconds

#easy_mp.pool_map(fixed_func=lambda n: myfunc(n), args=renren, processes=8)
#easy_mp.pool_map(fixed_func=lambda n: myfunc2(n), args=processing_list, processes=8)

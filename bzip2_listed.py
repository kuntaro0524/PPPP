import os,sys
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp
import glob
import datetime

def bzipfunc(targetfile):
	command="bzip2 %s"%targetfile.strip()
	os.system(command)
	print "Bzipping %s has been finished"%targetfile.strip()

filelist=open(sys.argv[1],"r").readlines()

#starttime=datetime.datetime.now()
easy_mp.pool_map(fixed_func=lambda n: bzipfunc(n), args=filelist, processes=8)

import sys,os,math,numpy
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/10.Zoo/Libs/")
import glob
import MyException
import time
import datetime
import CrystalSpot
import AnaShika
import CrystalSpot
import HD5CBF
import DirectoryProc
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp


if __name__=="__main__":

	# directory list where '_spotfinder' exists
	logfile=open("result.txt","w")

	# Spot finder list
	dp=DirectoryProc.DirectoryProc(".")
        smr_list=dp.findTargetFile("summary.dat")

	for i in smr_list:
		smpath=os.path.abspath(i)
		uedir="%s/../../"%smpath
		master_file_path=os.path.abspath(uedir)
		#print master_file_path
		master_file=glob.glob("%s/*master.h5"%master_file_path)[0]
		paths=master_file_path.split('/')
		outprefix=paths[-2]
		search_prefix="%s_"%outprefix

		spotfinder_dir=os.path.abspath("%s/../"%smpath)
		print spotfinder_dir,outprefix,search_prefix

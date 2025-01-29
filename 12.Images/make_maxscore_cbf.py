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

	# CBF output files
	cbf_dir="./CBFs"

        # directory list where '_spotfinder' exists
        logfile=open("result.txt","w")

	results_list=[]

        # Spot finder list
        dp=DirectoryProc.DirectoryProc(".")
        smr_list=dp.findTargetFile("summary.dat")

	# DUMMY VALUES
	cxyz=(0.7379,   -11.5623,    -0.0629)
	phi=0.0
	nimages_all=10
	completeness=0.01

        for i in smr_list:
                smpath=os.path.abspath(i)
                uedir="%s/../../"%smpath
                master_file_path=os.path.abspath(uedir)
                #print master_file_path
                master_file=glob.glob("%s/*master.h5"%master_file_path)[0]
                paths=master_file_path.split('/')
                outprefix=paths[-2]
                anaprefix="%s_"%outprefix

                spotfinder_dir=os.path.abspath("%s/../"%smpath)
                #print spotfinder_dir,outprefix,search_prefix

		ashika=AnaShika.AnaShika(spotfinder_dir,cxyz,phi)

		ashika.readSummary(anaprefix,nimages_all,completeness,timeout=120)
		max_image,max_score=ashika.getMaxScoreImageNum(anaprefix,kind="n_spots")

		print "MAX=",max_score

                # outputname
                absout=os.path.abspath(cbf_dir)
                outputname="%s/%s_%05d.cbf"%(absout,outprefix,max_image)

		# Absolute path
		logfile.write("%s %5d %8.2f %s\n"%(master_file,max_image,max_score,outputname))
                results_list.append((master_file,max_image,outputname,max_score))

		# Score sorting

	results_list.sort(key=lambda x:int(x[3]),reverse=True)
	params_list=[]
	for r in results_list:
		master_file,max_image,outputname,max_score=r
                params_list.append((master_file,max_image,max_image,outputname))

logfile.close()

h2c=HD5CBF.HD5CBF()
easy_mp.pool_map(fixed_func=lambda n: h2c.merge(n), args=params_list, processes=8)

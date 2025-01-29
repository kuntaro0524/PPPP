import sys,os,math,numpy
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/10.Zoo/Libs/")
import MyException
import time
import datetime
import CrystalSpot
import AnaShika
import CrystalSpot
import HD5CBF
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp


if __name__=="__main__":

	# directory list where '_spotfinder' exists
	pin_list=open(sys.argv[1],"r").readlines()

	# CBF output directory
	cbf_dir="./CBFs/"

# TEMPLATE
#./hirota-HIR0001-07/scan
#./hirota-HIR0001-14/scan
#./hirota-HIR0002-13/scan

#./hirota-HIR0001-03/scan/vscan

	results_list=[]

	for pin in pin_list:
		pin=pin.strip()

		if pin.rfind("vscan")!=-1:
			prefix="vscan_"
			tmp1=pin.replace(".","").split('/')
			outprefix=tmp1[1]+"_vert"
		else:
			#print "PING=",pin
			# Extract prefix from the line
			tmp1=pin.replace(".","").split('/')
			
			prefix0=tmp1[1].strip()
			prefix=prefix0+"_"
			outprefix=prefix0
	
		dire_spotfinder="%s/_spotfinder/"%pin
		dire_master="%s/"%pin
	
		cxyz=(0.7379,   -11.5623,    -0.0629)
		phi=0.0
	
		#print dire_spotfinder
		ashika=AnaShika.AnaShika(dire_spotfinder,cxyz,phi)
	
		nimages_all=10
		completeness=0.01
	
		ashika.readSummary(prefix,nimages_all,completeness,timeout=120)
		max_image,max_score=ashika.getMaxScoreImageNum(prefix,kind="n_spots")

		# Crystl finding
        	#crystals=ashika.findCrystals(prefix0,kind="n_spots",dist_thresh=0.01001,score_thresh=5)
		#print len(crystals)

		# outputname
		absout=os.path.abspath(cbf_dir)
		outputname="%s/%s_%05d.cbf"%(absout,outprefix,max_image)

		# Absolute path
		abspath=os.path.abspath(dire_master)
		masterfile="%s/%smaster.h5"%(abspath,prefix)
		results_list.append((masterfile,max_image,max_image,outputname))

h2c=HD5CBF.HD5CBF()
easy_mp.pool_map(fixed_func=lambda n: h2c.merge(n), args=results_list, processes=8)

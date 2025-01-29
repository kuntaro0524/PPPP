import sys,os,math
import socket
from Count import *
from MyException import *
from File import *
import Device

# Make sure pin photodiode is swithced to No. 3 signal cable

if __name__=="__main__":
	host = '172.24.242.41'
	dev=Device.Device(host)
	dev.init()

	tune_log=open("test.log","w")

	f=File("./")

	fname="%03d_mirror_half.log"%f.getNewIdx3()
	ofile=open(fname,"w")

	# Ensure if a shutter is closed.
	dev.closeAllShutter()
	
	# Move detectory-y and diffractometer stage to Original Y position
        #dev.finishMirrorHalf()

	# Set Attenuator to 600um to scan diffractometer stage
	dev.setAttThick(600.0)

	# preparation of diffractometer scan
	dev.prepScanCoaxCam()

	# Get current YZ positions of diffractometer
	curr_sty=dev.stage.getYmm()
	curr_stz=dev.stage.getZmm()

	tune_log.write("Sty=%12.5f Stz=%12.5f\n"%(curr_sty,curr_stz))

	# Scan
	fwhm_ymm,center_ymm=dev.stage.scanY("MOVE")
	fwhm_zmm,center_zmm=dev.stage.scanZ("MOVE")

	tune_log.write("Sty=%12.5f Stz=%12.5f\n"%(center_ymm,center_zmm))
	tune_log.write("dameter Sty=%12.5f Stz=%12.5f\n"%(fwhm_ymm,fwhm_zmm))

import sys,os,math
import socket
from Mirror import *
from MirrorTuneUnit import *
from Count import *
from MyException import *
from File import *
import Device

# Make sure pin photodiode is swithced to No. 3 signal cable

if __name__=="__main__":
	host = '172.24.242.41'
	dev=Device.Device(host)
	dev.init()

	f=File("./")

	fname="%03d_mirror_half.log"%f.getNewIdx3()
	ofile=open(fname,"w")

	####### TCS scan
    	cnt_ch1=0 #0
    	cnt_ch2=3 #1

	# TCS scan parameters
    	scan_apert=0.05
    	scan_another_apert=0.5
    	scan_start=1.4
    	scan_end=2.2
    	scan_step=0.05
    	scan_time=0.2

	# Energy 
    	energy=12.3984
	
	# Energy change
    	dev.mono.changeE(energy)

	# Gap 
    	dev.id.moveE(energy)

	# Dtheta1 tune
    	prefix="%03d"%f.getNewIdx3()
    	dev.mono.scanDt1PeakConfig(prefix,"DTSCAN_FULLOPEN",dev.tcs)

	# current TCS position
	tcsv_before,tcsh_before=dev.tcs.getPosition()

	# TCS vertical scan
    	prefix="%03d"%f.getNewIdx3()
    	prefix="%03d_tcs"%f.getNewIdx3()
    	vfwhm,vcenter1=dev.tcs.scanVrel(prefix,0.05,0.50,1.5,scan_step,cnt_ch1,cnt_ch2,scan_time)
    	hfwhm,hcenter1=dev.tcs.scanHrel(prefix,0.50,0.05,1.5,scan_step,cnt_ch1,cnt_ch2,scan_time)
    	dev.tcs.setApert(0.1,0.1)
	
	# count IC
	pin_value,ic_value=dev.countPin(pin_ch=3)

	tcsv_after,tcsh_after=dev.tcs.getPosition()
	diffv=tcsv_after-tcsv_before
	diffh=tcsh_after-tcsh_before
	ofile.write("TCS scan after %8.5f %8.5f \n(diffv,diffh)=(%8.5f,%8.5f)\n"% \
		(vcenter1,hcenter1,diffv,diffh))

	# Ensure
	dummy_input = raw_input('Please ensure the PIN No.3 is connected to PicoAmp [ENTER]')

	# Preparation of mirror half
	dev.prepMirrorHalf()

	# D theta1 tune before mirror positional tuning
        dev.tuneDt1("./")

	# Slit1 open
	dev.slit1.openV()

	# Initial position
	init_y,init_z=dev.mirror.getYZ()
	print"Initial position (HFM_Y,VFM_Z)=(%7d,%7d)"%(init_y,init_z)
	ofile.write("Initial mirror position (HFM_Y,VFM_Z)=(%7d,%7d)\n"%(init_y,init_z))

	# Mirror Evacuation (3 mm)
	dev.mirror.evacVFM_z()
	dev.mirror.evacHFM_y()

	# Current position
	curr_y,curr_z=dev.mirror.getYZ()
	print "Current position (HFM_Y,VFM_Z)=(%7d,%7d)\n"%(curr_y,curr_z)

	# Direct beam intensity 
	dev.mtu.monDirPIN()
	i_dir,dummy=dev.countPin()
	ofile.write("Direct intensity:%5d\n"%i_dir)

	# VFM tune
	dev.mtu.monVFMPIN()
	dev.mirror.tuneVFM_z(init_z)
	i_vfm,dummy=dev.countPin()
	ofile.write("VMF intensity:%5d\n"%i_vfm)
	print "VFM scan finished"

	# HFM tune
	dev.mtu.monBothPIN()
	dev.mirror.tuneHFM_y(init_y)
	i_both,dummy=dev.countPin()
	ofile.write("Both intensity:%5d\n"%i_both)
	print "HFM scan finished"

	# Transmission calculation
	# Direct to vertical focusing
	trans_v=float(i_vfm)/float(i_dir)
	trans_h=float(i_both)/float(i_vfm)
	trans_both=float(i_both)/float(i_dir)
	ofile.write("Trans V: %8.5f H: %8.5f BOTH: %8.5f\n"%(trans_v,trans_h,trans_both))

	# Final position
	final_y,final_z=dev.mirror.getYZ()
	print"Final position (HFM_Y,VFM_Z)=(%7d,%7d)"%(final_y,final_z)
	ofile.write("Final position (HFM_Y,VFM_Z)=(%7d,%7d)\n"%(final_y,final_z))

	diff_y=final_y-init_y
	diff_z=final_z-init_z
	diff_hfmy_um=diff_y/10.0
	diff_vfmz_um=diff_z/10.0
	ofile.write("Diff (dy,dz)=(%7d,%7d)\n"%(diff_y,diff_z))
	ofile.write("Diff (dy,dz)=(%8.5f,%8.5f)[um]\n"%(diff_hfmy_um,diff_vfmz_um))

	# Translate both mirrors for matching relative configuration
	# VFM y should be moved by 'diff_y' 
	curr_vfm_y=dev.mirror.getVFM_y()
	final_vfm_y=curr_vfm_y+diff_y
	dev.mirror.setVFM_y(final_vfm_y)

	curr_hfm_z=dev.mirror.getHFM_z()
	final_hfm_z=curr_hfm_z+diff_z
	dev.mirror.setHFM_z(final_hfm_z)
	ofile.write("Matching relativ position of HFM and VFM\n"
	ofile.write("Moving VFM-Y from %7d to %7d\n"%(curr_vfm_y,final_vfm_y))
	ofile.write("Moving HFM-Z from %7d to %7d\n"%(curr_hfm_z,final_hfm_z))
	ofile.close()

	# Slit1 open
	dev.closeAllShutter()

	# Waiting for switching the PIN
	dummy_input = raw_input('Please ensure the PIN No.6 is connected to PicoAmp[ENTER]')

	# Making log file for stage tuning
	fname="%03d_stagetune.log"%f.getNewIdx3()
	ofile=open(fname,"w")
	
	# Move detectory-y and diffractometer stage to Original Y position
        dev.finishMirrorHalf()

	# Set Attenuator to 600um to scan diffractometer stage
	dev.setAttThick(600.0)

	# preparation of diffractometer scan
	dev.prepScanCoaxCam()

	# Get current YZ positions of diffractometer
	curr_sty=dev.stage.getYmm()
	curr_stz=dev.stage.getZmm()

	ofile.write("Previous Sty=%12.5f Stz=%12.5f\n"%(curr_sty,curr_stz))

	# Scan
	fwhm_ymm,center_ymm=dev.stage.scanY("MOVE")
	fwhm_zmm,center_zmm=dev.stage.scanZ("MOVE")

	# dY, dZ
	diffyum=(fwhm_ymm-curr_sty)*1000.0
	diffzum=(fwhm_zmm-curr_stz)*1000.0

	ofile.write("Current position Sty=%12.5f Stz=%12.5f\n"%(center_ymm,center_zmm))
	ofile.write("Current diameter Sty=%12.5f Stz=%12.5f\n"%(fwhm_ymm,fwhm_zmm))
	ofile.write("Diff.   position Dy= %12.5f[um] Dz =%12.5f[um]\n"%(diffyum,diffzum))

	# Make sure 
	ofile.close()

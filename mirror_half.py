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

	# Preparation of mirror half
	dev.prepMirrorHalf()

	# D theta1 tune before mirror positional tuning
        dev.tuneDt1("./")

	# Slit1 open
	dev.slit1.openV()

	# Initial position
	init_y,init_z=dev.mirror.getYZ()
	print"Initial position (Y,Z)=(%7d,%7d)"%(init_y,init_z)

	ofile.write("Initial position (Y,Z)=(%7d,%7d)\n"%(init_y,init_z))

	# Mirror Evacuation (3 mm)
	dev.mirror.evacVFM_z()
	dev.mirror.evacHFM_y()

	# Current position
	curr_y,curr_z=dev.mirror.getYZ()
	print "Current position (Y,Z)=(%7d,%7d)\n"%(curr_y,curr_z)

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
	print"Final position (Y,Z)=(%7d,%7d)"%(final_y,final_z)
	ofile.write("Final position (Y,Z)=(%7d,%7d)\n"%(final_y,final_z))

	diff_y=final_y-init_y
	diff_z=final_z-init_z
	ofile.write("Diff (dy,dz)=(%7d,%7d)\n"%(diff_y,diff_z))

	# Translate both mirrors for matching relative configuration
	# VFM y should be moved by 'diff_y' 
	curr_vfm_y=dev.mirror.getVFM_y()
	final_vfm_y=curr_vfm_y+diff_y
	dev.mirror.setVFM_y(final_vfm_y)

	curr_hfm_z=dev.mirror.getHFM_z()
	final_hfm_z=curr_hfm_z+diff_z
	dev.mirror.setHFM_z(final_hfm_z)
	print"Matching relative position of HFM and VFM"
	ofile.write("Moving VFM-Y from %7d to %7d\n"%(curr_vfm_y,final_vfm_y))
	ofile.write("Moving HFM-Z from %7d to %7d\n"%(curr_hfm_z,final_hfm_z))

	# Slit1 open
	dev.closeAllShutter()

	# Make sure 
	ofile.close()

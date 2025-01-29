import os,sys,math
import numpy

photon_flux=3E12
beam_area=1 # um^2

print "Photon flux=",photon_flux,"[phs/s]"
print "Beam area=",beam_area,"[um^2]"

dose_when_fixed_point=photon_flux/beam_area/6E10*20.0
print dose_when_fixed_point," MGy"

for step in numpy.arange(1,11,1):
	for speed in numpy.arange(1,52,2):
		print "STEP=%6.1f [um] SPEED=%3d"%(step,speed)
		scan_speed=speed #Hz

		# Goniometer translation speed
		g_speed=step*scan_speed # um/sec

		# Crystal size
		c_size=1.0
		time=c_size/g_speed
	
		print "ExpTime(1um cry)=%8.4f"%time,
		dose_for_each_crystal=dose_when_fixed_point*time
		print "Dose=%5.1f[MGy]"%dose_for_each_crystal

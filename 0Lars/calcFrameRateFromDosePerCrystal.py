import os,sys,math

phis=float(sys.argv[1])
phie=float(sys.argv[2])
dphi=float(sys.argv[3])

vec_length=float(sys.argv[4])
aimed_dose=float(sys.argv[5])

print "PROGRAM PHISTART PHIEND DPHI VECTOR_LENGTH AIMED_DOSE"

# calculation start
# Dose for 2x2 beam @ 10.05 keV
dps=231 # MGy/s

# Entire rotation range
phi_tot=phie-phis

# number of frames
nframe=int(phi_tot/dphi)
print "# of frames=",nframe

# Input dose -> exposure time
cry_size=2.0

# Exposure for each crystal
t_cry=aimed_dose/dps #[sec]

# Translation speed
ts=cry_size/t_cry

# Total exposure time
t_tot=vec_length/ts

# Frame rate
frame_rate=float(nframe)/t_tot

print "Frame rate=%5.2f [Hz]  Exposure time for each frame=%5.2f [sec]"%(frame_rate,1.0/frame_rate)

# Rotation speed
rs=phi_tot/t_tot
print "Rotation speed = %5.2f [deg/sec]"%rs

# Goniometer translation speed
ts=vec_length/t_tot
print "Goniometer speed: %5.2f [um/sec]"%ts

# Rotation/crystal
phi_cry=rs*t_cry

# dose for each crystal
dpc=dps*t_cry

# Total experimental time
print "Total exposure in the scan\t: %5.2f [sec]"%t_tot


print "Exposure time\t: %5.2f [sec/crystal]"%t_cry
print "Dose for each crystal \t:%5.2f [MGy]"%dpc
print "Rotation/crystal \t:%5.2f [deg]"%phi_cry


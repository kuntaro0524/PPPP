import sys,os
import Gauss
import numpy

if __name__=="__main__":
	g=Gauss.Gauss(1.0,0)

	if len(sys.argv) != 4:
		print "PROGRAM BEAMSIZE_FWHM[um] CRYSIZE[um] FRAMERATE[Hz]"
		sys.exit(1)

	# beam size
	beamsize_fwhm=float(sys.argv[1]) #[um]
	crysize=float(sys.argv[2]) # [um]
	frame_rate=float(sys.argv[3]) # Unit[Hz]

	###################################################
	# Experimental conditions
	###################################################
	vector_length=crysize #[um] = crystal length
	osc_range=90.0 #[deg]  total oscillation range
	osc_width=1.0 #[deg] oscillation width

	###################################################
	# Further calculation
	###################################################
	total_num_frames=int(osc_range/osc_width)
	total_time_for_dataset=float(total_num_frames)/frame_rate #[sec]
	gonio_speed=vector_length/total_time_for_dataset #[um/sec]

########## Along time axis
	resolution=1000.0
	start_time=0.0
	end_time=total_time_for_dataset
	capture_rate=end_time/resolution # simulation rate of time
	print "# total time :",total_time_for_dataset
	print "# gonio speed:",gonio_speed

##### PLRD function setting #############
	g.setSigmaFromFWHM(beamsize_fwhm) # FWHM of utilized beam should be adopted
	g.setTotalArea(1.0) # integrated area is 1.0

##### Virtual crystal
	cry_length_width=1.00 #[um]
	cry_length_array_num=int(vector_length/cry_length_width)

	vcrystal=[]
	for i in numpy.arange(0,cry_length_array_num):
		vcrystal.append(0.0)

	#print len(vcrystal)
	
##### Time loop ######
#### View all of gaussians on the virtual crystals 
#### Each gauss distribution is shown with "capture_rate" [sec]
	for time in numpy.arange(start_time,end_time,capture_rate):
		# Translation during in "time_for_integ_width"
		mu_from_origin=gonio_speed*time
		#print " ",mu_from_origin
		#print ""
		
		# Gauss function
		g.setMu(mu_from_origin)
		# Simply display a current gauss distribution 
		x,y=g.getGauss2()

		# Accumulate a current gaussian distribution to 
		# the virtual crystal above
		for i in numpy.arange(0,cry_length_array_num):
			range_start=float(i)*cry_length_width
			range_end=range_start+cry_length_width
			integrated_area=g.integrate2(range_start,range_end,cry_length_width)
			print "VCRY: %12.5f %12.5f %12.5f"%(range_start,range_end,integrated_area)
			vcrystal[i]+=integrated_area

	for i in numpy.arange(0,cry_length_array_num):
		range_start=float(i)*cry_length_width
		print "PLT: %12.5f %12.5f"%(range_start,vcrystal[i])

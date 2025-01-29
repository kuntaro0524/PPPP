from GonioVec import *
from AttFactor import *

# 2014/05/28 K.Hirata
# For multi-crystal data collection
# 2014/10/23 Modified for Readout option for MX225HE

class MultiCrystalHE:
	def __init__(self):
		self.dir="~/"
		self.dataname="test"
		self.offset=0
		self.exptime=1.0
		self.wavelength=1.0
		self.startphi=0.0
		self.endphi=90.0
		self.stepphi=1.0
		self.cl=200.0
		self.att_index=0
		self.isAdvanced=0
		self.npoints=1
		self.astep=0
		self.ainterval=1
		self.scan_interval=1
		self.beamsize_idx=0
		self.x1=1.0
		self.y1=1.0
		self.z1=1.0
		self.x2=1.0
		self.y2=1.0
		self.z2=1.0
		self.isSlow=False
		self.isReadBeamSize=False

	def setDir(self,dir):
		self.dir=dir
	def setDataName(self,dataname):
		self.dataname=dataname
	def setOffset(self,offset):
		self.offset=offset
	def setExpTime(self,exptime):
		self.exptime=exptime
	def setWL(self,wavelength):
		self.wavelength=wavelength
	def setScanCondition(self,startphi,endphi,stepphi):
		self.startphi=startphi
		self.endphi=endphi
		self.stepphi=stepphi
	def setCameraLength(self,cl):
		self.cl=cl
	def setAttIdx(self,index):
		self.att_index=index
	def setAttThickness(self,thickness):
		# thickness [um]
        	self.att_index=self.getAttIndex(thickness)
	def setScanInt(self,scan_interval):
		self.scan_interval=scan_interval
	def setSlowOn(self):
		self.isSlow=True
	def stepAdvanced(self,startvec,endvec,astep,ainterval,startphi,stepphi,interval):
		self.astep=astep/1000.0 # [mm]
		self.ainterval=ainterval
		self.scan_interval=interval
		self.setAdvancedVector(startvec,endvec)
		# calculation of vector length
		gv=GonioVec()
		lvec=gv.makeLineVec(startvec,endvec)
		length=gv.calcDist(lvec)*1000.0
		print length
		# npoints
		self.npoints=int(length/astep)
		self.isAdvanced=1
		# rotation
		self.stepphi=stepphi
		self.startphi=startphi
		# end phi
		self.endphi=self.startphi+self.stepphi*self.npoints*ainterval*self.scan_interval

	def setAdvanced(self,npoints,astep,ainterval):
		self.npoints=npoints
		self.astep=astep
		self.ainterval=ainterval
		self.isAdvanced=1

	def setAdvancedVector(self,start,end):
		self.x1=float(start[0])
		self.y1=float(start[1])
		self.z1=float(start[2])
		self.x2=float(end[0])
		self.y2=float(end[1])
		self.z2=float(end[2])

	def make(self,sch_file,info_list):
		# Firstly remove the 'sch_file'
		command="/bin/rm -f %s"%sch_file
		os.system(command)
		ofile=open(sch_file,"w")

		dataidx=0
		for info in info_list:
			# Data prefix
			dataidx+=1
			prefix,x,y,z=info
			self.dataname="%s_%03d"%(prefix,dataidx)

			ofile.write("Job ID: 0\n")
			ofile.write("Status: 0 # -1:Undefined  0:Waiting  1:Processing  2:Success  3:Killed  4:Failure  5:Stopped  6:Skip  7:Pause\n")
			ofile.write("Job Mode: 0 # 0:Check  1:XAFS  2:Single  3:Multi\n")
			ofile.write("Crystal ID: Unknown\n")
			ofile.write("Tray ID: Not Used\n")
			ofile.write("Well ID: 0 # 0:Not Used\n")
			ofile.write("Cleaning after mount: 0 # 0:no clean, 1:clean\n")
			ofile.write("Not dismount: 0 # 0:dismount, 1:not dismount\n")
			ofile.write("Data Directory: %s/\n"%self.dir)
			ofile.write("Sample Name: %s\n"%self.dataname)
			ofile.write("Serial Offset: %5d\n"%self.offset)
			ofile.write("Number of Wavelengths: 1\n")
			ofile.write("Exposure Time: %8.2f 1.000000 1.000000 1.000000 # [sec]\n"%self.exptime)
			ofile.write("Direct XY: 2000.000000 2000.000000 # [pixel]\n")
			ofile.write("Wavelength: %8.4f 1.020000 1.040000 1.060000 # [Angstrom]\n"%self.wavelength)
			ofile.write("Centering: 3 # 0:Database  1:Manual  2:Auto  3:None\n")
			ofile.write("Detector: 0 # 0:CCD  1:IP\n")
			ofile.write("Scan Condition: %8.2f %8.2f %8.2f  # from to step [deg]\n"%(self.startphi,self.endphi,self.stepphi))
			ofile.write("Scan interval: 1 # [points]\n")
			ofile.write("Wedge number: 1  # [points]\n")
			ofile.write("Wedged MAD: 1  #0: No   1:Yes\n")
			ofile.write("Start Image Number: 1\n")
			ofile.write("Goniometer: 0.00000 0.00000 0.00000 0.00000 0.00000 #Phi Kappa [deg], X Y Z [mm]\n")
			ofile.write("CCD 2theta: 0.000000  # [deg]\n")
			ofile.write("Detector offset: 0.0 0.0  # [mm] Ver. Hor.\n")
			ofile.write("Camera Length: %8.3f  # [mm]\n"%self.cl)
			#ofile.write("Beamstop position: 20.000000  # [mm]\n")
			ofile.write("IP read mode: 1  # 0:Single  1:Twin\n")
			#ofile.write("DIP readout diameter: 400.000000  # [mm]\n")
			ofile.write("CMOS frame rate: 3.000000  # [frame/s]\n")
			ofile.write("CCD Binning: 2  # 1:1x1  2:2x2\n")

			# For MX225HE setting
			if self.isSlow==True:
				ofile.write("CCD Adc: 0  # 0:Normal  1:High gain 2:Low noise 3:High dynamic\n")
			else :
				ofile.write("CCD Adc: 1  # 0:Normal  1:High gain 2:Low noise 3:High dynamic\n")
	
			ofile.write("CCD Transform: 1  # 0:None  1:Do\n")
			ofile.write("CCD Dark: 1  # 0:None  1:Measure\n")
			ofile.write("CCD Trigger: 0  # 0:No  1:Yes\n")
			ofile.write("CCD Dezinger: 0  # 0:No  1:Yes\n")
			ofile.write("CCD Subtract: 1  # 0:No  1:Yes\n")
			ofile.write("CCD Thumbnail: 0  # 0:No  1:Yes\n")
			ofile.write("CCD Data Format: 0  # 0:d*DTRK  1:RAXIS\n")
			ofile.write("Oscillation delay: 100.000000  # [msec]\n")
			ofile.write("Anomalous Nuclei: Mn  # Mn-K\n")
			ofile.write("XAFS Mode: 0  # 0:Final  1:Fine  2:Coarse  3:Manual\n")
			ofile.write("Attenuator: %5d\n"%self.att_index)
			ofile.write("XAFS Condition: 1.891430 1.901430 0.000100  # from to step [A]\n")
			ofile.write("XAFS Count time: 1.000000  # [sec]\n")
			ofile.write("XAFS Wait time: 30  # [msec]\n")
			ofile.write("Transfer HTPFDB: 0  # 0:No, 1:Yes\n")
			ofile.write("Number of Save PPM: 0\n")
			ofile.write("Number of Load PPM: 0\n")
			ofile.write("PPM save directory: /tmp\n")
			ofile.write("PPM load directory: /tmp\n")
			ofile.write("Comment:  \n")
			ofile.write("Advanced mode: 2 # 0: none, 1: vector centering, 2: multiple centering\n")
			ofile.write("Advanced vector centering type: 1 # 0: set step, 1: auto step, 2: gradual move\n")
			ofile.write("Advanced npoint: 2 # [mm]\n")
			ofile.write("Advanced step: 0.000 # [mm]\n")
			ofile.write("Advanced interval: %d # [frames]\n"%self.ainterval)
			ofile.write("Advanced gonio coordinates 1: %12.5f %12.5f %12.5f # id, x, y, z\n"%(x,y,z))
			ofile.write("Advanced gonio coordinates 2: %12.5f %12.5f %12.5f # id, x, y, z\n"%(x,y,z))
			ofile.write("Advanced shift: 0 # flag for shift\n")
			ofile.write("Advanced shift speed: 0.00000 #[mm/sec] \n")

		ofile.close()

	def makeGUI(self,outdir,wavelength,info_list,distance,startphi,endphi,osc_width,att_thick):
		phirange=endphi-startphi
		nframe=int(phirange/osc_width)
		#print nframe

		# exptime T[sec]: meaning
		# Full flux x T[sec] exposure = 20 MGy 
		# Attenuator thickness
		attfac=AttFactor()
		att_idx=attfac.getAttIndexConfig(att_thick)

		self.setCameraLength(distance)
		self.setScanCondition(startphi,endphi,osc_width)
		self.setDir(outdir)
		self.setAttIdx(att_idx)

		# Schedule file
		home_dir=os.environ['HOME']
		ofile="%s/ike.sch"%home_dir
		self.make(ofile,info_list)

        def getAttIndex(self,t):
		attfac=AttFactor()
		att_idx=attfac.getAttIndexConfig(t)
		return att_idx

#_beam_size_begin:
#_label: [h 1.00 x  v 10.00 um]
#_outline: [rectangle 0.0010 0.0100 0.0 0.0 ]
#_object_parameter: tc1_slit_1_width 0.040 mm
#_object_parameter: tc1_slit_1_height 0.5 mm
#_flux_factor: 1.000
#_beam_size_end:

if __name__=="__main__":
	t=MultiCrystal()

	if len(sys.argv)!=7:
		print len(sys.argv)
		print "Usage: PROG GLISTFILE MIDPHI OSCWIDTH NFRAMES DISTANCE[mm] EXPOSURE_20MGy[sec]"
		sys.exit(1)

	# Oscillation condition from command line
	mid_phi=float(sys.argv[2])
	osc_width=float(sys.argv[3])
	nframe=int(sys.argv[4])
	total_range=osc_width*nframe

	# Distance
	dist=float(sys.argv[5])
	t.setCameraLength(dist)

	# Exposure time to read Henderson limit
	exptime=float(sys.argv[6])

	osc_katagawa=total_range/2.0
	#print osc_katagawa
	start_phi=mid_phi-osc_katagawa
	end_phi=mid_phi+osc_katagawa
	#print start_phi,end_phi

	print "Center Oscillation=%8.2f"%mid_phi
	print "Oscillation width =%8.2f"%osc_width
	print "# Number of frames=%8d"%nframe
	print "Total oscillation =%8.2f"%total_range
	print "Start:%8.2f END:%8.2f"%(start_phi,end_phi)
	
	t.setScanCondition(start_phi,end_phi,osc_width)

	## Read gonio list
	lines=open(sys.argv[1],"r").readlines()

	infolist=[]
	for line in lines:
		cols=line.split()
		if len(cols)==5:
			com,x,y,z=cols[0],float(cols[1]),float(cols[2]),float(cols[3])
			list="multi",x,y,z
			infolist.append(list)
		else:
			x,y,z=cols[0],float(cols[1]),float(cols[2])
			list="multi",x,y,z
			infolist.append(list)

	dir=os.path.abspath("./")
	t.setDir(dir)

	# Attenuator thickness
	attfac=AttFactor()

	best_transmission=exptime/nframe
	best_thick=attfac.getBestAtt(1.0,best_transmission)
	print "Suggested Al thickness = %8.1f[um]"%best_thick

	att_idx=attfac.getAttIndexConfig(best_thick)
	t.setAttIdx(att_idx)

	home_dir=os.environ['HOME']
	ofile="%s/yatta.sch"%home_dir
	t.make(ofile,infolist)

class ScheduleBSS:

	def __init__(self):
		print "init"
		self.dir="~/"
		self.dataname="test"
		self.offset=1
		self.exptime=1.0
		self.wavelength=1.0
		self.startphi=0.0
		self.endphi=90.0
		self.stepphi=1.0
		self.cl=200.0
		self.att_index=0
		self.isAdvanced=0
		self.npoints=0
		self.astep=0
		self.ainterval=0
		self.x1=1.0
		self.y1=1.0
		self.z1=1.0
		self.x2=1.0
		self.y2=1.0
		self.z2=1.0

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

	def setAdvanced(self,npoints,astep):
		self.npoints=npoints
		self.astep=astep
		self.isAdvanced=1

	def setAdvancedVector(self,start,end):
		self.x1=float(start[0])
		self.y1=float(start[1])
		self.z1=float(start[2])
		self.x2=float(end[0])
		self.y2=float(end[1])
		self.z2=float(end[2])

	def make(self,sch_file):
		ofile=open(sch_file,"w")

		ofile.write("Job ID: 0\n")
		ofile.write("Status: 0 # -1:Undefined  0:Waiting  1:Processing  2:Success  3:Killed  4:Failure  5:Stopped  6:Skip  7:Pause\n")
		ofile.write("Job Mode: 0 # 0:Check  1:XAFS  2:Single  3:Multi\n")
		ofile.write("Crystal ID: Unknown\n")
		ofile.write("Tray ID: Not Used\n")
		ofile.write("Well ID: 0 # 0:Not Used\n")
		ofile.write("Cleaning after mount: 0 # 0:no clean, 1:clean\n")
		ofile.write("Not dismount: 0 # 0:dismount, 1:not dismount\n")
		ofile.write("Data Directory: %s\n"%self.dir)
		ofile.write("Sample Name: %s\n"%self.dataname)
		ofile.write("Serial Offset: %5d\n"%self.offset)
		ofile.write("Number of Wavelengths: 1\n")
		ofile.write("Exposure Time: %8.1f 1.000000 1.000000 1.000000 # [sec]\n"%self.exptime)
		ofile.write("Direct XY: 2000.000000 2000.000000 # [pixel]\n")
		ofile.write("Wavelength: %8.4f 1.020000 1.040000 1.060000 # [Angstrom]\n"%self.wavelength)
		ofile.write("Centering: 3 # 0:Database  1:Manual  2:Auto  3:None\n")
		ofile.write("Detector: 0 # 0:CCD  1:IP\n")
		ofile.write("Scan Condition: %8.2f %8.2f %8.2f  # from to step [deg]\n"%(self.startphi,self.endphi,self.stepphi))
		ofile.write("Scan interval: 1  # [points]\n")
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
		ofile.write("CCD Adc: 0  # 0:Slow  1:Fast (ADSC CCD only)\n")
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
		ofile.write("PPM save directory: /isilon/users/target/target/\n")
		ofile.write("PPM load directory: /isilon/users/target/target/\n")
		ofile.write("Comment:  \n")
		ofile.write("Advanced mode: %d # 0: none, 1: vector centering, 2: multiple centering\n"%self.isAdvanced)
		ofile.write("Advanced vector centering type: 1 # 0: set step, 1: auto step, 2: gradual move\n")
		ofile.write("Advanced npoint: %d # [mm]\n"%self.npoints)
		ofile.write("Advanced step: %8.4f # [mm]\n"%self.astep)
		ofile.write("Advanced interval: %d # [frames]\n"%self.ainterval)
		ofile.write("Advanced gonio coordinates 1: %12.5f %12.5f %12.5f # id, x, y, z\n"%(self.x1,self.y1,self.z1))
		ofile.write("Advanced gonio coordinates 2: %12.5f %12.5f %12.5f # id, x, y, z\n"%(self.x2,self.y2,self.z2))

		ofile.close()

if __name__=="__main__":
	t=ScheduleBSS()
	t.make("TEST.SCH")

#from GonioVec import *
import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/10.Zoo/Libs/")
from AttFactor import *

# 2014/05/28 K.Hirata
# For multi-crystal data collection
# 2015/07/02 K.Hirata modified
# For automated data collection
# 2017/12/09 multi crystal job -> One schedule file 
class MultiCrystalZoo:
	def __init__(self):
		self.dir="~/"
		self.prefix="multi"
		self.offset=0
		self.exptime=0.1
		self.wavelength=1.0
		self.startphi=0.0
		self.endphi=90.0
		self.stepphi=1.0
		self.cl=200.0
		self.att_index=0
		self.isAdvanced=0
		self.npoints=1
		self.astep=0
		self.ainterval=1 # Multi-crystal mode this should be always 1
		self.scan_interval=1
		self.beamsize_idx=0
		self.crystal_id="unknown"
		self.x1=1.0
		self.y1=1.0
		self.z1=1.0
		self.x2=1.0
		self.y2=1.0
		self.z2=1.0
		self.isSlow=False
		self.isReadBeamSize=False
		self.isShutterless=False

	def setDir(self,dir):
		self.dir=dir
	def setCrystalID(self,crystal_id):
		self.crystal_id=crystal_id
	def setPrefix(self,prefix):
		self.prefix=prefix
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
	def setShutterlessOn(self):
		self.isShutterless=True

	def setBeamsizeIndex(self,index):
		self.beamsize_idx=index

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

	def makeMulti(self,schedule_file,gonio_list):
		ofile=open(schedule_file,"w")
		strs=self.makeSchStr(gonio_list)
		nfile=0
		for line in strs:
			ofile.write("%s"%line)
		ofile.close()

	def makeSchStr(self,gxyz_list):
		schstr=[]
		idx=1
		for gxyz in gxyz_list:
			# Data prefix
			if len(gxyz_list)!=1:
				prefix="%s-%03d"%(self.prefix,idx)
			else:
				prefix=self.prefix
			if idx>1:
				schstr+=self.makeSchStrEach(prefix,gxyz,det_param=False)
			else:
				schstr+=self.makeSchStrEach(prefix,gxyz,det_param=True)
			idx+=1

		return schstr

	# 170417 implemented for new advanced setting 'multiple crystal'
	# schedule_file: file name
	# gonio_list: goniometer XYZ coordinates
	# ntimes: 1
	# det_param: True for successive data collection
	def makeMultiCrystalAdvanced(self,schedule_file,gonio_list,ntimes,det_param=True):
		i_xyz=1
		schstr=[]

		ofile=open(schedule_file,"w")
                ofile.write("Job ID: 0\n")
                ofile.write("Status: 0 # -1:Undefined  0:Waiting  1:Processing  2:Success  3:Killed  4:Failure  5:Stopped  6:Skip  7:Pause\n")
                ofile.write("Job Mode: 0 # 0:Check  1:XAFS  2:Single  3:Multi\n")
                ofile.write("Crystal ID: %s\n"%self.crystal_id)
                ofile.write("Tray ID: Not Used\n")
                ofile.write("Well ID: 0 # 0:Not Used\n")
                ofile.write("Cleaning after mount: 0 # 0:no clean, 1:clean\n")
                ofile.write("Not dismount: 0 # 0:dismount, 1:not dismount\n")
                ofile.write("Data Directory: %s/\n"%self.dir)
                ofile.write("Sample Name: %s\n"%self.prefix)
                ofile.write("Serial Offset: %5d\n"%self.offset)
                ofile.write("Number of Wavelengths: 1\n")
		ofile.write("File Name Suffix: h5\n")

                # BSS can skip detector setup for shortening Zoo data collection 2016/09/14
                if det_param==True:
                        ofile.write("Detector Setup Level: 10\n")
                else:
                        ofile.write("Detector Setup Level: 0\n")
                # Shutterless measurement
                ofile.write("Shutterless measurement: 1 # 0:no, 1:yes\n")
                ofile.write("Exposure Time: %8.4f 1.000000 1.000000 1.000000 # [sec]\n"%self.exptime)
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
                ofile.write("IP read mode: 1  # 0:Single  1:Twin\n")
                ofile.write("CMOS frame rate: -1.000000  # [frame/s]\n")
                ofile.write("Beam Size: %d\n"%self.beamsize_idx)
                ofile.write("CCD Binning: 1  # 1:1x1  2:2x2\n")
                ofile.write("CCD Adc: 0  # 0:Normal  1:High gain 2:Low noise 3:High dynamic\n")
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
		ofile.write("Advanced mode: 3 # 0: none, 1: vector centering, 2: multiple centering, 3: multi-crystals\n")
		ofile.write("Advanced npoint: 2 # [mm]\n")
    		ofile.write("Advanced step: 0.00000 # [mm]\n")
    		ofile.write("Advanced interval: 1 # [frames]\n")
		for gxyz in gonio_list:
			x,y,z=gxyz
                	ofile.write("Advanced gonio coordinates %d: %12.5f %12.5f %12.5f # id, x, y, z\n"%(i_xyz,x,y,z))
			i_xyz+=1
    		ofile.write("Advanced shift: 0 # flag for shift\n")
    		ofile.write("Advanced shift speed: 0.000000 # [mm/sec]\n")
    		ofile.write("Raster Scan Type: 2 # 0:vertical, 1:horizontal, 2: 2D\n")
    		ofile.write("Raster Vertical Points: 10\n")
    		ofile.write("Raster Horizontal Points: 10\n")
    		ofile.write("Raster Vertical Step: 0.0150 # [mm]\n")
    		ofile.write("Raster Horizontal Step: 0.0100 # [mm]\n")
    		ofile.write("Raster Vertical Center: 0.0000 # [mm]\n")
    		ofile.write("Raster Horizontal Center: 0.0000 # [mm]\n")
    		ofile.write("Raster Rotation Flag: 0 # 0:not rotate, 1:rotate\n")
    		ofile.write("Raster Rotation Range: 0.000 # [deg] rotation range\n")
    		ofile.write("Raster Zig-Zag Flag: 1 # 0: off, 1:on\n")
    		ofile.write("Comment:\n")
		ofile.close()

	def makeMultiMulti(self,schedule_file,gonio_list,ntimes):
		i_xyz=0
		schstr=[]
		for gxyz in gonio_list:
			for i_data in range(0,ntimes):
				# Data prefix
				prefix="%s_%03d_%02d"%(self.prefix,i_xyz,i_data)
				schstr+=self.makeSchStrEach(prefix,gxyz)
			i_xyz+=1

		# Making the schedule file
		ofile=open(schedule_file,"w")
		for line in schstr:
			ofile.write("%s"%line)
		ofile.close()

	def makeSchStrEach(self,prefix,gxyz,det_param=True):
		schstr=[]
		x,y,z=gxyz
                schstr.append("Job ID: 0\n")
                schstr.append("Status: 0 # -1:Undefined  0:Waiting  1:Processing  2:Success  3:Killed  4:Failure  5:Stopped  6:Skip  7:Pause\n")
                schstr.append("Job Mode: 0 # 0:Check  1:XAFS  2:Single  3:Multi\n")
                schstr.append("Crystal ID: %s\n"%self.crystal_id)
                schstr.append("Tray ID: Not Used\n")
                schstr.append("Well ID: 0 # 0:Not Used\n")
                schstr.append("Cleaning after mount: 0 # 0:no clean, 1:clean\n")
                schstr.append("Not dismount: 0 # 0:dismount, 1:not dismount\n")
                schstr.append("Data Directory: %s/\n"%self.dir)
                schstr.append("Sample Name: %s\n"%prefix)
                schstr.append("Serial Offset: %5d\n"%self.offset)
                schstr.append("Number of Wavelengths: 1\n")
		# BSS can skip detector setup for shortening Zoo data collection 2016/09/14
                if det_param==True:
                        schstr.append("Detector Setup Level: 10\n")
                else:
                        schstr.append("Detector Setup Level: 0\n")
		# Shutterless measurement
                if self.isShutterless==True:
                        schstr.append("Shutterless measurement: 1 # 0:no, 1:yes\n")
                else:
                        schstr.append("Shutterless measurement: 0 # 0:no, 1:yes\n")
                schstr.append("Exposure Time: %8.4f 1.000000 1.000000 1.000000 # [sec]\n"%self.exptime)
                schstr.append("Direct XY: 2000.000000 2000.000000 # [pixel]\n")
                schstr.append("Wavelength: %8.4f 1.020000 1.040000 1.060000 # [Angstrom]\n"%self.wavelength)
                schstr.append("Centering: 3 # 0:Database  1:Manual  2:Auto  3:None\n")
                schstr.append("Detector: 0 # 0:CCD  1:IP\n")
                schstr.append("Scan Condition: %8.2f %8.2f %8.2f  # from to step [deg]\n"%(self.startphi,self.endphi,self.stepphi))
                schstr.append("Scan interval: 1 # [points]\n")
                schstr.append("Wedge number: 1  # [points]\n")
                schstr.append("Wedged MAD: 1  #0: No   1:Yes\n")
                schstr.append("Start Image Number: 1\n")
                schstr.append("Goniometer: 0.00000 0.00000 0.00000 0.00000 0.00000 #Phi Kappa [deg], X Y Z [mm]\n")
                schstr.append("CCD 2theta: 0.000000  # [deg]\n")
                schstr.append("Detector offset: 0.0 0.0  # [mm] Ver. Hor.\n")
                schstr.append("Camera Length: %8.3f  # [mm]\n"%self.cl)
                schstr.append("IP read mode: 1  # 0:Single  1:Twin\n")
                schstr.append("CMOS frame rate: -1.000000  # [frame/s]\n")
		schstr.append("Beam Size: %d\n"%self.beamsize_idx)
                schstr.append("CCD Binning: 2  # 1:1x1  2:2x2\n")
                schstr.append("CCD Adc: 0  # 0:Normal  1:High gain 2:Low noise 3:High dynamic\n")
                schstr.append("CCD Transform: 1  # 0:None  1:Do\n")
                schstr.append("CCD Dark: 1  # 0:None  1:Measure\n")
                schstr.append("CCD Trigger: 0  # 0:No  1:Yes\n")
                schstr.append("CCD Dezinger: 0  # 0:No  1:Yes\n")
                schstr.append("CCD Subtract: 1  # 0:No  1:Yes\n")
                schstr.append("CCD Thumbnail: 0  # 0:No  1:Yes\n")
                schstr.append("CCD Data Format: 0  # 0:d*DTRK  1:RAXIS\n")
                schstr.append("Oscillation delay: 100.000000  # [msec]\n")
                schstr.append("Anomalous Nuclei: Mn  # Mn-K\n")
                schstr.append("XAFS Mode: 0  # 0:Final  1:Fine  2:Coarse  3:Manual\n")
                schstr.append("Attenuator: %5d\n"%self.att_index)
                schstr.append("XAFS Condition: 1.891430 1.901430 0.000100  # from to step [A]\n")
                schstr.append("XAFS Count time: 1.000000  # [sec]\n")
                schstr.append("XAFS Wait time: 30  # [msec]\n")
                schstr.append("Transfer HTPFDB: 0  # 0:No, 1:Yes\n")
                schstr.append("Number of Save PPM: 0\n")
                schstr.append("Number of Load PPM: 0\n")
                schstr.append("PPM save directory: /tmp\n")
                schstr.append("PPM load directory: /tmp\n")
                schstr.append("Comment:  \n")
                schstr.append("Advanced mode: 2 # 0: none, 1: vector centering, 2: multiple centering\n")
                schstr.append("Advanced vector centering type: 1 # 0: set step, 1: auto step, 2: gradual move\n")
                schstr.append("Advanced npoint: 2 # [mm]\n")
                schstr.append("Advanced step: 0.000 # [mm]\n")
                schstr.append("Advanced interval: %d # [frames]\n"%self.ainterval)
                schstr.append("Advanced gonio coordinates 1: %12.5f %12.5f %12.5f # id, x, y, z\n"%(x,y,z))
                schstr.append("Advanced gonio coordinates 2: %12.5f %12.5f %12.5f # id, x, y, z\n"%(x,y,z))
                schstr.append("Advanced shift: 0 # flag for shift\n")
                schstr.append("Advanced shift speed: 0.00000 #[mm/sec] \n")

		return schstr

	def makeGUI(self,outdir,wavelength,info_list,distance,startphi,endphi,osc_width,att_thick,beamsize_index):
		phirange=endphi-startphi
		nframe=int(phirange/osc_width)

		# exptime T[sec]: meaning
		# Full flux x T[sec] exposure = 20 MGy 
		# Attenuator thickness
		attfac=AttFactor()
		att_idx=attfac.getAttIndexConfig(att_thick)

		self.setWL(wavelength)
		self.setCameraLength(distance)
		self.setScanCondition(startphi,endphi,osc_width)
		self.setDir(outdir)
		self.setAttIdx(att_idx)
		self.beamsize_idx=beamsize_index

		# making gonio list
		gonio_list=[]
		for info in info_list:
			prefix,xmm,ymm,zmm=info
			gonio_list.append((xmm,ymm,zmm))

		# Making the schedule file
		home_dir=os.environ['HOME']
		ofile="%s/ike.sch"%home_dir
        	self.makeMultiCrystalAdvanced(ofile,gonio_list,ntimes=1)

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

	schedule_file="/isilon/users/target/target/ikeike.sch"
	# format of gonio list
	# RD     0.2762   -11.3427    -0.5062      130.0

	lines=open(sys.argv[1],"r").readlines()
	gonio_list=[]
	for line in lines:
		cols=line.split()
		print cols
		x=float(cols[2])
		y=float(cols[3])
		z=float(cols[4])
		gonio_list.append((x,y,z))

	ntimes=1
	t.setDir("/isilon/users/target/target/Staff/kuntaro/171207/In-Situ/02-03/data/")
	t.setScanCondition(-52.5,-47.5,0.1)
	t.setCameraLength(250.0)
	t.setAttThickness(500)
        t.makeMultiCrystalAdvanced(schedule_file,gonio_list,ntimes)

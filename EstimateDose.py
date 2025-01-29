import sys,os,math

class EstimateDose():
	def __init__(self):
		self.logfile="test.log"
		self.energy=12.3984
		self.vbeam_size_um=10.0
		self.hbeam_size_um=10.0
		self.phosec=2E12
		self.exptime=1.0


	def setLogfile(self,logfile):
		self.logfile=logfile
	
	def setExpTime(self,exp_time):
		self.exptime=exp_time

	def setBeamsize(self,vbeam_um,hbeam_um):
		self.vbeam_size_um=vbeam_um
		self.hbeam_size_um=hbeam_um

	def setPhosec(self,phosec):
		self.phosec=phosec

	def writeCom(self,comfile):
		# beam size should be in 'mm'
		vbeam_mm=self.vbeam_size_um/1000.0
		hbeam_mm=self.hbeam_size_um/1000.0

		comstring="""
raddose << EOF > %s
ENERGY %12.5f
CELL 78 78 36 90 90 90"
NRES 129
NMON 8
SATM Na 1500 CL 1500
SOLVENT 0.38
CRYST 0.5 0.5 0.05
BEAM  %8.4f %8.4f
PHOSEC %8.1e
EXPO %5.1f
IMAGE 1
EOF 
		"""%(self.logfile,self.energy,vbeam_mm,hbeam_mm,self.phosec,self.exptime)
		#print vbeam_mm,hbeam_mm
		f=open(comfile,"w")
		f.write("%s"%comstring)
		f.close()

	def runCom(self,comfile):
		os.system("csh %s"%comfile)
		#os.system("grep image %s"%self.logfile)
		lines=open("%s"%self.logfile).readlines()
		for line in lines:
			if line.rfind("image")!=-1:
				#print line.split()
				return float(line.split()[5])/1E6

	def getDose(self,h_beam_um,v_beam_um,phosec,exp_time,energy=12.3984):
		comname="tttt.com"
		self.setPhosec(phosec)
		self.setExpTime(exp_time)
		self.setBeamsize(v_beam_um,h_beam_um)
		self.energy=energy
		self.writeCom(comname)
		dose=self.runCom(comname)
		return dose

if __name__=="__main__":
	e=EstimateDose()
	#dose_1sec=e.getDose(10,9,7E12,1.0)

	# 160425 K.Hirata 3x3 um , 5x5 um
	#dose_1sec=e.getDose(10,15,1.0E13,1.0)

	# 160509 wl=1.0A 10x15 um
	en=9.95
	dose_1sec=e.getDose(5,5,9.9E10,1.0,energy=en)
	print dose_1sec
	
	# Aimed dose 10~15 MGy
	# For 10 MGy
	exp_10MGy=10.0/dose_1sec

	# For 10 MGy
	exp_15MGy=15.0/dose_1sec


	# Full flux exposure
	required_degree=10.0 #[deg.]
	phi_step=0.5 #[deg.]
	nframes=int(required_degree/phi_step)

	exp_per_frame_10MGy=exp_10MGy/float(nframes)
	exp_per_frame_15MGy=exp_15MGy/float(nframes)

	# Maximum frame rate
	max_frame_rate=20.0 #[Hz]
	min_exp_time=1.0/max_frame_rate

	if min_exp_time > exp_per_frame_10MGy:
		"ERROR 10MGy"
	if min_exp_time > exp_per_frame_15MGy:
		"ERROR 15MGy"

	print "10 MGy: Total= %10.5f [sec] Exp/frame=%5.3f[sec]"%(exp_10MGy, exp_per_frame_10MGy)
	print "15 MGy: Total= %10.5f [sec] Exp/frame=%5.3f[sec]"%(exp_15MGy, exp_per_frame_15MGy)

	

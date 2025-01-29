import sys,os,math
import datetime,time

class BSSlog():
	def __init__(self):
		self.logdir="/isilon/blconfig/bl32xu/log/"
		#self.logdir="/isilon/BL32XU/BLsoft/PPPP/10.Zoo/ZooConfig/log/"
		self.now=datetime.datetime.now()
		self.strs=[]
		self.isRead=False

		# number of raster scan
		self.n_raster=0
		self.n_raster_images=0
		self.n_datasets=0

	def setDate(self,year,month,date):
		timstr="%04d%02d%02d"%(year,month,date)
                self.now=datetime.datetime.strptime(timstr,'%Y%m%d')
		self.logname=self.now.strftime("bss_%Y%m%d.log") 

	def setLogFile(self,logname):
		self.logname=logname

	def readLogFile(self):
		self.logname="%s/%s"%(self.logdir,self.logname)
		self.loglines=open(self.logname,"r").readlines()
		self.isRead=True
		return 

	def getNdatasets(self):
		if self.isRead==False: self.readLogFile()
		for line in self.loglines:
			if line.rfind("4D scan from")!=-1:
				self.n_datasets+=1
				#print line
		print self.n_datasets

	def analyzeRaster(self):
		if self.isRead==False: self.readLogFile()
		for line in self.loglines:
			 if line.rfind("JOB Raster scan started.")!=-1:
				self.n_raster+=1
			 if line.rfind("Raster scan status:")!=-1:
				#print line
				cols=line.split()
				if cols[3]!=None:
					col1,col2=cols[3].split('/')
					if int(col1)==int(col2):
						print cols[9],col1
						self.n_raster_images+=int(col1)
				#Raster scan status: 372/961 image acquisition finished. 2016/10/22 [Sat] 00:04:23:352
		print self.logname,"NRASTER=",self.n_raster,"NRASTER_IMAGE=",self.n_raster_images,float(self.n_raster_images)/50.0," sec/day"

	def getMountLog(self):
		self.n_mounts=0

		if self.isRead==False: self.readLogFile()
		search_word="Sample Changer is mounting" 

		# Get time stamps on the SPACE mount
		self.mount_time_list=[]
		for line in self.loglines: 
			if line.rfind(search_word)!=-1:
				self.n_mounts+=1
				cols=line.split()
				# Time stamp is the last column
				ymd=cols[len(cols)-3]
				tim=cols[len(cols)-1]
				tim_cols=tim.split(':')
				recst_tim_str="%s %02d:%02d:%02d"%(ymd,int(tim_cols[0]),int(tim_cols[1]),int(tim_cols[2]))
				print recst_tim_str
				tmp_datetime=datetime.datetime.strptime(recst_tim_str, '%Y/%m/%d %H:%M:%S')
				self.mount_time_list.append(tmp_datetime)
		
		savet=self.mount_time_list[0]
		self.duty_mins=[]
		for mt in self.mount_time_list:
			duty_cycle=(mt-savet).seconds/60.0
			print "Cycle=%5.1f mins"%(duty_cycle)
			self.duty_mins.append(duty_cycle)
			savet=mt

		last_mount=self.mount_time_list[-1]
		curr_time=datetime.datetime.now()
		diff_time=(curr_time-last_mount).seconds/60.0
		cfile=open(".tmp","w")
		if diff_time > 60.0:
			cfile.write("%s Users' experiment should be finished!!\n"%(curr_time))
		else:
			cfile.write("Still working: %s\n"%last_mount)
		cfile.close()
		
		command="nkf -j .tmp | mail -s \"User experiment at BL32XU\" hirata@spring8.or.jp"
		os.system(command)

if __name__=="__main__":
	bsslog=BSSlog()
	#bsslog.setLogFile(sys.argv[1])
	#bsslog.analyzeRaster()
	#bsslog.getNdatasets()
	bsslog.setDate(2017,10,25)
	bsslog.analyzeRaster()
	#bsslog.getMountLog()
	#while(1):
		#bsslog.getMountLog()
		#time.sleep(1800)

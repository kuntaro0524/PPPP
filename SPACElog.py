import sys,os,math
import datetime,numpy

class SPACElog():
	def __init__(self):
		self.root="/isilon/blconfig/bl32xu/space/"
		self.now=datetime.datetime.now()
		self.strs=[]
		self.isRead=False

	def readToday(self):
		self.year=self.now.year
		self.month=self.now.month
		self.day=self.now.day
		print self.day
		self.logname=datetime.datetime.now().strftime("savefile_%m%d.txt") 
		self.logname="%s/%s/%s"%(self.root,self.year,self.logname)
		print self.logname

		self.loglines=open(self.logname,"r").readlines()
		self.isRead=True
		return 

	def getMountLog(self):
		self.n_mounts=0

		if self.isRead==False: self.readToday()
		search_word="I/put/bl_32in_sc_all/mount_"

		#25 23:54:47 I/put/bl_32in_sc_all/mount_2_1_0.000000, sd = 1632
		# Get time stamps on the SPACE mount
		self.mount_time_list=[]
		for line in self.loglines: 
			if line.rfind(search_word)!=-1:
				self.n_mounts+=1
				cols=line.split()
				# Time stamp is the second column
				timstr=cols[1]
				timstr="%04d-%02d-%02d %s"%(self.year,self.month,self.day,timstr)
				tmp_datetime=datetime.datetime.strptime(timstr,'%Y-%m-%d %H:%M:%S')
				self.mount_time_list.append(tmp_datetime)

		if self.n_mounts==0:
			print "No mount sequces"
			return
		
		savet=self.mount_time_list[0]
		self.duty_mins=[]
		for mt in self.mount_time_list:
			duty_cycle=(mt-savet).seconds/60.0
			#print "Cycle=%5.1f mins"%(duty_cycle)
			self.duty_mins.append(duty_cycle)
			savet=mt

		# Average cycle on SPACE mounting
		cfile=open(".splog","w")
		cyc_mins=numpy.array(self.duty_mins)
		nmounts=len(cyc_mins)
		cfile.write("SPACElog: %5d mounts: average %5.1f mins\n"%(nmounts,cyc_mins.mean()))
		#%s Users' experiment should be finished!!\n"%(curr_time,last_mount))

		last_mount=self.mount_time_list[-1]
		curr_time=datetime.datetime.now()
		diff_time=(curr_time-last_mount).seconds/60.0
		if diff_time > 60.0:
			cfile.write("SPACElog: %s Users' experiment should be finished!!\n"%(curr_time,last_mount))
		else:
			cfile.write("SPACElog: Still working: %s\n"%last_mount)
		cfile.close()
		
		command="nkf -j .tmp | mail -s \"User experiment at BL32XU\" hirata@spring8.or.jp"
		#os.system(command)

if __name__=="__main__":
	space_log=SPACElog()
	space_log.readToday()
	space_log.getMountLog()

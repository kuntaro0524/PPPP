import datetime
import time

class Date:

	def __init__(self):
		self.tdy=datetime.datetime.today()
		self.today=datetime.date.today().isoformat()

	def getToday(self):
		print datetime.datetime.now()
		return self.today

	def getTodayDire(self):
		today=self.getToday()
		today=today[2:]
		tmp=today.replace("-","")
		return tmp

	def getTimeDire(self):
		line=str(self.tdy)
		current_time=line.split()[1]

		#print current_time
		icut=current_time.rfind(":")

		return current_time[:icut].replace(":","")

	def getOkutsuTime(self,timestr):
		timestr=timestr[:timestr.rfind(".")]
		tt=datetime.datetime.strptime(timestr,"%Y/%m/%d %H:%M:%S")

		return tt
		#tt=datetime.datetime.today()
		#print tt.year,tt.month,tt.day
		#datestr,timestr=timestr.split()
		#print datestr,timestr
		#ystr,mstr,dstr=datestr.split("/")
		#print "Year:%s"%ystr
		#print "Month:%s"%mstr
		#print "Date:%s"%dstr
		#tt.year=ystr
		#tt.month=mstr
		#tt.day=dstr

	def getDiffSec(self,dtstart,dt1):
		diff=dt1-dtstart
		#print diff.days
		#print diff.seconds

		seconds=diff.days*24*60*60+diff.seconds

		return seconds

if __name__=="__main__":
	#print (tmptime-ppp).seconds
	date=Date()

	#print date.getToday()
	#print date.getTodayDire()
	#print date.getTimeDire()
	print date.getOkutsuTime("2011/06/20 06:57:20.067763")

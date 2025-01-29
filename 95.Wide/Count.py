import sys
import socket
import time
import datetime
import math
import timeit

from Received import *
from File import *
from AnalyzePeak import *

class Count:

	def __init__(self,server,ch1,ch2):
		self.s=server
		self.ch1=ch1+1
		self.ch2=ch2+1
		self.is_count=0

        def __storeCountMsec(self,cnttime):
                strtime=str(cnttime)+"msec"
		#print strtime
                com1="put/bl_32in_st2_counter_1/clear"
                com2="put/bl_32in_st2_counter_1/"+strtime
                com3="get/bl_32in_st2_counter_1/query"

        	# counter clear
                self.s.sendall(com1)
                recbuf=self.s.recv(8000)
                #print "CLEAR: "+recbuf

        	# get counter value
                self.s.sendall(com2)
                self.s.recv(8000)
		time_msec=cnttime/1000.0
                time.sleep(time_msec) # wait
                self.s.sendall(com3)

                recbuf=self.s.recv(8000)
                #print "COUNT:"+recbuf

                # obtain the 3rd column in the returned buffer
                cnt_buf=Received(recbuf).get(3)

		return cnt_buf

        def __storeCount(self,cnttime):
                strtime=str(cnttime)+"sec"
                com1="put/bl_32in_st2_counter_1/clear"
                com2="put/bl_32in_st2_counter_1/"+strtime
                com3="get/bl_32in_st2_counter_1/query"

        	# counter clear
                self.s.sendall(com1)
                recbuf=self.s.recv(8000)
                #print "CLEAR: "+recbuf

        	# get counter value
                self.s.sendall(com2)
                self.s.recv(8000)
                time.sleep(cnttime) # wait
                self.s.sendall(com3)

                recbuf=self.s.recv(8000)
                #print "COUNT:"+recbuf

                # obtain the 3rd column in the returned buffer
                cnt_buf=Received(recbuf).get(3)

		return cnt_buf

        def getCount(self,time):
		retinfo=self.__storeCount(time)
		#print retinfo
		info_list=retinfo.split('_')

		ch1_value=int(info_list[self.ch1].replace("count",""))
		ch2_value=int(info_list[self.ch2].replace("count",""))

		rtn_list=[ch1_value,ch2_value]

                return rtn_list

        def getCountMsec(self,time):
		retinfo=self.__storeCountMsec(time)
		#print retinfo
		info_list=retinfo.split('_')

		ch1_value=int(info_list[self.ch1].replace("count",""))
		ch2_value=int(info_list[self.ch2].replace("count",""))

		rtn_list=[ch1_value,ch2_value]

                return rtn_list

	def getPIN(self,gain):
		if self.is_count==0:
			self.getCount(1.0)
    		const_gain=math.pow(10,float(gain-1.0))
    		value=self.current/const_gain
    		str="Count:%8d PIN value: %8.3f uA"%(self.current,value)

		return str

	def calcPIN(self,energy):
		print "calcPIN"
		#flux=(3.6/energy)*(1/(1-exp(absorption)*2.33*0.03)*(currennt/1.602E-19)

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	
	counter=Count(s,3,0)
	f=File("./")

	# Total time
	total_time=float(sys.argv[1])
	
        prefix="%03d"%f.getNewIdx3()
	ofilename="%s_time.scn"%prefix
	of=open(ofilename,"w")

	# initialization
	starttime=time.time()
	of.write("#### %s\n"%starttime)
	ttime=0
	while (ttime <= total_time ):
		#currtime=datetime.datetime.now()
		currtime=time.time()
		ttime=currtime-starttime
		ch1,ch2=counter.getCountMsec(10)
		#print "12345 %8.4f %12d %12d\n" %(ttime,ch1,ch2)
		of.write("12345 %8.4f %12d %12d\n" %(ttime,ch1,ch2))
	of.close()

	# file open
	ana=AnalyzePeak(ofilename)
	x,y1,y2=ana.prepData3(1,2,3)

	py1=ana.getPylabArray(y1)
	py2=ana.getPylabArray(y2)

	mean1=py1.mean()
	mean2=py2.mean()
	std1=py1.std()
	std2=py2.std()

	print "COUNTER1:%5d Average: %12.5f Std.:%12.5f (%8.3f perc.)\n"%(3,py1.mean(),py1.std(),py1.std()/py1.mean()*100.0)
	print "COUNTER2:%5d Average: %12.5f Std.:%12.5f (%8.3f perc.)\n"%(0,py2.mean(),py2.std(),py2.std()/py2.mean()*100.0)

	#print py1.mean(),py2.mean()
	#print py1.std(),py2.std()

	s.close()


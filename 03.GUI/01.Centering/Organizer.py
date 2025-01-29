import sys
import socket
import time

from Received import *
from CounterInfo import *

class Organizer:
	def __init__(self,srv,bl,device,motor):
		self.srv=srv
		if motor=="":
			self.axisstr=bl+"_"+device
		else:
			self.axisstr=bl+"_"+device+"_"+motor
		self.qcommand="get/"+self.axisstr+"/"+"query"
		#print self.axisstr
		#print "QCOMMAND:"+self.qcommand

	def moveRelative(self,value,unit):
		curr_position=self.getPosition()
		aimed_position=curr_position+value
		self.move(aimed_position,unit)

	def move(self,value,unit):
		if unit=="pulse":
			tmpvalue=int(value)
		else :
			tmpvalue=value

		strvalue=str(tmpvalue)+unit
		print "Moving %s to %s" % (self.axisstr,strvalue)
		command="put/"+self.axisstr+"/"+strvalue
		#print command

	######	sending move command
    		self.srv.sendall(command)
		print self.srv.recv(8000) # dummy buffer

    		while True:
		#### Get query information
    			self.srv.sendall(self.qcommand)
    			recbuf = self.srv.recv(8000)
			#print recbuf
    			rrrr=Received(recbuf)

		#### CASE: query is 'OK' or 'inactive'
    			if rrrr.checkQuery():
				#print "Finished: current status="+rrrr.readQuery()
				return 1
			time.sleep(0.5)

	def query(self):
		self.srv.sendall(self.qcommand)
		recbuf=self.srv.recv(8000)
    		rrrr=Received(recbuf)
		return rrrr.readQuery()

	def getPosition(self):
		com="get/"+self.axisstr+"/position"
		self.srv.sendall(com)
		recbuf=self.srv.recv(8000)
		
		tmpf=Received(recbuf)
		position=tmpf.readQuery()

		#print position

		if position.find("mm")!=-1:
			value=float(position.replace("mm",""))
			return(value,"mm")
		elif position.find("pulse")!=-1:
			value=int(position.replace("pulse",""))
			return(value,"pulse")
		elif position.find("deg")!=-1:
			value=float(position.replace("deg",""))
			return(value,"deg")
		elif position.find("um")!=-1:
			value=float(position.replace("um",""))
			return(value,"um")
		else :
			print "Unknown value"
			return(0,0)

	def getAperture(self):
		com="get/"+self.axisstr+"/aperture"
		self.srv.sendall(com)
		recbuf=self.srv.recv(8000)
		
		tmpf=Received(recbuf)
		position=tmpf.readQuery()

		#print position

		if position.find("mm")!=-1:
			value=float(position.replace("mm",""))
			return(value,"mm")
		elif position.find("pulse")!=-1:
			value=int(position.replace("pulse",""))
			return(value,"pulse")
		elif position.find("deg")!=-1:
			value=float(position.replace("deg",""))
			return(value,"deg")
		elif position.find("um")!=-1:
			value=float(position.replace("um",""))
			return(value,"um")
		else :
			print "Unknown value"
			return(NULL,NULL)

        def getEnergy(self):
                com="get/"+self.axisstr+"/energy"
                self.srv.sendall(com)
                recbuf=self.srv.recv(8000)

                tmpf=Received(recbuf)
                position=tmpf.readQuery()

                if position.find("kev")!=-1:
                        value=float(position.replace("kev",""))
                        return(value,"kev")
                else :
                        print "Unknown value"
                        return(NULL,NULL)

        def getRamda(self):
                com="get/"+self.axisstr+"/wavelength"
                self.srv.sendall(com)
                recbuf=self.srv.recv(8000)

                tmpf=Received(recbuf)
                position=tmpf.readQuery()

                if position.find("angstrome")!=-1:
                        value=float(position.replace("angstrome",""))
                        return(value,"angstrome")
                else :
                        print "Unknown value"
                        return(NULL,NULL)

        def getAngle(self):
                com="get/"+self.axisstr+"/angle"
                self.srv.sendall(com)
                recbuf=self.srv.recv(8000)

                tmpf=Received(recbuf)
                position=tmpf.readQuery()

                if position.find("degree")!=-1:
                        value=float(position.replace("degree",""))
                        return(value,"degree")
                else :
                        print "Unknown value"
                        return(NULL,NULL)

	def axisScan(self,ofile,scan_start,scan_end,scan_step,cnt_ch,cnt_ch2,cnt_time,unit):
		# maximum count
		maxcnt=[0]*2
		maxval=[0]*2

    		of=file(ofile,"w")
    		diff=scan_end-scan_start
    		ndata=int(round(diff/scan_step)+1)
    		#print "data number = %5d" % ndata

		# save this position
    		saved_position=list()
    		saved_position=self.getPosition()

    		#print "Saved current position:"+saved_position

    		for x in range(0,ndata):
			current_x=scan_start+x*scan_step

			if(unit=="pulse"):
				current_x=int(current_x)
				
			#print current_x,cnt_time
    			self.move(current_x,unit)
			# Counter channel
    			value1=self.getCount(cnt_ch,cnt_time)
    			value2=self.getCount(cnt_ch2,cnt_time)
			print "%12.5f ch1: %12d, ch2:%12d"%(current_x,value1,value2)
			line="12345 %12.5f %8d %8d\n" %(current_x,value1,value2)

			## maximum count
			if maxcnt[0]<value1:
				maxcnt[0]=value1
				maxval[0]=current_x
				print "1:FIND!!! MAXVALUE= "+str(maxcnt[0])+" "+str(maxval[0])
			if maxcnt[1]<value1:
				maxcnt[1]=value1
				maxval[1]=current_x
				print "2:FIND!!! MAXVALUE= "+str(maxcnt[0])+" "+str(maxval[0])

			of.write(line)

		of.close()
		## set this axis to the initial position
    		self.move(saved_position[0],saved_position[1])
		return maxval

	def getCount(self,ch,cnttime):
		strtime=str(cnttime)+"sec"
		com1="put/bl_32in_st2_counter_1/clear"
		com2="put/bl_32in_st2_counter_1/"+strtime
		com3="get/bl_32in_st2_counter_1/query"

	# counter clear
		self.srv.sendall(com1)
		recbuf=self.srv.recv(8000)
		#print "CLEAR: "+recbuf

	# get counter value
		self.srv.sendall(com2)
		self.srv.recv(8000)
		time.sleep(cnttime) # wait
		self.srv.sendall(com3)

		recbuf=self.srv.recv(8000)
		#print "COUNT:"+recbuf

		# obtain the 3rd column in the returned buffer
		cnt_buf=Received(recbuf).get(3)

		ci=CounterInfo(cnt_buf)
		retinfo=ci.get(ch).replace("count","")
		#print "count=%s"%retinfo

		return int(retinfo)

import sys
import socket
import time

from Received import *

class Motor:
	def __init__(self,srv,motor,unit):
	# server 
		self.srv=srv
	# motor name
		self.motor=motor
	# command for query
		self.qcommand="get/"+self.motor+"/"+"query"
	# unit
		self.unit=unit

	# moving the axis
	def move(self,value):
		# in the case: pulse 
		if self.unit=="pulse":
			tmpvalue=int(value)
		else :
			tmpvalue=float(value)
		# making a sending command
		strvalue=str(tmpvalue)+self.unit
		print "Moving %s to %s" % (self.motor,strvalue)
		command="put/"+self.motor+"/"+strvalue

		######	sending move command
    		self.srv.sendall(command)
		tmpstr=self.srv.recv(8000) # dummy acquisition

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
			time.sleep(0.1)

	##  get a position from MS
	def getPosition(self):
		com="get/"+self.motor+"/position"
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

#!/bin/env python 
import sys
import socket
import time
import math
import datetime

#
class CryoCont:

	def __init__(self,server):
		self.s=server

	def getValue(self):
                command="I/get/db1000/value?"
		self.s.sendall(command)
                tmpstr=self.s.recv(8000) # dummy acquisition
		
		cols=tmpstr.split('/')
		rtn=float(cols[3].replace("K",""))
		return rtn

	def setValue(self,value):
		temperature="%3.0fk"%value
		print temperature
                command="I/put/db1000/%s"%temperature
		self.s.sendall(command)
                tmpstr=self.s.recv(8000) # dummy acquisition
		print tmpstr

if __name__=="__main__":
	host = '192.168.163.107'
	port = 2001
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	temp=float(sys.argv[1])
	logfile=sys.argv[2]

	cr=CryoCont(s)
	cr.setValue(temp)

	iok=0

	of=open(logfile,"w")

	#####################
        # initialization
	#####################
        starttime=time.time()
        of.write("#### %s\n"%datetime.datetime.now())
	current= float(cr.getValue())
        of.write("#### start: %5.2f K target: %5.2f\n"%(current,temp))
        ttime=0
        while (1):

		# Current temperature
                current= float(cr.getValue())
                diff=math.fabs(temp-current)
                currtime=time.time()
                ttime=currtime-starttime

                of.write("%8.4f %8.3f\n" %(ttime,current))
		of.flush()
                print "Current %8.2f K (Diff:%8.2f K to %8.2fK)"%(current,diff,temp)
                if diff<0.5:
                        iok+=1
                        if iok>5:
                                break
                else:
                        iok=0
                time.sleep(1.0)

	of.close()

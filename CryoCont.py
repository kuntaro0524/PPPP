#!/bin/env python 
import sys
import socket
import time
import math

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

	if len(sys.argv)!=2 :
		print "Usage: program [HIGH/LOW]"
		sys.exit(1)

	command=sys.argv[1]

	if command=="HIGH":
		temp=90.0
	elif command=="LOW":
		temp=45.0
	elif command=="HIGHER":
		temp=150.0
	else:
		print "Invalid command"
		sys.exit(1)

	cr=CryoCont(s)
	cr.setValue(temp)

	iok=0
	while(1):
                current= float(cr.getValue())
                diff=math.fabs(temp-current)
                print "Current %8.2f K (Diff:%8.2f K to %8.2fK)"%(current,diff,temp)
                if diff<0.5:
                        iok+=1
                        if iok>5:
                                break
                else:
                        iok=0
                time.sleep(1.0)


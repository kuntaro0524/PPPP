#!/bin/env python 
import sys
import socket
import time
import datetime
#from Count import *

class MXserver:
	def __init__(self):
		host = '192.168.163.32'
        	port = 2222
        	self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        	self.s.connect((host,port))
	
	def getState(self):
		message="get_state"
		self.s.sendall(message)
		rec=self.s.recv(8000)
		return rec

	def abort(self): # stop data collection
		message="abort"
		print self.s.recv(8000) # dummy buffer

	def end_automation(self): # stop the server program
		message="end_automation"
		print self.s.recv(8000) # dummy buffer

	def close_connection(self): # close connection
		message="close connection"
		print self.s.recv(8000) # dummy buffer

	def close(self):
		self.s.close()

if __name__=="__main__":
	mxs=MXserver()
	option=sys.argv[1]

	if option=="abort":
		print mxs.getState()
		mxs.abort()
		print mxs.getState()

	elif option=="terminate":
		print mxs.getState()
		mxs.end_automation()

	mxs.close()

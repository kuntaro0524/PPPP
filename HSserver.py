import socket
import time
import datetime
import sys,os

# modiied by YK @ 141113
# not yet test

class HSserver:
	def __init__(self):
		host = '192.168.163.32'
		port = 2222
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((host,port))

	def abort(self):
		com="abort"
		self.s.sendall(com)
		recbuf = self.s.recv(8000)
		print recbuf

	def end_automation(self):
		com="end_automation"
		self.s.sendall(com)
#		recbuf = self.s.recv(8000)
#		print recbuf

	def close_connection(self):
		com="close connection"
		self.s.sendall(com)
		recbuf = self.s.recv(8000)
		print recbuf

	def getState(self):
		com="get_state"
		self.s.sendall(com)
		recbuf=self.s.recv(8000)
		print recbuf
		return recbuf

	def close(self):
		self.s.close()


if __name__=="__main__":
        hss=HSserver()
	if (len(sys.argv) < 2):
		print "input some key"
	elif (sys.argv[1] == "end_automation"):
		hss.end_automation()
	elif (sys.argv[1] == "close"):
		hss.close_connection()
	elif (sys.argv[1] == "get_state"):
		hss.getState()
	elif (sys.argv[1] == "abort"):
		hss.abort()
	else:
		print "wrong key"

#	hss.close()

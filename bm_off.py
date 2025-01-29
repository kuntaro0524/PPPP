import sys
import socket
import time

# My library
import BM

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	print "Moving Scintillator Monitor"
	moni=BM.BM(s)

	moni.offXYZ()

	s.close()

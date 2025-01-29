#!/bin/env python 
# coding: shift_jis
import sys
import socket
import time
import datetime 
import codecs

class SP8CHAT:
	def __init__(self):
		host="sp8chat.spring8.or.jp"
		port = 23
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((host,port))

	def init(self):
		# Beamline name
                self.s.sendall("bl32xu")
                tmpstr=self.s.recv(8000) # dummy acquisition
		print tmpstr
                self.s.sendall("\n")
                tmpstr=self.s.recv(8000) # dummy acquisition
		print tmpstr

	def getChars(self):
		com="!"
                self.s.sendall(com)
                tmpstr=self.s.recv(100000) # dummy acquisition
		print tmpstr

		ofile=open("test.txt","w")
		ofile.write("%s\n"%tmpstr)
		ofile.close()

if __name__=="__main__":
	sp8chat=SP8CHAT()
	sp8chat.init()
	sp8chat.getChars()

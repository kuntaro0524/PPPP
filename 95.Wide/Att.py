import sys
import socket
import time

# My library
from Motor import *

class Att:
	def __init__(self,server):
		self.s=server
    		self.att=Motor(self.s,"bl_32in_st2_att_1_rx","pulse")

		self.um1000=-2160
		self.um1500=-2340
		self.um2000=-2520
		self.um600=-1440
		self.um700=-1620
		self.um800=-1800
		self.um900=-1980
		self.um200=-720
		self.um400=-1080
		
	def att1500um(self):
		self.att.move(-2340)
	def att1000um(self):
		self.att.move(-2160)
	def att200um(self):
		self.att.move(self.um200)
	def att600um(self):
		self.att.move(self.um600)
	def att800um(self):
		self.att.move(self.um800)
	def att400um(self):
		self.att.move(self.um400)
	def att0um(self):
		self.att.move(0)

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	att=Att(s)
	#att.att1000um()
	#att.att0um()
	#att.att200um()

	s.close()

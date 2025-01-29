import sys
import socket
import time

# My library
from Motor import *

#
class BM:
	def __init__(self,server):
		self.s=server
    		self.moni_y=Motor(self.s,"bl_32in_st2_monitor_1_y","pulse")
    		self.moni_z=Motor(self.s,"bl_32in_st2_monitor_1_z","pulse")
		
		self.off_pos=-75000 # pulse
		self.on_pos=-500 # pulse
	
	def on(self):
		self.moni_z.move(self.on_pos)

	def off(self):
		self.moni_z.move(self.off_pos)

	def set(self,position):
		self.moni_z.move(position)

	def relmove(self,value):
		self.moni_z.relmove(value)

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	print "Moving Scintillator Monitor"
	print "type on/off:"
	option=raw_input()
	moni=BM(s)

	#if option=="on":
		#moni.on()
	#elif option=="off":
		#moni.off()
	#else:
		#moni.set(-40000)
	#s.close()

import time
import socket
import sys

#import Motor as Motor
from File import *
from Motor import *

class AxesInfo:
	def __init__(self,server):
		self.s=server
		self.isStore=-1

	def all(self,ofname):
		ofile=open(ofname,"a")
#		ofile.write("%12s%7s\n" % Motor(self.s,"bl_32in_st2_detector_1_y","pulse").getPosition())
#		ofile.write("%12s%7s\n" % Motor(self.s,"bl_32in_st2_detector_1_y","pulse").getPosition())
		MX_x=Motor(self.s,"bl_32in_st2_detector_1_x","pulse").getPosition()[0]
		CMOS_z=Motor(self.s,"bl_32in_st2_detector_2_z","pulse").getPosition()[0]
		ofile.write("CMOS_z, %s, MX225HE_x, %s\n"%(CMOS_z,MX_x))

		ofile.close()
		return 1

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	f=File("./")
	ax=AxesInfo(s)

    	ofile="detector.dat"   #hashi 100615
	ax.all(ofile)              #hashi 100615
	#print ax.getLeastInfo() 
	

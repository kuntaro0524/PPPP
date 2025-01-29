from Stage import *
from Att import *
import socket,sys,os,math

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	stage=Stage(s)
	att=Att(s)
	att.init()
	#yyy= stage.getYmm()
	#zzz= stage.getZmm()
	#stage.getSpeed()
	#print yyy,zzz
	att.setAttThick(600)
	stage.scanY("MOVE")
	stage.scanZ("MOVE")

	s.close()

import os,sys,math,socket
from Att import *

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        att=Att(s)
	print att.setAtt(float(sys.argv[1]))

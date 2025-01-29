import sys
import socket
import time
from Received import *
from Motor import *
from IDparam import *


if __name__=="__main__":
	com="./
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	
	qcommand="get/bl_32in_id_gap/query"
        s.sendall(qcommand)
        recbuf=s.recv(8000)
	print recbuf
        #rrrr=Received(recbuf)
	#print rrrr

	s.close()

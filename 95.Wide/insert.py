import sys
import socket
import time

from Motor import *
from Light import *
from Cryo import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	light=Light(s)
	cryo=Cryo(s)

	light.on()
	cryo.on()

	s.close()

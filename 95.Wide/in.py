import sys
import socket
import time

from Motor import *
from BS import *
from Colli import *
from Light import *
from Cryo import *
from Zoom import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	bs=BS(s)
	colli=Colli(s)
	light=Light(s)
	cryo=Cryo(s)
	zoom=Zoom(s)

	bs.go(0)
	colli.go(0)
	cryo.go(400)
	light.on()

	s.close()

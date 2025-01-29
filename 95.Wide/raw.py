#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Organizer import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

#

while True:
    print 'Type message...'
    msg = raw_input()
    if msg == '':
	s.close()
	break

## Sending message
    s.sendall(msg)
    print s.recv(8000)

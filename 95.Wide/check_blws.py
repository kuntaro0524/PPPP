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
    #msg = "get/bl_32in_id_gap/query"
    msg = "get/bl_32in_st2_cryo_1_z/query"

## Sending message
    s.sendall(msg)
    print s.recv(8000)
    break

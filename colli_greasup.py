#!/bin/env python 
import sys
import socket
import time
import datetime 

# My library
from Received import *
from Motor import *
from BSSconfig import *
from Colli import *
from File import *

if __name__=="__main__":
    host = '172.24.242.41'
    port = 10101

    f=File("./")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))

    coli=Colli(s)

    for num in range(10):
        print("\nnum %d\n" % num)
        coli.moveZ(1815)
        print coli.getZ()
        #exit()

        coli.moveZ(-70000)
        print coli.getZ()

    coli.moveZ(-70000)
    print coli.getZ()
    s.close()

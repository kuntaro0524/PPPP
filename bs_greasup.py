import sys
import socket
import time
import datetime

# My library
from File import *
from BS import *

if __name__=="__main__":
    host = '172.24.242.41'
    port = 10101
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))

    bs=BS(s)

    for num in range(10):
        bs.moveZ(6029)
        z=bs.getZ()
        print z
        #exit()

        bs.moveZ(-70000)
        z=bs.getZ()
        print z

    bs.moveZ(-70000)
    z=bs.getZ()
    print z
    s.close()


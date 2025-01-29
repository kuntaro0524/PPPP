#!/bin/env python 
import sys
import socket
import time
import math
from pylab import *

# My library
from ExSlit1 import *
from Shutter import *
from Light import *
from CCDlen import *
from Cover import *
from CMOS import *
from Colli import *
from BS import *
from Att import *

while True:
    #host = '192.168.163.1'
    host = '172.24.242.41'
    port = 10101
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))

    ##	Device definition
    exs1=ExSlit1(s)
    shutter=Shutter(s)
    light=Light(s)
    clen=CCDlen(s)
    covz=Cover(s)
    colli=Colli(s)
    bs=BS(s)
    att=Att(s)

    ## Cover check
    time.sleep(1.5)
    clen.evac()
    covz.on()
    if covz.isCover():
        exs1.openV()
        print "Slit1 lower blade opened"
        light.off()
        print "Light went down"
        shutter.open()
        print "Shutter on diffractometer was opened"

    print "Beamstopper off"
    bs.off()
    print "Collimator off"
    colli.off()
    print "Collimator off"
    colli.off()
    print "Attenuator is set to 0"
    att.init()
    att.setAttThick(0)
    break

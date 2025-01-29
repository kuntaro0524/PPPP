#!/bin/env python 
import sys
import socket
import time
import datetime

# My library
import Device

while True:
    host = '172.24.242.41'

    # Initialization
    dev=Device.Device(host)
    dev.init()

    logfile=open("tcs.log","a")

# change time by YK 170930
#    wait_minutes=15.0
#    wait_minutes=5.0
    wait_minutes=1.0

    #dev.prepScan()

    for i in range(0,10):
#        dev.tuneDt1("./")
        nowt=datetime.datetime.now()
        dev.tcs.setApert(5,5)

# insert by YK 170930
#        dev.prepScan()

        #ipin,iic=dev.countPin(pin_ch=3)
        #logfile.write("%s %5.1fx%5.1f ipin= %8d iic=%8d\n"%(nowt,3,3,ipin,iic))

        dev.tcs.setApert(-0.1,-0.1)
        nowt=datetime.datetime.now()
        dev.tcs.setApert(0.1,0.1)
        #ipin,iic=dev.countPin(pin_ch=3)
        #logfile.write("%s %5.1fx%5.1f ipin= %8d iic=%8d\n"%(nowt,0.1,0.1,ipin,iic))
        #logfile.flush()

        dev.closeAllShutter()
        print "now sleeping"
        time.sleep(60.0*wait_minutes)

    logfile.close() # s.close() <- socket close?
    break

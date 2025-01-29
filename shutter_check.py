#!/bin/env python 
import sys
import socket
import time
import datetime

import Device

if __name__=="__main__":
        host = '172.24.242.41'
	dev=Device.Device(host)
	dev.init()
	cnt=0
	bad_count=0
	ofile=open("shutter.log","w")
	while(1):
		now=datetime.datetime.now()
		dev.shutter.open()
		t1= dev.shutter.isOpen()
		open_intensity,p=dev.countPin()
		time.sleep(2.0)
		dev.shutter.close()
		t2= dev.shutter.isOpen()
		time.sleep(2.0)
		close_intensity,p=dev.countPin()
		if close_intensity!=0:
			bad_count+=1
		print "%s CNT:GOOD=%10d BAD=%10d ON_FLAG=%s OFF_FLAG=%s O/C=%d/%d"%(now,cnt,bad_count,t1,t2,open_intensity,close_intensity)
		ofile.write("%s CNT:GOOD=%5d BAD=%5d ON_FLAG=%s OFF_FLAG=%s O/C=%5d/%5d\n"%(now,cnt,bad_count,t1,t2,open_intensity,close_intensity))
		ofile.flush()
		cnt+=1

#!/bin/env python 
import sys
import socket
import time
from  File import *
from  Mono import *
from TCS import *
from ConfigFile import *

# My library
from Motor import *

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))


	conf=ConfigFile()

	try :
                ## Dtheta 1
                scan_dt1_ch1=int(conf.getCondition2("DTSCAN_NORMAL","ch1"))
                scan_dt1_ch2=int(conf.getCondition2("DTSCAN_NORMAL","ch2"))
                scan_dt1_start=int(conf.getCondition2("DTSCAN_NORMAL","start"))
                scan_dt1_end=int(conf.getCondition2("DTSCAN_NORMAL","end"))
                scan_dt1_step=int(conf.getCondition2("DTSCAN_NORMAL","step"))
                scan_dt1_time=conf.getCondition2("DTSCAN_NORMAL","time")
                tcsv=conf.getCondition2("DTSCAN_NORMAL","tcsv")
                tcsh=conf.getCondition2("DTSCAN_NORMAL","tcsh")

        except MyException,ttt:
                print ttt.args[0]
		print "Check your config file carefully.\n"
		sys.exit(1)

	tcs=TCS(s)
	mono=Mono(s)

	for i in range(0,5):
    		tcs.setApert(tcsv,tcsh)
		f=File("./")
		prefix="%03d"%f.getNewIdx3()
        	mono.scanDt1Peak(prefix,scan_dt1_start,scan_dt1_end,scan_dt1_step,scan_dt1_ch1,scan_dt1_ch2,scan_dt1_time)  #hashi 100628
		time.sleep(3600)

	s.close()

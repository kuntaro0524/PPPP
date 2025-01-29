#!/bin/env python
import sys
import socket
import time
import datetime

from numpy import *
from Procedure import *
from File import *
from Stage import *

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	proc=Procedure(s)
	stage=Stage(s)
	f=File("./")

        # StageY scan and Move
        prefix="%03d"%f.getNewIdx3()
        stage.scanYneedle(prefix,0.001,20,3,0,1.0)
        datfile="%s_stagey.scn"%prefix
        ycenter=proc.analyzeKnife(datfile)
        stage.setYmm(ycenter)
	print "Final stage position: %8.5f\n"%ycenter

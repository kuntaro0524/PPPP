#!/bin/env python 
import sys
import socket
import time
import math
from pylab import *

from ExSlit1 import *
from Light import *
from BS import *
from Colli import *
from Cryo import *


#
if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        exs1=ExSlit1(s)
        light=Light(s)
        bs=BS(s)
        coli=Colli(s)
	cryo=Cryo(s)

	print "Goto Expreimental setup\n"

#	cryo.moveTo(600)
	bs.on()
	coli.on()
	light.off()
	exs1.openV()

	print "\nReady for Expriment\n"


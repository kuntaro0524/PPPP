from Stage import *
from Shutter import *
from File import *
from ExSlit1 import *
from Light import *
import socket

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	# Required equipments
        stage=Stage(s)
	slit1=ExSlit1(s)
	shutter=Shutter(s)
	light=Light(s)
	f=File(".")

	# Slit1 open
        slit1.openV()
        shutter.open()
        light.off()

        #stage.scanYneedle
	prefix="%03d"%f.getNewIdx3()

        stage.scanYwire(prefix,0.002,80,3,0,0.2)

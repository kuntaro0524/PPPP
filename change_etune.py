import socket,os,sys

from Procedure import *

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        proc=Procedure(s)

	en=float(sys.argv[1])

	if en <8.5 or en>20.0:
		print "Invalid energy : 8.5 - 20.0 keV"
		sys.exit(1)

	proc.changeEandTune(en)


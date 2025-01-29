import socket,os,sys

from Procedure import *

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        proc=Procedure(s)

	proc.prepCapture()
        print proc.captureBM(sys.argv[1])

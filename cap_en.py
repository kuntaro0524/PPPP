import socket,os,sys
import numpy as np

from Procedure import *

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        proc=Procedure(s)

	en_list=np.arange(18.5,8.5,-0.3)
	
	print en_list,len(en_list)
	
	proc.makePikaTable(en_list)

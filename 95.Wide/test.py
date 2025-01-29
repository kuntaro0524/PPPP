import sys
from Zoom import *
from Gonio import *
from Capture import *
from TemplateMatch import *

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	gonio=Gonio(s)

	x=gonio.getXmm()
	y=gonio.getYmm()
	z=gonio.getZmm()

	print x,y,z

import sys,os
from Gonio import *
from Enc import *
from Shutter import *

if __name__=="__main__":

        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        shutter=Shutter(s)
	gonio=Gonio(s)
	count=Count(s,1,0)

	# read gonio xyz
	x=int(gonio.getX()[0])
	y=int(gonio.getY()[0])
	z=int(gonio.getZ()[0])

	gonio.kill()

	# Encoder class
        enc=Enc()
        enc.openPort()
	enc.resetEnc(x,y,z)

        of=open(sys.argv[1],"w")
	starttime=time.time()

	list=[]
	save=0
	while(1):
		ti=time.time()
		diff=ti-starttime
                openflag=shutter.isOpen()

		# Counting
                ch1,ch2=count.getCountMsec(1)

                #str="%8.4f %8.5f %8.5f %8.5f %5d %5d\n"%(diff,enc.getX(),enc.getY(),enc.getZ(),openflag,int(ch1))
                of.write("%8.4f %8.5f %8.5f %8.5f %5d %5d\n"%(diff,enc.getX(),enc.getY(),enc.getZ(),openflag,int(ch1)))
                #of.flush()
                #time.sleep(0.05) # wait

        enc.closePort()

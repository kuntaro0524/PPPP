import os,sys,math,socket
from File import *
from AnalyzePeak import *
from Count import *
from Att import *
from Count import *

#2014/04/12 The first code by K.Hirata

if __name__=="__main__":
	# Establishing MS server connection
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	# Attenuator motor drive
	att=Att(s)
	# Counter 
	counter=Count(s,3,0)

	# ofile
	of=open("att_fac.scn","w")

	idx=0
	for pls in arange(0,3600,100):
		att.move(pls)
		istr=counter.getPIN(1.0)
		of.write("%5d, %5d, %s\n"%(idx,pls,istr))
		print istr
		of.flush()
		idx+=1
	of.close()
	s.close()
"""
        att=AttFactor()
        #list=[1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000]
        #attlist=[0.0,500,1000,1500,1900,3000,6000]
        attlist=[0.0,50,100,150,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,3000,6000]
        #list=[0.0159,0.01095,0.00750,0.00502,0.00250,0.00171,0.00112,0.00076]
        #list=[0.02416,0.00394,0.00073]

        wave=float(sys.argv[1])
        #trans=float(sys.argv[2])
        flux=float(sys.argv[2])

        for thick in attlist:
                value=float(thick)
                attfac=att.calcAttFac(wave,thick)
                print "%6.1f %12.5f %12.2e"%(thick,attfac,attfac*flux)

        #print att.getBestAtt(wave,trans)
"""

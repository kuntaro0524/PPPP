import sys,os,math
import ProcHD5

if __name__=="__main__":
	nread=int(sys.argv[2])
	ph=ProcHD5.ProcHD5(sys.argv[1],nread)
	ph.test()
	ph.setCenter(1554.7,1597.8)
	ph.calcCircle(1000,25)

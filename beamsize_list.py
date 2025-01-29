import sys,os
import TCSsimple
import socket
import BeamsizeConfig

if __name__=="__main__":
	config_dir="/isilon/BL32XU/BLsoft/PPPP/10.Zoo/ZooConfig/"
	bsc=BeamsizeConfig.BeamsizeConfig(config_dir)
	tw,th,bs,ff=bsc.getBeamParamList()
	print tw,th,bs,ff
	i = 0
	for b in bs:
		p,q,r=b
		print "%5.1f (H) x %5.1f (V)um"%(q,r)
		print tw[i], th[i]
		i+=1

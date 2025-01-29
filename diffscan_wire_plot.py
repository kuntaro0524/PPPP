from DiffscanLog import *

if __name__=="__main__":

        dl=DiffscanLog(sys.argv[1])
        dl.prep()

	datafile=sys.argv[2]

	iff=open(datafile,"r")
	ilines=iff.readlines()
	iff.close()

	tmp=[]
	for line in ilines:
		value=int(line.split()[1])
		tmp.append(value)

	#print len(tmp)
	
	xyz=dl.getBlock(0)
	
	idx=0
	for line in xyz:
		print "%8.4f %8.4f %8.4f %12d"%(float(line[2])*1000,
				float(line[3])*1000,float(line[4])*1000,tmp[idx])
		#print float(line[2]),float(line[3]),float(line[4])
		idx+=1

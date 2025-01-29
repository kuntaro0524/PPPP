import os,sys
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import XDSascii

lines=open(sys.argv[1],"r").readlines()
dsets=[]

ofile=open("list_for_xscale.dat","w")

for line in lines:
	iii= line.rfind("multi")
	cutline= line[iii:]
	cols=cutline.split('/')
	ndata= float(cols[0].replace("multi_","").split('-')[0])/100.0
	#print "%5d %s\n"%(ndata,line.strip()),
	dsets.append((line,ndata))

dsets.sort(key=lambda x:x[1])

xds_ascii_list=[]
for d in dsets:
	line,ndata=d
	xds_ascii_list.append(line.strip().replace("INPUT_FILE=",""))

score_list=[]
for xa in xds_ascii_list:
        xdsas=XDSascii.XDSascii(xa)
	sumi=xdsas.calcDP()
	score_list.append((xa,sumi))

score_list.sort(key=lambda x:x[1])

for com in score_list:
	xa,sumi=com
	ofile.write("INPUT_FILE=%-100s !%8.1f\n"%(xa,sumi))

ofile.close()


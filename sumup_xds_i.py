import sys,os,numpy

lines=open(sys.argv[1],"r").readlines()

sum=0.0
for line in lines:
	#print line
	if line.rfind("!")!=-1:
		continue
	cols=line.split()
	sum+=float(cols[4])

print sum

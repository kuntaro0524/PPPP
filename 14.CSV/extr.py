import sys,os

lines=open(sys.argv[1],"r").readlines()

nline=0
for line in lines:
	if nline >= 2E6 and nline<3E6:
		print line,
	nline+=1

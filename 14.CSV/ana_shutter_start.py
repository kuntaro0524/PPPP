import sys,os,math

lines=open(sys.argv[1],"r").readlines()

okline=0
nline=0
for line in lines:
	cols=line.split()
	t_shutter=float(cols[0])
	if t_shutter > 1.0:
		okline+=1
		print line,
	if okline>118000:
		break

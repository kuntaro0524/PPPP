import sys,os,math

lines=open(sys.argv[1],"r").readlines()


for line in lines:
	cols=line.split()
	t_shutter=float(cols[0])
	if t_shutter > 1.0:
		print line

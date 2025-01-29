import sys,os,math

lines=open(sys.argv[1],"r").readlines()

for line in lines:
	cols=line.split()
	print cols[0],cols[1],cols[4],cols[5],cols[6]

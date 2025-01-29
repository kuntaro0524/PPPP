import sys,math,os
import numpy

mode="n_spots"

lines=open("summary.dat","r").readlines()

nread=0
nprefix=0

names=[]
all=[]
tdat=[]
tmpx=[]
tmpn=[]

for idx in range(1,len(lines)):
	cols=lines[idx].split()
	prefix=cols[0]
	#print prefix

	if lines[idx].rfind(mode)!=-1:
		continue
	
	# The first one
	if nprefix==0:
		sname=prefix
		names.append(prefix)
		print sname
		x=float(cols[2])
		n=float(cols[4])
		tmpx.append(x)
		tmpn.append(n)
		nprefix+=1

	elif prefix==sname:
		x=float(cols[2])
		n=float(cols[4])
		tmpx.append(x)
		tmpn.append(n)
		continue
	else:
		# Ato shori
		xa=numpy.array(tmpx)
		na=numpy.array(tmpn)

		data=xa,na
		all.append(data)
		
		tmpx=[]
		tmpn=[]

		names.append(prefix)
		sname=prefix
		print sname
		nprefix+=1

for a in all:
	xa,ya=a
	for x,y in zip(xa,ya):
		print x,y

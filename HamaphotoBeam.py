#!/usr/bin/python2.6
import sys
from numpy import *
import numpy as np
import os

ifile=open(sys.argv[1],"r")

lines=ifile.readlines()
nline=len(lines)

oned=[]
ncol=0
summed=0.0
for line in lines:
	cols=line.split()
	ncol=len(cols)
	for col in cols:
		value=float(col)
		oned.append(value)

# Calculation of heavy-center of peak
nar=np.array(oned)
# average value
ave=nar.sum()/float(ncol*nline)
#print ave
thresh=ave*5.0

align=nar.reshape(nline,ncol)

#print align

sumi=0.0
sumx=0.0
sumy=0.0
for i in arange(0,ncol):
	for j in arange(0,nline):
		value=align[j][i]
		if value>thresh:
			x=float(i)
			y=float(j)
			sumx+=x*value
			sumy+=y*value
			sumi+=value

cenx=sumx/sumi
ceny=sumy/sumi

print cenx,ceny

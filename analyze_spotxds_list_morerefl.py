import sys,math,os

lines=open("better_index_150.dat","r").readlines()

def count_indexed_refl(filename):
	lines=open(filename,"r").readlines()
	n_good=0
	for line in lines:
		cols=line.split()
		h=int(cols[4])
		k=int(cols[5])
		l=int(cols[6])
		if h==0 and k==0 and l==0:
			continue
		else:
			n_good+=1
	return n_good

for line in lines:
	cols=line.split()
	filename=cols[0]
	print "%20s %5d"%(filename,count_indexed_refl(filename))

import sys,os,math

lines=open(sys.argv[1],"r").readlines()

all_n=bad_n=0

for line in lines:
	#print line
	all_n+=1
	cols=line.split()
	h=int(cols[4])
	k=int(cols[5])
	l=int(cols[6])
	if h==0 and k==0 and l==0:
		bad_n+=1

good_n=all_n-bad_n
fraction=float(good_n)/float(all_n)

print "%20s Indexed fraction = %8.3f"%(sys.argv[1],fraction)

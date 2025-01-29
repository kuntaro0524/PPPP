import os,sys

lines=open(sys.argv[1],"r").readlines()

lists=[]
for line in lines:
	cols=line.split()	
	#print cols
	fname=cols[0]
	score=float(cols[1])
	lists.append((fname,score))

sortlist=sorted(lists,key=lambda x:float(x[1]),reverse=True)

for l in sortlist:
	
	print "%70s %10.1f"%(l[0],l[1])

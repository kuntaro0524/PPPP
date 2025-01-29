import os,sys
from libtbx import easy_mp


def get_value_from_CSV(paramlist):
	filename,cols=paramlist
	nng=0
	infile=open(filename,"r")
	lines=infile.readlines()

	for line in lines[10:]:
		#print line
		if line.rfind("QNAN")!=-1:
			nng+=1
		else:
			value=float(line.replace(",",""))
			print value
			cols.append(value)
	infile.close()
	return nng

# Data1
col1=[]
file1=sys.argv[1]

col2=[]
file2=sys.argv[2]

# Making para list
params=[]
params.append((file1,col1))
params.append((file2,col2))

easy_mp.pool_map(fixed_func=lambda n: get_value_from_CSV(n), args=params, processes=8)

print col1,col2
#for c1,c2 in zip(col1,col2):
	#print c1,c2

import os,sys
from libtbx import easy_mp

header=10

def get_value_from_CSV(csvfile):
	nng=0
	infile=open(csvfile,"r")
	lines=infile.readlines()

	cols=[]
	nline=0

	for line in lines[header:]:
		#print line
		if line.rfind("QNAN")!=-1:
			nng+=1
		else:
			value=float(line.replace(",",""))
			cols.append(value)
	print "CSVFILE %s : %5d"%(csvfile,nng)
	print "COLS=%5d"%len(cols)
	infile.close()
	return cols

# Data1
file1=sys.argv[1]
file2=sys.argv[2]
file3=sys.argv[3]
file4=sys.argv[4]

# Making para list
params=[]
params.append(file1)
params.append(file2)
params.append(file3)
params.append(file4)

cols=easy_mp.pool_map(fixed_func=lambda n: get_value_from_CSV(n), args=params, processes=8)

outfile=open("test.log","w")
for c1,c2,c3,c4 in zip(cols[0],cols[1],cols[2],cols[3]):
	c1v=float(c1)
	c2v=float(c2)
	c3v=float(c3)
	c4v=float(c4)
	outfile.write("%8.5f %8.5f %8.5f %8.5f\n"%(c1,c2,c3,c4))

outfile.close()

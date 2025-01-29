import sys,os,math

# /isilon/users/target/target/Staff/kuntaro/161206/pH4.5/_kamoxds/03.Holder/data/multi014_1-50/XDS_ASCII.HKL_noscale

lines=open(sys.argv[1],"r").readlines()
lines_spots=open(sys.argv[2],"r").readlines()

prefix_list=[]
for line in lines:
	cols=line.split("/")
	prefix=cols[12]
	prefix_list.append(prefix)

for line in lines_spots:
	cols=line.split()
	i=cols[0].find("/")+1
	j=cols[0].rfind("_")
	pre_search=cols[0][i:j]

	for lline in lines:
		if lline.rfind(pre_search)!=-1:
			print lline,

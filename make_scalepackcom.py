import sys,os,math

# 2015/04/16 K.Hirata
# 1) go to the scaling directory
# 2) "ls ../where/xfiles/are/*.x > xfiles.dat"
# 3) python this_program xfiles.dat
# 4) you can get

xfiles=open(sys.argv[1],"r").readlines()

bunches=[]

# The 1st directory & prefix
o=xfiles[0].rfind("_")
save_prefix=xfiles[0][:o]

cnt=0

for xfile in xfiles:
	#print xfile

	# Directory & Prefix extraction
	o=xfile.rfind("_")
	dirfix=xfile[:o]
	
	if save_prefix==dirfix:
		cnt+=1
	# Change to the next data
	else:
		contents=save_prefix,cnt
		#print contents
		bunches.append(contents)
		save_prefix=dirfix
		cnt=1

#bunches.sort()
	
idx=1
ofile=open("sector.dat","w")

postref_bufs=[]
for bunch in bunches:
	prefix,cnt=bunch
	startnum=1
	endnum=cnt

	# idx: sequential frame number in SCALEPACK
	ofile.write("sector 1 to %d\n"%endnum)
	ofile.write("FILE %5d '%s_00####.x'\n"%(idx,prefix))

	inner_start=idx
	inner_end=idx+cnt-1
	com= "%4d to %4d"%(inner_start,inner_end)
	postref_bufs.append(com)
	idx+=cnt

print inner_end
ofile.close()

idx=0
postref_sectors=""
for postref in postref_bufs:
	idx+=1
	postref_sectors+="%s"%postref
	if idx%3==0:
		postref_sectors+="\n"

prfile=open("postref.in","w")
#print postref_sectors
prfile.write("add partials %s\n"%postref_sectors)
prfile.write("fit batch rotx %5d to %5d\n"%(1,inner_end))
prfile.write("fit batch roty %5d to %5d\n"%(1,inner_end))
prfile.write("fit crystal cell %5d to %5d\n"%(1,inner_end))
prfile.write("fit crystal mosaicity %5d to %5d\n"%(1,inner_end))
	
	#print "add partials 


comfile=open("test.com","w")


comstr="""
#!/bin/csh
scalepack << eof > scale1.log
resolution 25.00 2.00
number of zones 20
estimated error
0.03 0.03 0.03 0.03 0.03
0.03 0.03 0.03 0.03 0.03
0.03 0.03 0.03 0.03 0.03
0.03 0.03 0.03 0.03 0.03
error scale factor 1.3
default scale 10
rejection probability 0.0001
write rejection file
reference film 6
scale restrain 0.01
fix b
print cc1/2
space group C2
output file 'output1.sca'
ignore overloads
intensity bins
@postref.in
postrefine 0
format denzo_ip
@sector.dat
eof

scalepack << eof > scale2.log
@reject
resolution 25.00 2.00
number of zones 20
estimated error
0.03 0.03 0.03 0.03 0.03
0.03 0.03 0.03 0.03 0.03
0.03 0.03 0.03 0.03 0.03
0.03 0.03 0.03 0.03 0.03
error scale factor 1.3
default scale 10
rejection probability 0.0001
reference film 6
scale restrain 0.01
fix b
print cc1/2
space group C2
output file 'output2.sca'
ignore overloads
intensity bins
@postref.in
postrefine 0
format denzo_ip
@sector.dat"""

comfile.write(comstr)
comfile.close()

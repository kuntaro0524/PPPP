import sys,os,math

xfiles=open("xfiles.dat","r").readlines()

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

idx=0
postref_sectors=""
for postref in postref_bufs:
	idx+=1
	postref_sectors+="%s"%postref
	if idx%3==0:
		postref_sectors+="\n"

print postref_sectors
print "add partials ",postref_sectors
	
	#print "add partials 

#print postref_bufs
"""
add partials 1 to 5 6 to 10 11 to 15
16 to 20 21 to 25 26 to 30
"""

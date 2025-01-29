import sys,os,math

lines=open(sys.argv[1],"r").readlines()

time=lines[0].split()[1]

print time,

idx=0
for line in lines:
	#print line,

	# FE slit Vert, Hori position
	if line.rfind("##### Front End ####")!=-1:
		fe_vert=float(lines[idx+1].split()[2])
		fe_hori=float(lines[idx+2].split()[2])
		print "%8.3f %8.3f"%(fe_vert,fe_hori),

	# TCS slit Vert, Hori position
	if line.rfind("##### TC slit ####")!=-1:
		tcs_vert=float(lines[idx+3].split()[2])
		tcs_hori=float(lines[idx+4].split()[2])
		print "%8.3f %8.3f"%(tcs_vert,tcs_hori),

	# Ty1 value
	if line.rfind("Ty1")!=-1:
		ty1=int(line.split()[2])
		print "%8d"%ty1,

	# Mirror parameters
	if line.rfind("VFM-z")!=-1:
		vfmz=int(line.split()[2])
		print "%8d"%vfmz,
	if line.rfind("HFM-y")!=-1:
		hfmy=int(line.split()[2])
		print "%8d"%hfmy
	idx+=1


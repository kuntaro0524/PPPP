
f=open("130_12.398000_gonioz_drv.scn","r")

lines=f.readlines()

for i in range(0,len(lines)):
	line=lines[i]
	line=line.strip()
	print "1234 %s 1234\n" % line,

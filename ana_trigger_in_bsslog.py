import os,sys,math

lines=open(sys.argv[1],"r").readlines()

for line in lines:
	if line.rfind("FILE_NAME")!=-1:
		print line,
	if line.rfind("scan_from")!=-1:	
		print line,
	if line.rfind("mode=")!=-1:	
		print line,
	if line.rfind("center #")!=-1:	
		print line,
	if line.rfind("frate")!=-1:
		print line
	if line.rfind("goniometer moves to crystal")!=-1:
		print line,
	if line.rfind("trigger")!=-1:
		print line,

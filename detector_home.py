import sys,os,math

if len(sys.argv)!=3:
	print "Usage: python this_program BSS_CAMERALENGTH FIT2D_CAMERALENGTH"
	sys.exit(1)

bss_cl=float(sys.argv[1])
fit2d_cl=float(sys.argv[2])

bssconfig="/isilon/blconfig/bl32xu/bss/bss.config"

lines=open(bssconfig,"r").readlines()

# Reading home_shift
# Detector 1_x axis
idx=0
for line in lines:
	if line.rfind("detector_1_x")!=-1:
		break
	idx+=1

for line in lines[idx:]:
	if line.rfind("_axis_end")!=-1:
		break
	if line.rfind("_home_value")!=-1:
		if line[0]!="#":
			cols=line.split(':')
			home_value=float(cols[1])
			#print home_value

new=home_value-(bss_cl-fit2d_cl)

print "_home_value: %8.3f"%new

print "(old _home_value = %8.3f)"%home_value

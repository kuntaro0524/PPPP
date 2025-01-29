import os,sys
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import XDSascii
import XSCALEinp

# relative directory
#if len(sys.argv)==3:
	#rel_dir=sys.argv[2]


#print rel_dir
# XSCALE.INP reading
xsi=XSCALEinp.XSCALEinp(sys.argv[1])
input_xds_list=xsi.getInputList()

dsets=[]

ofile=open("list_for_xscale.dat","w")

score_list=[]
for xa in input_xds_list:
	filepath="../%s"%xa
        xdsas=XDSascii.XDSascii(filepath)
	sumi=xdsas.calcDP()
	score_list.append((filepath,sumi))

score_list.sort(key=lambda x:x[1])

for com in score_list:
	xa,sumi=com
	ofile.write("INPUT_FILE=%-100s ! %10.1f\n"%(xa,sumi))

ofile.close()

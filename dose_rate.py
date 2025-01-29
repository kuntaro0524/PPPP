import sys,os,math,numpy
from File import *
from Gonio import *
f=File("./")

def gen_schedule(outdir,prefix,att_index,exptime,gx,gy,gz,serialoffset,cl):
	lines=open("/isilon/BL32XU/BLsoft/PPPP/template.sch").readlines()
	for line in lines:
		#OUTDIR
		line=line.replace("OUTDIR",outdir)
		#PREFIX
		line=line.replace("PREFIX",prefix)
		#EXPTIME
		string="%8.2f"%exptime
		line=line.replace("EXPTIME",string)
		#SERIALOFFSET
		string="%10d"%serialoffset
		line=line.replace("SERIALOFFSET",string)
		#GX,GY,GZ
		sx="%8.5f"%gx
		sy="%8.5f"%gy
		sz="%8.5f"%gz
		line=line.replace("GX",sx)
		line=line.replace("GY",sy)
		line=line.replace("GZ",sz)
		#ATTTHICK
		string="%5d"%att_index
		line=line.replace("ATTTHICK",string)
		#CL
		string="%10.1f"%cl
		line=line.replace("CL",string)
		print line,

##############################################################################
# CONDITION
#host = '192.168.163.1'
host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
g=Gonio(s)

outdir=f.getAbsolutePath()+"/"
cen_xyz=g.getXYZmm()
att_index=7
cl=200.0

##############################################################################

# Unit [um]
y_diff=numpy.arange(-7.5,7.5+0.5,0.5)
z_diff=numpy.arange(-7.5,7.5+0.5,0.5)

for tidx in range(0,5):
	# Horizontal scan for LD
	serial_offset=0
	prefix="lh%02d"%tidx
	for yd in y_diff:
		cx,cy,cz=cen_xyz[0],cen_xyz[1],cen_xyz[2]
		gx=cx
		gy=cy+yd/1000.0
		gz=cz
		gen_schedule(outdir,prefix,att_index,0.1,gx,gy,gz,serial_offset,cl)
		serial_offset+=1

	# Vertical scan for LD
	serial_offset=0
	prefix="lv%02d"%tidx
	for zd in z_diff:
		cx,cy,cz=cen_xyz[0],cen_xyz[1],cen_xyz[2]
		gx=cx
		gy=cy
		gz=cz+zd/1000.0
		gen_schedule(outdir,prefix,att_index,0.1,gx,gy,gz,serial_offset,cl)
		serial_offset+=1

	# High dose scan
	cx,cy,cz=cen_xyz[0],cen_xyz[1],cen_xyz[2]
	prefix="hd%02d"%tidx
	gen_schedule(outdir,prefix,0,0.05,gx,gy,gz,0,cl)

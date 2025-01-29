
import sys
from Zoom import *
from Gonio import *
from Capture import *
from TemplateMatch import *

if __name__=="__main__":

        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	# option
	op="BOTH"
	if len(sys.argv)!=1:
		op=sys.argv[1]

	# Low magnification template image
	tmplow_ppm="/isilon/BL32XU/BLsoft/PPPP/01.Data/00.CenteringPictures/TemplateFile/template_low.ppm"
	# Low magnification template image
	tmphigh_ppm="/isilon/BL32XU/BLsoft/PPPP/01.Data/00.CenteringPictures/TemplateFile/template_high.ppm"

	# Output ppm file
	odir="/isilon/users/target/target/Staff/"
	tmpfile="tmp_needle.ppm"
	ofile=odir+tmpfile

	# Output log file
	zz_db_file="/isilon/users/target/target/Staff/zz_db.txt"
	zzf=open(zz_db_file,"a")

	gonio=Gonio(s)
        cap=Capture()
	zoom=Zoom(s)

	z1=0

	# Initial information
	d=datetime.datetime.now()
	init_zz=gonio.getZZmm()*1000.0
	zzf.write("%s"%d,)

	# Pixel resolution
	## Low magnification 
	pix2um_lowz=10.0/14.5  # [um/pixel]
	pix2um_lowy=10.0/16.0  # [um/pixel]
	pix2um_highz=1.0/26.75 # [um/pixel]
	pix2um_highy=5.0/67.0  # [um/pixel]

	# Center cross position in pixels
	cross_low_y=271
	cross_high_z=215
	#cross_high_y=

	if op=="BOTH":
		# for low magnification
		zoom.zoomOut()

		# Alignment of needle
		for i in range(0,3):
			for phistart in [0.0, 90.0]:
				# first phi
				gonio.rotatePhi(phistart)
        			cap.capture(ofile)
				tm=TemplateMatch(tmplow_ppm,ofile)
				y0,z0=tm.getXY()
		
				# phi 180 relative
				gonio.rotatePhi(phistart+180.0)
        			cap.capture(ofile)
				tm=TemplateMatch(tmplow_ppm,ofile)
				y1,z1=tm.getXY()
	
				# average y0,y1 position
				yave=(y0+y1)/2.0

	        		movey_pix=cross_low_y-yave
	        		movey_um=movey_pix*pix2um_lowy
	
	        		gonio.moveTrans(movey_um)
	
				diff1=(z1-z0)
				dist=diff1*pix2um_lowz/2.0
				gonio.moveUpDown(dist)

	# for high magnification
	zoom.zoomIn()
	# Y axis tune first
	cap.capture(ofile)
	tm=TemplateMatch(tmphigh_ppm,ofile)
	y0,z0=tm.getXY()
	#tm.show()
	movey_pix=272-y0
	movey_um=movey_pix*pix2um_highy
	gonio.moveTrans(movey_um)

	# Alignment of needle at High magnification factor
	for i in range(0,3):
		for phistart in [0.0, 90.0]:
			# first phi
			gonio.rotatePhi(phistart)
        		cap.capture(ofile)
			tm=TemplateMatch(tmphigh_ppm,ofile)
			y0,z0=tm.getXY()
	
			# phi 180 relative
			gonio.rotatePhi(phistart+180.0)
        		cap.capture(ofile)
			tm=TemplateMatch(tmphigh_ppm,ofile)
			y1,z1=tm.getXY()

			# average y0,y1 position
			#yave=(y0+y1)/2.0
	        	#movey_pix=originy-yave
	        	#movey_um=movey_pix*pix2um_highy
	        	#gonio.moveTrans(movey_um)
	
			diff1=(z1-z0)
			dist=diff1*pix2um_highz/2.0
			gonio.moveUpDown(dist)

	# ZZ alignment
	#cap.capture(ofile)
	#tm=TemplateMatch(tmphigh_ppm,ofile)
	#z1=tm.getXY()[1]
	#hari_center=z1+89
	#diffp=cross_high_z-hari_center
	#movep=-diffp*pix2um_highz
	#gonio.moveZZrel(movep)

	# final information
	final_zz=gonio.getZZmm()*1000.0
	diff=final_zz-init_zz
	zzf.write("Initial: %12.5f [um] Final:%12.5f [um] delta(ZZ): %12.5f [um]"%(init_zz,final_zz,diff))

	cap.disconnect()

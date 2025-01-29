import sys
import time
from Zoom import *
from Gonio import *
from Capture import *
from TemplateMatch import *

class CenteringNeedle:

	def __init__(self,gonio,capture,zoom):
		self.gonio=gonio
		self.cap=capture
		self.zoom=zoom

	def dataZ(self):
		ooo=open("Y.dat","w")

		self.gonio.moveUpDown(-3.0)

		for i in range(0,5):
			# Output ppm file
			odir="/isilon/users/target/target/Staff/BLtune/"
			tmpfile="high_needle_%03d.ppm"%i
			ofile=odir+tmpfile

			move_um=1.0
			self.gonio.moveUpDown(move_um)

                	# Low magnification template image
                	tmplow_ppm="/isilon/BL32XU/BLsoft/PPPP/01.Data/00.CenteringPictures/TemplateFile/template_low.ppm"

                        # first phi
                        self.cap.capture(ofile)
			time.sleep(1)
                        tm=TemplateMatch(tmplow_ppm,ofile)
                        y0,z0=tm.getXY()
			#tm.show()

			## current gonio
			z=self.gonio.getZmm()*1000.0

			moved=move_um*i

			ooo.write("%8.5f %8.5f %8.5f %8.5f\n"%(moved,z,y0,z0))
			time.sleep(1)

		ooo.close()

	def dataY(self):
		ooo=open("Y.dat","w")

		self.gonio.moveTrans(-5.0)

		for i in range(0,5):
			# Output ppm file
			odir="/isilon/users/target/target/Staff/BLtune/"
			tmpfile="high_needle_%03d.ppm"%i
			ofile=odir+tmpfile

			move_um=1.0
			self.gonio.moveTrans(move_um)

                	# Low magnification template image
                	tmplow_ppm="/isilon/BL32XU/BLsoft/PPPP/01.Data/00.CenteringPictures/TemplateFile/template_low.ppm"

                        # first phi
                        self.cap.capture(ofile)
			time.sleep(1)
                        tm=TemplateMatch(tmplow_ppm,ofile)
                        y0,z0=tm.getXY()
			#tm.show()

			## current gonio
			y=self.gonio.getYmm()*1000.0

			moved=move_um*i

			ooo.write("%8.5f %8.5f %8.5f %8.5f\n"%(moved,y,y0,z0))
			time.sleep(1)

		ooo.close()

	def dataZZ(self):
		self.gonio.moveZZrel(-3.0)

		ooo=open("ZZ.dat","w")
		for i in range(1,6):
			move_um=1.0
			self.gonio.moveZZrel(move_um)

			# High magnification template image
			tmphigh_ppm="/isilon/BL32XU/BLsoft/PPPP/01.Data/00.CenteringPictures/TemplateFile/template_high.ppm"

			# Output ppm file
			odir="/isilon/users/target/target/Staff/tmp/"
			tmpfile="high_needle_%03d.ppm"%i
			ofile=odir+tmpfile

			curr_zz=gonio.getZZmm()*1000.0

			self.cap.capture(ofile,10000)
			tm=TemplateMatch(tmphigh_ppm,ofile)
			y0,z0=tm.getXY()
			tm.show()

			ooo.write("%8.5f %8.5f %8.5f\n"%(curr_zz,y0,z0))

		ooo.close()

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        gonio=Gonio(s)
        capture=Capture()
	zoom=Zoom(s)

        p=CenteringNeedle(gonio,capture,zoom)
	#p.centeringLow()
	#p.centeringHigh()
	p.dataZZ()
	#p.dataY()
	#p.dataZ()


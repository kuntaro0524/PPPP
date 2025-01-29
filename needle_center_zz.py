from NeedlePicture import *
from Gonio import *
from Capture import *
from Light import *
import math
from Zoom import *

class RotationCenter:
	def __init__(self):
        	#host = '192.168.163.1'
        	host = '172.24.242.41'
        	port = 10101
        	self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        	self.s.connect((host,port))
		self.isPrep=False
		self.cap=Capture()
		self.gonio=Gonio(self.s)
		self.light=Light(self.s)
		self.zoom=Zoom(self.s)
		self.f=File("./")

	def prep(self):
		self.light.on()
		self.isPrep=True

	def zoomIn(self):
		self.zoom.zoomIn()

	def finish(self):
		self.light.off()
		self.isPrep=False
		self.cap.disconnect()

	def capturePos(self):
		rotang=self.gonio.getPhi()
		filename="%s/needle_%fdeg.ppm"%(self.f.getAbsolutePath(),rotang)
		self.cap.capture(filename,1200)
		fwhm,center=self.capAna(filename)
		return fwhm,center

	def captureRot(self,rotang):
		# making a file name
		filename="%s/needle_%fdeg.ppm"%(self.f.getAbsolutePath(),rotang)
		if self.isPrep==False:
			self.prep()
		self.gonio.rotatePhi(rotang)
		self.cap.capture(filename,1200)
		fwhm,center=self.capAna(filename)

		print "FINISHED CaptureROT"
		return fwhm,center

	def tuneGonioZZ(self):
		savep=self.gonio.getZZ()
		fwhm,center=self.capturePos()
		print "FWHM CENTER:"
		print fwhm,center

		diff=center-240
		print "CENTER ZURE",diff
        	pix2um_highz=0.07125   # [um/pixel]
		diff_um=diff*pix2um_highz
		#print diff_um

		# GONIO ZZ PULSE
		curr_zz=self.gonio.getZZ()
		relmove=int(diff_um/0.5)
		target=curr_zz+relmove
		self.gonio.moveZZpulse(target)
        	print "Final position=",self.gonio.getZZ()

	def tuneGonio(self,phi1,phi2):
       		# Pixel resolution
        	pix2um_highz=0.07125   # [um/pixel]
        	pix2um_highy=0.07327   # [um/pixel]

		while(1):
			f1,c1=self.captureRot(phi1)
			if f1!=0.0 and c1!=0.0:
				break
		while(1):
			f2,c2=self.captureRot(phi2)
			if f2!=0.0 and c2!=0.0:
				break

		## Diff [pix]
		diff=c1-c2
		diff_um=diff*pix2um_highz
	
		print "DIFF: %8.3f [um]\n"%diff_um

		self.gonio.moveUpDown(-diff_um)
		return math.fabs(diff_um)
		
	def capAna(self,needle_pic):
        	np=NeedlePicture(needle_pic)
		fwhm,center=np.getCenterFWHM()
		return fwhm,center

if __name__=="__main__":

	rc=RotationCenter()
	rc.tuneGonioZZ()

	#curr=rc.capturePos()




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

	def captureRot(self,rotang):
		# making a file name
		filename="%s/needle_%fdeg.ppm"%(self.f.getAbsolutePath(),rotang)
		if self.isPrep==False:
			self.prep()
		self.gonio.rotatePhi(rotang)
		#filename="%s/test.ppm"%self.f.getAbsolutePath()
		self.cap.capture(filename,1200)
		fwhm,center=self.capAna(filename)

		#print "FINISHED CaptureROT"
		return fwhm,center

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
		return diff_um
		
	def capAna(self,needle_pic):
        	np=NeedlePicture(needle_pic)
		fwhm,center=np.getCenterFWHM()
		return fwhm,center

if __name__=="__main__":

	rc=RotationCenter()

	while(1):
		d1=rc.tuneGonio(0,180)
		d2=rc.tuneGonio(90,270)

		if fabs(d1)<0.5 and fabs(d2)<0.5:
			break

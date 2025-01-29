#from opencv.cv import LoadImageM
#from opencv.highgui import *

from Gonio import *
from Capture import *

import Image
import os
import sys
from opencv.cv import *
from opencv.highgui import *

## Z
## 5um = 67pulse (2 ave)

## Y
## 10um = 136pix

class TemplateMatch:
	def __init__(self,template_ppm,target_ppm):
		self.template_ppm=template_ppm
		self.target_ppm=target_ppm

	def setNewTarget(self,target_ppm):
		self.target_ppm=target_ppm

	def getXY(self):
		self.tmp_img=cvLoadImage(self.template_ppm)
		self.obj_img=cvLoadImage(self.target_ppm)
		dst_size=cvSize(self.obj_img.width-self.tmp_img.width+1,self.obj_img.height-self.tmp_img.height+1)
		dst_img=cvCreateImage(dst_size,IPL_DEPTH_32F,1)
		cvMatchTemplate(self.obj_img,self.tmp_img,dst_img,CV_TM_CCOEFF_NORMED)

		self.p1=CvPoint()
		self.p2=CvPoint()
		status=cvMinMaxLoc(dst_img,self.p1,self.p2)

		return self.p2.x,self.p2.y

	def show(self):
		corner_point=cvPoint(self.p2.x+self.tmp_img.width,self.p2.y+self.tmp_img.height)
		cvRectangle(self.obj_img,self.p2,corner_point,CV_RGB(255,0,0),2)
		cvCircle(self.obj_img,self.p2,5,CV_RGB(255,0,0),2)
		cvNamedWindow("image",1)
		cvShowImage("image",self.obj_img)
		cvWaitKey(0)

if __name__=="__main__":

        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	gonio=Gonio(s)
        cap=Capture()

        tmphighppm="/isilon/BL32XU/BLsoft/PPPP/01.Data/00.CenteringPictures/TemplateFile/template_high.ppm"

	z1=0

	for i in range(0,3):
		# Set to phi=0.0deg
		gonio.rotatePhi(0.0)
		ofile="/isilon/users/target/target/ppp.ppm"
        	cap.capture(ofile)
		tm=TemplateMatch(tmphighppm,ofile)
		z0=tm.getXY()[1]
		tm.show()
	
		# Set to phi=180.0deg
		gonio.rotatePhi(180.0)
		ofile="/isilon/users/target/target/ppp.ppm"
        	cap.capture(ofile)
		tm=TemplateMatch(tmphighppm,ofile)
		z1=tm.getXY()[1]
		tm.show()

		diff1=(z1-z0)
		print z0,z1,diff1
		dist=diff1/float(67)*5.0/2.0
		gonio.moveUpDown(dist)

	for i in range(0,3):
		# Set to phi=90.0deg
		gonio.rotatePhi(90.0)
		ofile="/isilon/users/target/target/ppp.ppm"
        	cap.capture(ofile)
		tm=TemplateMatch(tmphighppm,ofile)
		z0=tm.getXY()[1]
		tm.show()
	
		# Set to phi=270.0deg
		gonio.rotatePhi(270.0)
		ofile="/isilon/users/target/target/ppp.ppm"
        	cap.capture(ofile)
		tm=TemplateMatch(tmphighppm,ofile)
		z1=tm.getXY()[1]
		tm.show()

		diff1=(z1-z0)
		dist=diff1/float(67)*5.0/2.0
		gonio.moveUpDown(dist)

	#tm.setNewTarget("phi0_gonioz_0.10mm.ppm")
	#z1=tm.getXY()[1]
	#tm.show()

	#tm.setNewTarget("phi0_gonioz_0.20mm.ppm")
	#z2=tm.getXY()[1]
	#tm.show()

	#diff1=z1-z0
	#diff2=z2-z1

	#print diff1,diff2

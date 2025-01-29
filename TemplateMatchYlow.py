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

        tmplowppm="/isilon/BL32XU/BLsoft/PPPP/01.Data/00.CenteringPictures/TemplateFile/template_low.ppm"

	gonio=Gonio(s)
        cap=Capture()

	z1=0

	# Set to phi=0.0deg
	ofile="/isilon/users/target/target/ppp.ppm"
       	cap.capture(ofile)

	tm=TemplateMatch(tmplowppm,ofile)
	y1=tm.getXY()[0]
	tm.show()

	# Movement
	originy=271

	movey_pix=originy-y1
	movey_um=movey_pix/16*10.00
	
	gonio.moveTrans(movey_um)

import cv2
import copy
import sys
import numpy as np
import socket
from Inocc2 import *

WIDTH = 640
HEIGHT = 480
SELECT_COLOUR = (255, 0, 0)  # blue
SAVE_COLOUR = (0, 255, 0)	# green
default_ouput = "cropped.jpg"

class DrawRectangleMouse:
	def __init__(self,imagefile):
		self.original = cv2.imread(imagefile)
		cv2.namedWindow('Original image')
		cv2.imshow('Original image', self.original)
		self.isDrawing = False
		self.x0=0
		self.y0=0
		self.isLocked = False
		self.isStarted = False

	'''Displays original image with coloured rectangle indicating cropping area
   	and updates the displayed cropped image'''
	def update(self,endx, endy, colour=SELECT_COLOUR):
		print "UPDATE"
		img = np.copy(self.original)
		cv2.rectangle(img, (self.x0, self.y0), (endx, endy), colour, 3)
		self.cenx=(self.x0+endx)/2.0
		self.ceny=(self.y0+endy)/2.0
		cv2.circle(img,(self.cenx,self.ceny),5,(0,0,255),2)
	
		self.width=np.fabs(endx-self.x0)
		self.height=np.fabs(endy-self.y0)
	
		location=(0,30)
		fontscale=1.0
		color=(255,190,0) #sky blue  
		fontface=cv2.FONT_HERSHEY_PLAIN
		msg="Rectanglar Width = %5d , Height = %5d"%(self.width,self.height)
		cv2.putText(img,msg,location,fontface,fontscale,color)  
	
		cv2.imshow('Original image', img)

	def show_cropped(self,event, x, y, flags, param):
		'''Mouse callback function - updates position of mouse and determines
	   	if image display should be updated.'''
		endx,endy=0,0
	
		if event == cv2.EVENT_RBUTTONDOWN:
			print "Locked = false"
			self.x0,self.y0=0,0
			self.update(0,0)
			self.isLocked=False
			self.isStarted=False
	
		if event == cv2.EVENT_LBUTTONDOWN:
			if self.isLocked==False:
				self.isDrawing = True
				self.isStarted = True
				self.x0,self.y0=x,y
				endx,endy=x,y
			else:
				self.isDrawing = False
				print "ONakaippai"
	
		if event == cv2.EVENT_LBUTTONUP:
			print "BUTTONUP"
			self.isDrawing = False
			endx,endy=x,y
			self.isStarted=False
			self.isLocked=True
	
		if event == cv2.EVENT_MOUSEMOVE:
			if self.isStarted==False or self.isLocked==True:
				self.isDrawing=False
			else:
				print "Korekarakakuyo",self.isStarted,self.isLocked
				self.isDrawing = True
				print "MOVING",x,y
				endx,endy=x,y
		
			if self.isDrawing:
				print "DRAWING",self.x0,self.y0,endx,endy
				self.update(endx,endy)

	def run(self):
		'''Entry point'''
		cv2.setMouseCallback('Original image', self.show_cropped)
	
		while True:
			key = cv2.waitKey(1) & 0xFF  # 0xFF is for 64 bit computer
			if key == 27:  # escape
				break
			elif key == ord("s"):
				cv2.imwrite(args["output"], _cropped)
				self.update(self.x0, self.y0, colour=SAVE_COLOUR)
		
		cv2.destroyAllWindows()
		return self.cenx,self.ceny,self.width,self.height

if __name__ == '__main__':

	# Server setting
	ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ms.connect(("192.168.163.1", 10101))
	crycen=crycen(ms)

	phi,cenx,ceny,cenz=crycen.get_axes_info_float()
	print phi,cenx,ceny,cenz

	filename="/isilon/BL32XU/BLsoft/PPPP/03.GUI/04.SACLA-KUMA/capture.ppm"
	crycen.get_coax_image(filename, convert=False)

	# DrawRectangleMouse
	drm=DrawRectangleMouse(filename)
	cenx,ceny,width,height=drm.run()
	print cenx,ceny,width,height
	crycen.move_by_img_px(cenx,ceny)

        pix_size_um=crycen.get_pixel_size()
	print pix_size_um
	entire_width=pix_size_um*width
	entire_height=pix_size_um*height

	print "Width  = %8.1f[um]"%entire_width
	print "Height = %8.1f[um]"%entire_height

	print "Hori 10um beam: %5d"%(int(entire_width/10.0)+1)
	print "Vert 10um beam: %5d"%(int(entire_height/10.0)+1)

	ms.close()

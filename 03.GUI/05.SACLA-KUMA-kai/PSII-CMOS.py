import cv2
import copy
import sys
import numpy as np
import socket
import datetime
from DrawRectangleMouse import *
from Inocc2 import *

if __name__ == '__main__':
	ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ms.connect(("192.168.163.1", 10101))

	crycen=crycen(ms)
	phi,cenx,ceny,cenz=crycen.get_axes_info_float()
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

	steph=30.0 #um
	stepv=30.0 #um

	print "Width  = %8.1f[um]"%entire_width
	print "Height = %8.1f[um]"%entire_height

	np_h=int(entire_width/steph)
	np_v=int(entire_height/stepv)

	print "Hori %5.1f um step beam: %5d"%(steph,np_h)
	print "Vert %5.1f um step beam: %5d"%(stepv,np_v)

	# Step [um] -> Step [pixel]
	step_hpix=steph/pix_size_um
	step_vpix=stepv/pix_size_um

	# Start point # horizontal
	start_h=float(cenx)+(float(np_h)-1)/2.0*step_hpix
	start_v=float(ceny)+(float(np_v)-1)/2.0*step_vpix
	end_h=float(cenx)-(float(np_h)-1)/2.0*step_hpix
	end_v=float(ceny)-(float(np_v)-1)/2.0*step_vpix

	#print start_h,end_h
	#print start_v,end_v

	tttt = cv2.imread(filename)
	#cv2.namedWindow('test')
	#cv2.imshow('test',tttt)

	npoints=0
	for x in arange(start_h,end_h-step_hpix,-step_hpix):
		for y in arange(start_v,end_v-step_vpix,-step_vpix):
			npoints+=1
			#print x,y
			cv2.circle(tttt,(int(x),int(y)),0.5,(0,0,255),2)
	print "NPOINTS=%5d"%npoints

	fontscale=1.0
	location=(0,30)  
	fontface=cv2.FONT_HERSHEY_PLAIN
	color=(0,0,0)
	total_frames=np_h*np_v
	msg="(H,V)=(%d,%d)pts nFrames=%7d step=%5.2f[um]"%(np_h,np_v,total_frames,steph)
	cv2.putText(tttt,msg,location,fontface,fontscale,color)  
	location=(0,50)  
	msg="Time: %s"%(datetime.datetime.now())
	cv2.putText(tttt,msg,location,fontface,fontscale,color)  
	cv2.imshow("Checking irradiation points:",tttt)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	now=datetime.datetime.now()
	print now
	timestamp=now.strftime("%Y%m%d-%H%M")
	print timestamp
	imglog="PSII-%s.png"%timestamp
	cv2.imwrite(imglog,tttt)

	ms.close()

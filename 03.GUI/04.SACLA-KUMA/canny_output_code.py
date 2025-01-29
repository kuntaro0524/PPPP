# -*- coding: utf-8 -*-
import cv2
import numpy as np
  
if __name__ == '__main__':
	gray = cv2.imread("crystal.png",0)
	edge = cv2.Canny(gray,150,200)
	#print edge
	height,width=gray.shape
	print height,width
	print gray.size

### EDGE coordinates
	# height=480, width=640
	for x in np.arange(0,width-1):
		ya=[]
		for y in np.arange(0,height-1):
			min_pix=9999
			max_pix=-9999
			min_pix_flag=False
			if edge[y][x] > 200:
				print "OK"
				ya.append(y)
				"""
				if min_pix_flag==False:
					min_pix=y
					min_pix_flag=True
					continue
				if min_pix_flag==True and max_pix < y:
					max_pix=y
				"""
		print ya
		if len(ya)>2:
			yna=np.array(ya)
			ymin=yna.min()
			ymax=yna.max()
			print "Y min-max=",x,ymin,ymax
			#print min_pix,max_pix

	cv2.imshow("Show Image",edge)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

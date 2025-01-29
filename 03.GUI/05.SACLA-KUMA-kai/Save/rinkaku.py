# -*- coding: utf-8 -*-
import cv2,sys
import numpy as np
 
def main():
	im = cv2.imread(sys.argv[1])
	# Gray scale
	print cv2.COLOR_BGR2GRAY
	gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)				 
	# 2 valuize
	th = cv2.threshold(gray,127,255,0)[1]	   
	# Edge scan
	cnts = cv2.findContours(th,1,2)[0]						  
	# Search max edge
	areas = [cv2.contourArea(cnt) for cnt in cnts]
	cnt_max = [cnts[areas.index(max(areas))]][0]				
	# Draw max edge
	cv2.drawContours(im,[cv2.convexHull(cnt_max)],0,(255),-1)   
	# Results
	cv2.imshow("Show Image",im)								 
	cv2.waitKey(0)											  
	cv2.destroyAllWindows()									 

if __name__ == "__main__":
	main()

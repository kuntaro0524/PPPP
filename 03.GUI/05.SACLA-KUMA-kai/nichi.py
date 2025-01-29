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
	cv2.imshow("Show Image",th)								 
	cv2.waitKey(0)											  
	cv2.destroyAllWindows()									 

if __name__ == "__main__":
	main()

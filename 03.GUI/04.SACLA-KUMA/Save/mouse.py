# coding: UTF-8
import cv2
import numpy as np

global img
def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
		cv2.circle(img,(x,y),5,(255,0,0),-1)
		cv2.imshow('image',img)
		cv2.waitKey(0)

img = cv2.imread('crystal.png')
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)
cv2.imshow('image',img)

while(True):
	if cv2.waitKey(0):
		break
cv2.destroyAllWindows()

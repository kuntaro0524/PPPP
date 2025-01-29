import cv2
import numpy as np

img=cv2.imread('crystal.png',0)
cv2.line(img,(0,0),(50,50),(255,0,0),5)
cv2.rectangle(img,(50,20),(100,40),(0,255,0),3)

cv2.imshow('result',img)

cv2.waitKey(0)
cv2.destroyAllWindows()

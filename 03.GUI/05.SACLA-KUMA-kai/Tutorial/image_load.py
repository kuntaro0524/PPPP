import cv2
import numpy as np

img=cv2.imread('crystal.png')
cv2.imshow('result',img)

cv2.waitKey(0)
cv2.destroyAllWindows()

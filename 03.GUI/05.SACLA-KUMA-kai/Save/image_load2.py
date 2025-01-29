import cv2
import numpy as np

gray=cv2.imread('crystal.png',0)
cv2.imshow('result',gray)

cv2.waitKey(0)
cv2.destroyAllWindows()

# -*- coding: utf-8 -*-
import cv2
  
if __name__ == '__main__':
    gray = cv2.imread("crystal.png",0)
    edge = cv2.Canny(gray,100,200)
    cv2.imshow("Show Image",edge)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

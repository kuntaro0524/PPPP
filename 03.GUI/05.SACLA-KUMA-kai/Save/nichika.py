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
    for y in np.arange(0,height):
        for x in np.arange(0,width):
            #print x,y
            if edge[y][x]>250:
               print x,y

    cv2.imshow("Show Image",edge)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

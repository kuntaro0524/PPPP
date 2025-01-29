# -*- coding: utf-8 -*-
import cv2
 
def nothing(x):
    pass
 
if __name__ == '__main__':
 
    cv2.namedWindow("Canny")
    gray = cv2.imread("crystal.png",0)

    # Track bar
    cv2.createTrackbar("th1","Canny",0,255,nothing)
    cv2.createTrackbar("th2","Canny",0,255,nothing)

    while(1):
        # value from track bar
        th1 = cv2.getTrackbarPos("th1","Canny")
        th2 = cv2.getTrackbarPos("th2","Canny")
        # Edge
        edge = cv2.Canny(gray,th1,th2)
        # Display
        cv2.imshow('test',edge)
        # Termination
        k = cv2.waitKey(1)
        if k == 27:
            break
 
    cv2.destroyAllWindows()

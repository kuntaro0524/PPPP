import cv2,sys

img=cv2.imread(sys.argv[1])

imgray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh=cv2.threshold(imgray,127,255,0)
contours=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
#image,contours,hierarchy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(img,contours,-1,(0,255,0),3)
cv2.imshow("TEST",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
#img=cv2.drawContours(img,contours,3,(0,255,0),3)

#cnt=countrous[4]
#img=cv2.drawContours(img,[cnt],0,(0,255,0),3)

import cv2,sys


img = cv2.imread(sys.argv[1])
#cv2.namedWindow('TEST')
cv2.imshow("TEST",img)
cv2.waitKey(0)
cv2.destroyAllWindows()


import cv2

image=cv2.imread("cry01.png")
image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
humo=cv2.HuMoments(cv2.moments(image)).flatten()

# coding: UTF-8
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()	
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) &amp 0xFF == ord('q'):
        break

#全ての処理が終了したあとはストリームを解放
cap.release()
cv2.destroyAllWindows()


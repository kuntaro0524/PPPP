import cv2

cap = cv2.VideoCapture(1)

while(True):
	ret, frame = cap.read()
	frame = cv2.resize(frame, (int(frame.shape[1]*2), int(frame.shape[0]*2)))

	cv2.imshow('Raw frame', frame)
	
	edframe = frame
	cv2.putText(edframe, 'hogehoge', (0,50), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3, cv2.LINE_AA)
	
	cv2.imshow('Edited Frame', edframe)

	k = cv2.waitKey(1)
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()

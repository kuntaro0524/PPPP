import cv2
import numpy as np
 
def onMouse( event, x, y, flag, params ):
	wname, img = params
 
	if event == cv2.EVENT_MOUSEMOVE:
		img2 = np.copy( img )
		h, w = img2.shape[0], img2.shape[1]
		cv2.line( img2, ( x, 0 ), ( x, h - 1 ), ( 255, 0, 0 ) )
		cv2.line( img2, ( 0, y ), ( w - 1, y ), ( 255, 0, 0 ) )
		cv2.imshow( wname, img2 )
 	
	if event == cv2.EVENT_LBUTTONDOWN:
		print ( x, y )
 
wname = "lenna"
cv2.namedWindow( wname )
img = cv2.imread( "lenna.png" )
 
cv2.setMouseCallback( wname, onMouse, [ wname, img ] )
cv2.imshow( wname, img )
 
# exit when ESC-key is pressed
while cv2.waitKey( 0 ) != 27:
	pass
cv2.destroyAllWindows()  

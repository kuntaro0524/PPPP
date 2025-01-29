import cv2
import numpy as np
import sys

# Numpy 'empty' function
# np.empty(shape, dtype=None)
# Return a new array of given shape and type, without initializing entries.

drawing_box=False

cv2.rectangle(img,(50,20),(100,40),(0,255,0),3)
 	
def onMouse( event, x, y, flag, params ):
	wname, img, ptlist = params
 	
	if event == cv2.EVENT_MOUSEMOVE:
		if drawing == True:
			if mode==True:
				cv2.rectangle(img
		img2 = np.copy( img )
		h, w = img2.shape[0], img2.shape[1]
		cv2.line( img2, ( x, 0 ), ( x, h - 1 ), ( 255, 0, 0 ) )
		cv2.line( img2, ( 0, y ), ( w - 1, y ), ( 255, 0, 0 ) )
		cv2.imshow( wname, img2 )
 
	if event == cv2.EVENT_LBUTTONDOWN:
		drawing_box=True
		ix=x
		iy=y

	if event == cv2.EVENT_LBUTTONUP:
		drawing_box=False
		if ptlist.add( x, y ):
			print '[%d] ( %d, %d )' % ( ptlist.pos - 1, x, y )

wname = sys.argv[0]
cv2.namedWindow( wname )
RX, RY = 3, 3 # reduction ratio of images
npoints = 4
 
#fnList = [ "hoge.jpg", "cry.png" ]
fn="crystal.png"
 
img = cv2.imread( fn )
ptlist = PointList( npoints )
cv2.setMouseCallback( wname, onMouse, [ wname, img, ptlist ] )

while(1):
	img2=np.copy(img)
	if (drawing_box) :
		print ptlist
		#draw_box(img2,box)

#cv2.imshow("TEST",img2)
cv2.waitKey( 0 )
cv2.destroyAllWindows() 

print ptlist.getP()
 

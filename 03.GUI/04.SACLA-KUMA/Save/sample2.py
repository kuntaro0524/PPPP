import cv2
import numpy as np
import sys
 
 
class PointList():
	def __init__( self, npoints ):
		self.npoints = npoints
		self.ptlist = np.empty( ( npoints, 2 ), dtype = int )
		self.pos = 0
 	
	def add( self, x, y ):
		if self.pos < self.npoints:
			self.ptlist[self.pos, :] = [ x, y ]
			self.pos += 1
			return True
		return False
 	
def onMouse( event, x, y, flag, params ):
	wname, img, ptlist = params
 	
	if event == cv2.EVENT_MOUSEMOVE:
		img2 = np.copy( img )
		h, w = img2.shape[0], img2.shape[1]
		cv2.line( img2, ( x, 0 ), ( x, h - 1 ), ( 255, 0, 0 ) )
		cv2.line( img2, ( 0, y ), ( w - 1, y ), ( 255, 0, 0 ) )
		cv2.imshow( wname, img2 )
 
	if event == cv2.EVENT_LBUTTONDOWN:
		if ptlist.add( x, y ):
			print '[%d] ( %d, %d )' % ( ptlist.pos - 1, x, y )
			if ptlist.pos == ptlist.npoints:
				print 'All points have selected. Press ESC-key.'
		else:
			print 'All points have selected. Press ESC-key.'
 
wname = sys.argv[0]
cv2.namedWindow( wname )
RX, RY = 3, 3 # reduction ratio of images
npoints = 5
 
#fnList = [ "hoge.jpg", "cry.png" ]
fnList = [ "lenna.png"]
nimg = len( fnList )
ptarray = np.empty( ( nimg, npoints, 2 ), dtype = int )
 
for i, fn in enumerate( fnList ):
	print '##### [%d] %s' % ( i, fn )
	img_raw = cv2.imread( fn )
	img = cv2.resize( img_raw, ( img_raw.shape[1]/RX, img_raw.shape[0]/RY ) )
	ptlist = PointList( npoints )
	cv2.setMouseCallback( wname, onMouse, [ wname, img, ptlist ] )
	cv2.imshow( wname, img )
 
	while cv2.waitKey( 0 ) != 27:
		pass

	ptarray[i, :, :] = ptlist.ptlist * [ RX, RY ]
 
cv2.destroyAllWindows() 

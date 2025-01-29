import cv2
import numpy as np
import sys

# Numpy 'empty' function
# np.empty(shape, dtype=None)
# Return a new array of given shape and type, without initializing entries.
 
class PointList():
	def __init__( self, npoints ):
		self.npoints = npoints
	
		# array for post-treatment
		self.ptlist = np.empty( ( npoints, 2 ), dtype = int )

		# Number of points already 'Left cricked'
		self.pos = 0
 	
	def add( self, x, y ):
		print self.pos, self.ptlist
		if self.pos < self.npoints:
			self.ptlist[self.pos, :] = [ x, y ]
			self.pos += 1
			return True
		return False
 	
def onMouse( event, x, y, flag, params ):
	wname, img, ptlist = params
 	
	#if event == cv2.EVENT_MOUSEMOVE:
		#img2 = np.copy( img )
		#h, w = img2.shape[0], img2.shape[1]
		#cv2.line( img2, ( x, 0 ), ( x, h - 1 ), ( 255, 0, 0 ) )
		#cv2.line( img2, ( 0, y ), ( w - 1, y ), ( 255, 0, 0 ) )
		#cv2.imshow( wname, img2 )
 
	if event == cv2.EVENT_LBUTTONDOWN:
		if ptlist.add( x, y ):
			print '[%d] ( %d, %d )' % ( ptlist.pos - 1, x, y )
			if ptlist.pos == ptlist.npoints:
				print 'All points have selected. Press ESC-key.'
		else:
			print ptlist.ptlist
			img2 = np.copy( img )
			xy_tuples=[]
			for point in ptlist.ptlist:
				x,y=point
				xy_tuples.append((x,y))
			
			for n in np.arange(1,ptlist.npoints):
				cv2.line( img2, xy_tuples[n-1], xy_tuples[n], (255,0,0))
			cv2.line( img2, xy_tuples[n], xy_tuples[0], (255,0,0))
			cv2.imshow( wname, img2 )
 
wname = sys.argv[0]
cv2.namedWindow( wname )
RX, RY = 3, 3 # reduction ratio of images
npoints = 4
 
#fnList = [ "hoge.jpg", "cry.png" ]
fnList = [ "crystal.png"]
nimg = len( fnList )
ptarray = np.empty( ( nimg, npoints, 2 ), dtype = int )
 
for i, fn in enumerate( fnList ):
	print '##### [%d] %s' % ( i, fn )
	img = cv2.imread( fn )
	#img = cv2.resize( img_raw, ( img_raw.shape[1]/RX, img_raw.shape[0]/RY ) )
	ptlist = PointList( npoints )
	cv2.setMouseCallback( wname, onMouse, [ wname, img, ptlist ] )
	cv2.imshow( wname, img )
 
	while cv2.waitKey( 0 ) != 27:
		pass

	ptarray[i, :, :] = ptlist.ptlist * [ RX, RY ]
 
cv2.destroyAllWindows() 

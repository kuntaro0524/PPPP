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
		#print self.pos, self.ptlist
		if self.pos < self.npoints:
			self.ptlist[self.pos, :] = [ x, y ]
			self.pos += 1
			return True
		return False

	def getP(self):
		return self.ptlist

	def clearAll(self):
		self.pos=0
		print "All saved points are deleted."
		self.ptlist=np.empty((self.npoints,2),dtype=int)

class DrawPolygon():
	def __init__(self):
		self.flag=False

	def onMouse(self, event, x, y, flag, params ):
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
	
		if event == cv2.EVENT_MBUTTONDOWN:
			#print ptlist.ptlist
			img2 = np.copy( img )
			xy_tuples=[]
	
			xtotal=0
			ytotal=0
			for point in ptlist.ptlist:
				x,y=point
				xtotal+=x
				ytotal+=y
				xy_tuples.append((x,y))
	
			# Drawing the center of gravity
			grav_x=int(xtotal/float(ptlist.npoints))
			grav_y=int(ytotal/float(ptlist.npoints))
	
			print "Gravity:",grav_x,grav_y
				
			for n in np.arange(1,ptlist.npoints):
				cv2.line( img2, xy_tuples[n-1], xy_tuples[n], (255,0,0))
	
			cv2.line( img2, xy_tuples[n], xy_tuples[0], (255,0,0))
			cv2.circle(img2,(grav_x,grav_y),5,(0,255,255),-1)
			cv2.imshow( wname, img2 )
	
		if event == cv2.EVENT_RBUTTONDOWN:
			print "Clear saved positions"
			ptlist.clearAll()
			img2 = np.copy( img )
			cv2.imshow( wname, img2 )
 	
	def run(self,imagename):
		wname = "Click 4 times to define a square & Push center mouse button"
		cv2.namedWindow( wname )
		npoints = 4
 	
		#fnList = [ "hoge.jpg", "cry.png" ]
		img = cv2.imread(imagename)
		ptlist = PointList( npoints )
		cv2.setMouseCallback( wname, self.onMouse, [ wname, img, ptlist ] )
		cv2.imshow( wname, img )
		cv2.waitKey( 0 )
		print ptlist.getP()
		cv2.destroyAllWindows() 
		# Drawing the center of gravity
		xtotal=0
		ytotal=0
		xylist=[]
		for point in ptlist.ptlist:
			x,y=point
			xylist.append((x,y))
			xtotal+=x
			ytotal+=y
		# Drawing the center of gravity
		grav_x=int(xtotal/float(ptlist.npoints))
		grav_y=int(ytotal/float(ptlist.npoints))
		return grav_x,grav_y,xylist

if __name__ == "__main__":
	dpm=DrawPolygon()
	print dpm.run("crystal.png")
	#print crycen.get_pixel_size()
	#crycen.get_coax_image("/isilon/BL32XU/BLsoft/PPPP/03.GUI/04.SACLA-KUMA/test.ppm", convert=False)
	#crycen.move_by_img_px(157,167)

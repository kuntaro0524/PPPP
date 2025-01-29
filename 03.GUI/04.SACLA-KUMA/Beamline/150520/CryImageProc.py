import cv2,sys,math
import numpy as np

class CryImageProc():
	def __init__(self,imagefile):
		self.imagefile=imagefile

	def canny2(self,c1=150,c2=200,aperture_size=3):
		im = cv2.imread(self.imagefile)
		im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		cv2.GaussianBlur(im_gray, (3,3), 0, im_gray)
		kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(9,9))
		dilated = cv2.dilate(im_gray, kernel)
		im_edge = cv2.Canny(dilated, c1,c2,aperture_size)
		cv2.imshow("Show Image",im_edge)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		return im_edge

	def canny(self,low_thresh=50,high_thresh=200):
		gray = cv2.imread(self.imagefile,0)
		self.edge = cv2.Canny(gray,low_thresh,high_thresh)

		self.height,self.width=gray.shape
		print "Height:",self.height	
		print "Width :",self.width

		self.edge_min_max(self.edge)
		cv2.imshow("Show Image",self.edge)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	def edge_min_max(self,np_image):
		saved_point=[]
		for y in np.arange(0,self.height):
			for x in np.arange(0,self.width):
				if np_image[y][x]>250:
					saved_point.append((x,y))
		nas=np.array(saved_point)
		for e in nas:
			print e
		#print nas

if __name__ == "__main__":
	cip=CryImageProc(sys.argv[1])
	cip.canny()

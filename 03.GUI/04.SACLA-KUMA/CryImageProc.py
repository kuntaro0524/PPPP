import cv2,sys,math
import numpy as np
import pylab as plt

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
		for x in np.arange(0,self.width):
			for y in np.arange(0,self.height):
				if np_image[y][x]>250:
					saved_point.append((x,y))
		nas=np.array(saved_point)
		#for e in nas:
			#print e
		#print nas

# Example
#http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html

	def contours(self,imagefile):
		img = cv2.imread(imagefile,0)
		ret,thresh = cv2.threshold(img,127,255,0)
		contours,hierarchy = cv2.findContours(thresh, 1, 2)
		cnt = contours[0]
		M = cv2.moments(cnt)
		print M

	def rotatedRectangle(self):
		img = cv2.imread(self.imagefile,0)
		ret,thresh = cv2.threshold(img,127,255,0)
		contours,hierarchy = cv2.findContours(thresh, 1, 2)
		cnt = contours[0]
		M = cv2.moments(cnt)
		print M

		x,y,w,h=cv2.boundingRect(cnt)
		imim=cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		rect = cv2.minAreaRect(cnt)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		im = cv2.drawContours(im,[box],0,(0,0,255),2)

	def labeling(self):
    		im = cv2.imread(self.imagefile)
		gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) # Gray trans
		th = cv2.threshold(gray,127,255,0)[1]       # 2 chika
		# Edge extraction
		cnts = cv2.findContours(th,1,2)[0]          # Rinkaku
		cv2.drawContours(im,cnts,-2,(255,0,0),-1)   # Max rinkaku
		# Results
		cv2.imshow("Show Image",im)                 # display
		cv2.waitKey(0)                              # Wait keys
		cv2.destroyAllWindows()                     # Window destroy

	def labeling2(self):
		im = cv2.imread(self.imagefile)
		gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		th = cv2.threshold(gray,30,150,0)[1]
		cnts = cv2.findContours(th,1,2)[0]		
		areas = [cv2.contourArea(cnt) for cnt in cnts]
		cnt_max = [cnts[areas.index(max(areas))]][0]
		cv2.drawContours(im,[cv2.convexHull(cnt_max)],0,(255),-1)   
		cv2.imshow("Show Image",im)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	def rinkaku(self):
		im = cv2.imread(self.imagefile)
		im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		#im_gray_smooth=cv2.GaussianBlur(im_gray,(11,11),0)
		ret,th1 = cv2.threshold(im_gray,130,255,cv2.THRESH_BINARY)
		contours, hierarchy = cv2.findContours(th1,cv2.RETR_TREE,\
                                       cv2.CHAIN_APPROX_SIMPLE)
		cv2.drawContours(im,contours,-1,(0,255,0),3)
		plt.title('input image')
		plt.subplot(2,2,2),plt.imshow(im,'gray')
		plt.title('output image')
		#plt.subplot(2,2,3),plt.imshow(im_gray_smooth,'gray')
		#plt.title("Gray+gauss")
		plt.subplot(2,2,4),plt.imshow(th1,'gray')
		plt.title('Nichika')
		plt.show()

	def gauss_binarization(self,filename):
		im = cv2.imread(filename)
		# Gray scale
		gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		# Gaussian blur
		blur = cv2.GaussianBlur(gray,(3,3),0)
		# 2 valuize
		th = cv2.threshold(blur,127,255,0)[1]
		self.image_show(th)
		return th

	def image_show(self,image_bunch):
		cv2.imshow("Show Image",image_bunch)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	def best_codes(self,filename):
		th=self.gauss_binarization(filename)
		return self.edge_bin_codes(th)

	def edge_bin_codes(self,imdata):
		### EDGE coordinates
		# Normal videosrv output
        	# height=480, width=640
		height,width=imdata.shape
		print height,width

		x_ymin_ymax=[]
        	for x in np.arange(0,width-1):
                	ya=[]
                	for y in np.arange(0,height-1):
                        	if imdata[y][x] == 0:
                                	ya.append(y)
                	if len(ya)>2:
                        	yna=np.array(ya)
                        	ymin=yna.min()
                        	ymax=yna.max()
				x_ymin_ymax.append((x,ymin,ymax))
		return np.array(x_ymin_ymax)

	def edge_codes(self,imdata):
		### EDGE coordinates
		# Normal videosrv output
        	# height=480, width=640
		height,width=imdata.shape
		print height,width

        	for x in np.arange(0,width-1):
                	ya=[]
                	for y in np.arange(0,height-1):
                        	min_pix=9999
                        	max_pix=-9999
                        	min_pix_flag=False
                        	if imdata[y][x] > 200:
                                	ya.append(y)
                	if len(ya)>2:
                        	yna=np.array(ya)
                        	ymin=yna.min()
                        	ymax=yna.max()
                        	print "Y min-max=",x,ymin,ymax
 
if __name__ == "__main__":
	cip=CryImageProc(sys.argv[1])
	#cip.canny()
	#cip.rotatedRectangle()
	#cip.labeling()
	#cip.labeling2()
	#cip.rinkaku()
	#th=cip.gauss_binarization()
	#a=cip.edge_bin_codes(th)
	a=cip.best_codes(sys.argv[1])
	for b in a:
		print b

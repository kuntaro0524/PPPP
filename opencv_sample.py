#from opencv.cv import LoadImageM
#from opencv.highgui import *

import Image
import os
import sys
from opencv.cv import *
from opencv.highgui import *
import Image


#filename="/isilon/users/target/target/SomePPMs/100609/image000.ppm"
filename="/isilon/BL32XU/BLsoft/PPPP/20.ppm"
im=Image.open(filename)
img=cvLoadImage(filename,CV_LOAD_IMAGE_GRAYSCALE)

x=im.size[0]
y=im.size[1]

gray=cvCreateImage(cvSize(x,y),8,1)
edge1=cvCreateImage(cvSize(x,y),32,1)
edge2=cvCreateImage(cvSize(x,y),8,1)
edge3=cvCreateImage(cvSize(x,y),32,3)

cvCornerHarris(gray,edge1,5,5,0.1)
cvCanny(gray,edge2,20,100)

cvNamedWindow("win")
cvShowImage("win",gray)
cvNamedWindow("win3")
cvShowImage("win3",edge2)

cvWaitKey()

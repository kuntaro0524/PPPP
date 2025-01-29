
import Image
#im=Image.open("high_mag.ppm")

from opencv.cv import *
from opencv.highgui import *

#t=IplImiage()

image="high_mag.ppm"

tmpimg=cvLoadImage(image)
dstimg=cvCreateImage(cvGetSize(tmpimg),IPL_DEPTH_8U,1)

cvSmooth(tmpimg,dstimg,CV_GAUSSIAN,5)
cvThreshold(tmpimg,dstimg,0,255,CV_THRESH_BINARY | CV_THRESH_OTSU)

cvNamedWindow("THRESH")
cvShowImage(dstimg)
cvWaitKey(0)

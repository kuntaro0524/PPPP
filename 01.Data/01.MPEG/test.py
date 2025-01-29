import Image
import os
import sys
#import cv
from opencv.cv import *
from opencv.highgui import *

cvNamedWindow("TEST",CV_WINDOW_AUTOSIZE)
capture=cvCaptureFromAVI("test.avi")

from PIL import Image
from numpy import *
import sys

im1=Image.open("./sample_000001.img")
pixel=im1.load()

for x in range(0,3072,16):
	for y in range(0,3072,16):
		print x,y,pixel[x,y],
	print "\n\n"

#print im1.format

im1arr=asarray(im1)

#print im1arr
#print len(im1arr)

resultImage=Image.fromarray(im1arr)
#resultImage.save("test.png")

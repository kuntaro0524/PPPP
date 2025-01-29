import os
import sys
import math
#from  pylab import * 
import socket
import pylab
import scipy
import numpy
#from numpy import *
from pylab import *
from scipy.interpolate import splrep,splev,interp1d,splprep
from MyException import *

class Anew:

	def __init__(self,datfile):
		self.fname=datfile
		self.isRead=0

	def readFile(self):
		ofile=open(self.fname,"r")
		self.lines=ofile.readlines()
		ofile.close()

	def loadFile(self):
		self.data =numpy.loadtxt(self.fname, comments='#' ,delimiter=' ',dtype=(float))

		print self.data

if __name__=="__main__":
	ana=Anew(sys.argv[1])
	ana.loadFile()


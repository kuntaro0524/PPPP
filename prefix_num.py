import sys
import os
import glob
import datetime
from File import *
if __name__=="__main__":

	f=File("./")
	print "%03d"%(f.getNewIdx3())

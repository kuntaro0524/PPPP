import os
import sys
import math
#from  pylab import *
from  AnalyzeData import *

if __name__=="__main__":

		ana=AnalyzeData(sys.argv[1])
		ana.storeData(1,2)

		newfile=sys.argv[1].replace(".scn","_norm.scn")

		xdat,ydat=ana.getData()
		ana.clear()
		
		ana.storeData(1,3)
		jnkx,y2=ana.getData()

		newy=ana.divData(ydat,y2)

		ana.writeData(newfile,xdat,newy)


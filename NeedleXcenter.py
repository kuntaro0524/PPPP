import sys
import time
from Zoom import *
from Gonio import *
from Capture import *
from TemplateMatch import *
from ExSlit1 import *
from Shutter import *
from Light import *
from BS import *
from Colli import *

class NeedleXcenter:

	def __init__(self):
                host = '172.24.242.41'
                port = 10101
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host,port))
		self.gonio=Gonio(s)
		self.count=Count(s,3,1)
		self.shutter=Shutter(s)
		self.exs1=ExSlit1(s)
		self.light=Light(s)
		self.colli=Colli(s)
		self.bs=BS(s)

	def prep(self):
		# Preparation
		self.exs1.openV()
		self.bs.goOff()
		self.colli.goOff()
		self.shutter.open()
		self.light.goOff()

	def finish(self):
		# Ending
		self.shutter.close()
		self.exs1.closeV()
		self.light.goOn()

	def scan2(self,prefix,phi,width,step):
		self.gonio.rotatePhi(phi)
		# width, step -> [mm]
		o1="%s_%f.scn"%(prefix,phi)

		of1=open(o1,"w")

		# Current position is regarded as a center of the needle
		savex,savey,savez=self.gonio.getXYZmm()

		# scan setting
		npoints=int(width/step)+1
		
		# the 1st position
		start_position=-width/2.0*1000.0 # [um]
		self.gonio.moveUpDown(start_position)

		# Scan step
		cntmin=9999.999
		for idx in arange(0,npoints):
			move_um=step*1000.0 # [um]
			self.gonio.moveUpDown(move_um)
			tx,ty,tz=self.gonio.getXYZmm()
			cnt=int(self.count.getCount(0.2)[0])
			of1.write("12345 %8.3f %5d 1234\n"%(idx*move_um,cnt))
			if cntmin>cnt:
				cntmin=cnt
				mx,my,mz=tx,ty,tz

		print mx,my,mz
		
		
		# close file
		of1.close()

		# Recover the position
		self.gonio.moveXYZmm(savex,savey,savez)

if __name__=="__main__":

	f=File("./")
	nx=NeedleXcenter()

	nx.prep()
	for i in range(0,1):
		prefix="%03d_0deg"%f.getNewIdx3()
		nx.scan2(prefix,0,0.05,0.001)
		prefix="%03d_180deg"%f.getNewIdx3()
		nx.scan2(prefix,180,0.05,0.001)
	#for i in range(0,1):
		#prefix="%03d_90deg"%f.getNewIdx3()
		#nx.scan2(prefix,90,0.05,0.001)
		#prefix="%03d_270deg"%f.getNewIdx3()
		#nx.scan2(prefix,270,0.05,0.001)

	nx.finish()

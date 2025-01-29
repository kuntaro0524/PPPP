import os,sys
from ScheduleBSS import *
from numpy import *

class PLRD:

	def __init__(self):
		# setting
		self.center=(0.5,0.5,0.5)
		self.step=0.0005
		self.dnum=21
		self.dist=150.0
		self.althick_low=1200
		self.althick_high=0
		self.althick=600
		self.exptime=1.0
		self.exptime_low=1.0
		self.exptime_high=1.0
		self.wl=1.00
		self.stepphi=0.1
		self.startphi=0
		self.endphi=0.1
		self.ntime=5

	def setCenter(self,center):
		self.center=center

	def setScanCondition(self,startphi,endphi,stepphi):
		self.startphi=startphi
		self.endphi=endphi
		self.stepphi=stepphi
	
	def setStep(self,step):
		self.step=step
	
	def setNpoint(self,npts):
		self.dnum=npts

	def setDist(self,dist):
		self.dist=dist

	def setLow(self,thick,exptime):
		self.althick_low=thick
		self.exptime_low=exptime

	def setAl(self,thick):
		self.althick=thick

	def setHigh(self,thick,exptime):
		self.althick_high=thick
		self.exptime_high=exptime

	def setWL(self,wl):
		self.wl=wl

	def setNtime(self,ntime):
		self.ntime=ntime

	def genSchefile(self,outdir,prefix,ld_beamh,ld_beamv,hd_beamh,hd_beamv):
		t=ScheduleBSS()

		# Phi range
		t.setScanCondition(self.startphi,self.endphi,self.stepphi)

		# start vector Y 
		sy=self.center[1]-self.step*(self.dnum-1)/2.0
		# end vector Y 
		ey=self.center[1]+self.step*(self.dnum-1)/2.0

		# start vector Z 
		sz=self.center[1]-self.step*(self.dnum-1)/2.0
		# end vector Z 
		ez=self.center[1]+self.step*(self.dnum-1)/2.0

		# root setting
		t.setDir(outdir)
		t.setCameraLength(self.dist)
		t.setWL(self.wl)

		for nobs in range(0,self.ntime):
			offset=0

			# Low dose experiments
			t.setAttThickness(self.althick_low)
			t.setExpTime(self.exptime_low)

			cnt=0
			for ycode in arange(sy,ey,self.step):
				t.setOffset(offset)
				schefile="%s_%02d_%02d.sch"%(prefix,nobs,offset)
				t.setDataName("ld%02d"%nobs)
				offset+=1
				code=(self.center[0],ycode,self.center[2])
				if cnt==0:
					t.makeMultiPosBeam(schefile,code,ld_beamh,ld_beamv)
				else:
					t.makeMultiPos(schefile,code)
				cnt+=1
	
			# High dose experiments
			t.setAttThickness(self.althick_high)
			t.setExpTime(self.exptime_high)
			t.setOffset(0)
			schefile="%s_%02d_%02d.sch"%(prefix,nobs,offset)
			t.setDataName("hd%02d"%nobs)
			t.makeMultiPosBeam(schefile,self.center,hd_beamh,hd_beamv)

		#s.close()

        def genRDscan(self,outdir,prefix):

                t=ScheduleBSS()

                # Phi range
                t.setScanCondition(self.startphi,self.endphi,self.stepphi)

                # root setting
                t.setDir(outdir)
                t.setCameraLength(self.dist)
                t.setWL(self.wl)

                offset=0
                for nobs in range(0,self.ntime):

                        # Low dose experiments
                        t.setAttThickness(self.althick)
                        t.setExpTime(self.exptime)

                        t.setOffset(offset)
                        schefile="%s_%02d.sch"%(prefix,nobs)
                        t.setDataName("rd")
                        t.makeMultiPos(schefile,self.center)
                        offset+=1


if __name__=="__main__":
	
	mpr=PLRD()

	# Up-down from current phi
        curr_phi=100.0
        curr_phi=math.radians(curr_phi)

	# condition setting
        mpr.setCenter([0.5,0.5,0.5])
	mpr.setScanCondition(0,0.1,0.1)
        mpr.setStep(0.001)
        mpr.setNpoint(31)
        mpr.setDist(150.0)
        mpr.setLow(1200,0.5)
	mpr.setHigh(0,2.0)
	mpr.setWL(1.342)
        mpr.setNtime(2)
	mpr.genSchefile("./","test",1,1.5,1,1.5)

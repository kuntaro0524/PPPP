import sys,os,math 

class Resolution:

	def __init__(self,width):
		self.wavelength=1.0
		self.CL=300.0
		self.energy_base=12.3984
		self.energy=12.3984
		self.edge_from_center=width/2.0
		self.limit_short=105.0
		self.limit_long=600.0

	def setWL(self,wl):
		self.wavelength=wl
		self.energy=self.energy_base/self.wavelength
		
	def setCL(self,cl):
		self.CL=cl

	def setEnergy(self,en):
		self.energy=en
		self.wavelength=self.energy/self.energy_base

	# detsize : 225mm for MX225
	def setDetSize(self,detsize):
		self.edge_from_center=detsize/2.0

	def calcEdgeResol(self):
		two_theta=math.atan(self.edge_from_center/self.CL)
		theta=two_theta/2.0
		#l=2d*sin(theta)
		d=self.wavelength/2.0/math.sin(theta)
		return d

	def getDistResol(self,d):
		sintheta=self.wavelength/2.0/d
		theta=math.asin(sintheta)
		two_theta=2.0*theta

		cl=self.edge_from_center/math.tan(two_theta)

		self.limit_short=105.0
		self.limit_long=600.0

		if cl<self.limit_short:
			return 105.0
		elif cl>self.limit_long:
			return 600.0

		cl=round(cl)

		return cl

if __name__=="__main__":
	res=Resolution(233)
	#res.setWL(1.45683)
	wavelength=float(sys.argv[1])
	desired_resolution=float(sys.argv[2])
	res.setWL(wavelength)

	print res.getDistResol(desired_resolution)


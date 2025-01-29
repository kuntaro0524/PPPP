import math

class IDparam:

	def __init__(self):
		#self.p1=-3.90483
		#self.p2=23.37527
		#self.p3=9.75211

		# 102015 determined
		#self.p1=-3.59798
		#self.p2=22.583
		#self.p3=9.38048

		# 100217 determined (scanned with 1um resolution)
		self.p1=-3.62198
		self.p2=22.6115
		self.p3=9.37671

# Energy (keV)
	def getGap(self,energy):
                #print self.p2/energy-1
		gap=self.p1*math.log(self.p2/energy-1)+self.p3
		gapchar="%12.3f"%gap
		#print "gap=%12.5f\n"%float(gapchar)
		return float(gapchar)

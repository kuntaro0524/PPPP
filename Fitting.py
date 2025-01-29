import numpy
import matplotlib.pyplot as plt
import scipy.optimize
import re
import os

class Fitting:
	def __init__(self):
		print "init"

	def linearFit(self):
    		x = numpy.array(x)
    		y = numpy.array(y)
    		A = numpy.vstack([x, numpy.ones(len(x))]).T
    		m, c = numpy.linalg.lstsq(A, y)[0]
    		return m , c

	# function to fit
    	def func(self,x,a,b):
       		return a*numpy.exp(-b*x)

	def fitExp(self,x,y,filename):
    		# initial guess for the parameters
    		parameter_initial = numpy.array([0.0, 0.0]) #a, b
    	
    		parameter_optimal, covariance = scipy.optimize.curve_fit(self.func, x, y, p0=parameter_initial)
    		print "paramater =", parameter_optimal
	
    		self.y_expected = self.func(x,parameter_optimal[0],parameter_optimal[1])
	
    		self.initial_value=y[0]
    		self.half_of_initial=self.initial_value/2.0
	
    		self.a=parameter_optimal[0]
    		self.b=parameter_optimal[1]

    		self.expected_half=-(1.0/self.b)*numpy.log(self.half_of_initial/self.a)
		self.x=x
		self.y=y

		return self.expected_half

	def makePlotPNG(self,pngfile,comment="plot for K.Hirata"):
    		log1="Initial =%8.1f Half =%8.1f"%(self.initial_value,self.half_of_initial)
    		log3="Datasets=%5.2f"%self.expected_half
 	
    		plt.text(10,self.half_of_initial,"%s"%log1)
    		plt.text(10,self.half_of_initial+0.1*self.half_of_initial,"%s"%log3)

    		plt.plot(self.x, self.y_expected, "-", label="Fitted")
    		plt.plot(self.x, self.y, "o-", label="Observed")
    		plt.xlabel("# of datasets")
		plt.suptitle(comment, fontsize=16)
    		plt.ylabel("Total summed intensity XDS_ASCII.HKL")
    		plt.legend(loc="upper right")
    		plt.grid("on")
    		plt.savefig(pngfile)
    		#plt.show()

		return self.expected_half

	def fittingOnFile(self,filename,i_colx=0,i_coly=1):
		xa,ya=self.read(filename,i_colx,i_coly)
		expected_half=self.fitExp(xa,ya,filename)
		return expected_half

	def read(self,filename,i_colx=0,i_coly=1):
    		lines=open(filename).readlines()
    		xdat=[]
    		ydat=[]
    		for line in lines:
			sp=line.split()
			dnum,tot_int=map(lambda x: float(x), [sp[i_colx],sp[i_coly]])
			print dnum,tot_int
			xdat.append(dnum)
			ydat.append(tot_int)
		
    		xa=numpy.array(xdat)
    		ya=numpy.array(ydat)
	
    		return xa,ya

	def anaLin(xa,ya):
    		width_m, width_c = lm(xa,ya)
    		print "Width: y = %.4fx + %.4f" % (width_m, width_c)
	
    		yfitted=xa*width_m+width_c
		
    		initial_value=ya[0]
    		half_of_initial=initial_value/2.0
    		expected_half=(half_of_initial-width_c)/width_m
	
    		log1="Initial =%8.1f Half =%8.1f"%(initial_value,half_of_initial)
    		log3="Datasets=%5.2f"%expected_half
 	
    		plt.text(2,half_of_initial,"%s"%log1)
    		plt.text(3,half_of_initial+0.1*half_of_initial,"%s"%log3)
	
    		plt.plot(xa, yfitted, "-", label="Fitted")
    		plt.plot(xa, ya, "o-", label="Observed")
    		plt.xlabel("# of datasets")
    		plt.ylabel("Total summed intensity XDS_ASCII.HKL")
    		plt.legend(loc="upper right")
    		plt.grid("on")
    		out_prefix = os.path.splitext(os.path.basename(wirelog))[0]
    		plt.savefig(out_prefix+"_width.png")
    		plt.show()

	def polyFit(self,xa,ya,n,isArray=True):
		if isArray:
			x=numpy.array(xa)
			y=numpy.array(ya)
		else:
			x=xa
			x=ya
		
		fitted_curve=numpy.poly1d(numpy.polyfit(x,y,30))

		return fitted_curve

	def estimatePolyFit(self,xstart,ystart,ndata,fitted_curve):
		xp=numpy.linspace(xstart,ystart,ndata)
		
		plt.plot(x,y,'o',xp,fitted_curve(xp),'--')
		plt.show()
		plt.savefig("test.png")

if __name__ == "__main__":
    import sys

    ft=Fitting()
    ft.fittingOnFile(sys.argv[1],1,2)
    lines=open(sys.argv[1],"r").readlines()
	
    xd=[]
    yd=[]
    for line in lines:
            cols=line.split()
            en=float(cols[0])
            dose_per_1E8=float(cols[1])
            xd.append(en)
            yd.append(dose_per_1E8)

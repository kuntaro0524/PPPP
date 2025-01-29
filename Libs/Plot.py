import pylab,numpy,sys
import matplotlib.pyplot as plt

class Plot:
	def __init__(self):
		self.isInit=False

	def init(self):
		self.fig = plt.figure()
		self.fig.subplots_adjust(bottom=0.2)
		self.ax = self.fig.add_subplot(111)
		self.outname="out.eps"

	def setOutputFile(self,filename):
		self.outname=filename

	def setXlimit(self,xmin,xmax):
		plt.xlim([xmin,xmax])

	def setYlimit(self,ymin,ymax):
		plt.ylim([ymin,ymax])

	def plot(self,xa,ya,plot_type,label):
		print plot_type,label
		plt.plot(xa,ya,plot_type,label=label)

	def setAxesLabels(self,xlabel,ylabel,fontsize=24):
		#plt.ylabel("Crystallographic R-factor [%]",fontsize=18)
		#plt.xlabel(r'$d^{*2}$ [$\AA^{-2}$]',fontsize=18)
		plt.xlabel(xlabel,fontsize=fontsize)
		plt.xlabel(ylabel,fontsize=fontsize)

	def setTics(self,labelsize):
		plt.tick_params(labelsize=labelsize)

	def plotNormal(self,xlabel,ylabel,xarray,yarrays,labels,types,outfile):
		# Set xlabel, ylabel
		self.setAxesLabels(xlabel,ylabel,fontsize=24)
		self.outname=outfile
		plt.legend(loc='upper left',fontsize=24)

		for ya,label,plot_type in zip(yarrays,labels,types):
			plt.plot(xarray,ya,plot_type=plot_type,label=label)

		plt.savefig(self.outname,dpi=300)

if __name__ == "__main__":
	lines=open(sys.argv[1],"r").readlines()

	da=[]
	ra=[]
	fra=[]
	n_blank_line=0
	for line in lines:
    		cols=line.split()
    		if len(cols)==0:
			n_blank_line+=1
			if n_blank_line==2:
				break
			else:
				continue
    		da.append(float(cols[2]))
    		ra.append(float(cols[3])*100.0)
    		fra.append(float(cols[4])*100.0)

	nda=numpy.array(da)
	nra=numpy.array(ra)
	nfa=numpy.array(fra)

	pppp=Plot()
	pppp.init()
	yarrays=[nra,nfa]
	labels=["R-factor","Free-R"]
	types=["o-","x-"]
	outfile="test.eps"
	pppp.plotNormal("d*2","R-factors",nda,yarrays,labels,types,outfile)
	#pppp.setAxesLabels(self,xlabel,ylabel,fontisize=24):
	#pppp.plot(nda,nra,plot_type="o-",label="R-factor")
	#pppp.plot(nda,nfa,plot_type="x-",label="Free-R")

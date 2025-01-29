import sys,os,math

class XDSascii():
	def __init__(self,xds_ascii):
		self.xds_ascii=xds_ascii
		self.isRead=False
		self.iobs_list=[]

	def calcDP(self):
		lines=open(self.xds_ascii).readlines()
		total_i=0.0
		for line in lines:
			# skip comment lines
			if line[0]=="!":
				continue
			cols=line.split()
			iobs=float(cols[3])
			self.iobs_list.append(iobs)
			total_i+=iobs
		#self.isRead=True
		return total_i

if __name__=="__main__":
	xdsas=XDSascii(sys.argv[1])
	print "%s %10.1f"%(sys.argv[1],xdsas.calcDP())

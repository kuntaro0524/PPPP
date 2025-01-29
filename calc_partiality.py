import sys,os
import iotbx.mtz
import datetime

sys.path.append("/Users/kuntaro/00.Develop/Prog/02.Python/Libs/")
from ReflWidthStill import *
from ReadMtz import *
from DetectorArea import *
from Qshell import *

class hoge:
	def __init__(self,ref_mtz,still_mtz):
		self.ref_mtz=ref_mtz
		self.still_mtz=still_mtz

	def init(self,sn_thresh=2.0):
		rmtz=ReadMtz(self.ref_mtz)
		smtz=ReadMtz(self.still_mtz)
		# Extract intensity related cctbx.array
		self.refI = rmtz.getIntensityArray()
		self.stiI = smtz.getIntensityArray()

		# Detector coordinate
		xda=smtz.getColumn("XDET")
		yda=smtz.getColumn("YDET")
		self.xdet=xda.data()
		self.ydet=yda.data()

		print "INITIAL(stiI): ",len(self.stiI.data())

		# M/ISYMM
		m_isym=smtz.getColumn("M_ISYM")
		ba=smtz.getColumn("BATCH")

		# Detector area setting
		self.da=DetectorArea(3072,8,4)
		self.da.init()

		# Carefull choice of common reflections
		junk,self.refI=rmtz.commonInfo(self.stiI,self.refI) # otameshi  OK Reduced # refl. in stiI (only 1 reflection) #OK

		self.isyms=m_isym.data()
		self.ba=ba.data()


	def evaluate(self):
		ofile=open("ref.txt","w")
		for (hkl1,rI,rsigI) in self.refI:
			h,k,l=hkl1
			#print "%s"%hkl1
			ofile.write("%5d%5d%5d %12.2f %12.2f\n"%(h,k,l,rI,rsigI))
		ofile.close()

		ofile=open("sort.txt","w")
		#for (hkl1,sI,ssigI),isym,x,y in zip(self.stiI,self.isyms,self.xdet,self.ydet):
		#for (hkl1,sI,ssigI),isym in zip(self.stiI,self.isyms):

		# Initialization
		h2,k2,l2=self.refI.indices()[0]

		idx=0
		n=0
		for (hkl1,sI,ssigI),isym,batch in zip(self.stiI,self.isyms,self.ba):
			h,k,l=hkl1
			#print "HKL= %5d %5d %5d"%(h,k,l)

			if n==0:
				saved_isym=isym

			# 20 reflections are checked
			if idx+20 >= len(self.refI.data()):
				maxidx=len(self.refI.data())
			else:
				maxidx=idx+20

			eqflag=False
			for ch in range(idx,maxidx):
				h2,k2,l2=self.refI.indices()[ch]
				#print "REF %5d %5d %5d %5d"%(h2,k2,l2,ch),
				if h!=h2 or k!=k2 or l!=l2:
					#print "Different!"
					if ch==idx:
						ofile.write("\n\n")
					continue
				else:
					if isym!=saved_isym:
						ofile.write("\n\n")
					#print "Equivalent!"
					eqflag=True
					idx=ch
					break

			#print eqflag,h,k,l,h2,k2,l2

			# check if equivalent
			if eqflag==False:
				#print "This reflection is not included in reference data"
				continue

			# when the loop reaches the final index of self.refI.data()
			#print idx,len(self.refI.data())
			if idx==len(self.refI.data()):
				print "Something wrong"
				break

			rI=self.refI.data()[idx]
			rrI=self.refI.sigmas()[idx]

			assert h==h2
			assert k==k2
			assert l==l2

			# Pobs calculation
			pobs=sI/rI

			# save ISYM
			saved_isym=isym

			# detector area index
			#didx=self.da.idx(x,y)
			#ofile.write("%5d%5d%5d %12.2f %12.2f %5d\n"%(h,k,l,sI,ssigI,isym))
			#ofile.write("%5d%5d%5d %12.2f %12.2f\n"%(h,k,l,sI,ssigI))
			ofile.write("%5d%5d%5d %5d %5d %12.2f %12.2f %12.2f %12.2f %8.5f\n"%(h,k,l,batch,isym,sI,ssigI,rI,rrI,pobs))
			#ofile.write("%5d%5d%5d %5d%5d%5d %5d\n"%(h,k,l,h2,k2,l2,idx))
			#print "%5d%5d%5d %5d%5d%5d %5d\n"%(h,k,l,h2,k2,l2,idx)
			n+=1
		ofile.close()

if __name__ == "__main__":

	h=hoge(sys.argv[1],sys.argv[2])

	h.init(0.0)
	h.evaluate()

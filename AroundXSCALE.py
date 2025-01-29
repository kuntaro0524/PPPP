import sys,os,math

class AroundXSCALE():
	def __init__(self,thispath="./"):
		self.thispath=thispath
		self.inpfiles_in_inpfile=[]

		# XSCALE.INP lines except for 'input file' definitions
		self.otherlines=[]

	def getOtherLinesInputFiles(self):
		filepath="%s/XSCALE.INP"%self.thispath
		self.inplines=open(filepath,"r").readlines()

		for line in self.inplines:
        		if line.rfind("INPUT_FILE")!=-1:
				self.inpfiles_in_inpfile.append(line)
                		continue
        		else:
                		self.otherlines.append(line)
		return self.otherlines

	def getRfactorSortedInputFiles(self):
		filepath="%s/XSCALE.LP"%self.thispath
		lp_lines=open(filepath,"r").readlines()

		line_idx=0
		flist=[]
		for line in lp_lines:
        		if line.rfind("R-FACTORS FOR INTENSITIES OF DATA SET")!=-1:
                		#print line,line_idx,lp_lines[line_idx+5]
                		cols=line.split()
                		line2=lp_lines[line_idx+5]
                		cols2=line2.split()
                		rfac=float(cols2[1].replace("%",""))
                		fname=cols[6]
                		flist.append((rfac,fname))
        		line_idx+=1

		# R-factor sorted file list
		flist.sort(key=lambda x:x[0])
		return flist

	def getFileListOfEnoughReflections(self,nthresh=10000):
		filepath="%s/XSCALE.LP"%self.thispath
		lp_lines=open(filepath,"r").readlines()

		file_index=0
		flist=[]
		read_flag=False
		self.good_list=[]
		self.bad_list=[]
		for line in lp_lines:
			#print line
        		if line.rfind("SET# INTENSITY  ACCEPTED REJECTED")!=-1:
				read_flag=True
				continue
			if read_flag==True:
				cols=line.split()
				if len(cols)==0:
					break
				if len(cols)>0 and cols[0].isdigit()==False:
					break
				nrefl=int(cols[2])
				fname=cols[4]
				if nrefl >= nthresh :
					self.good_list.append(fname)
				else:
					self.bad_list.append(file_index)
			file_index+=1
		return self.good_list

	# R-factor sorted list: rfactor_sorted_list from XSCALE.LP
	# Enough number of reflections : good_nrefl_list from XSCALE.LP
	# This routine returns commond list of reflections in XSCALE.LP
	def getGoodList(self,nthresh=10000):
		good_nrefl_list=self.getFileListOfEnoughReflections(nthresh)
		rfactor_sorted_list=self.getRfactorSortedInputFiles()

		# find very good from 2 lists
		new_list=[]
		for v,f in rfactor_sorted_list:
			for g in good_nrefl_list:
				if g==f:
					new_list.append(g)

		return new_list

	def get_xscale_inp(self,nfiles):
        	file_list=[]
        	idx=0
        	for f in flist:
                	idx+=1
                	file_list.append(f[1])
                	if idx == nfiles:
                        	break
        	return file_list

if __name__ == "__main__":
	ax=AroundXSCALE()
	#test1=ax.getFileListOfEnoughReflections()
	#test2=ax.getRfactorSortedInputFiles()
	test2=ax.getGoodList()

	for f in test2:
		print f

	lines=ax.getOtherLinesInputFiles()
	print lines

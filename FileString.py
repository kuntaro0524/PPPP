import os,sys,math

class FileString:

	def __init__(self,filename):
		self.filename=filename
		self.initFlag=False

	def init(self):
		self.lines=open(self.filename).readlines()
		self.initFlag=True

	def extractFromTo(self,from_str,to_str):
		if self.initFlag==False:
			self.init()
		idx=0
		from_str_index=to_str_index=-1
		for line in self.lines:
			if line.rfind(from_str)!=-1:
				from_str_index=idx
			if line.rfind(to_str)!=-1:
				to_str_index=idx
			idx+=1

		if from_str_index==-1 or to_str_index==-1:
			return ""
		body=[]
		#print from_str_index,to_str_index
		for i in range(from_str_index,to_str_index):
			body.append(self.lines[i])
		return body

	def makePlot(self,tablestr,col_x,col_y,plotfile="plot.plt"):
		n_max_col=0
		for shell in tablestr:
			cols=shell.split()
			if len(cols) > n_max_col:
				n_max_col=len(cols)
	
		#print n_max_col

		ofile=open(plotfile,"w")
		for shell in tablestr:
			cols=shell.split()
			if len(cols)==n_max_col:
				ofile.write("%s %s\n"%(cols[col_x],cols[col_y]))
		ofile.close()

if __name__=="__main__":

	fs=FileString(sys.argv[1])

	frstr="****                Things for loggraph, R factor and others                ****"
    	tostr="****                      Fom and SigmaA vs resolution                      ****"

	search_table=fs.extractFromTo(frstr,tostr)
	fs.makePlot(search_table,0,11)
		
"""
lines=open(sys.argv[1]).readlines()
r_thresh=float(sys.argv[2])
r_total_thresh=float(sys.argv[3])

line_idx=0
all_datasets=[]
shell_flag=False
read_flag=False

for line in lines:
	#print "Processing:", line
	if line.rfind("R-FACTORS FOR INTENSITIES OF DATA SET")!=-1:
		#print "PATTERN1"
		shell_flag=True
		tmpstr=[]
		tmpstr.append(line)
	if shell_flag==True and line.rfind("LIMIT")!=-1:
		#print "PATTERN2"
		read_flag=True
	if read_flag==True:
		if line=="" or line=="\n":
			continue
		tmpstr.append(line)
	if read_flag==True and (line.rfind("total")!=-1 or line.rfind("***")!=-1):
		#print "PATTERN4"
		read_flag=False
		shell_flag=False
		all_datasets.append(tmpstr)

n_data=len(all_datasets)
n_good_lowres=0
n_good_total=0
for each_data in all_datasets:
	#print "################"
	lowest_res_rsym=float((each_data[2].replace("%","")).split()[1])
	total_rsym=float((each_data[11].replace("%","")).split()[1])
	#print lowest_res_rsym,total_rsym

	if lowest_res_rsym < r_thresh and total_rsym < r_total_thresh:
		print "INPUT_FILE=",each_data[0].split()[6]
		n_good_lowres+=1
	if total_rsym < r_total_thresh:
		n_good_total+=1

#print n_good_lowres,n_good_total
"""

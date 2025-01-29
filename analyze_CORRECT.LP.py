import sys,os

"""
 SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION
 RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  CC(1/2)  Anomal  SigAno   Nano
   LIMIT     OBSERVED  UNIQUE  POSSIBLE     OF DATA   observed  expected                                      Corr

     6.40        3718     992       995       99.7%      20.6%     19.8%     3706    4.35     23.9%    95.6*     1    0.891     351
     4.54        7014    1807      1807      100.0%      23.0%     21.4%     7010    4.43     26.7%    94.3*     5    0.963     753
     3.72        9013    2303      2303      100.0%      22.7%     21.3%     9011    4.58     26.3%    94.2*     1    0.923    1000
     3.22       10322    2734      2734      100.0%      28.2%     25.3%    10319    3.55     32.9%    90.8*     4    0.958    1213
     2.88       10053    3093      3094      100.0%      35.9%     32.8%    10013    2.35     43.1%    81.3*     6    0.993    1362
     2.63       10655    3412      3420       99.8%      52.5%     47.4%    10572    1.42     63.5%    67.2*     1    0.900    1480
     2.44       12766    3743      3748       99.9%      67.5%     63.5%    12733    1.02     80.2%    60.3*     5    0.847    1693
     2.28       14078    4011      4012      100.0%      76.3%     73.1%    14047    0.84     90.0%    57.2*     1    0.802    1826
     2.15       14867    4216      4227       99.7%      91.0%     89.3%    14773    0.61    106.9%    48.3*     2    0.763    1896
    total       92487   26312     26340       99.9%      37.5%     35.1%    92184    2.07     44.2%    90.3*     3    0.877   11574
"""

class anaCORRECT():
	def __init__(self,fname):
		ifile=open(fname,"r")
		self.lines=ifile.readlines()
		ifile.close()

	def read(self):
		flag=0
		skip=0
		start=0
		idx=0
		for line in self.lines:
			if line.find("SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION")!=-1:
				start=idx
			idx+=1
		end=idx

		dmin_save=0.0
		cc_half_mon=0.0
		for i in range(start,end):
			line=self.lines[i]
			if line=="\n":
				continue
			cols=line.split()
			#print cols
			if flag==1 and skip < 3:
				skip+=1
				continue
			if line.find("SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION")!=-1:
				flag=1
				skip+=1
				continue
			if flag==1 and cols[0]=="total":
				break
			if flag==1:
				dmin=float(cols[0])
				ds2=1.0/dmin/dmin
				dmin=float(cols[0])
				ds2=ds2
				rfact=float(cols[5].replace("%",""))
				isigi=float(cols[8])
				cc_half=float(cols[10].replace("%","").replace("*",""))
			
				if cc_half < 50.0:
					print "%5.1f"%dmin_save
					break

				dmin_save=dmin

			print "%5.3f, %5.3f,%8.3f,%8.3f,%8.3f"%(dmin,ds2,rfact,isigi,cc_half)
if __name__=="__main__":
	ac=anaCORRECT(sys.argv[1])
	ac.read()

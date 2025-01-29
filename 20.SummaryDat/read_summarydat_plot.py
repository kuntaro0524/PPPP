import sys,os,math,numpy,scipy
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/10.Zoo")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/10.Zoo/Libs/")
import scipy.spatial as ss
import MyException
import time
import datetime
import AnaHeatmap


# Read "summary.dat" 
sumlines=open("summary.dat","r").readlines()
score_type="n_spots"
threshold=15

for l in sumlines[1:]:
	cols=l.split()
	tmp_type=cols[3]

	if tmp_type!="n_spots":
		continue
	else:
		score=float(cols[4])
		if score > threshold:
			print l,
		#xyi_list.append((x,y,int(cols[5].replace(".img","").split('_')[1])))

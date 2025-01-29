import os,sys,math

sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")

from AnalyzePeak import *

infile=open(sys.argv[1],"r")
lines=infile.readlines()

ana=AnalyzePeak(sys.argv[1])

flag=False
xlist=[]
ylist=[]
for line in lines:
	cols=line.split()

	if len(cols)==0 and flag==False:
		flag=True
		continue

	if flag==True and len(cols)!=0:
		xlist.append(float(cols[0]))
		ylist.append(float(cols[1]))


xa,ya,tmp=ana.prepPylabArray(xlist,ylist,xlist)

half=(ya.max()+ya.min())/2.0

#print half

for idx in arange(0,len(xa)-1):

	# Nobori
	if ya[idx]>half and ya[idx+1]<=half:
		#print ya[idx],ya[idx+1]
		nobori_idx=idx
		# 1D line calculation
		dx=xa[idx+1]-xa[idx]
		dy=ya[idx+1]-ya[idx]
		grad_n=dy/dx
		sepp_n=ya[idx+1]-grad_n*xa[idx+1]
		x1_sol=(half-sepp_n)/grad_n

	# Kudari
	if ya[idx]<half and ya[idx+1]>=half:
		#print ya[idx],ya[idx+1]
		kudari_idx=idx
		# 1D line calculation
		dx=xa[idx+1]-xa[idx]
		dy=ya[idx+1]-ya[idx]
		grad_k=dy/dx
		sepp_k=ya[idx+1]-grad_k*xa[idx+1]
		x2_sol=(half-sepp_k)/grad_k

print "%4.2f"%math.fabs(x1_sol-x2_sol)

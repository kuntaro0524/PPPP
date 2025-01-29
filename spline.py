from AnalyzePeak import *
ana=AnalyzePeak("./test.dat")

px,py=ana.prepData2(1,2)
print px,py
en_list,stz_list=ana.spline(px,py,1000)

i=0
for e in en_list:
        rtn_gap=round(stz_list[i],4)
	print "%12.5f %12.5f"%(e,rtn_gap)
	i+=1

import sys
import socket
import time
from Received import *
from Organizer import *
from IDparam import *

class ID:
	def __init__(self,srv):
		self.srv=srv	# server 
    		self.id=Organizer(srv,"bl_32in","id_gap","")

	def getE(self,energy):
		return IDparam().getGap(energy)

	def moveE(self,energy):
		gap=IDparam().getGap(energy)
		if gap < 7.4:
			print "Gap should be set more than 7.4mm"
			print "In this time, 7.4mm is set to ID"
			gap=7.4
		#print gap
		self.move(gap)

	def move(self,gap):
		# float gap -> yuukou suuji 3 keta
		gap=float(str("%8.3f"%gap))
		# Constructer
    		for x in range(1,5):
        		self.id.move(gap,"mm")
        		current_value=float(self.id.getPosition()[0])

        		if current_value==gap:
				return 1
        		print "current value=%8.3f"%current_value

	def tune(self,start,end,width,channel,time,ofile):
		maxvalue=-99999
		maxgap=0.0

		of=open(ofile,"w")

		ndata=int((end-start)/width)+1
		
		if ndata < 1:
			print "Abort!!!"
			sys.exit()

		for n in range(0,ndata):
			current=start+float(n)*width
			current=float(str("%8.4f"%current))

			if current < 7.4 or current > 45.0 :
				print "Abort!!"
				sys.exit()

			print "moving %8.3f \n" % current
			self.move(current)
        		count=self.id.getCount(channel,time)
			if count > maxvalue:
				maxvalue=count
				maxgap=current

			of.write("12345 %12.5f %12d\n"%(current,count))


		of.close()
		return maxgap

	def findPeak(self,energy,prefix,cnt_ch):

		file1=prefix+"_coarse_id.scn"
		file2=prefix+"_fine_id.scn"
		file3=prefix+"_superfine_id.scn"

    		center=self.getE(energy)
    		start=float(center)-0.5
    		end=float(center)+0.5
		print "ID scan range %8.5f - %8.5f\n"%(start,end)
    		max=self.tune(start,end,0.1,cnt_ch,0.2,file1)
    		print "MAX:%12.5f\n" % max

		# fine tune
    		center=max
    		start=float(center)-0.1
    		end=float(center)+0.1

    		max=self.tune(start,end,0.005,cnt_ch,0.2,file2)
    		print "MAX:%12.5f\n" % max

		# ultra fine tune
		center=max
		start=float(center)-0.01
		end=float(center)+0.01
    		max=self.tune(start,end,0.001,cnt_ch,0.2,file3)
    		print "MAX:%12.5f\n" % max

		self.move(max)

	def findPeakLowEnergy(self,energy,prefix,cnt_ch):

		file1=prefix+"_coarse_id.scn"
		file2=prefix+"_fine_id.scn"
		file3=prefix+"_superfine_id.scn"

    		center=self.getE(energy)


    		start=float(center)-0.5
		if start < 7.4:
			start=7.4

    		end=float(center)+0.5
		print "ID scan range %8.5f - %8.5f\n"%(start,end)
    		max=self.tune(start,end,0.1,cnt_ch,0.2,file1)
    		print "MAX:%12.5f\n" % max

		# fine tune
    		center=max
    		start=float(center)-0.1

		if start<7.4:
			start=7.4

    		end=float(center)+0.1

    		max=self.tune(start,end,0.005,cnt_ch,0.2,file2)
    		print "MAX:%12.5f\n" % max

		# ultra fine tune
		center=max
		start=float(center)-0.01
		if start<7.4:
			start=7.4

		end=float(center)+0.01
    		max=self.tune(start,end,0.001,cnt_ch,0.2,file3)
    		print "MAX:%12.5f\n" % max

		self.move(max)

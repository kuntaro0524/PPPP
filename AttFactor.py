import sys
import socket
import time
import math
import numpy 

class AttFactor:
	def __init__(self):
		dummy=1
		self.isInit=False
		
	def cnFactor(self,wl):
		cnfac=0.028*math.pow(wl,5)-0.188*math.pow(wl,4)+0.493*math.pow(wl,3)-0.633*math.pow(wl,2)+0.416*math.pow(wl,1)+0.268
		return cnfac

	def calcMu(self,wl,cnfac):
		mu=38.851*math.pow(wl,3)-2.166*math.pow(wl,4)+1.3*cnfac
		return mu

	def calcAttFac(self,wl,thickness,material="Al"):
		# thickness [um]
		if material=="Al":
			cnfac=self.cnFactor(wl)
			mu=self.calcMu(wl,cnfac)
			attfac=math.exp(-mu*thickness/10000)
			return attfac
		else:
			return -1

	def calcThickness(self,wl,transmission,material="Al"):
		# thickness [um]
		if material=="Al":
			cnfac=self.cnFactor(wl)
			mu=self.calcMu(wl,cnfac)
			thickness=(-1.0*math.log(transmission)/mu)*10000
			return thickness
		else:
			return -1

	def getBestAtt(self,wl,transmission):
		if self.isInit == False:
			self.readAttConfig()

		cnfac=self.cnFactor(wl)
		mu=self.calcMu(wl,cnfac)
		thickness=(-1.0*math.log(transmission)/mu)*10000

		print "IDEAL thickness: %8.1f[um]"%thickness

		if thickness <= 0.0:
			return 0.0 #[um]

		for att in self.att_thick:
			if thickness < att:
				return att

	# 150528 Mainly for shutterless measurement
	# wl		: wavelength
	# transmission	: transmission
	# exptime	: intended exposure time for each frame
	def chooseBestConditions(self,wl,transmission,exptime):
		if self.isInit == False:
			self.readAttConfig()

		cnfac=self.cnFactor(wl)
		mu=self.calcMu(wl,cnfac)
		real_transmission=transmission/exptime

		while (1):
			# The first estimation of the transmission by the defined 'exptime'
			thickness=self.calcThickness(wl,real_transmission)
			print thickness,exptime

			if thickness<0.0:
				exptime+=0.01
				print "Exptime=",exptime
			else:
				break

		print "Exposure time:",exptime
		bestatt=self.getBestAtt(wl,real_transmission)
		attfac=self.calcAttFac(wl,bestatt)
		print "BESTATT/ATTFAC=",bestatt,attfac

		ppp=real_transmission/attfac
		final_exptime=exptime*ppp
		print "Final exposure time:",final_exptime

		print attfac*final_exptime,real_transmission

		#for att in self.att_thick:
			#if thickness < att:
				#return att

	def readAttPulse(self):
		self.bssconfig="/isilon/blconfig/bl32xu/bss/bss.config"
		confile=open(self.bssconfig,"r")
		lines=confile.readlines()
		confile.close()
		self.att_pulse=[]

                for line in lines:
                        if line.find("Attenuator1")!=-1:
                                line=line.replace(":","")
                                cols=line.split()
                                ncols=len(cols)
                                if ncols == 4:
					#print cols[0].replace("Attenuator1_","")
					if cols[2]=="None":
						continue
					self.att_pulse.append(int(cols[3]))
		print self.att_pulse

		"""
		Attenuator1_0: None None 3500
		Attenuator1_1: Al 100um 3181
		Attenuator1_2: Al 150um 3160
		Attenuator1_3: Al 200um 3138
		Attenuator1_4: Al 250um 3117
		Attenuator1_5: Al 300um 3095
		Attenuator1_6: Al 350um 3073
		Attenuator1_7: Al 400um 3052
		Attenuator1_8: Al 450um 3030
		Attenuator1_9: Al 500um 3009
		Attenuator1_10: Al 550um 2987
		Attenuator1_11: Al 600um 2966
		Attenuator1_12: Al 650um 2944
		Attenuator1_13: Al 700um 2922
		Attenuator1_14: Al 750um 2901
		Attenuator1_15: Al 800um 2879
		Attenuator1_16: Al 850um 2858
		Attenuator1_17: Al 900um 2836
		Attenuator1_18: Al 950um 2814
		Attenuator1_19: Al 1000um 2793
		Attenuator1_20: Al 1100um 2750
		Attenuator1_21: Al 1200um 2707
		Attenuator1_22: Al 1300um 2663
		Attenuator1_23: Al 1400um 2620
		Attenuator1_24: Al 1500um 2577
		Attenuator1_25: Al 1600um 2534
		Attenuator1_26: Al 1700um 2491 
		Attenuator1_27: Al 1800um 2448
		Attenuator1_28: Al 2000um 2361
		Attenuator1_29: Al 2500um 2145 
		Attenuator1_30: Al 3000um 1930
		Attenuator1_31: Al 3500um 1714
		Attenuator1_32: Al 4000um 1498
		Attenuator1_33: Al 4500um 1282
		Attenuator1_34: Al 5000um 1066
		Attenuator1_35: Al 5500um 850
		Attenuator1_36: Auto    9999
		"""
	def readAttConfig(self):
		self.bssconfig="/isilon/blconfig/bl32xu/bss/bss.config"
		confile=open(self.bssconfig,"r")
		lines=confile.readlines()
		confile.close()

		self.att_idx=[]
		self.att_thick=[]

		for line in lines:
			if line.find("Attenuator_Menu_Label")!=-1:
				line=line.replace("[","").replace("]","").replace("{","").replace("}","")
				cols=line.split()
				ncols=len(cols)
				if ncols == 4:
					if cols[2].find("um")!=-1:
						tmp_thick=float(cols[2].replace("um",""))
						tmp_attidx=int(cols[3])
						# storage
						self.att_idx.append(tmp_attidx)
						self.att_thick.append(tmp_thick)

		self.att_idx=numpy.array(self.att_idx)
		self.att_thick=numpy.array(self.att_thick)

		# DEBUG
		for i,thick in zip(self.att_idx,self.att_thick):
			print i,thick

		# flag on
		self.readAttPulse()
		self.isInit=True

        def getAttPulseConfig(self,t):
                if self.isInit == False:
                        self.readAttConfig()
                if t<=0.0:
                        return 3500
                for thick,pulse in zip(self.att_thick,self.att_pulse):
                        if thick==t:
                                return pulse
                print "Something wrong: No attenuator at this beamline"
                return -9999

	def getAttIndexConfig(self,t):
		if self.isInit == False:
			self.readAttConfig()
		if t<=0.0:
			return 0
		for i,thick in zip(self.att_idx,self.att_thick):
			if thick==t:
				return i
		print "Something wrong: No attenuator at this beamline"
		return -9999

	# For KUMA GUI
	def getAttList(self):
		if self.isInit == False:
			self.readAttConfig()
		ppp=numpy.insert(self.att_thick,0,0.0)
		print "att_thick",self.att_thick
		print "ppp      ",ppp
		char_list=[]
		for thickness in ppp:
			thick_char="%5.1f"%thickness
			char_list.append(thick_char)
		return char_list

	def getList(self):
		if self.isInit == False:
			self.readAttConfig()
		return self.att_thick,self.att_idx,self.att_pulse

if __name__=="__main__":
	att=AttFactor()

	#att.getAttIndexConfig(100)
	#att.readAttPulse()
	#att.readAttConfig()
	print "#########################"
        llll= att.getAttList()
	print "#########################"

	#print "ALIST print"
	#print att.getBestAtt(1.0, 0.076)
	print 700,att.calcAttFac(1.0,700)
	print 1000,att.calcAttFac(1.0,1000)
	#wavelength=1.0

from Stage import *
import sys
import datetime
import math

class StageTune:
	def __init__(self,stage,capture,bm,shutter,att,mono,zoom,bs,cryo):
		self.stage=stage
		self.cap=capture
		self.bm=bm
		self.shutter=shutter
		self.att=att
		self.mono=mono
		self.zoom=zoom
		self.bs=bs
		self.cryo=cryo

	def savePosition(self):
		file="/isilon/users/target/target/Staff/BLtune/stage.dat"
		en=self.mono.getE()

		of=open(file,"a")
		date=datetime.datetime.now()

		curr_y=self.stage.getYmm()
		curr_z=self.stage.getZmm()

		diff_y,diff_z=self.diffLast()

		if fabs(diff_y) >=20.0 or fabs(diff_z) >=20.0:
			print "Something wrong in stage tune!!"
			print "diff (Y,Z)=(%8.4f,%8.4f)\n"%(diff_y,diff_z)
			sys.exit(1)

		of.write("%s: %8.3f    %8.4f %8.4f ( %8.4f %8.4f )\n"%(date,en,curr_y,curr_z,diff_y,diff_z))

		of.close()

	def diffLast(self):
		file="/isilon/users/target/target/Staff/BLtune/stage.dat"

		ifile=open(file,"r")
		lines=ifile.readlines()
		line=lines[len(lines)-1]
		#print line

		prev_y=float(line.split()[3])
		prev_v=float(line.split()[4])

		print "PREVIOUS %12.5f %12.5f\n" %(prev_y,prev_v)

		diff_y=1000.0*(prev_y-self.stage.getYmm())
		diff_z=1000.0*(prev_v-self.stage.getZmm())

		ifile.close()

		# return difference table parameters in [um]
		return diff_y, diff_z

	#############################################
        	# Automatic stage tune #
	#############################################
	def doAutomatic(self,capfile):
		# Cryo off
		self.cryo.off()

		# Zooom
		self.zoom.zoomIn()
		
        	# Center cross in [pix]
        	#ceny=322 # 100717, 100725, 100726, 100728-noon
        	#cenz=239 # 100717, 100725, 100726, 100728-noon
        	ceny=320 # 100717, 100724, 100725, 100728
        	cenz=240 # 100717, 100724, 100725, 100728
	
        	# Beam monitor on
        	self.bm.set(0)

		# Beam stopper on
        	self.bs.on()

		# Attenuator setting
		en=self.mono.getE()
		if en<=9.5:
			self.att.att0um()
		#elif en<=11.0:
			#self.att.att400um()
		elif en<=13.0:
			#self.att.att1000um()
			self.att.att1500um()
			#self.att.att600um() # 100724 weak beam
		else :
			self.att.att1500um()

		# Shutter open
        	self.shutter.open()

        	for i in range(0,3):
                	print self.stage.getZmm(), self.stage.getYmm()
                	# caputure
			try:
                		y,z=self.cap.captureBM(capfile)
			except MyException,ttt:
				print ttt.args[0]
				sys.exit(1)
	
                	# diff x,y
                	dy=y-ceny
                	dz=z-cenz
	
                	# pixel to micron [um/pixel] in high zoom
                	p2u_z=7.1385E-2
                	p2u_y=9.770E-2
	
                	z_move=-dz*p2u_z
                	y_move=dy*p2u_y
	
                	print "Z: %8.4f [um]"%z_move
                	print "Y: %8.4f [um]"%y_move

			if math.fabs(z_move) > 500 or math.fabs(y_move) > 500:
				print "SOMETHING WRONG"
				sys.exit(1)
	
                	#print z_move
                	self.stage.moveZum(z_move)
                	self.stage.moveYum(y_move)
			time.sleep(3)

		# Save position
		self.savePosition()

		# Shutter close
        	self.shutter.close()
	
        	# Beam monitor off
        	self.bm.set(-75000)

        	# Beam stopper
        	self.bs.off()

        	# Attenuator setting
        	self.att.att0um()

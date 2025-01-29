import time
import datetime

from Organizer import *

class AxesInfo:

	def __init__(self,server):
		self.s=server
		self.isStore=-1

	def storeInfo(self):
		self.id_gap=Organizer(s,"bl_32in","id_gap","").getPosition()

		self.fes_vert=Organizer(s,"bl_32in","fe_slit_1","vertical").getPosition()
		self.fes_hori=Organizer(s,"bl_32in","fe_slit_1","horizontal").getPosition()
		self.fes_height=Organizer(s,"bl_32in","fe_slit_1","height").getAperture()
		self.fes_width=Organizer(s,"bl_32in","fe_slit_1","width").getAperture()

		self.mono_theta=Organizer(s,"bl_32in","tc1_stmono_1","theta").getPosition()
		self.mono_y1=Organizer(s,"bl_32in","tc1_stmono_1","y1").getPosition()
		self.mono_z1=Organizer(s,"bl_32in","tc1_stmono_1","z1").getPosition()
		self.mono_dtheta1=Organizer(s,"bl_32in","tc1_stmono_1","dtheta1").getPosition()
		self.mono_thetay1=Organizer(s,"bl_32in","tc1_stmono_1","thetay1").getPosition()
		self.mono_z2=Organizer(s,"bl_32in","tc1_stmono_1","z2").getPosition()
		self.mono_thetax2=Organizer(s,"bl_32in","tc1_stmono_1","thetax2").getPosition()
		self.mono_thetay2=Organizer(s,"bl_32in","tc1_stmono_1","thetay2").getPosition()
		self.mono_xt=Organizer(s,"bl_32in","tc1_stmono_1","xt").getPosition()
		self.mono_zt=Organizer(s,"bl_32in","tc1_stmono_1","zt").getPosition()

		self.tcs_height=Organizer(s,"bl_32in","tc1_slit_1","height").getAperture()
		self.tcs_width=Organizer(s,"bl_32in","tc1_slit_1","width").getAperture()
		self.tcs_vert=Organizer(s,"bl_32in","tc1_slit_1","vertical").getPosition()
		self.tcs_hori=Organizer(s,"bl_32in","tc1_slit_1","horizontal").getPosition()

		self.vfm_y=Organizer(s,"bl_32in","st2_mv_1","y").getPosition()
		self.vfm_z=Organizer(s,"bl_32in","st2_mv_1","z").getPosition()
		self.vfm_tx=Organizer(s,"bl_32in","st2_mv_1","tx").getPosition()
		self.vfm_ty=Organizer(s,"bl_32in","st2_mv_1","ty").getPosition()
		self.vhm_y=Organizer(s,"bl_32in","st2_mh_1","y").getPosition()
		self.vhm_z=Organizer(s,"bl_32in","st2_mh_1","z").getPosition()
		self.vhm_tz=Organizer(s,"bl_32in","st2_mh_1","tz").getPosition()

	def getID(self):
		if isStore==-1:
			self.storeInfo()

		rtnstr="ID gap:		%12.5f mm"%self.id_gap
		return(stnstr)

	def getFES(self):
		if isStore==-1:
			self.storeInfo()

		print "FES (H x W)=(%12.5f mmx %12.5f mm)"%(self.fes_height,self.fes_width)
		print "FES (V , H)=(%12.5f mm, %12.5f mm)"%(self.fes_hori,self.fes_hori)

	def mono(self):
		#print "MONO: %12.5f pulse"%self.mono_theta=Organizer(s,"bl_32in","tc1_stmono_1","theta").getPosition()
		#print "MONO: %12.5f pulse"%self.mono_y1=Organizer(s,"bl_32in","tc1_stmono_1","y1").getPosition()
		#print "MONO: %12.5f pulse"%self.mono_z1=Organizer(s,"bl_32in","tc1_stmono_1","z1").getPosition()
		#print "MONO: %12.5f pulse"%self.mono_dtheta1=Organizer(s,"bl_32in","tc1_stmono_1","dtheta1").getPosition()
		#print "MONO: %12.5f "%self.mono_thetay1=Organizer(s,"bl_32in","tc1_stmono_1","thetay1").getPosition()
		#print "MONO: %12.5f "%self.mono_z2=Organizer(s,"bl_32in","tc1_stmono_1","z2").getPosition()
		#print "MONO: %12.5f "%self.mono_thetax2=Organizer(s,"bl_32in","tc1_stmono_1","thetax2").getPosition()
		#print "MONO: %12.5f "%self.mono_thetay2=Organizer(s,"bl_32in","tc1_stmono_1","thetay2").getPosition()
		#print "MONO: %12.5f "%self.mono_xt=Organizer(s,"bl_32in","tc1_stmono_1","xt").getPosition()
		print "mono"
		#print "MONO: %12.5f "%self.mono_zt=Organizer(s,"bl_32in","tc1_stmono_1","zt").getPosition()

	def all(self,ofname):
    		d=datetime.datetime.today()

		ofile=open(ofname,"w")
		ofile.write("### %s ####\n"%d)
    		ofile.write( "##### ID #####\n")
    		ofile.write( "ID gap\t:%12s%7s\n" % Organizer(self.s,"bl_32in","id_gap","").getPosition())
    		ofile.write( "##### Front End ####\n")
    		ofile.write( "vert\t:%12s%7s\n" % Organizer(self.s,"bl_32in","fe_slit_1","vertical").getPosition())
    		ofile.write( "hori\t:%12s%7s\n" % Organizer(self.s,"bl_32in","fe_slit_1","horizontal").getPosition())
    		ofile.write( "height\t:%12s%7s\n" % Organizer(self.s,"bl_32in","fe_slit_1","height").getAperture())
    		ofile.write( "width\t:%12s%7s\n" % Organizer(self.s,"bl_32in","fe_slit_1","width").getAperture())
    		ofile.write( "##### Monochromator ####\n")
    		ofile.write( "Energy\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_stmono_1","").getEnergy())
    		ofile.write( "Angle\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_stmono_1","").getAngle())
    		ofile.write( "Wavelength\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_stmono_1","").getRamda())
    		ofile.write( "Theta\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_stmono_1","theta").getPosition())
    		ofile.write( "Y1\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_stmono_1","y1").getPosition())
    		ofile.write( "Z1\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_stmono_1","z1").getPosition())
    		ofile.write( "Dth1\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_stmono_1","dtheta1").getPosition())
    		ofile.write( "Ty1\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_stmono_1","thetay1").getPosition())
    		ofile.write( "Z2\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_stmono_1","z2").getPosition())
    		ofile.write( "Tx2\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_stmono_1","thetax2").getPosition())
    		ofile.write( "Ty2\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_stmono_1","thetay2").getPosition())
    		ofile.write( "Xt\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_stmono_1","xt").getPosition())
    		ofile.write( "Zt\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_stmono_1","zt").getPosition())
    		ofile.write( "##### TC slit ####\n")
    		ofile.write( "height\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_slit_1","height").getAperture())
    		ofile.write( "width\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_slit_1","width").getAperture())
    		ofile.write( "vert\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_slit_1","vertical").getPosition())
    		ofile.write( "hori\t:%12s%7s\n" % Organizer(self.s,"bl_32in","tc1_slit_1","horizontal").getPosition())
    		ofile.write( "##### Mirror ####\n")
    		ofile.write( "VFM-y\t:%12s%7s\n" % Organizer(self.s,"bl_32in","st2_mv_1","y").getPosition())
    		ofile.write( "VFM-z\t:%12s%7s\n" % Organizer(self.s,"bl_32in","st2_mv_1","z").getPosition())
    		ofile.write( "VFM-tx\t:%12s%7s\n" % Organizer(self.s,"bl_32in","st2_mv_1","tx").getPosition())
    		ofile.write( "VFM-ty\t:%12s%7s\n" % Organizer(self.s,"bl_32in","st2_mv_1","ty").getPosition())
    		ofile.write( "HFM-y\t:%12s%7s\n" % Organizer(self.s,"bl_32in","st2_mh_1","y").getPosition())
    		ofile.write( "HFM-z\t:%12s%7s\n" % Organizer(self.s,"bl_32in","st2_mh_1","z").getPosition())
    		ofile.write( "HFM-tz\t:%12s%7s\n" % Organizer(self.s,"bl_32in","st2_mh_1","tz").getPosition())
		ofile.write("##### Stage ####\n")
		ofile.write("Stage-y\t:%12s%7s\n" % Organizer(self.s,"bl_32in","st2_stage_1","y").getPosition())
		ofile.write("Stage-z\t:%12s%7s\n" % Organizer(self.s,"bl_32in","st2_stage_1","z").getPosition())
		ofile.write("Gonio phi\t:%12s%7s\n" % Organizer(self.s,"bl_32in","st2_gonio_1","phi").getPosition())
		ofile.write("Gonio x\t:%12s%7s\n" % Organizer(self.s,"bl_32in","st2_gonio_1","x").getPosition())
		ofile.write("Gonio y\t:%12s%7s\n" % Organizer(self.s,"bl_32in","st2_gonio_1","y").getPosition())
		ofile.write("Gonio z\t:%12s%7s\n" % Organizer(self.s,"bl_32in","st2_gonio_1","z").getPosition())
		ofile.write("Gonio zz\t:%12s%7s\n" % Organizer(self.s,"bl_32in","st2_gonio_1","zz").getPosition())

		ofile.close()

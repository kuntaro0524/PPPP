import time
import socket
import sys

#import Motor as Motor
from File import *
#from Motor import *

class Polling:
	def __init__(self,server):
		self.s=server
		self.isStore=-1

	def poll(self,ofname):
		ofile=open(ofname,"w")
#	A-ch
		com_s1u="get/bl_32in_st2_slit_1_upper/status"
		com_s1l="get/bl_32in_st2_slit_1_lower/status"
		com_s1h="get/bl_32in_st2_slit_1_hall/status"
		com_s1r="get/bl_32in_st2_slit_1_ring/status"
		com_s2u="get/bl_32in_st2_slit_2_upper/status"
		com_s2l="get/bl_32in_st2_slit_2_lower/status"
		com_s2h="get/bl_32in_st2_slit_2_hall/status"
		com_s2r="get/bl_32in_st2_slit_2_ring/status"
#	B-ch
		com_mvty="get/bl_32in_st2_mv_1_ty/status"
		com_mhtz="get/bl_32in_st2_mh_1_tz/status"
		com_mvtx="get/bl_32in_st2_mv_1_tx/status"
		com_mvz="get/bl_32in_st2_mv_1_z/status"
		com_mvy="get/bl_32in_st2_mv_1_y/status"
		com_mhz="get/bl_32in_st2_mh_1_z/status"
		com_mhy="get/bl_32in_st2_mh_1_y/status"
		com_micx="get/bl_32in_st2_coax_1_x/status"
#	C-ch
		com_micz="get/bl_32in_st2_coax_1_zoom/status"
		com_colliy="get/bl_32in_st2_collimator_1_y/status"
		com_colliz="get/bl_32in_st2_collimator_1_z/status"
		com_att="get/bl_32in_st2_att_1_rx/status"
		com_monz="get/bl_32in_st2_monitor_1_z/status"
		com_mony="get/bl_32in_st2_monitor_1_y/status"
		com_bsz="get/bl_32in_st2_bs_1_z/status"
		com_bsy="get/bl_32in_st2_bs_1_y/status"
#	D-ch
		com_gphi="get/bl_32in_st2_gonio_1_phi/status"
		com_gx="get/bl_32in_st2_gonio_1_x/status"
		com_gy="get/bl_32in_st2_gonio_1_y/status"
		com_gz="get/bl_32in_st2_gonio_1_z/status"

#	E-ch
		com_gzz="get/bl_32in_st2_gonio_1_zz/status"
		com_lz="get/bl_32in_st2_light_1_z/status"
		com_sty="get/bl_32in_st2_stage_1_y/status"
		com_stz="get/bl_32in_st2_stage_1_z/status"
		com_mx="get/bl_32in_st2_detector_1_x/status"
		com_cryo="get/bl_32in_st2_cryo_1_z/status"
		com_dety="get/bl_32in_st2_detector_1_y/status"
		com_cmos="get/bl_32in_st2_detector_2_z/status"

#	F-ch
		com_m1="get/bl_32in_st2_motor_1/status"
		com_m2="get/bl_32in_st2_motor_2/status"
		com_m3="get/bl_32in_st2_motor_3/status"
		com_m4="get/bl_32in_st2_motor_4/status"

#		ofile.write("count, a1, a2, a3, a4, a5, a6, a7, a8\n")
#		ofile.write("count, b1, b2, b3, b4, b5, b6, b7, b8\n")
#		ofile.write("count, c1, c2, c3, c4, c5, c6, c7, c8\n")
#		ofile.write("count, d1, d3, d4, d5\n")
#		ofile.write("count, e1, e2, e3, e4, e5, e6, e7, e8\n")
#		ofile.write("count, f1, f2, f3, f4\n")


		ofile.write("count, MX225_X, CMOS_Z, Gonio_ZZ, Light_Z, St_Y, St_Z, Cryo_Z, Detector_Y, Monitor_Y, Monitor_Z, BS_Y, BS_Z, M1, M2, M3, M4\n")
		print("count, MX225_X, CMOS_Z, Gonio_ZZ, Light_Z, St_Y, St_Z, Cryo_Z, Detector_Y, Monitor_Y, Monitor_Z, BS_Y, BS_Z, M1, M2, M3, M4")

		mony0=0
		monz0=0
		bsy0=0
		bsz0=0

		gzz0=0
		lz0=0
		sty0=0
		stz0=0
		mx0=0
		cryo0=0
		dety0=0
		cmos0=0

		m10=0
		m20=0
		m30=0
		m40=0

		count=0

#		count=100000
		while 1:
#		while count:

			self.s.sendall(com_mony)
			recbuf=self.s.recv(8000)
			self.tmp_mony=recbuf.split("/")

			self.s.sendall(com_monz)
			recbuf=self.s.recv(8000)
			self.tmp_monz=recbuf.split("/")

			self.s.sendall(com_bsy)
			recbuf=self.s.recv(8000)
			self.tmp_bsy=recbuf.split("/")

			self.s.sendall(com_bsz)
			recbuf=self.s.recv(8000)
			self.tmp_bsz=recbuf.split("/")

			self.s.sendall(com_gzz)
			recbuf=self.s.recv(8000)
			self.tmp_gzz=recbuf.split("/")

			self.s.sendall(com_lz)
			recbuf=self.s.recv(8000)
			self.tmp_lz=recbuf.split("/")

			self.s.sendall(com_sty)
			recbuf=self.s.recv(8000)
			self.tmp_sty=recbuf.split("/")

			self.s.sendall(com_stz)
			recbuf=self.s.recv(8000)
			self.tmp_stz=recbuf.split("/")

			self.s.sendall(com_mx)
			recbuf=self.s.recv(8000)
			self.tmp_mx=recbuf.split("/")

			self.s.sendall(com_cryo)
			recbuf=self.s.recv(8000)
			self.tmp_cryo=recbuf.split("/")

			self.s.sendall(com_dety)
			recbuf=self.s.recv(8000)
			self.tmp_dety=recbuf.split("/")

			self.s.sendall(com_cmos)
			recbuf=self.s.recv(8000)
			self.tmp_cmos=recbuf.split("/")

			self.s.sendall(com_m1)
			recbuf=self.s.recv(8000)
			self.tmp_m1=recbuf.split("/")

			self.s.sendall(com_m2)
			recbuf=self.s.recv(8000)
			self.tmp_m2=recbuf.split("/")

			self.s.sendall(com_m3)
			recbuf=self.s.recv(8000)
			self.tmp_m3=recbuf.split("/")

			self.s.sendall(com_m4)
			recbuf=self.s.recv(8000)
			self.tmp_m4=recbuf.split("/")

#			ofile.write("SEND: %s\n"%(com_mx))
#			ofile.write("RECV: %s\n"%(recbuf_mx))
#			ofile.write("%s MX225HE X: %s\n"%(d_mx, self.tmp_mx[3]))
#			ofile.write("SEND: %s\n"%(com_cmos))
#			ofile.write("RECV: %s\n"%(recbuf_cmos))
#			ofile.write("%s    CMOS Z: %s\n"%(d_mx, self.tmp_cmos[3]))

			if (self.tmp_mx)[3]!=mx0 or (self.tmp_cmos)[3]!=cmos0 or (self.tmp_gzz)[3]!=gzz0 or (self.tmp_lz)[3]!=lz0 or (self.tmp_sty)[3]!=sty0 or (self.tmp_stz)[3]!=stz0 or (self.tmp_cryo)[3]!=cryo0 or (self.tmp_dety)[3]!=dety0 or (self.tmp_mony)[3]!=mony0 or (self.tmp_monz)[3]!=monz0 or (self.tmp_bsy)[3]!=bsy0 or (self.tmp_bsz)[3]!=bsz0 or (self.tmp_m1)[3]!=m10 or (self.tmp_m2)[3]!=m20 or (self.tmp_m3)[3]!=m30 or (self.tmp_m4)[3]!=m40:
				ofile.write("\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s\n"%(count, self.tmp_mx[3], self.tmp_cmos[3], self.tmp_gzz[3], self.tmp_lz[3], self.tmp_sty[3], self.tmp_stz[3], self.tmp_cryo[3],
				 self.tmp_dety[3], self.tmp_mony[3], self.tmp_monz[3], self.tmp_bsy[3], self.tmp_bsz[3], self.tmp_m1[3], self.tmp_m2[3], self.tmp_m3[3], self.tmp_m4[3]))
				print("\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s"%(count, self.tmp_mx[3], self.tmp_cmos[3], self.tmp_gzz[3], self.tmp_lz[3], self.tmp_sty[3], self.tmp_stz[3], self.tmp_cryo[3],
				 self.tmp_dety[3], self.tmp_mony[3], self.tmp_monz[3], self.tmp_bsy[3], self.tmp_bsz[3], self.tmp_m1[3], self.tmp_m2[3], self.tmp_m3[3], self.tmp_m4[3]))
				mony0=self.tmp_mony[3]
				monz0=self.tmp_monz[3]
				bsy0=self.tmp_bsy[3]
				bsz0=self.tmp_bsz[3]
				sty0=self.tmp_sty[3]
				stz0=self.tmp_stz[3]
				gzz0=self.tmp_gzz[3]
				cryo0=self.tmp_cryo[3]
				lz0=self.tmp_lz[3]
				dety0=self.tmp_dety[3]
				mx0=self.tmp_mx[3]
				cmos0=self.tmp_cmos[3]
				m10=self.tmp_m1[3]
				m20=self.tmp_m2[3]
				m30=self.tmp_m3[3]
				m40=self.tmp_m4[3]
				
			time.sleep(0.01)
			count += 1
		
		ofile.close()
		return 1

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	f=File("./")
        prefix="%03d"%f.getNewIdx3()

	ax=Polling(s)

    	ofile=prefix+"_poll.dat"   #hashi 100615
	ax.poll(ofile)              #hashi 100615
	#print ax.getLeastInfo() 
	

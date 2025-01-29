import sys,math,os,socket
import DrawPolygonMouse
import Inocc2
import time

tmpfile="/isilon/BL32XU/BLsoft/PPPP/03.GUI/04.SACLA-KUMA/test.ppm"
server_IP="192.168.163.1"
server_port=10101

if __name__ == "__main__":
	dpm=DrawPolygonMouse.DrawPolygon()
	ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ms.connect((server_IP, server_port))
	crycen=Inocc2.crycen(ms)

	# Current cross center Gonio xyz values
	phi,cenx,ceny,cenz=crycen.get_axes_info_float()
	print phi,cenx,ceny,cenz
	filename=tmpfile
	crycen.get_coax_image(filename,convert=False)
	#crycen.move_by_img_px(157,167)
	grav_x,grav_y,xylist=dpm.run(filename)
	#crycen.move_by_img_px(grav_x,grav_y)

	gxyz=[]
	for xy in xylist:
		x,y=xy
		print "PIXPLOT ",x,y
		tx,ty,tz=crycen.calc_gxyz_of_pix_at(x,y,cenx,ceny,cenz,phi)
		print "GONIOPLOT ",tx,ty,tz
		gxyz.append((tx,ty,tz))

	#print xylist
	print gxyz

	for xyz in gxyz:
		x,y,z=xyz
		crycen.move_gonio_abs(phi,x,y,z)
		time.sleep(3)
	#x,y=dpm.run(filename)
	#crycen.move_by_img_px(x,y)
	ms.close()

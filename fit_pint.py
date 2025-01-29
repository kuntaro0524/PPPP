import cv2,sys,socket
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/10.Zoo/Libs/")
import Gonio
import Capture

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

gonio=Gonio.Gonio(s)
capture=Capture.Capture()
 
def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()


# load the image, convert it to grayscale, and compute the
# focus measure of the image using the Variance of Laplacian
# method


# if the focus measure is less than the supplied threshold,
# then the image should be considered "blurry"

def fitPint(pitch,ntimes,prefix):
	index=0
	logfile="%s_plot.txt"%prefix
	ofile=open(logfile,"w")
	nwing=ntimes/2+1
	gonio.movePint(-nwing*pitch)

	score_max=-999999
	for index in range(0,ntimes+2):
		# show the image
		gonio.movePint(pitch)
		imname="/isilon/users/target/target/%s%03d.ppm"%(prefix,index)
		image=capture.capture(imname)
	
		image = cv2.imread(imname)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		fm = variance_of_laplacian(gray)
	
		text = "Boketenai"
		if fm < 1000:
			text = "Blurry"
		logtext="%s %s"%(text,fm)
		cv2.putText(image, logtext, (10, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
		cv2.imwrite("%s%02d.png"%(prefix,index),image)
		ofile.write("%s %8.5f %s \n"%(imname,pitch*index,fm))
		print("%s %8.5f %s \n"%(imname,pitch*index,fm))
	
		if score_max < fm:
			score_max=fm
			x,y,z=gonio.getXYZmm()
	
		index+=1

	gonio.moveXYZmm(x,y,z)
	return x,y,z

fitPint(200,10,"200_20")
fitPint(100,10,"100_10")


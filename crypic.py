import os
from Gonio import *
from Capture import *

if __name__=="__main__":

        #host = '172.24.242.54' # BL41XU MS IP address
        #host = '172.24.242.54' # BL41XU MS IP address
        host = '172.24.242.41'
        port = 10101
	
	# Open a connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	# init
        gonio=Gonio(s)
        cap=Capture()

	# File name
	#prefix="snapshot"
	prefix=sys.argv[1]

	# curr dire
	abspath=os.path.abspath("./")
	root_filename="%s/%s"%(abspath,prefix)

	# phi list
	save=gonio.getPhi()
	off90=save+90.0

	phi_list=[save,off90]
	
	for phi in phi_list:
		# rotation
		gonio.rotatePhi(phi)
		# capture
		phistr="_%05.1f.ppm"%phi
		fname=root_filename+phistr
		cap.captureWithCross(fname)

	gonio.rotatePhi(save)

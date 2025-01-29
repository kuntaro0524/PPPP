import os
from Gonio import *
from Capture import *

if __name__=="__main__":

        #host = '172.24.242.54' # BL41XU MS IP address
        host = '172.24.242.41' # BL41XU MS IP address
        port = 10101
	
	# Open a connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	# init
        gonio=Gonio(s)
        cap=Capture()

	# File name
	prefix="snapshot"
	#prefix=sys.argv[1]

	# curr dire
	abspath=os.path.abspath("./")
	root_filename="%s/%s"%(abspath,prefix)

	# phi list
	phi_list=[0.0,90.0,180.0,270.0]
	
	for phi in phi_list:
		# rotation
		gonio.rotatePhi(phi)
		# capture
		phistr="%05.1f.ppm"%phi
		fname=root_filename+phistr
		cap.capture(fname)

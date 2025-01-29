import socket
import time
import datetime

# My library
from ExSlit1 import *
from File import *
from Att import *
from MyException import *
from BS import *
from Shutter import *
from Colli import *
from Light import *
from ExSlit1 import *

if __name__ == "__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	
	useColli=True

	exptime=float(sys.argv[1])

	# Devices
	shutter=Shutter(s)
	colli=Colli(s)
	bs=BS(s)
	slit1=ExSlit1(s)
	light=Light(s)

	# Prep open
	# Shutter close
	shutter.close()

	# BS on
	#bs.on()
	bs.off()

	# Collimator
	if useColli:
		colli.on()

	# Slit1 open
	slit1.openV()

	# Light on
	#light.goOn()

	# Wait
	time.sleep(5)

	# Exposure
	shutter.open()
	time.sleep(exptime)
	shutter.close()

	# Slit1 close
	colli.off()
	slit1.closeV()

	s.close()

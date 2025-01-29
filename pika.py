import socket
import time
import datetime

# My library
import Morning

def time_now():
	strtime=datetime.datetime.now().strftime("%H:%M:%S")
	return strtime

def date_now():
	strtime=datetime.datetime.now().strftime("%Y%m%d-%H%M")
	return strtime

if __name__=="__main__":
	mng=Morning.Morning("./")

	# Scintillator set position
	#time.sleep(180)
	#mng.prepBC()
	#picy,picz=mng.doCapAna("pika")
	#mng.setAtt(1000)
	# Open shutter
	#mng.prepScan()
	mng.finishBC()

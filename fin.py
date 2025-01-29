import socket
import time
import datetime

# My library
import Morning

if __name__=="__main__":
	mng=Morning.Morning("./")

	# Finish (remove beam monitor)
	mng.finishBC()
	mng.finishExposure()

	mng.allFin()
	logf.close()

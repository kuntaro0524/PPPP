import socket
import time
import datetime

# My library
from Morning import Morning

if __name__=="__main__":
	mng=Morning("./")

	mng.prepBC()
	mng.doCapAna("captest")
	mng.finishBS()
	mng.allFin()

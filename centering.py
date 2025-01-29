import sys,os,math,cv2,socket
import datetime
import numpy as np
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/10.Zoo/Libs/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/10.Zoo/")
from MyException import * 
import CryImageProc 
import CoaxImage
import BSSconfig
import Centering

from File import *

import matplotlib
import matplotlib.pyplot as plt

if __name__ == "__main__":
	ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ms.connect(("172.24.242.41", 10101))
	cnt=Centering.Centering(ms)
	phi_face=90

	start_time=datetime.datetime.now()
	backimg="/isilon/BL32XU/BLsoft/PPPP/10.Zoo/back.ppm"

	cnt.setBack(backimg)
	rwidth,rheight,phi_face,gonio_info=cnt.doAll(ntimes=2,skip=False,loop_size="small")
	print gonio_info,rwidth,rheight
	end_time=datetime.datetime.now()
	cons_time=end_time-start_time
	print start_time,end_time,cons_time

	ms.close()

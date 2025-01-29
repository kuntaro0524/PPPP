from numpy import *
import Device
import socket,time
import AttFactor

if __name__=="__main__":
        host = '172.24.242.41'
	dev=Device.Device(host)
	dev.init()


	attfac=AttFactor.AttFactor()
	thick_list,idx_list,pulse_list=attfac.getList()
	for t,p in zip(thick_list,pulse_list):
		print t,p

import sys
import socket
import time

# My library
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import Device

if __name__=="__main__":
    host = '172.24.242.41'

    dev = Device.Device(host)
    dev.finishBM()

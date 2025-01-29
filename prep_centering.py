import socket
import time
import datetime

# My library
import Device

if __name__=="__main__":
    dev = Device.Device("172.24.242.41")
    dev.init()

    dev.prepCentering()

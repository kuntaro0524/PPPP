#!/bin/env python 
import errno
import sys
import socket
import time
import datetime
import os
import numpy
from socket import error as socket_error
from MyException import *

beamline = "BL32XU"
# Copy from BL41XU ZOO 190419 K. Hirata

class Capture:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 10101
        self.open_sig = False  # network connection to videoserv
        self.isPrep = False
        self.user = os.environ["USER"]

        # Command for BL45XU
        # VIDEOSRV name for searching process via 'ps'
        self.videosrv = "videosrv"
        # Is videosrv running?"
        self.check_running = "ps -el > ./tmp"
        # Kill command
        self.kill_com = "killall videosrv"
        # Start command
        # BL32XU previous
        #self.start_com = "videosrv --v4l2 &"
        # BL32XU 2020.09.25 CCD camera of coax-camera is replaced.
        self.start_com="/usr/local/bss/videosrv3 --load_json=/blconfig/video/vg51/vg51.json --grab_mode opencv &"

        self.isDark = False

        if beamline == "BL45XU":
            # BL45XU setting
            # These values are not good for a transparent cryo-protectant
            # self.bright_default = 27000 #self.contrast_default = 36000
            # 2019/05/15 capture bright, contrast = 27000, 40000
            # Auto contrast was switched off
            # Back light was replaced by a darker one.
            # Baba-san guaged up the light power today (The values were not suitable for nylon loops)
            # self.bright_default = 27000
            # self.contrast_default = 40000
            # After tuning on 2019/05/19
            # After tuning on 2019/05/29 (Nakamura-san switched off the auto white balance
            self.bright_default = 30000
            self.contrast_default = 27000
        if beamline == "BL32XU":
            # obsoleted parameters
            # self.bright_default = 4000
            #self.bright_default = 3000
            #self.bright_default = 8000 # 240118 YK
            self.bright_default = 2800 # 240318 YK
            self.contrast_default = 18000
            #self.gain_default = 1200
            #self.gain_default = 3500 # YK@240118
            self.gain_default = 7500 # YK@240318
            if self.isDark == True:
                self.bright_default = 5500
                self.contrast_default = 5500

    def prep(self):
        if self.open_sig == True:
            self.isPrep = True
            # Set brightness 190418
            self.setBright(self.bright_default)
            # Set contrast 190418
            self.setContrast(self.contrast_default)
            # Set gain 201002
            self.setGain(self.gain_default)
            return True
        # Connection failed
        else:
            while (1):
                isConnect = self.connect()
                if isConnect == True:
                    self.isPrep = True
                    # Set brightness 190418
                    self.setBright(self.bright_default)
                    # Set contrast 190418
                    self.setContrast(self.contrast_default)
                    return True
                else:
                    self.restartVideoSrv()
                    time.sleep(3.0)

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.host, self.port))
            self.open_sig = True
        except socket_error as serr:
            return False
        return True

    def checkRunning(self):
        os.system(self.check_running)
        lines = open("./tmp", "r").readlines()

        for line in lines:
            if line.rfind(self.videosrv) != -1:
                return True
        return False

    def restartVideoSrv(self):
        # Kill videosrv
        os.system(self.kill_com)
        os.system(self.start_com)

    def disconnect(self):
        if self.open_sig == True:
            self.open_sig = False
            self.isPrep = False
            print "Closing the port..."
            self.s.close()

    #def setBright(self, bright=40000):
    #def setBright(self, bright=8000): # YK@240118
    def setBright(self, bright=2800): # YK@240318
        # set brightness
        com_bright = "put/video_brightness/%d" % bright
        self.s.sendall(com_bright)
        recbuf = self.s.recv(8000)
        print "setBright:",recbuf

    def setCross(self):
        com1 = "put/video_cross/on"
        self.s.sendall(com1)
        recbuf = self.s.recv(8000)

    # print recbuf

    def unsetCross(self):
        com1 = "put/video_cross/off"
        self.s.sendall(com1)
        recbuf = self.s.recv(8000)
        print recbuf

    def setContrast(self, contrast):
        com1 = "put/video_contrast/%d" % contrast
        self.s.sendall(com1)
        recbuf = self.s.recv(8000)
        print "setContrast:",recbuf

    def setGain(self, gain):
        com1 = "put/video_color/%d" % gain
        self.s.sendall(com1)
        recbuf = self.s.recv(8000)
        print "setGain:",recbuf

    # Quick capture : 190419
    #def capture(self, filename, speed=150, cross=False):
    # speed is not required except for BL32XU, probablly. K. Hirata 190419
    #def capture(self, filename, speed=150, cross=False):
    #def capture(self, filename, speed=3000, cross=False):
    #def capture(self, filename, speed=8000, cross=False): # YK 240118
    def capture(self, filename, speed=2800, cross=False): # YK 240318
        if self.isPrep == False:
            print "Preparation is called from capture function"
            self.prep()

        # comment out for BL45XU
        #if speed is not None:
            #self.setShutterSpeed(speed)
            #time.sleep(0.1)
        # moved to 'initialization'
        # self.setBright(bright)
        
        # For BL32XU  2022/12/06
        self.setBright(speed)

        self.setGain(self.gain_default)  # YK@240118

        # Unset cross
        if cross == False:
            self.unsetCross()
        else:
            self.setCross()
        com1 = "get/video_grab/%s" % filename
        print(com1)
        try:
            self.s.sendall(com1)
            recbuf = self.s.recv(8000)
            print recbuf
        except socket.error as e:
            raise MyException("capture failed!")

    def setShutterSpeed(self, speed):
        """ for BL32XU only
        command="ssh -l %s %s \"echo %d > /sys/class/video4linux/video0/shutter_width\""%(self.user,self.host,speed)
        os.system(command)
        """
        print "BL41XU skipped"

    def setBinning(self, binning):
        """
        if self.isPrep==0:
            self.prep()
        if self.open_sig==0:
            while (1):
                if self.connect()==True:
                    break
                else:
                    print "Retry Connection"
                    time.sleep(5)

        com1="put/video_prompt/on"
        self.s.sendall(com1)
        recbuf=self.s.recv(8000)
        #print "debug::",recbuf
        com1="put/video_binning/%d"%binning
        self.s.sendall(com1)
        recbuf=self.s.recv(8000)
        #print "debug::",recbuf
        """
        print "BL41XU skipped"

    def getBinning(self):
        if self.isPrep == False:
            self.prep()
        if self.open_sig == False:
            while (1):
                if self.connect() == True:
                    break
                else:
                    print "Retry Connection"
                    time.sleep(5)

        com1 = "get/video_binning/"
        self.s.sendall(com1)
        recbuf = self.s.recv(8000)
        print "debug::", recbuf
        sp = recbuf.split("/")
        if len(sp) == 5:
            return int(sp[-2])


if __name__ == "__main__":
    cap = Capture()
    cappath = "/isilon/BL32XU/BLsoft/PPPP/"
    print cap.prep()
    filename = os.path.join(cappath,"%s.ppm" % (sys.argv[1]))

    cap.capture(filename)

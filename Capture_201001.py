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
import Gonio
import Singleton

# My library
from BeamCenter import *

class Capture(Singleton.Singleton):
    def __init__(self):
        self.host='127.0.0.1' # for BL32XU videosrv DFK72 YK@190315
        self.port = 10101
        self.open_sig=False # network connection to videoserv
        self.isPrep=False
        self.user=os.environ["USER"]

        # Command for BL41XU
        # VIDEOSRV name for searching process via 'ps'
        #self.videosrv="videosrv" for BL41XU
        # For BL32XU Zoo
        self.videosrv="/usr/local/bss/videosrv.sh" # DFK72 YK@190315
        # For BL32XU Normal
        self.videosrv="/usr/local/bss/videosrv.sh"  #DFK72 YK@190315

        # Is videosrv running?
        self.check_running="ps -el > ./tmp"

        # Kill command
        #self.kill_com="killall videosrv"
        #self.kill_com="killall video_srv2"  #DFK72 YK@190315
        self.kill_com="killall videosrv3"  #DFK72 YK@190315
        # Start command
        ##self.start_com="ssh -XC -c arcfour %s %s --artray 3 &"%(self.host,self.videosrv)
        #self.start_com="%s --dfk 3 &"%(self.videosrv)   #DFK72 YK@190315
        self.start_com="%s --v4l2 &"%(self.videosrv)   #WAT231S2 YK@200121

        # Capture cross is false
        self.isCross=False
        
        # Brightness setting for BL32XU
        #self.def_bright=7500
        # Modified 2017/04/25 because lens contamination got to be terrible
        #self.def_bright=10000
        #self.def_bright=16     #DFK72 YK@190315
        self.bright=44000     #WAT231S2 YK@200121
        self.contrast=32768   

        #self.def_bright=50000 This is for Oda Kazumasa RED FILM 170729
        # shutter speed
        #self.speed=200
        self.speed=40   #DFK72 YK@190315 : Minimum magnification best exposure time

    def prep(self):
        if self.open_sig==True:
            print "In Capture::prep Already opened!!"
            self.isPrep = True
            return True

        # Connection failed
        else:
            doesItLive=self.confirmToStartVSRV(ntimes=10)
            if doesItLive==False:
                print "Failed to start VIDEOSRV"
                return False
            isItConnected=self.confirmToConnect(ntimes=10)
            if isItConnected==False:
                print "Failed to connect to VIDEOSRV"
                return False

        # Unset cross
        time.sleep(0.2)
        print "unset Cross"
        self.unsetCross()
        # set Brightness
        time.sleep(0.2)
        print "set bright=", self.bright
        self.setBright(self.bright)
        time.sleep(0.2)
        # set speed
        print "set speed"
        if self.speed is not None:
            self.setShutterSpeed(self.speed)
            time.sleep(0.1)
        self.isPrep = True

    def confirmToStartVSRV(self,ntimes=10):
        ncount=0
        while(1):
            ncount+=1
            # Running check
            isRun=self.checkRunning()
            print "isRun:",isRun
            if isRun==False:
                print "VIDEOSRV is not running"
                print "Booting the program..."
                self.restartVideoSrv()
            else:
                print "VIDEOSRV is running"
                return True
            print "tryToStartVideoSrv: trial=%5d"%ncount
            if ncount==ntimes:
                print "Giving up starting up VIDEOSRV"
                return False

    def confirmToConnect(self,ntimes=10):
        ncount=0
        while(1):
            ncount+=1
            # Try to connect
            isConnect=self.connect()
            if isConnect==True:
                print "normally connected!"
                self.isPrep=True
                return True
            if ncount==ntimes:
                print "Giving up connecting to VIDEOSRV from python"
                return False
            time.sleep(1.0)

    def connect(self):
        print "Now connection will be established."
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.host,self.port))
            self.open_sig=True
        except socket_error as serr:
            return False
        return True

    def checkRunning(self):
        # Temp file
        #tmpfile=tempfile.TemporaryFile()
        os.system("rm -rf ./tmp")
        #check_running="ssh %s \"ps aux | grep videosrv\" > ./tmp"%self.host
        #check_running="ps aux | grep video_srv2 > ./tmp"  #DFK72 YK@190315
        check_running="ps aux | grep videosrv3 > ./tmp"  #DFK72 YK@190315
        os.system(check_running)
        lines=open("./tmp","r").readlines()

        for line in lines:
            if line.rfind("grep")!=-1:
                continue
            if line.rfind(self.videosrv)!=-1:
                return True
        return False

    def restartVideoSrv(self):
        # Kill videosrv
        os.system(self.start_com)

    def disconnect(self):
        if self.open_sig==True:
            self.open_sig=False
            self.isPrep=False
            print "Closing the port..."
            self.s.close()

    def setBright(self,bright):
        # set brightness
        print "setBright bright=", bright
        com_bright="put/video_brightness/%d"%bright
        self.s.sendall(com_bright)  
        recbuf=self.s.recv(8000)   

        #command="v4l2-ctl --set-ctrl gain=%d" % (bright)     #for DFK72 YK@190315
        #command="v4l2-ctl --set-ctrl brightness=%d" % (bright)     #for WAT231S2 YK@200121
        #os.system(command)           #for DFK72 YK@190315
        #print recbuf

    def setContrast(self, contrast):
        com1 = "put/video_contrast/%d" % contrast
        self.s.sendall(com1)
        recbuf = self.s.recv(8000)
        print "setContrast:",recbuf

    def setCross(self):
        com1="put/video_cross/on"
        self.s.sendall(com1)
        recbuf=self.s.recv(8000)
        #print recbuf

    def unsetCross(self):
        com1="put/video_cross/off"
        self.s.sendall(com1)
        recbuf=self.s.recv(8000)

    #def capture(self,filename,exptime=40):
    def capture(self,filename,bright=44000,contrast=32500):

        if self.isPrep==False:
            print "Preparation is called from capture function"
            self.prep()

        # Set default brightness
        self.setBright(bright)   # for WAT231S2 YK@200121
        print "Setting bright in capture", bright
        self.setContrast(contrast)
        #self.setShutterSpeed(exptime)  # for DFK72 YK

        time.sleep(0.1)
        com1="get/video_grab/%s"%filename
        try:
            self.s.sendall(com1)
            recbuf=self.s.recv(8000)
        except socket.error as e:
            raise MyException("capture failed!")

        time.sleep(0.2)
        return

    def setShutterSpeed(self,speed):
        # For BL32XU
        ##command="ssh -l %s %s \"echo %d > /sys/class/video4linux/video0/shutter_width\""% \
        ##    (self.user,self.host,speed)
        # For DFK72 YK@190315
#        command="ssh -l %s %s \"v4l2-ctl --set-ctrl gain=%d\""% \
#            (self.user,self.host,speed)
        command="v4l2-ctl --set-ctrl exposure_absolute=%d" % (speed)
        os.system(command)
        """ for BL32XU only
        print "BL41XU skipped"
        """
    
    def setBinning(self, binning):
        if self.isPrep==False:
            print "Preparation is called from capture function"
            self.prep()

        com1="put/video_prompt/on"
        self.s.sendall(com1)
        recbuf=self.s.recv(8000)
        #print "debug::",recbuf
        com1="put/video_binning/%d"%binning
        self.s.sendall(com1)
        recbuf=self.s.recv(8000)
        #print "debug::",recbuf

    def getBinning(self):
        if self.isPrep==False:
            self.prep()

        com1="get/video_binning/"
        self.s.sendall(com1)
        recbuf=self.s.recv(8000)
        #print "debug::",recbuf
        sp = recbuf.split("/")
        if len(sp) == 5:
            binning=int(sp[-2])
            print "Binning is %5d"%binning
            return binning

    #def aveCenter(self,prefix,avetime=5,speed=40):    #DFK72 YK@190315
    def aveCenter(self,prefix,avetime=5,bright=44000):    #WAT231S2 YK@200121
        totx=toty=0

        for i in range(0,avetime):
            filename="%s_%03d.ppm"%(prefix,i)
            #self.capture(filename,speed)  # for DFK72
            self.capture(filename,bright)    # for WAT231S2 YK@200121
            time.sleep(0.5)
            pp=BeamCenter(filename)
            #x,y=pp.find()
            x,y=pp.findRobust()

            totx+=x
            toty+=y

        cenx=totx/float(avetime)
        ceny=toty/float(avetime)

        return cenx,ceny

if __name__=="__main__":
    cappath="/isilon/BL32XU/BLsoft/PPPP/10.Zoo/Libs/"
    idx=0

    import Device_200929
    #dev=Device.Device("192.168.163.1")
    dev=Device_200929.Device("172.24.242.41")
    dev.init()
    #dev.capture.prep()
    #dev.capture.unsetCross()
    #picpath="/isilon/BL32XU/BLsoft/PPPP/10.Zoo/back_171016_10000_200.ppm"
    #picpath="/isilon/BL32XU/BLsoft/PPPP/10.Zoo/BackImages/back.ppm"
    picpath="/isilon/BL32XU/BLsoft/PPPP/needle.ppm"
    #picpath="/isilon/BL32XU/BLsoft/PPPP/10.Zoo/redlight.ppm"
    #dev.capture.setBright(65535)

    #dev.capture.setShutterSpeed(500)
    #dev.capture.capture(picpath,exptime=130)   #for DFK72 YK
    #def capture(self,filename,brig=40,contrast=contrast):
    #dev.capturesetShutterSpeed(self,speed):
    #dev.capture.capture(picpath,bright=10000,contrast=10000)    # for WAT231S2 YK@2000121
    dev.capture.capture(picpath, bright=37800, contrast=65535)

    #print dev.capture.getBinning()

    """
    for i in numpy.arange(0,100):
        dev.capture.getBinning()
        dev.setBinning(self, binning):
        time.sleep(0.2)
    """

    """
    phi_list=[0,30,60,90,120,150,180]

    for phi in phi_list:
        dev.gonio.rotatePhi(phi)
        picpath="%s/test_%05.2f.ppm"%(cappath,phi)
        dev.capture.prep()
        dev.capture.capture(picpath)
    """

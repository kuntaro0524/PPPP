import sys,os,math,cv2,socket,time,copy,datetime
from Mono import *
from MBS import *
from DSS import *
from ID import *
from TCS import *
from RingCurrent import *


class Asing():
    def __init__(self):
        host = '172.24.242.41'
        port = 10101
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host,port))

#        self.s=server

        self.id=ID(self.s)
        self.mono=Mono(self.s)
        self.tcs=TCS(self.s)
        self.mbs=MBS(self.s)
        self.dss=DSS(self.s)
        self.rc=RingCurrent(self.s)

    def isDump(self,wavelength):
        en=12.3984/wavelength
        gap=self.id.getE(en)
        print "target ID gap", gap

        # Status check
        status_mbs=self.mbs.getStatus()
        status_dss=self.dss.getStatus()
        ir=self.rc.getRingCurrent()
        status_id=self.id.isLocked()
        status_gap=self.id.getGap()

        print "Ring Current =", ir
        print "ID Status =",status_id
        print "ID Gap =",status_gap
        print "MBS Status =",status_mbs
        print "DSS_Status =",status_dss
        print ""

        if ir < 10.0:
            print("Ring Current is low")
            return True
        if status_mbs!="open":
            print("MBS is not opened")
            return True
#        if status_dss!="open":
#            print "DSS is not opened", status_dss
#            return True
        if status_id != 0:
            print("ID is locked")
            return True
        if status_gap > 40:
            print("ID open")
            return True
        return False

    def recover(self,wavelength):
        en=12.3984/wavelength
        gap=self.id.getE(en)

        ir=self.rc.getRingCurrent()
        status_id=self.id.isLocked()
        status_gap=self.id.getGap()
        status_mbs=self.mbs.getStatus()

        print "In Recover"
        print "Ring Current =", ir
        print "ID Status =",status_id
        print "ID Gap =",status_gap
        print "MBS Status =",status_mbs
        print ""

        if ir < 90.0:
            print "Ring Current is low"
            return False

        if status_mbs == "close":
            print "\ntry MBS open"
            if self.mbs.openTillOpen(wait_interval=10,ntrial=10)==False:
                print "MBS failed"
                return False
            print "\nMBS status in Recovered: Current status = ", status_mbs

        print "ID Gap =",status_gap
        if status_id == 0:
        #if status_gap != gap:
            print "\nID status is Unlocked, try ID change"
            if self.id.moveTillMove(gap,wait_interval=120,ntrial=10)==False:
                print "ID change failed"
                return False
            status_gap=self.id.getGap()
            print "\nID status in Recovered: Current Status = ", status_id, status_gap
        if status_id == 2:
            print "\ntry ID change but ID status is faile"
            if self.id.moveTillMove(gap,wait_interval=120,ntrial=10)==False:
                print "ID change failed"
                return False
            status_gap=self.id.getGap()
            print "\nID status in Recovered: Current Status = ", status_id, status_gap
        else:
            print "\nID status is Locked, wait unlocked"
            return False
        status_gap=self.id.getGap()
        if status_gap > gap:
            print "\ntry ID change again"
            if self.id.moveTillMove(gap,wait_interval=120,ntrial=20)==False:
                print "ID change failed"
                return False
            print "\nID status in Recovered: Current Status is ", status_id, status_gap

#       print "\ntry DSS open"
#        if self.dss.openTillOpen(wait_interval=60,ntrial=10)==False:
#            print "DSS open failed"
#            return False

        # Tune dtheta1
#        status_dss=self.dss.getStatus()
#        if status_dss=="open":
#            print "\nDTScan"
#            prefix="temporal"
#            self.mono.scanDt1PeakConfig(prefix,"DTSCAN_FULLOPEN",self.tcs)
#            today = datetime.date.today()
#            print(today)
#            return True

        #return False
        return True

if __name__=="__main__":
#    host = '172.24.242.41'
#    port = 10101 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s.connect((host,port))

    Wavelength=1.0

    asing=Asing()

    while True:
        if (asing.isDump(Wavelength) == True):
            now = datetime.datetime.now()
            print now
            print ""
            print "Dumpped"
            print "Start Recovering"
            if asing.recover(Wavelength) == True:
                print "\nFinish Recoverd from Dump !!\n"
            else:
                print "waiting for Beam Injection\n"
                time.sleep(60)
        else:
            now = datetime.datetime.now()
            print now
            print "Normal Running\n"
            time.sleep(600)


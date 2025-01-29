#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Motor import *
from MyException import *
from BSSconfig import *
from Count import *

# suddenly changed to +1 2018/04/06
#self.sense_y=1

#
class BS:
    def __init__(self,server):
        self.s=server
        self.bs_y=Motor(self.s,"bl_32in_st2_bs_1_y","pulse")
        self.bs_z=Motor(self.s,"bl_32in_st2_bs_1_z","pulse")
        self.sense_y=-1
        self.sense_z=1

        self.isInit=False
        self.v2p=2000

        # Default value
        self.off_pos=-2000 # pulse
        #self.off_pos=-500 # pulse
        self.evac_pos=-60000 # pulse
        self.on_pos=0 # pulse

        # Z limit
        #self.z_upper_limit=7500
        #self.z_lower_limit=-90000
        #self.z_upper_limit=5000
        #self.z_lower_limit=-75000
        #self.z_upper_limit=0
        #self.z_lower_limit=-70000
        self.z_upper_limit=0
        self.z_lower_limit=-2000

    def travelLimit2Limit(self):
        self.moveZ(self.z_upper_limit)
        self.moveZ(self.z_lower_limit)

    def getEvacuate(self):
        bssconf=BSSconfig()

        try:
            tmpon,tmpoff=bssconf.getBS()
        except MyException,ttt:
            print ttt.args[0]

        self.on_pos=float(tmpon)*self.v2p
        self.off_pos=float(tmpoff)*self.v2p

        self.isInit=True
        print self.on_pos,self.off_pos

    def getZ(self):
        return self.sense_z*int(self.bs_z.getPosition()[0])
    def getY(self):
        return self.sense_y*int(self.bs_y.getPosition()[0])

    def moveY(self,pls):
        self.bs_y.move(pls)

    def moveZ(self,pls):
        v=pls*self.sense_z
        self.bs_z.move(v)

    def scan2D(self,prefix,startz,endz,stepz,starty,endy,stepy):
        counter=Count(self.s,3,0)
        oname="%s_bs_2d.scn"%prefix
        of=open(oname,"w")

        min_y=99999.9999
        min_z=99999.9999
        cnt_min=9999999.9
        for z in arange(startz,endz,stepz):
            self.moveZ(self.sense_z*z)
            for y in range(starty,endy,stepy):
                self.moveY(self.sense_y*y)
                cnt=int(counter.getCount(0.2)[0])
                if cnt_min > cnt:
                    min_y=y
                    min_z=z
                of.write("%5d %5d %12d\n"%(y,z,cnt))
                of.flush()
            of.write("\n")
        of.close()
        return min_y,min_z

    def go(self,pvalue):
        self.bs_z.nageppa(pvalue)

    def on(self):
        if self.isInit==False:
            self.getEvacuate()
        self.bs_z.move(self.on_pos)

    def off(self):
        self.bs_z.move(self.off_pos)

    def goOn(self):
        if self.isInit==False:
            self.getEvacuate()
        self.go(self.on_pos)

    def evacManual(self):
        self.go(self.evac_pos)

    def presetZ(self,pulse):
        self.bs_z.preset(pulse)

    def goOff(self):
        if self.isInit==False:
            self.getEvacuate()
        self.go(self.off_pos)

    def isMoved(self):
        isY=self.bs_y.isMoved()
        isZ=self.bs_z.isMoved()

        if isY==0 and isZ==0:
            return True
        if isY==1 and isZ==1:
            return False

    def presetZ(self,pulse):
        self.bs_z.preset(pulse)

    def goOff(self):
        if self.isInit==False:
            self.getEvacuate()
        self.go(self.off_pos)

    def isMoved(self):
        isY=self.bs_y.isMoved()
        isZ=self.bs_z.isMoved()

        if isY==0 and isZ==0:
            return True
        if isY==1 and isZ==1:
            return False

if __name__=="__main__":
    host = '172.24.242.41'
    port = 10101
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))

    #print "Moving BS"
    #print "type on/off:"
    #option=raw_input()
    bs=BS(s)
    #print bs.getZ()
    #print bs.getY()
    #bs.evacManual()
    #print bs.getZ()
    #print bs.getZ()
    #bs.travelLimit2Limit()
    #bs.moveZ(-2000)
    #bs.presetZ(0)

    bs.moveZ(0)
    bs.moveY(0)

    z=bs.getZ()
    y=bs.getY()
    print z,y

    #def scan2D(self,prefix,startz,endz,stepz,starty,endy,stepy):
    #bs.scan2D(-200,200,20,-100,100,20)
    #bs.go(-30000)

    bs.off()
    #bs.on()
    #if option=="on":
    #bs.on()
    #elif option=="off":
    #bs.off()
    #s.close()
    s.close()

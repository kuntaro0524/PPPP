import sys,os,math

class CheckMTZ:

    def __init__(self,mtzname):
        self.mtzname=mtzname

    def extractFreeRcolumn(self):
        com="mtzdmp 

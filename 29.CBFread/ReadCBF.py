import h5py,glob,sys
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp
from PIL import Image
import PIL.ImageOps 
import numpy,os
import glob
import cv2

class ReadCBF:
    def __init__(self, cbf_file):
        self.cbf_file = cbf_file
        self.isRead = False

    def process(self):
        #print self.cbf_file
        #print cbf.modules()
        #arr, ndimfast, ndimslow = cbf.load_cbf_as_numpy(self.cbf_file,quiet=False)
        arr, ndimfast, ndimslow = cbf.load_minicbf_as_numpy(self.cbf_file,quiet=False)
        #print "mean=", numpy.mean(arr)
        #print arr, type(arr),arr.shape(),ndimfast, ndimslow
        ppp=arr.reshape(ndimfast, ndimslow)
        print "TYPE=",type(ppp),ppp.shape
        """
        for i in range(0,ndimfast):
            for j in range(0,ndimslow):
                value = ppp[i,j]
                if value > 20:
                    print i,j,value
        """
        return ppp

    def proc(self,array):
        print type(array),array.shape
        result1 = cv2.threshold(array,10,150,0)[1]
        cv2.imwrite(result1,"test.png")

    def pickup(self):
        print "test"

    def read(self):
        content = cbf.read(self.cbf_file)

if __name__ == "__main__":
    rc = ReadCBF(sys.argv[1])
    p = rc.process()
    rc.proc(p)
    #rc.read()

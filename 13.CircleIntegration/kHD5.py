import h5py
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp
import glob
import pylab as plt
import numpy

class kHD5:

    def __init__(self,masterfile):
        self.masterfile=masterfile
        self.isRead=False

    def read(self):
        # Read body information from master file
        #self.data=eiger.extract_data(self.masterfile,imgno,apply_pixel_mask=False)
        self.isRead=True

    def test(self):
        x=numpy.linspace(0,10,100)
        yorg=numpy.sin(x)
        y=numpy.sin(x)+numpy.random.randn(100)*0.2

        num=5.0
        b=numpy.ones(num)/num

        y2=numpy.convolve(y, b, mode='same')

        plt.plot(x,yorg,'r',label='original')
        plt.plot(x,y,'k-',label='genkei')
        plt.plot(x,y2,'b--', label='idouheikin')
        plt.legend()
        plt.savefig("test.png")

    def cutoff(self,imgno,threshold):
        data=eiger.extract_data(self.masterfile,imgno,apply_pixel_mask=False)
        nh,nv=data.shape
        ave=data.mean()
        for i in range(0,nh):
            for j in range(0,nv):
                if data[i,j]<ave:
                    data[i,j]=0
                    
        self.writeCBF(data,"tttt.cbf")

    def plotVline(self,imgno,horizontal_pix):
        data=eiger.extract_data(self.masterfile,imgno,apply_pixel_mask=False)
        nh,nv=data.shape
        vlist=[]
        for i in range(0,nv):
            vlist.append(data[horizontal_pix,i])
        vline=numpy.array(vlist)
        print vline.mean()

        

        #dline=data[horizontal_pix:horizontal_pix,0:vpix]
        #print dline

        #linedata=data[horizontal_pix:horizontal_pix,:]
        #print linedata
        #for i in len(linedata.shape):
            #print linedata[0:i]
        #for i in range(0, len(data[horizontal_pix:])):
            #print data[horizontal_pix:i]

    def writeCBF(self,data,outfile):
        h = eiger_hdf5_interpreter.Interpreter().getRawHeadDict(self.masterfile)
        h5 = h5py.File(self.masterfile, "r")

        h["Detector"] = h5["/entry/instrument/detector/description"].value
        h["ExposurePeriod"] = h5["/entry/instrument/detector/frame_time"].value

        cbf.save_numpy_data_as_cbf(data.flatten(), size1=data.shape[1], size2=data.shape[0], title="conv_%d"%imgno,
                             cbfout=outf,
                             pilatus_header="""\
# Detector: %(Detector)s, S/N %(SerialNumber)s
# Pixel_size %(PixelX)e m x %(PixelY)e m
# %(SensorMaterial)s sensor, thickness %(SensorThickness).3e m
# Exposure_time %(ExposureTime).6f s
# Exposure_period %(ExposurePeriod).6f s
# Count_cutoff %(Overload)d counts
# Wavelength %(Wavelength).6f A
# Detector_distance %(Distance).3e m
# Beam_xy (%(BeamX).1f, %(BeamY).1f) pixels
# Start_angle %(PhiStart).6f deg.
# Angle_increment %(PhiWidth).6f deg.
""" % h)


    def conv(self,imgno,outf):
        # Read header information from master file
        data=eiger.extract_data(self.masterfile,imgno,apply_pixel_mask=False)

        h = eiger_hdf5_interpreter.Interpreter().getRawHeadDict(self.masterfile)
        h5 = h5py.File(self.masterfile, "r")

        h["Detector"] = h5["/entry/instrument/detector/description"].value
        h["ExposurePeriod"] = h5["/entry/instrument/detector/frame_time"].value

        cbf.save_numpy_data_as_cbf(data.flatten(), size1=data.shape[1], size2=data.shape[0], title="conv_%d"%imgno,
                             cbfout=outf,
                             pilatus_header="""\
# Detector: %(Detector)s, S/N %(SerialNumber)s
# Pixel_size %(PixelX)e m x %(PixelY)e m
# %(SensorMaterial)s sensor, thickness %(SensorThickness).3e m
# Exposure_time %(ExposureTime).6f s
# Exposure_period %(ExposurePeriod).6f s
# Count_cutoff %(Overload)d counts
# Wavelength %(Wavelength).6f A
# Detector_distance %(Distance).3e m
# Beam_xy (%(BeamX).1f, %(BeamY).1f) pixels
# Start_angle %(PhiStart).6f deg.
# Angle_increment %(PhiWidth).6f deg.
""" % h)

    def run(self,paramlist):
        masterfile,startnum,endnum,outf=paramlist
        frameno=10
        data = None
        sel = None
        nimage=0

        for i in range(startnum,endnum):
            tmp = eiger.extract_data(masterfile, i, apply_pixel_mask=False)
            if data is None: data = tmp
            else:
                data += tmp
                #sel = tmp >= 0
                #data[sel] += tmp[sel]
                #print data
        if sel is None: sel = tmp < 0
        else: sel |= tmp < 0

        data[sel] = -10
        
        h = eiger_hdf5_interpreter.Interpreter().getRawHeadDict(masterfile)
        h5 = h5py.File(masterfile, "r")
        
        h["Detector"] = h5["/entry/instrument/detector/description"].value
        h["ExposurePeriod"] = h5["/entry/instrument/detector/frame_time"].value
        cbf.save_numpy_data_as_cbf(data.flatten(), size1=data.shape[1], size2=data.shape[0], title="merged_%d"%frameno,
                             cbfout=outf,
                             pilatus_header="""\
# Detector: %(Detector)s, S/N %(SerialNumber)s
# Pixel_size %(PixelX)e m x %(PixelY)e m
# %(SensorMaterial)s sensor, thickness %(SensorThickness).3e m
# Exposure_time %(ExposureTime).6f s
# Exposure_period %(ExposurePeriod).6f s
# Count_cutoff %(Overload)d counts
# Wavelength %(Wavelength).6f A
# Detector_distance %(Distance).3e m
# Beam_xy (%(BeamX).1f, %(BeamY).1f) pixels
# Start_angle %(PhiStart).6f deg.
# Angle_increment %(PhiWidth).6f deg.
""" % h)

if __name__ == "__main__":
    import sys
    master_file=sys.argv[1]
    startnum=int(sys.argv[2])

    h5=kHD5(master_file)
    outf="out.cbf"
    #conv(master_file,startnum,outf)
    imgno=1 
    horizontal_pix=1535
    #h5.plotVline(imgno,horizontal_pix)
    h5.cutoff(imgno,3.0)
    #h5.test()

import h5py,glob
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp
from PIL import Image
import PIL.ImageOps 
import numpy,os
import glob

class ConvertHD5:
    def __init__(self,conds):
        self.masterfile,self.startnum,self.endnum,self.outf=conds
        self.frameno=10
        self.data = None
        self.sel = None
        self.nimage=0

    def process(self):
        print "START-END=",self.startnum,self.endnum

        for i in range(self.startnum,self.endnum):
            tmp = eiger.extract_data(self.masterfile, i, apply_pixel_mask=False)
            if self.data is None: self.data = tmp
            else:
                self.data += tmp
        if self.sel is None: self.sel = tmp < 0
        else: self.sel |= tmp < 0

        self.data[self.sel] = -10

        h = eiger_hdf5_interpreter.Interpreter().getRawHeadDict(self.masterfile)
        h5 = h5py.File(self.masterfile, "r")
        
        h["Detector"] = h5["/entry/instrument/detector/description"].value
        h["ExposurePeriod"] = h5["/entry/instrument/detector/frame_time"].value
        cbf.save_numpy_data_as_cbf(self.data.flatten(), 
            size1=self.data.shape[1], 
            size2=self.data.shape[0], 
            title="merged_%d"%self.frameno,
            cbfout=self.outf,
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
        
        """ Not so good images
        d=self.data.flatten()
        size1,size2= self.data.shape
        #print size1,size2
        rsd=d.reshape(size1,size2)
        pil_img=Image.fromarray(numpy.uint8(rsd))
        reimage=pil_img.resize((800,800))
        pngname=self.outf.replace(".cbf",".png")
        #reimage=PIL.ImageOps.invert(reimage)
        reimage.save(pngname)
        """

        # ADXV image convert
        prefix=self.outf.replace(".cbf","")
        final_jpg="%s.jpg"%prefix
        tmp_jpg="%s_junk.jpg"%prefix
        command="adxv -sa -jpeg_scale 0.35 %s %s\n"%(self.outf,tmp_jpg)
        command+="sleep 2.0\n"
        print "CBF_FILE=",self.outf
        print "TMP_JPG=",tmp_jpg
        print "FINAL_JPG=",final_jpg
        command+="convert %s -font Times-Roman -pointsize 24 -gravity south -annotate 0 \"%s\" %s\n"%(tmp_jpg,self.outf,final_jpg)
        command+="sleep 2.0\n"
        command+="\\rm -Rf %s\n"%tmp_jpg

        print command
        os.system(command)
        
        return final_jpg
        """
        command="tar cvfz cbf.tgz *.cbf"
        os.system(command)
        command="\rm -Rf *.cbf"
        os.system(command)
        """

if __name__ == "__main__":
    import sys

    master_file=sys.argv[1]
    startnum=int(sys.argv[2])
    endnum=int(sys.argv[3])
    num_of_merge=int(sys.argv[4])

    n_frames=endnum-startnum+1
    n_block=int(n_frames/num_of_merge)

    proc_list=[]
    for i in range(0,n_block):
        bl_start=i*num_of_merge+1
        bl_end=bl_start+num_of_merge-1
        block_id=i+1
        filename="merged_%05d.cbf"%block_id
        proc_list.append((master_file,bl_start,bl_end,filename))

    print "making %05d files"%len(proc_list)
    easy_mp.pool_map(fixed_func=lambda n: ConvertHD5(n).process(), args=proc_list, processes=8)

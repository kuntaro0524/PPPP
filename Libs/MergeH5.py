import h5py,glob
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp
from PIL import Image
import PIL.ImageOps 
import numpy,os
import glob

class MergeH5:
    def __init__(self):
        self.isPrep = False
        self.nproc = 16

    def setNproc(self, nproc):
        self.nproc = nproc

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

        #h["Detector"] = h5["/entry/instrument/detector/description"].value
        h["Detector"] = "PILATUS3 6M"
        h["SerialNumber"] = "60-0125"
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

    def sumUpOsc(self, param_list):
        masterfile, startnum, endnum, out_img = param_list
        data = None
        sel = None

        print "Processing %05d - %05d : %s" % (startnum, endnum, out_img)
        # Loop of summing up images
        for imgnum in range(startnum, endnum):
            tmp = eiger.extract_data(masterfile, imgnum, apply_pixel_mask=False)
            if data is None:
                data = tmp
            else:
                data += tmp

        if sel is None:
            sel = tmp < 0
        else:
            sel |= tmp < 0

        data[sel] = -10

        h = eiger_hdf5_interpreter.Interpreter().getRawHeadDict(masterfile)
        #print "parametrs = " , h
        h5 = h5py.File(masterfile, "r")

        h["Detector"] = "PILATUS3 6M"
        h["SerialNumber"] = "60-0125"
        h["ExposurePeriod"] = h5["/entry/instrument/detector/frame_time"].value
        cbf.save_numpy_data_as_cbf(data.flatten(),
                                   size1=data.shape[1],
                                   size2=data.shape[0],
                                   title=out_img,
                                   cbfout=out_img,
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

        return True

    # Multiple dose slicing data
    # lys01_master.h5
    # data_000001.h5 1-100
    # data_000002.h5 101-200
    # data_000003.h5 201-300
    # data_000004.h5 301-400...

    def sumUpList(self, param_list):
        # sumnum_list:
        masterfile, sumnum_list, outdir, outprefix, out_imgnum, start_phi, osc_phi = param_list
        data = None
        sel = None

        for imgindex in sumnum_list:
            print "Reading %s %05d" % (masterfile, imgindex)
            tmp = eiger.extract_data(masterfile, imgindex, apply_pixel_mask=False)

            if data is None:
                data = tmp
            else:
                data += tmp

        if sel is None:
            sel = tmp < 0
        else:
            sel |= tmp < 0

        data[sel] = -10

        h = eiger_hdf5_interpreter.Interpreter().getRawHeadDict(masterfile)
        h5 = h5py.File(masterfile, "r")

        h['PhiStart'] = start_phi
        h['PhiWidth'] = osc_phi
        print "parametrs = " , h

        out_img = "%s/%s_%06d.cbf" % (outdir, outprefix, out_imgnum)
        h["Detector"] = "PILATUS3 6M"
        h["SerialNumber"] = "60-0125"
        h["ExposurePeriod"] = h5["/entry/instrument/detector/frame_time"].value
        cbf.save_numpy_data_as_cbf(data.flatten(),
                                   size1=data.shape[1],
                                   size2=data.shape[0],
                                   title=out_img,
                                   cbfout=out_img,
                                   pilatus_header="""
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

    def sumUpList2(self, param_list):
        masterfile, sumnum_list, start_phi, osc_phi, out_image = param_list
        data = None
        sel = None

        for imgindex in sumnum_list:
            print "Reading %s %05d" % (masterfile, imgindex)
            tmp = eiger.extract_data(masterfile, imgindex, apply_pixel_mask=False)

            if data is None:
                data = tmp
            else:
                data += tmp

        if sel is None:
            sel = tmp < 0
        else:
            sel |= tmp < 0

        data[sel] = -10

        h = eiger_hdf5_interpreter.Interpreter().getRawHeadDict(masterfile)
        h5 = h5py.File(masterfile, "r")

        h['PhiStart'] = start_phi
        h['PhiWidth'] = osc_phi
        print "parametrs = " , h

        h["Detector"] = "PILATUS3 6M"
        h["SerialNumber"] = "60-0125"
        h["ExposurePeriod"] = h5["/entry/instrument/detector/frame_time"].value
        cbf.save_numpy_data_as_cbf(data.flatten(),
                                   size1=data.shape[1],
                                   size2=data.shape[0],
                                   title=out_image,
                                   cbfout=out_image,
                                   pilatus_header="""
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

    #    mh5.sumDoseSlicing(master_file, n_sum_time, nimg_per_data, outprefix)
    def sumDoseSlicing(self, masterfile, n_sum_time, nimg_per_data, outprefix, dphi=0.1):
        data = None
        sel = None

        # Loop of summing up images
        proc_params = []
        start_phi = 0.0
        for original_imgnum in range(1, nimg_per_data+1):
            sumnum_list = []
            # n_sum_time : the number of summation time
            for junk_index in range(0, n_sum_time):
                sum_up_index = original_imgnum + nimg_per_data * (junk_index)
                sumnum_list.append(sum_up_index)

            # sumup list
            params = masterfile, sumnum_list, original_imgnum, outprefix, start_phi, dphi
            #params = masterfile, sumnum_list, block_id, outprefix, start_phi, dphi * nsum_rotation

            proc_params.append(params)
            start_phi += dphi

        easy_mp.pool_map(fixed_func=lambda n: self.sumUpList(n), args=proc_params, processes=self.nproc)

        return True

    #    mh5.sumDoseSlicing(master_file, n_sum_time, nimg_per_data, outprefix)
    def sumDoseSlicingPhiSlicing(self, masterfile, n_sum_time, nsum_rotation, nimg_per_data, outprefix, dphi=0.1):
        data = None
        sel = None
        ###
        sum_info_rot = []
        # Number of blocks: images in each block are summed up.
        n_block = int(nimg_per_data / nsum_rotation)
        for i in range(0, n_block):
            # calculate start/end image number for each block.
            bl_start = i * nsum_rotation + 1
            bl_end = bl_start + nsum_rotation - 1
            block_id = i + 1
            # List up merging condition
            sum_info_rot.append((masterfile, bl_start, bl_end, block_id))

        print "SUM_INFO_ROT=", sum_info_rot
        print "NSUM_TIME=", n_sum_time

        # sum_info_rot
        # n_block -> 100 frames 0.1 deg
        # n_block -> 10 blocks for 10 summation, 5 blocks for 20 summation
        # Loop of summing up images
        proc_params = []
        # Loop for each 'block'
        start_phi = 0.0
        for master_file, bl_start, bl_end, block_id in sum_info_rot:
            sumnum_list = []
            # Calculate start phi value for each block for preparing header information.
            start_phi += dphi * nsum_rotation
            # Calculate 'output' image number from 'block' index.
            for original_imgnum in range(bl_start,bl_end):
                # n_sum_time : the number of summation time
                for junk_index in range(0, n_sum_time):
                    sum_up_index = original_imgnum + nimg_per_data * (junk_index)
                    sumnum_list.append(sum_up_index)
            # sumup list
            params = masterfile, sumnum_list, block_id, outprefix, start_phi, dphi * nsum_rotation
            proc_params.append(params)

        print "PROC_PARAMS=", proc_params

        easy_mp.pool_map(fixed_func=lambda n: self.sumUpList(n), args=proc_params, processes=self.nproc)

        return True

    #######################
    # Input list: 
    #######################
    # image_list = [
    #   ("data01_001_master.h5", 11, 20), 
    #   ("data01_002_master.h5", 11, 20),
    #   ("data01_003_master.h5", 11, 20),
    # ]
    #######################
    # Other required information
    #######################
    # Output file information.
    # outprefix: prefix of the file
    # image_num: image number of the output file.
    # osc_start: start phi angle for this image
    # osc_width: oscillation width for this image
    #######################
    def sumUpSimpleList(self, param_list):
        # sumnum_list:
        master_info_list, outdir, outprefix, outnum, osc_start, osc_width = param_list

        data = None
        sel = None

        for master_name, start_num, end_num in master_info_list:
            for imgnum in range(start_num, end_num+1):
                tmp = eiger.extract_data(master_name, imgnum, apply_pixel_mask=False)

                if data is None:
                    data = tmp
                else:
                    data += tmp

            if sel is None:
                sel = tmp < 0
            else:
                sel |= tmp < 0
    
            data[sel] = -10

        # header information from the final master file
        h = eiger_hdf5_interpreter.Interpreter().getRawHeadDict(master_name)
        h5 = h5py.File(master_name, "r")

        # Read phi start and end
        h['PhiStart'] = osc_start
        h['PhiWidth'] = osc_width

        # Set the output filename and image number
        out_img = "%s/%s_%06d.cbf" % (outdir, outprefix, outnum)
        h["Detector"] = "PILATUS3 6M"
        h["SerialNumber"] = "60-0125"
        h["ExposurePeriod"] = h5["/entry/instrument/detector/frame_time"].value
        cbf.save_numpy_data_as_cbf(data.flatten(),
                                   size1=data.shape[1],
                                   size2=data.shape[0],
                                   title=out_img,
                                   cbfout=out_img,
                                   pilatus_header="""
# Detector: %(Detector)s, S/N %(SerialNumber)s
# Pixel_size 7.5e-5 m x 7.5e-5 m
# %(SensorMaterial)s sensor, thickness %(SensorThickness).3e m
# Exposure_time %(ExposureTime).6f s
# Exposure_period %(ExposurePeriod).6f s
# Count_cutoff %(Overload)d counts
# Wavelength %(Wavelength).6f A
# Detector_distance %(Distance)f m
# Beam_xy (%(BeamX).1f, %(BeamY).1f) pixels
# Start_angle %(PhiStart).6f deg.
# Angle_increment %(PhiWidth).6f deg.
        """ % h)

    def sumUp(self, masterfile, n_sum_time, nsum_rotation, nimg_per_data, outprefix, dphi=0.1):
        mh5.sumUpSimpleList(image_list, outprefix, imgnum, rot_start, osc_width)


if __name__ == "__main__":
    import sys

    master_file=sys.argv[1]
    startnum=int(sys.argv[2])
    endnum=int(sys.argv[3])
    num_of_merge=int(sys.argv[4])

    n_frames=endnum-startnum+1
    n_block=int(n_frames/num_of_merge)

    # master_file, startnum, endnum, out_imgnum, out_prefix = param_list

    proc_list=[]
    for i in range(0,n_block):
        bl_start=i*num_of_merge+1
        bl_end=bl_start+num_of_merge-1
        block_id=i+1
        filename="merged_%05d.cbf"%block_id
        proc_list.append((master_file, bl_start, bl_end, filename))

    print "making %05d files"%len(proc_list)
    easy_mp.pool_map(fixed_func=lambda n: MergeH5().sumDoseSlicing(n), args=proc_list, processes=1)

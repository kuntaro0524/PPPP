import sys,os
import h5py
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp
import glob

class HD5CBF:
	def __init__(self):
		print "HD5CBF"

	def merge(self,conds):
                master_file,startnum,endnum,cbfile=conds
		endnum=endnum
		print "Processing %s %d %d"%(master_file,startnum,endnum)
		data=None
		sel=None
		nimage=0
		for i in range(startnum,endnum+1):
			print "Processing %s %d"%(master_file,i)
			tmp = eiger.extract_data(master_file, i, apply_pixel_mask=False)
			print "Extracging"
			if data is None: data = tmp
			else:
				data += tmp
		if sel is None: sel = tmp < 0
		else: sel |= tmp < 0
		data[sel] = -10

		frameno=0

		print "DONE LOOP"
		h = eiger_hdf5_interpreter.Interpreter().getRawHeadDict(master_file)
		h5 = h5py.File(master_file, "r")

		h["Detector"] = h5["/entry/instrument/detector/description"].value
		h["ExposurePeriod"] = h5["/entry/instrument/detector/frame_time"].value
		cbf.save_numpy_data_as_cbf(data.flatten(), size1=data.shape[1], size2=data.shape[0], title="merged_%d"%frameno,
                             cbfout=cbfile,
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

if __name__=="__main__":
        lines=open(sys.argv[1],"r").readlines()
        conds_list=[]
	mpmp=HD5CBF()

	root_dir="."

	print type(lines)
	image_index=100

        for line in lines:
		master_file=line.strip()
		prefix=master_file[master_file.rfind("/")+1:master_file.rfind("_master")]
		print "PREFIX",prefix
                startnum=image_index
                endnum=image_index
                cbf_dir="%s/%s/"%(root_dir,prefix)
        
                if os.path.exists(cbf_dir)==False:
                        os.mkdir(cbf_dir)

                cbfile="%s/head-%d.cbf"%(cbf_dir,image_index)
        
                compo=master_file,startnum,endnum,cbfile
                conds_list.append(compo)

	print "#######################"
	print conds_list[0]
	print "#######################"

        easy_mp.pool_map(fixed_func=lambda n: mpmp.merge(n), args=conds_list, processes=8)

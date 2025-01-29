import sys,os
import h5py
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp
import glob

#def run(masterfile, startnum,endnum,outf):
def run(masterfile, startnum,endnum,outf):
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


lines=open(sys.argv[1],"r").readlines()

infiles=[]
outfiles=[]
numranges=[]

for line in lines:
	cols=line.split()
	score=float(cols[1])
	fname=cols[0]
	#print fname
	iii=fname.rfind("multi")
	prefix=fname[:iii]
	numrange=fname[iii:].replace("XDS_ASCII.HKL","").replace("multi_","").replace("/","")
	dddd=numrange.split("-")
	startnum=int(dddd[0])
	endnum=int(dddd[1])
	midnum=int((startnum+endnum)/2.0)
	#print midnum
	core_start=midnum-5
	core_end=midnum+5
	master_file="%smulti_master.h5"%prefix
	#print master_file
	jjj=fname.rfind("data")
	root_dir=fname[:jjj]
	cbf_dir="%s/data/cbf/"%root_dir

	if os.path.exists(cbf_dir)==False:
		os.mkdir(cbf_dir)
	cbfile="%s/merged-%d-%d.cbf"%(cbf_dir,core_start,core_end)
	infiles.append(master_file)
	outfiles.append(cbfile)
	numranges.append((core_start,core_end))
	print "Processing %s %d-%d -> %s"%(master_file,core_start,core_end,cbfile)

easy_mp.pool_map(fixed_func=lambda n: run(files, n, "merged_%.6d.cbf"%n),
        args=numbers, processes=8)

	#run(master_file,core_start,core_end,cbfile)

"eme-BKK10-07/data/BKK10-07-multi_1-100/XDS_ASCII.HKL 11219.37855"

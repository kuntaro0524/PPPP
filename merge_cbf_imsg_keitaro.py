import h5py
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp
import glob

def run(files, frameno, outf):
  data = None
  sel = None
  for i, f in enumerate(files):
    print f
    tmp = eiger.extract_data(f, frameno, apply_pixel_mask=False)
    if data is None: data = tmp
    else:
      data += tmp
      #sel = tmp >= 0
      #data[sel] += tmp[sel]
      #print data
    if sel is None: sel = tmp < 0
    else: sel |= tmp < 0

  data[sel] = -10

  h = eiger_hdf5_interpreter.Interpreter().getRawHeadDict(files[0])
  h5 = h5py.File(files[0], "r")

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

  files = glob.glob("*master.h5")

  #for n in xrange(1, 20000):
  #  run(files, n, "merged_%.6d.cbf"%n)
  numbers = range(1,100)
  easy_mp.pool_map(fixed_func=lambda n: run(files, n, "merged_%.6d.cbf"%n),
                   args=numbers, processes=8)

  quit()

  n = int(sys.argv[1])
  outf = sys.argv[2]
  run(files, n, outf)

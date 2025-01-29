import sys
import iotbx.mtz

get_I_arrays = lambda x: filter(lambda y: y.is_xray_intensity_array(), x)

def	run(mtz1,mtz2):

	# MTZ file reading
	m1 = iotbx.mtz.object(mtz1).as_miller_arrays(merge_equivalents=False)
	m2 = iotbx.mtz.object(mtz2).as_miller_arrays(merge_equivalents=False)

	# Extract intensity related cctbx.array
	m1_I = get_I_arrays(m1)[0]
	m2_I = get_I_arrays(m2)[0]

	# Take common sets of these
	m1_c,m2_c=m1_I.common_sets(m2_I, assert_is_similar_symmetry=False)

	assert len(m1_c.data()) == len(m2_c.data())

	ofile=open("out.dat","w")

	for (hkl1,I1,sigI1),(hkl2,I2,sigI2) in zip(m1_c,m2_c):
		assert hkl1 == hkl2
		h=hkl1[0]
		k=hkl1[1]
		l=hkl1[2]
		ofile.write("%5d%5d%5d %12.1f%12.1f\n"%(h,k,l,I1,I2))

	ofile.close()
	print "Done."

if __name__ == "__main__":

	if len(sys.argv)!=2:
		print "MTZ1 MTZ2"

	mtz1 = sys.argv[1]
	mtz2 = sys.argv[2]
	
	run(mtz1,mtz2)

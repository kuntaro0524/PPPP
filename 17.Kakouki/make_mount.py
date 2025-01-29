import sys,os,math,numpy

origin=numpy.array([0,0,0])

material_thick=1.0
ana_size=3.0

def make_direction_vec(ana_size,depth):
	vecs=[]
	z_code=-(material_thick-depth)
	for evec in ([1,1],[1,-1],[-1,1],[-1,-1]):
		tvec=numpy.array([origin[0],origin[1]])+numpy.array(evec)*ana_size/2.0
		tvec2=numpy.array([tvec[0],tvec[1],z_code])
		vecs.append(tvec2)
	return vecs

inner_ana=make_direction_vec(ana_size,0.1)
middle_ana=make_direction_vec(5.5,0.2)
outer_ana=make_direction_vec(7.0,0.4)
outer_hori=make_direction_vec(7.5,0.1)

print outer_ana
new_origin=numpy.array([3.0,-50.0,outer_ana[3][2]])

shift_value=new_origin-outer_ana[3]
print shift_value

for ana in (inner_ana,middle_ana,outer_ana,outer_hori):
	for each in ana:
		newvec=each+shift_value
		print "%8.5f %8.5f %8.5f"%(newvec[0],newvec[1],newvec[2])


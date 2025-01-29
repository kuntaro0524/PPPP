run /oys/xtal/yamtbx/pymol_plugins/loadmtz.py
bg_color white
set ignore_case_chain
set mesh_width, 1
set ray_trace_fog, 0
set depth_cue, 0
set ray_shadows, 0

load /isilon/users/ktaroyam/ktaroyam/data/tomasan_lipid/from_tomasan/xscale_KAMO_cluster55_refmac9.pdb, org
load xscale_KAMO_cluster55_refmac9_omitside_refine_001.pdb, refined
as sticks
util.color_chains("elem C")

#loadmtz xscale_KAMO_cluster55_refmac9_omitside_refine_001.mtz, all, labels="FOFCWT,PHFOFCWT", isolevel=2.5
print run_loadmtz("xscale_KAMO_cluster55_refmac9_omitside_refine_001.mtz", "all", labels="FOFCWT,PHFOFCWT", isolevel=2.5)

python
while 1:
 if any(map(lambda x: "msh_" in x, cmd.get_names())):
  print "msh OK!"
  break
 print "waiting.."
 time.sleep(1)

python end

#color grey50, msh*
color green, msh*
hide everything, (org or refined) and not resn FCS

python
for c in "efgh":
 print cmd.align("org and chain %s"%c, "refined and chain %s"%c)
 print cmd.zoom("chain %s and resn FCS"%c)
 print cmd.orient("chain %s and resn FCS"%c)
 print cmd.clip("slab", 5)
 print cmd.png("FCS_2.5s_%s.png"%c, ray=1)

python end

print cmd.get_names()
quit


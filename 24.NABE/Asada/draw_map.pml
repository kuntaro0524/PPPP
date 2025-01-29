run /isilon/BL32XU/BLsoft/PPPP/24.NABE/loadmtz.py
bg_color white
set ignore_case_chain
set mesh_width, 0.5
set ray_trace_fog, 1
set depth_cue, 1
set fog_start, 0.65
set ray_shadows, 0
set ray_opaque_background, 1

load /isilon/BL32XU/BLsoft/PPPP/24.NABE/Asada/ligand.pdb, refined

#as stick
#as ribbon
#util.color_chains("elem C")
#set ribbon_color, red
util.chainbow("refined")

print run_loadmtz("/isilon/users/khirata/khirata/180921-Asada-Helix/_kamoproc_180627/merge_180628-AT2_zennbunose/blend_3.2A_framecc_b+B_1deg/cluster_3701/run_01/3.6A_500.0/ccp4/ref_fofc_001.mtz", "all", labels="FOFCWT,PHFOFCWT", isolevel=2.0)

python
while 1:
 if any(map(lambda x: "msh_" in x, cmd.get_names())):
  print "msh OK!"
  break
 print "waiting.."
 time.sleep(1)

python end

#color grey50, msh*
#color density, msh*
color green, msh*
hide everything, (org or refined)
#hide everything, (org or refined) and not resn CYS resi 512
#hide everything, (org or refined) and not resi 512
#show spheres, i. 512 i. 551 i. 592 i. 694
show stick, (org or refined)

python
for c in "A":
 #print cmd.align("refined and chain %s"%c)
 print cmd.set_view((\
    -0.297890395,    0.192615643,    0.934971035,\
     0.684920311,    0.725358844,    0.068785094,\
    -0.664939344,    0.660872340,   -0.348007053,\
    -0.000126556,   -0.000207768,  -95.317367554,\
    16.035675049,   39.944671631,    9.819516182,\
  -120.580986023,  311.214935303,  -20.000001907 ))
 print cmd.clip("slab", 60)
 print cmd.png("test.5s_%s.png"%c, ray=1)

python end

print cmd.get_names()
quit


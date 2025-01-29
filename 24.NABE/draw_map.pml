run /isilon/BL32XU/BLsoft/PPPP/24.NABE/loadmtz.py
bg_color white
set ignore_case_chain
set mesh_width, 0.5
set ray_trace_fog, 1
set depth_cue, 1
set fog_start, 0.65
set ray_shadows, 0
set ray_opaque_background, 1

load refine_001.pdb, refined
#as sticks
#as ribbon
#util.color_chains("elem C")
#set ribbon_color, red
util.chainbow("refined")

print run_loadmtz("refine_001.mtz", "all", labels="FOFCWT,PHFOFCWT", isolevel=3.0)

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
show ribbon, (org or refined)
show spheres, i. 512 i. 551 i. 592 i. 694

python
for c in "A":
 #print cmd.align("refined and chain %s"%c)
 print cmd.set_view((\
    -0.582486510,    0.489666939,   -0.648793697,\
    -0.612437904,   -0.789191008,   -0.045780167,\
    -0.534440637,    0.370677620,    0.759583592,\
    -0.000086047,    0.000138894, -125.319145203,\
   -32.740390778,   27.203845978,  -44.752834320,\
    44.238391876,  206.411544800,  -20.000000000 ))
 #print cmd.zoom("chain %s and resn CYS and resi 512"%c,10)
 #print cmd.orient("chain %s and resn LEU and resi 778"%c)
 print cmd.clip("slab", 60)
 print cmd.png("test.5s_%s.png"%c, ray=1)

python end

print cmd.get_names()
quit


import tempfile, subprocess, struct, os, numpy

class Error(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
# class Error

class MtzFile:

    def __init__(self, mtzfile):
        self.mtzheader = ""
        self.get_header(mtzfile)
    # __init__()

    def get_header(self, mtzin):
        def doSwap(m):
            s, n = 0, 4
            f = (m[0]>>4)& 0x0f
            if sys.byteorder != 'little': n = 1
            if f != 0 and f != n: s = 1
            return s == 1
        # doSwap()

        int_size = struct.calcsize("i")

        if not os.path.isfile(mtzin):
            raise Error("The file does not exist.")

        try:
            mtz = open(mtzin, 'rb')

            first4 = mtz.read(4)
            if first4 != b"MTZ ":
                raise Error("This file is not MTZ format: "+mtzin)

            mtz.seek(8, 0)
            to_swap = doSwap(struct.unpack('4B', mtz.read(4)))

            mtz.seek(4, 0)

            if to_swap:
                byteorder = "<>"[int(sys.byteorder == 'little')]
                hdrst, = struct.unpack(byteorder+'i', mtz.read(int_size))
            else:
                hdrst, = struct.unpack('i', mtz.read(int_size))

            mtz.seek(4*(hdrst-1), 0)
            header = mtz.read()

        finally:
            mtz.close()

        self.mtzheader = []

        while header:
            self.mtzheader.append(header[:80])
            header = header[80:]

    # get_header()

    def get_column(self):

        column = {}

        if not self.mtzheader: return None

        for line in self.mtzheader:
            item = line.split()
            if item[0] == "COLUMN":
                column.setdefault(item[2],[]).append(item[1])

        return column

    # get_column()

    def get_cell(self):
        for line in self.mtzheader:
            if line.startswith(b"CELL"):
                a, b, c, alpha, beta, gamma = map(lambda x: float(x), line.split()[1:])
                return a,b,c,alpha,beta,gamma
    # get_cell()

    def M_c2f(self):
        a, b, c, alpha, beta, gamma = self.get_cell()
        cos, sin = numpy.cos, numpy.sin
        alpha, beta, gamma = numpy.radians((alpha, beta, gamma))
        v = numpy.sqrt(1 -cos(alpha)**2 - cos(beta)**2 - cos(gamma)**2 + 2*cos(alpha)*cos(beta)*cos(gamma))
        return numpy.matrix( [
                [ 1.0 / a, -cos(gamma)/(a*sin(gamma)), (cos(alpha)*cos(gamma)-cos(beta)) / (a*v*sin(gamma))  ],
                [ 0.0,     1.0 / (b*sin(gamma)),         (cos(beta) *cos(gamma)-cos(alpha))/ (b*v*sin(gamma))  ],
                [ 0.0,     0.0,                        sin(gamma) / (c*v)                                    ] ]
                             )

# class mtzutil

def make_map(mtzin, limits, mapout, F1, PHI, FOM, grid_sample):
    progpath = lambda s:os.path.join(os.environ["CBIN"], s)
    # Run fft
    #CMD = '"%s" hklin "%s" mapout "%s"' % (progpath("fft"), mtzin, mapout)
    #CMD = ('"%s"'%progpath("fft"), 'hklin', '"%s"'%mtzin, 'mapout', '"%s"'%mapout)
    CMD = '%s hklin %s mapout %s' % (progpath("fft"), mtzin, mapout)
    print(CMD)
    p = subprocess.Popen(CMD, shell=True, cwd=os.getcwd(), stdin=subprocess.PIPE)
    #p = subprocess.Popen(CMD, cwd=os.getcwd(), stdin=subprocess.PIPE)
    if FOM is None:
        p.stdin.write(("labin F1=%s PHI=%s\n"%(F1, PHI)).encode())
    else:
        p.stdin.write("labin F1=%s PHI=%s W=%s\n"%(F1, PHI, FOM))

    p.stdin.write(b"xyzlim asu\n")
    p.stdin.write(b"grid sample %d\n" % grid_sample)
    p.stdin.write(b"end\n")
    p.stdin.close()

    if p.returncode is None:
        p.wait()

    # Run mapmask to scale by sigma
    CMD = '"%s" mapin "%s" mapout "%s"' % (progpath("mapmask"), mapout, mapout)
    print(CMD)
    p = subprocess.Popen(CMD, shell=True, cwd=os.getcwd(), stdin=subprocess.PIPE)
    p.stdin.write(b"scale sigma\n")
    p.stdin.write(b"end\n")
    p.stdin.close()
 
    if p.returncode is None:
        p.wait()

    # Run mapmask to crop region
    CMD = '"%s" mapin "%s" mapout "%s"' % (progpath("mapmask"), mapout, mapout)
    print(CMD)
    p = subprocess.Popen(CMD, shell=True, cwd=os.getcwd(), stdin=subprocess.PIPE)
    #p = subprocess.Popen(CMD, cwd=os.getcwd(), stdin=subprocess.PIPE)
    p.stdin.write(b"xyzlim %.3f %.3f %.3f %.3f %.3f %.3f\n" % (limits[0]+limits[1]+limits[2]))
    p.stdin.write(b"end\n")
    p.stdin.close()
 
    if p.returncode is None:
        p.wait()

# make_map()

def get_autoload_column(mtzin):
    mtz = MtzFile(mtzin)
    col = mtz.get_column()

    amp_2fofc = None
    amp_fofc = None
    phase_2fofc = None
    phase_fofc = None

    if not "F" in col and not "P" in col:
        return None

    if "2FOFCWT" in col["F"]:
        amp_2fofc = "2FOFCWT"
    elif "FWT" in col["F"]:
        amp_2fofc = "FWT"

    if "FOFCWT" in col["F"]:
        amp_fofc = "FOFCWT"
    elif "DELFWT" in col["F"]:
        amp_fofc = "DELFWT"


    if "PH2FOFCWT" in col["P"]:
        phase_2fofc = "PH2FOFCWT"
    elif "PHWT" in col["P"]:
        phase_2fofc = "PHWT"

    if "PHFOFCWT" in col["P"]:
        phase_fofc = "PHFOFCWT"
    elif "PHDELWT" in col["P"]:
        phase_fofc = "PHDELWT"

    print("%s %s %s %s"%(amp_2fofc, amp_fofc, phase_2fofc,phase_fofc))

    if amp_2fofc and amp_fofc and phase_2fofc and phase_fofc:
        return {"2fofc":(amp_2fofc, phase_2fofc),
                "fofc":(amp_fofc, phase_fofc)
                }
    else:
        return None
            
# get_autoload_column()

def run_loadmtz(mtzin, sel, labels=None, expand=5, grid_sample=3, carve=2, keep_file="False", isolevel=3.0):
    """
DESCRIPTION
   Load map file from mtzfile 
    
USAGE
   loadmtz mtzin, selection, [labels, [expand=5, [grid_sample=3, [carve=2, [keep_file=False]]]]]
   
ARGUMENTS
   mtzin = MTZ filename
   selection = atoms where electron density will be drawn
   labels = mtz labels. specify such like: FP, PHIM
            if unspecified, behaves like AutoOpenMTZ of Coot
            (it recognizes FWT,DELFWT, 2FOFCTWT,FOFCWT)
   expand = offset to limit
REQUIREMENTS
   CCP4 suite.
   This script uses fft and mapmask

AUTHORS
   Keitaro Yamashita, 2010
   """
    autoload = ( labels is None )
    name = os.path.splitext(os.path.basename(mtzin))[0]

    grid_sample = int(grid_sample)

    assert keep_file.lower() in ("1", "0", "true", "false")
    keep_file = keep_file.lower() in ("1", "true")

    # Find xyz limits
    stored.xyz = []
    mtz = MtzFile(mtzin)
    R = mtz.M_c2f() # limits must be fractional coordinates
    cmd.iterate_state(1, sel, "stored.xyz.append((x,y,z))")
    stored.xyz = [numpy.array(numpy.array(x)*R.transpose())[0] for x in stored.xyz]
    cell = mtz.get_cell()
    ex_x, ex_y, ex_z = expand/cell[0], expand/cell[1], expand/cell[2]
    xlim = min(stored.xyz, key=lambda x:x[0])[0]-ex_x, max(stored.xyz, key=lambda x:x[0])[0]+ex_x
    ylim = min(stored.xyz, key=lambda x:x[1])[1]-ex_y, max(stored.xyz, key=lambda x:x[1])[1]+ex_y
    zlim = min(stored.xyz, key=lambda x:x[2])[2]-ex_z, max(stored.xyz, key=lambda x:x[2])[2]+ex_z
    print("%s %s %s"%(xlim, ylim, zlim))
    #minc, maxc = numpy.array((xlim[0], ylim[0], zlim[0])), numpy.array((xlim[1], ylim[1], zlim[1]))
    #minc, maxc = (minc * R).tolist()[0], (maxc * R).tolist()[0]
    #print minc, maxc
    #xlim = minc[0], maxc[0]
    #ylim = minc[1], maxc[1]
    #zlim = minc[2], maxc[2]

    cmd.unset("normalize_ccp4_maps") # To keep sigma-scaled map..

    if autoload:
        cols = get_autoload_column(mtzin) 
        if not cols:
            print("Columns for auto-open not found.")
            return
        
        map_2fofc = name + "_2fofc"
        map_fofc = name + "_fofc"
        

        make_map(mtzin=mtzin, limits=(xlim,ylim,zlim), mapout=map_2fofc+".ccp4", 
                 F1=cols["2fofc"][0], PHI=cols["2fofc"][1], FOM=None, grid_sample=grid_sample)
        make_map(mtzin=mtzin, limits=(xlim,ylim,zlim), mapout=map_fofc+".ccp4", 
                 F1=cols["fofc"][0], PHI=cols["fofc"][1], FOM=None, grid_sample=grid_sample)

        cmd.load(map_2fofc+".ccp4", map_2fofc, quiet=1)
        cmd.load(map_fofc+".ccp4", map_fofc, quiet=1)

        cmd.isomesh(name="msh_"+map_2fofc, map=map_2fofc, level=1, selection=sel, carve=carve)
#        cmd.color("blue", "msh_"+map_2fofc)
        cmd.isomesh(name="msh_p_"+map_fofc, map=map_fofc, level=isolevel, selection=sel)
        cmd.color("green", "msh_p_"+map_fofc)
        cmd.isomesh(name="msh_n_"+map_fofc, map=map_fofc, level=-isolevel, selection=sel)
        cmd.color("red", "msh_n_"+map_fofc)

        if not keep_file:
            os.remove(map_2fofc+".ccp4")
            os.remove(map_fofc+".ccp4")
        
    else:
        labels = labels.replace('"', '')

        lab_F1 = labels.split(",")[0]
        lab_PHI = labels.split(",")[1]
        
        mapout = name + ".ccp4"
        make_map(mtzin=mtzin, limits=(xlim,ylim,zlim), mapout=mapout, 
                 F1=lab_F1, PHI=lab_PHI, FOM=None, grid_sample=grid_sample)

        # Load into PyMOL
        cmd.load(mapout, quiet=1)
        cmd.isomesh(name="msh_"+name, map=name, level=3, selection=sel)

        if not keep_file:
            os.remove(mapout)

# run_loadmtz()

cmd.extend("loadmtz", run_loadmtz)

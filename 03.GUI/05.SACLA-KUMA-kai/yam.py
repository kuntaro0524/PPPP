import sys,os,math,numpy

def read_camera_inf(infin):
    ret = {}
    origin_shift_x, origin_shift_y = None, None
    for l in open(infin):
        if "ZoomOptions1:" in l:
            ret["zoom_opts"] = map(float, l[l.index(":")+1:].split())
        elif "OriginShiftXOptions1:" in l:
            origin_shift_x = map(float, l[l.index(":")+1:].split())
        elif "OriginShiftYOptions1:" in l:
            origin_shift_y = map(float, l[l.index(":")+1:].split())

    # TODO read tvextender

    if None not in (origin_shift_x, origin_shift_y):
        assert len(origin_shift_x) == len(origin_shift_y)
        ret["origin_shift"] = zip(origin_shift_x, origin_shift_y)

    return ret
# read_camera_inf()

def read_bss_config(cfgin):
    ret = {}
    for l in open(cfgin):
        if "#" in l: l = l[:l.index("#")]
        if "Microscope_Zoom_Options:" in l:
            ret["zoom_pulses"] = map(int, l[l.index(":")+1:].split())
    return ret


class crycen:
    def __init__ (self, parent, ms, port=1921):
        self.parent = parent
        self.enable_xmlrpc = True
        self.xmlrpc_server = None
        self.thread = None
        self.ms = ms
        self.gonio = Gonio(ms)
        self.capture = Capture()

        # start XML-RPC server
        try:
            self.xmlrpc_server = xmlrpc_server(("", port), self)
            self.xmlrpc_server.socket.settimeout(0.01)
        except Exception, e:
            print "Error starting XML-RPC server:"
            print str(e)
        else:
            self.thread = threading.Thread(None, self.run)
            self.thread.start()
            print "xml-rpc server running on port %d" % port

        self.camera_inf = read_camera_inf(os.path.join(os.environ["BLCONFIG"], "video", "camera.inf"))
        self.bss_config = read_bss_config(os.path.join(os.environ["BLCONFIG"], "bss", "bss.config"))
        self.coax_pulse2zoom = dict(zip(self.bss_config["zoom_pulses"], self.camera_inf["zoom_opts"]))
        self.coax_zoom2pulse = dict(zip(self.camera_inf["zoom_opts"], self.bss_config["zoom_pulses"]))
        self.coax_zoom2oshift = dict(zip(self.camera_inf["zoom_opts"], self.camera_inf["origin_shift"]))
        self.coax_zpulse2pint = {0:19985, -16000:19980, -32000:19974, -48000:20024} # zoom pulse to pint pulse

        self.running = None # Shinoda centering program pexpect object
        self.runningf = None # Shinoda facing program pexpect object
        self.start_shinoda_centering_core()
        self.start_shinoda_facing_core()
    # __init__()

    def run(self, *args) :
        while self.xmlrpc_server is not None:
            self.xmlrpc_server.handle_request()
            time.sleep(.2)
    # run()

    def stop(self):
        self.xmlrpc_server = None
        if self.thread is not None:
            self.thread.join()
        self.capture.disconnect()
    # stop()

    def get_axes_info(self):
        phi = "%8.2f" % self.gonio.getPhi()
        gx = "%8.4f" % self.gonio.getXmm()
        gy = "%8.4f" % self.gonio.getYmm()
        gz = "%8.4f" % self.gonio.getZmm()
        #gzz = "%8.4f" % self.gonio.getZZmm()

        return phi, gx, gy, gz
    # get_axes_info()

    def move_gonio_abs(self, phi, gx, gy, gz):
        self.gonio.moveXYZmm(gx, gy, gz)
        self.set_gonio_phi(phi)
    # move_gonio_abs()

    def get_pixel_size(self): # returns in microns
        # X[mm] = X[px] / (C * Zoom * TvExtender)
        # C = 102.4375
        # TvExtender = 1
        #
        #     MM2P = _MM2P * ci[GetVideoChannel()].zoom * ci[GetVideoChannel()].tvext / (GetBinning()+1);
        # #define _MM2P 102.4375
        #     double X = ((double)px - WIDTH/2.0) / MM2P;
        # GetBinning()+1 == 4 when 4x4 bin (2 for 2x2 bin, 1 for 1x1 bin)
        """
        zoom, tvext: see $BLCONFIG/video/camera.inf
        (for st2_coax_1_zoom pulse value, see $CLBONFIG/bss/bss.config Microscope_Zoom_Options:
        """

        """
        XXX Not-thread safe!... but how this happened?

debug:: video_vdclickemu/put/3812_video_server/ok/0
Traceback (most recent call last):
  File "shinoda_centering_server.py", line 500, in BtnRun_onclick
    self.intr.do_centering()
  File "shinoda_centering_server.py", line 398, in do_centering
    oneaction(20*rotate_sign, i==0)
  File "shinoda_centering_server.py", line 385, in oneaction
    log_write("%.2d_shift= %.2f%% %.2f%% (%.2f %.2f um)"%((self.count, self.last_shift[0]*100., self.last_shift[1]*100.)+self.calc_shift_by_img_px(sx,sy, unit="um")))
  File "shinoda_centering_server.py", line 256, in calc_shift_by_img_px
    um_per_px = self.get_pixel_size()
  File "shinoda_centering_server.py", line 148, in get_pixel_size
    bin =  self.capture.getBinning()
  File "/isilon/BL32XU/BLsoft/Other/Yam/yamtbx/bl32xu/centering_support/hiratalib/Capture.py", line 178, in getBinning
    return int(sp[-2])
ValueError: invalid literal for int() with base 10: 'ok'
video_binning/get/3812_video_server/4/0

        """
        bin =  self.capture.getBinning()
        print "Binning=", bin

        zoom = self.get_zoom()
        print "Zoom=", zoom

        return 1.e3/(102.4375*zoom/bin)
    # get_pixel_size()

    def get_coax_center(self):
        zoom = self.get_zoom()
        print "Zoom=", zoom
        origin_shift = self.coax_zoom2oshift[zoom]
        return origin_shift
    # get_coax_center()

    def get_zoom(self):
        self.ms.sendall("get/bl_32in_st2_coax_1_zoom/query")
        recbuf = self.ms.recv(8000)
        print "debug::", recbuf

        sp = recbuf.split("/")
        if len(sp) == 5:
            ret = sp[-2]
            r = re.search("(.*)_([0-9-]+)pulse", ret)
            if r:
                assert r.group(1) == "inactive"
                return self.coax_pulse2zoom[int(r.group(2))]
    # get_zoom()

    def set_zoom(self, zoom):
        if zoom not in self.coax_zoom2pulse:
            print "Possible zoom:", self.coax_zoom2pulse.keys()
            return

        zoomaxis = Zoom(self.ms)
        zoom_pulse = self.coax_zoom2pulse[zoom]
        zoomaxis.move(zoom_pulse)
        
        if zoom_pulse not in self.coax_zpulse2pint:
            print "Error. Unknown zoom pulse for pint adjustment:", zoom_pulse
            return

        pintaxis = CoaxPint(self.ms)
        pint_pulse = self.coax_zpulse2pint[zoom_pulse]
        pintaxis.move(pint_pulse)
    # set_zoom()

    def set_axes(self):
        print "set axes"
        
        # left (-), right (+)
        self.gonio.moveTrans(dist)

        # down (-), up (+)
        self.gonio.moveUpDown(dist)

        # phi
        self.gonio.rotatePhiRelative(rot_ang)
        
        # pint
        self.gonio.movePint(dist)
    # set_axes()

    def rotate(self, deltaphi):
        self.gonio.rotatePhiRelative(deltaphi)
    # rotate()

    def set_gonio_phi(self, phi):
        self.gonio.rotatePhi(phi)
    # set_gonio_phi()

    def move(self, deltax, deltay):
        # left (-), right (+)
        self.gonio.moveTrans(deltax)

        # down (-), up (+)
        self.gonio.moveUpDown(deltay)
    # move()

    # vserv control
    def set_binning(self, bin):
        if bin==1: setbin = 0
        elif bin==2: setbin = 1
        elif bin==4: setbin = 3
        else:
            print "Invalid binning size"
            return None

        self.capture.setBinning(setbin)
    # set_binning()
    
    def get_coax_image(self, imgout, convert=False):
        self.capture.capture(imgout, speed=50) # 50 seems good..

        if convert:
            print "Converting.."
            subprocess.call(["convert", imgout, "-compress", "none", imgout])
    # get_coax_image()

    def calc_shift_by_img_px(self, sx, sy, units=("um",)):
        """
        sx,sy: x,y on shinoda's coordinate system. origin is right top.
        """
        if sx < 0 or sy < 0:
            print "Invalid sx or sy:", sx, sy

        um_per_px = self.get_pixel_size()
        origin_shift = self.get_coax_center()
        origin_shift = map(lambda x: x/um_per_px*1.e3, origin_shift)
        w, h = 640, 480
        cen_x, cen_y = w/2+origin_shift[0], h/2-origin_shift[1]
        print "Center: ", cen_x, cen_y

        #dx, dy = (deltax-cen_x)*um_per_px, (deltay-cen_y)*um_per_px
        dx, dy = (sx-w+cen_x), (sy-cen_y)

        ret = []
        for unit in units:
            if sx < 0 or sy < 0:
                ret.append((unit, (0,0)))
            elif unit == "um":
                ret.append((unit, (dx*um_per_px, dy*um_per_px)))
            elif unit == "px":
                ret.append((unit, (dx, dy)))
            elif unit == "rel":
                ret.append((unit, (dx/float(w), dy/float(h))))
            else:
                raise Exception("Unknown unit: %s"%unit)

        if len(ret) == 1:
            return ret[0][1]
        else:
            return dict(ret)
    # calc_shift_by_img_px()

    def move_by_img_px(self, sx, sy):
        """
        sx,sy: x,y on shinoda's coordinate system. origin is right top.
        """
        if sx < 0 or sy < 0:
            print "Invalid sx or sy:", sx, sy
            return
        dx, dy = self.calc_shift_by_img_px(sx, sy)
        print "move=", dx, dy
        self.move(dx, dy)
    # move_by_img_px()

    def let_bss_move(self, sx, sy):
        if sx < 0 or sy < 0:
            print "Invalid sx or sy:", sx, sy
            return
        
        w, h = 640, 480
        sx = w-sx
        assert 0 <= sx <= w
        assert 0 <= sy <= h
        self.capture.s.sendall("put/video_vdclickemu/%d_%d"%(sx,sy))
        print "let_bss_move::", self.capture.s.recv(8000)

        time.sleep(0.5)
        while True:
            if self.gonio.goniox.isMoved() and self.gonio.gonioy.isMoved() and self.gonio.gonioz.isMoved():
                return
            print "Waiting to stop.."
            time.sleep(0.1)
    # let_bss_move()

    def start_shinoda_centering_core(self):
        if self.running is None or not self.running.isalive():
            edir = "/isilon/BL32XU/BLsoft/Other/shinoda/loop_centering_current"
            self.running = pexpect.spawn('ssh oys09 "cd %s; ./out_simple_centering"'%edir)
    # start_shinoda_centering_core()
    
    def start_shinoda_facing_core(self):
        if self.runningf is None or not self.runningf.isalive():
            edir = "/isilon/BL32XU/BLsoft/Other/shinoda/loop_centering_current"
            self.runningf = pexpect.spawn('ssh oys09 "cd %s; ./out_simple_faceing"'%edir)
    # start_shinoda_facing_core()

    def copy_files(self, src_dest):
        for fs, fd in src_dest:
            shutil.copyfile(fs, fd)
    # copy_files

    def move_files(self, src_dest):
        for fs, fd in src_dest:
            shutil.move(fs, fd)
    # move_files

    def do_centering(self):
        log_root = "/isilon/BL32XU/BLsoft/Other/shinoda/loop_centering_current/logs"
        edir = "/isilon/BL32XU/BLsoft/Other/shinoda/loop_centering_current"

        log_dir = os.path.join(log_root, time.strftime("%y%m%d_%H%M%S"))
        os.mkdir(log_dir)
        inocclog.config(log_dir, stream=self.parent.logstream)
        inocclog.info("Started")
        inocclog.info("gonio_phixyz= %s %s %s %s" % self.get_axes_info())
        start_time = time.time()
        self.start_shinoda_centering_core()

        rotate_sign = -1 if self.gonio.getPhi() > 0 else 1

        self.count = 0
        self.ttt = None
        self.tmv = None
        self.last_shift = (0,0)
        def oneaction(phistep, isfirst=False):
            self.count += 1
            bk_files = []

            inocclog.info("current_phi= %.2f"%self.gonio.getPhi())
            inocclog.info("phi_step= %.2f"%phistep)

            if self.tmv is not None: self.tmv.join()

            inocclog.info("Capturing image 1")
            self.get_coax_image(os.path.join(edir, "tmp_img/img1.ppm"))
            bk_files.append((os.path.join(edir, "tmp_img/img1.ppm"), os.path.join(log_dir, "%.2d_img1.ppm"%self.count)))
            if not os.path.isfile(bk_files[-1][0]):
                inocclog.error("Capturing img1 failed.")
                return None # Should we retry?
                
            inocclog.info("Rotate phi")
            self.rotate(phistep)
            inocclog.info("Capturing image 2")
            self.get_coax_image(os.path.join(edir, "tmp_img/img2.ppm"))
            bk_files.append((os.path.join(edir, "tmp_img/img2.ppm"), os.path.join(log_dir, "%.2d_img2.ppm"%self.count)))
            if not os.path.isfile(bk_files[-1][0]):
                inocclog.error("Capturing img2 failed.")
                return None # Should we retry?

            if isfirst: # wait until core program started
                inocclog.info("waiting INOCC.. %s"%self.running.before)
                if self.running.expect(["input file name:", pexpect.EOF]) == 1:
                    inocclog.error("Core down?")
                    return

            t1 = time.time()
            self.running.sendline("./tmp_img/img1.ppm ./tmp_img/img2.ppm")
            inocclog.info("Start calculation")
            if self.running.expect(["input file name:", pexpect.EOF]) == 1:
                inocclog.error("Core down?")
                return
            t2 = time.time()

            for rf in glob.glob(os.path.join(edir, "result", "*")):
                inocclog.debug("Found result file: %s"%os.path.basename(rf))
                bk_files.append((rf, os.path.join(log_dir, "%.2d_%s"%(self.count, os.path.basename(rf)))))

            self.tmv = threading.Thread(target=self.move_files, args=(bk_files,))
            self.tmv.start()

            print "Before==>", self.running.before, "<==="
            lines = self.running.before.splitlines()
            if len(lines) == 2:
                sx, sy, decision = self.running.before.splitlines()[1].split()
                sx, sy = map(int, (sx, sy))
                #self.move_by_img_px(sx,sy)
                #self.let_bss_move(sx,sy)
                shift = self.calc_shift_by_img_px(sx,sy, units=("um", "rel"))
                self.last_shift = shift["rel"]
                self.ttt = threading.Thread(target=self.let_bss_move, args=(sx,sy)) # for async gonio rotation
                #self.ttt = threading.Thread(target=self.move_by_img_px, args=(sx,sy)) # for async gonio rotation
                self.ttt.start()
                inocclog.info("%.2d_result= %s (%.2f s)"%(self.count, self.running.before.splitlines()[1].strip(), t2-t1))
                inocclog.info("%.2d_shift= %.2f%% %.2f%% (%.2f %.2f um)"%((self.count, self.last_shift[0]*100., self.last_shift[1]*100.)+shift["um"]))
                return decision
            else:
                inocclog.error("%.2d_result= no return values (%.2f s)"%(self.count, t2-t1))
                return None
        # oneaction()

        maxtry = 3
        inocclog.info("Max Tries= %d"%maxtry)
        for i in xrange(maxtry):
            inocclog.info("Try %d"%(i+1))
            oneaction(10*rotate_sign, i==0)
            if i == 0:
                self.rotate(10*rotate_sign)
            elif i == 1:
                self.rotate(20*rotate_sign)
            elif i == 2:
                self.rotate(30*rotate_sign)
                
            if self.ttt is not None: self.ttt.join()
            if oneaction(10*rotate_sign) == "complete":
                inocclog.info("Complete with %d tries." % (i+1))
                if abs(self.last_shift[0]) > 0.1:
                    continue
            
                inocclog.info("Dameoshi.")
                self.rotate(60*rotate_sign)
                if self.ttt is not None: self.ttt.join()
                oneaction(10*rotate_sign)
                if self.ttt is not None: self.ttt.join()
                break

        inocclog.info("Finish (%.2f sec)" % (time.time()-start_time))
        print >>self.parent.logstream, "\n" 
        self.running.sendline("quit")
        print "See", log_dir

        self.start_shinoda_centering_core() # for next run
    # do_centering()

    def do_facing(self):
        log_root = "/isilon/BL32XU/BLsoft/Other/shinoda/loop_centering_current/logs"
        edir = "/isilon/BL32XU/BLsoft/Other/shinoda/loop_centering_current"

        log_dir = os.path.join(log_root, time.strftime("facing_%y%m%d_%H%M%S"))
        os.mkdir(log_dir)
        inocclog.config(log_dir, stream=self.parent.logstream)
        inocclog.info("Facing started")
        inocclog.info("gonio_phixyz= %s %s %s %s" % self.get_axes_info())
        start_time = time.time()
        self.start_shinoda_facing_core()

        rotate_sign = -1 if self.gonio.getPhi() > 0 else 1

        def oneaction(phistep, num):
            bk_files = []

            inocclog.info("current_phi= %.2f"%self.gonio.getPhi())
            inocclog.info("phi_step= %.2f"%phistep)
            inocclog.info("num= %d"%num)

            if self.runningf.expect(["input total file:", pexpect.EOF]) == 1:
                inocclog.error("Core down?")
                return

            self.runningf.sendline("%d"%num)

            for i in xrange(num):
                inocclog.info("Capturing image %.3d"%i)
                self.get_coax_image(os.path.join(edir, "tmp_img/img%.3d.ppm"%i))
                bk_files.append((os.path.join(edir, "tmp_img/img%.3d.ppm"%i), os.path.join(log_dir, "img%.3d.ppm"%i)))
                s = "%.2f ./tmp_img/img%.3d.ppm" % (self.gonio.getPhi(), i)
                self.runningf.sendline(s)
                inocclog.info("Captured: %s"%s)
                if i < num-1:
                    self.rotate(phistep)

            t1 = time.time()
            if self.runningf.expect(["input total file:", pexpect.EOF]) == 1:
                inocclog.error("Core down?")
                return
            t2 = time.time()

            threading.Thread(target=self.move_files, args=(bk_files,)).start()

            print "Before==>", self.runningf.before, "<==="
            lines = self.runningf.before.splitlines()
            if len(lines) == num+2:
                target_deg = float(self.runningf.before.splitlines()[-1].strip())
                inocclog.info("target_deg= %.2f (%.2f s)"%(target_deg, t2-t1))
                return target_deg
            else:
                inocclog.error("taget_deg= ?? (%.2f s)"%(t2-t1))
                return None
        # oneaction()

        target_deg = oneaction(30*rotate_sign, 6)
        self.set_gonio_phi(target_deg-45)
        self.runningf.sendline("quit")
        self.start_shinoda_facing_core()

        target_deg = oneaction(10*rotate_sign, 9)
        self.set_gonio_phi(target_deg)

        inocclog.info("Finish (%.2f sec)" % (time.time()-start_time))
        print >>self.parent.logstream, "\n" 
        self.runningf.sendline("quit")
        print "See", log_dir

        self.start_shinoda_facing_core() # for next run
    # do_facing()

    def take_picstures_debug(self, step, continuous=False):
        outd = os.path.abspath("pics_step_%.3d" % step)
        os.mkdir(outd)
        if not continuous:
            for deg in xrange(0, 360, step):
                self.rotate(step)
                self.get_coax_image(os.path.join(outd, "pic_%.3d.ppm"%deg))
        elif 0: # This is dangerous. change method!
            self.set_gonio_phi(0)
            t1 = threading.Thread(targe=self.rotate, args=(360,))
            t1.start()
            for d in xrange(0, 360, step):
                deg = self.gonio.getPhi()
                self.get_coax_image(os.path.join(outd, "cpic_%.3d.ppm"%deg))
                time.sleep(.5)
            t1.join()

if __name__ == "__main__":
	# camera information
        camera_inf = read_camera_inf(os.path.join(os.environ["BLCONFIG"], "video", "camera.inf"))
	# BSS configuration
        bss_config = read_bss_config(os.path.join(os.environ["BLCONFIG"], "bss", "bss.config"))
	# Pulse2zoom ratio
        coax_pulse2zoom = dict(zip(bss_config["zoom_pulses"], camera_inf["zoom_opts"]))
        coax_zoom2pulse = dict(zip(camera_inf["zoom_opts"], bss_config["zoom_pulses"]))
        coax_zoom2oshift = dict(zip(camera_inf["zoom_opts"], camera_inf["origin_shift"]))
        coax_zpulse2pint = {0:19985, -16000:19980, -32000:19974, -48000:20024} # zoom pulse to pint pulse



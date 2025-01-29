#!/usr/bin/env yamtbx.python

"""
* SHIKA (Spotfinder GUI) *

For KAKI cluster, this can be launched by (for 32XU):

ssh -X -t -R 1920:192.168.163.5:1920 oys09.spring8.or.jp "cd \"$PWD\"; yamtbx.python /oys/xtal/yamtbx/yamtbx/dataproc/command_line/spot_finder_gui.py \"$@\" kuma_addr=127.0.0.1:1920 force_ssh_from=10.10.55.50 adxv=/oys/xtal/adxv/1.9.7/adxv-1.9.7.i686FC11"

"""

import sys
import os
import math
import matplotlib
matplotlib.interactive( True )
matplotlib.use( 'WXAgg' )
import matplotlib.figure
import matplotlib.backends.backend_agg
import matplotlib.backends.backend_wxagg
from matplotlib.ticker import FuncFormatter
import wx
import wx.lib.newevent
import wx.lib.agw.pybusyinfo
import wx.html
import datetime
import time
import glob
import cPickle as pickle
import collections
import threading
import subprocess
import socket
import xmlrpclib
import re
import copy

import numpy
import scipy.spatial

import iotbx
import rstbx.viewer
import spotfinder.core_toolbox
import libtbx.phil
from cctbx.array_family import flex

import spot_finder_for_grid_scan
from yamtbx.dataproc import bl_logfiles
from yamtbx.dataproc.dataset import re_pref_num_ext
from yamtbx.dataproc import spotfinder_info
from yamtbx.util import get_number_of_processors, rotate_file
from yamtbx.dataproc.XIO import XIO
from yamtbx.dataproc.myspotfinder import shikalog

EventResultsUpdated, EVT_RESULTS_UPDATED = wx.lib.newevent.NewEvent()
EventDirWatcherStopped, EVT_DIR_WATCHER_STOPPED = wx.lib.newevent.NewEvent()
EventDirWatcherStarted, EVT_DIR_WATCHER_STARTED = wx.lib.newevent.NewEvent()
EventTargetDirChanged, EVT_TARGET_DIR_CHANGED = wx.lib.newevent.NewEvent()
EventScanlogsUpdated, EVT_SCANLOGS_UPDATED = wx.lib.newevent.NewEvent()
EventLogWatcherStopped, EVT_LOG_WATCHER_STOPPED = wx.lib.newevent.NewEvent()
EventLogWatcherStarted, EVT_LOG_WATCHER_STARTED = wx.lib.newevent.NewEvent()

gui_phil_str = """\
kuma_addr = None
 .type = str
 .help = "kuma address and port; like 192.168.163.5:1920"

imgview_host = None
 .type = str
 .help = "imgview address; like 192.168.163.5"

cuda = False
 .type = bool
 .help = CUDA module enabled

adxv = None
 .type = path
 .help = adxv command

force_ssh_from = None
 .type = str
 .help = Users must not change this parameter.

bl = 32xu 41xu
 .type = choice(multi=False)
 .help = Choose beamline where you start SHIKA
"""

class DiffScanManager:
    def __init__(self):
        self.clear()
    # __init__()

    def clear(self):
        self.scanlog = {} # directory: BssDiffscanLog object
        self.stats = collections.OrderedDict()  # filename: stats
    # clear()

    def add_scanlog(self, slog):
        slog = os.path.abspath(slog)
        self.scanlog[os.path.dirname(slog)] = bl_logfiles.BssDiffscanLog(slog)
    # add_scanlog()

    def update_scanlogs(self):
        for slog in self.scanlog.values():
            if os.path.isfile(slog.scanlog):
                slog.parse()
            else:
                shikalog.error("diffraction scan log is not found!: %s" %slog.scanlog)
    # update_scanlogs()

    def add_results(self, results):
        for f, stat in results:
            self.stats[f] = stat
    # add_results()

    def clear_results(self):
        self.stats = {}
    # clear_results()

    def is_already_processed(self, filename):
        return filename in self.stats

    def needs_to_be_processed(self, filename):
        """
        Check if the given file needs to be processed.
        No need to process if
        - not included in diffscan.log
        - first image in row (only if BSS creates such non-sense files)
        """

        scaninfo = self.get_scan_info(filename)
        if scaninfo is None:
            return False

        # return True here *if* BSS no longer creates such non-sense files.
        # this should be an option.

        if scaninfo.is_shutterless():
            r = scaninfo.get_file_number_based_on_template(filename)
            num = int(r.group(1))
            if scaninfo.hpoints > 1:
                return num%(scaninfo.hpoints+1) != 0 # if remainder is 0, discard the image.
            else:
                return num != 0 # discard 000.img
        else:
            return True
    # needs_to_be_processed()

    def get_grid_coord(self, filename):
        dirname = os.path.dirname(filename)
        if dirname not in self.scanlog:
            shikalog.warning("get_grid_coord(): directory is not found: %s" % dirname)
            return None

        return self.scanlog[dirname].get_grid_coord(os.path.basename(filename))
    # get_grid_coord()

    def get_scan_info(self, filename):
        dirname = os.path.dirname(filename)
        basename = os.path.basename(filename)

        if not dirname in self.scanlog:
            shikalog.warning("get_scan_info(): directory is not found: %s" % dirname)
            return None
        for scan in reversed(self.scanlog[dirname].scans):
            if scan.match_file_with_template(filename):
                return scan

        shikalog.warning("get_scan_info(): Not in scans: %s" % dirname)
        return None
    # get_scan_info()

    def get_gonio_xyz_phi(self, filename):
        dirname = os.path.dirname(filename)
        basename = os.path.basename(filename)

        if not dirname in self.scanlog:
            return None
        for scan in reversed(self.scanlog[dirname].scans):
            for f, c in scan.filename_coords:
                if basename == f:
                    if scan.is_shutterless():
                        return list(c[0]) + [scan.fixed_spindle]
                    else:
                        return list(c[0]) + [scan.osc_start]
        return None

    # get_gonio_xyz_phi()

# class DiffScanManager

class WatchDirThread:
    def __init__(self, parent):
        self.parent = parent
        self.interval = 5
        self.thread = None
        self.lock = threading.RLock() # when modifying diffscan_manager

    def start(self, interval=None):
        self.stop()

        self.keep_going = True
        self.running = True
        if interval is not None:
            self.interval = interval

        self.thread = threading.Thread(None, self.run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        if self.is_running():
            print "Stopping thread.. Wait."
            self.keep_going = False
            self.thread.join()
            wx.PostEvent(self.parent, EventDirWatcherStopped())
        else:
            print "Thread already stopped."

    def is_running(self):
        return self.thread is not None and self.thread.is_alive()

    def run(self):
        print "loop STARTED"
        wx.PostEvent(self.parent, EventDirWatcherStarted())
        while self.keep_going:
            #print "in timer.."
            watchdir = os.path.abspath(os.path.join(self.parent.txtTopDir.GetValue(), self.parent.cmbTargetDir.GetValue()))

            with self.lock:
                self.parent.diffscan_manager.update_scanlogs()

                if not watchdir in self.parent.diffscan_manager.scanlog:
                    continue

                img_files = {}
                scan_infos = {}
                for scan in self.parent.diffscan_manager.scanlog[watchdir].scans:
                    new_imgs = filter(lambda x: not self.parent.diffscan_manager.is_already_processed(x) and os.path.exists(x),
                                      map(lambda y: os.path.join(watchdir, os.path.basename(y[0])),
                                          scan.filename_coords)
                                      )
                    if len(new_imgs) > 0:
                        # In the same scan, detector type should not change..
                        detkey = self.parent.config_manager.get_key_by_img(new_imgs[0])
                        shikalog.info("DETECTOR_TYPE:: %s is %s" % (new_imgs[0], detkey))
                        img_files.setdefault(detkey, []).extend(new_imgs)
                        for img in new_imgs:
                            scan_infos[img] = (scan, self.parent.diffscan_manager.get_grid_coord(img)) # TODO maybe inefficient..

            for key, imgs in img_files.items():
                imgs = list(set(imgs)) # to prevent duplicates (when the same prefix..)
                params = self.parent.config_manager.get_params_by_key(key)
                if params.work_dir is None:
                    params.work_dir = os.path.join(watchdir, "_spotfinder")
                    if os.path.exists(params.work_dir):
                        assert os.path.isdir(params.work_dir)
                    else:
                        os.mkdir(params.work_dir)

                shikalog.info("Start to process %d images" % len(imgs))
                startt = time.time()
                result = spot_finder_for_grid_scan.run(imgs, params)
                delt = time.time() - startt
                shikalog.info("Time elapsed (%d images): %f s (%f s/frame)" % (len(imgs),delt, delt/len(imgs)))

                for f, res in result:
                    res.scan_info, res.grid_coord = scan_infos[f]

                with self.lock:
                    self.parent.diffscan_manager.add_results(result)

                ev = EventResultsUpdated(result=result, params=params)
                wx.PostEvent(self.parent, ev)

            if self.interval < 1:
                time.sleep(self.interval)
            else:
                for i in xrange(int(self.interval/.5)):
                    if self.keep_going:
                        time.sleep(.5)

        print "loop FINISHED"
        self.running = False
        wx.PostEvent(self.parent, EventDirWatcherStopped()) # Ensure the checkbox unchecked when accidentally exited.

    # run()
# class WatchDirThread

class WatchScanlogThread:
    def __init__(self, parent):
        self.parent = parent
        self.interval = 5
        self.thread = None
        self.notify_latest_dir = False
        self.latest_dir = None

        self.keep_going = True
        self.running = True

        self.thread = threading.Thread(None, self.run)
        self.thread.daemon = True
        self.thread.start()

    def start(self, interval=None):
        # Thread should be already started.
        # Just start to notify the latest directory.

        self.notify_latest_dir = True
        wx.PostEvent(self.parent, EventLogWatcherStarted())

        # To notify immediately
        if self.latest_dir is not None:
            wx.PostEvent(self.parent, EventTargetDirChanged(target=self.latest_dir))

        if interval is not None:
            self.interval = interval

        # If accidentally stopped
        if not self.is_running():
            self.keep_going = True
            self.running = True
            self.thread = threading.Thread(None, self.run)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        # Don't stop thread.
        # Just stop notification of latest directory.
        self.notify_latest_dir = False
        wx.PostEvent(self.parent, EventLogWatcherStopped())

    def is_running(self):
        return self.thread is not None and self.thread.is_alive()

    def run(self):
        print "loop2 STARTED"
        while self.keep_going:
            #print "in timer2.."
            if self.parent.txtTopDir.GetValue().strip() == "":
                continue

            topdir = os.path.abspath(self.parent.txtTopDir.GetValue())
            scanlogs = [] # (filename, date)

            for root, dirnames, filenames in os.walk(topdir):
                if "diffscan.log" in filenames:
                    scanlog = os.path.join(root, "diffscan.log")
                    scanlogs.append((scanlog, os.path.getmtime(scanlog)))

            if len(scanlogs) > 0:
                scanlogs.sort(key=lambda x:x[1], reverse=True)
                self.latest_dir = os.path.dirname(scanlogs[0][0])
                wx.PostEvent(self.parent, EventScanlogsUpdated(scanlogs=scanlogs))

                if self.notify_latest_dir:
                    wx.PostEvent(self.parent, EventTargetDirChanged(target=self.latest_dir))

            if self.interval < 1:
                time.sleep(self.interval)
            else:
                for i in xrange(int(self.interval/.5)):
                    if self.keep_going:
                        time.sleep(.5)

        print "loop2 FINISHED"
        self.running = False
        wx.PostEvent(self.parent, EventLogWatcherStopped())
    # run()
# class WatchScanlogThread

class ReportHTMLMakerThread:
    def __init__(self, parent):
        self.parent = parent
        self.interval = 1
        self.thread = None
        self.queue = []
        self.lock = threading.Lock()

        self.plotFrame = parent.plotFrame
        self.diffscan_manager = parent.diffscan_manager
        self.plot_data = None

    def start(self, interval=None):
        self.stop()

        self.keep_going = True
        self.running = True
        if interval is not None:
            self.interval = interval

        self.thread = threading.Thread(None, self.run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        if self.is_running():
            self.keep_going = False
            self.thread.join()
        else:
            pass

    def is_running(self):
        return self.thread is not None and self.thread.is_alive()

    def run(self):
        while self.keep_going:
            if len(self.queue) > 0:
                wdir, rotate = None, None
                # take from queue
                with self.lock:
                    self.queue = list(set(self.queue))
                    wdir, rotate = self.queue.pop(0)

                self.make(wdir, rotate)
                self.make_dat(wdir)

            if self.interval < 1:
                time.sleep(self.interval)
            else:
                for i in xrange(int(self.interval/.5)):
                    if self.keep_going:
                        time.sleep(.5)

        self.running = False
    # run()

    """
    Create HTML report.
    XXX Currently, width is fixed (always 600).
    XXX Currently, only hi_pass_resolution_spots are used. If not available (in case XDS, other?), all are used.
    TODO resolve code duplication in prepare_plot()
    TODO Results should be ordered as in diffscan.log
    TODO Don't make the same plot again. (save & check hash of data)
    """
    def prepare_plot(self, f, kind, wdir):
        def normalize_max(v, maximum=400.):
            max_v = max(v)
            f = maximum / max_v if max_v > 0 else 1.
            return map(lambda x:f*x + 1., v) # add 1 to make zero-value pickable
        # normalize_max()

        scan_prefix = f[:f.index(" ")] if " (phi=" in f else f
        pngout = os.path.join(wdir, "plot_%s%s.png" % (scan_prefix, kind))

        xs, ys, ds, imgfs = [], [], [], []
        zero_xs, zero_ys = [], [] # For values of zero
        for imgf, stat in self.plot_data[f]:
            gc = stat.grid_coord
            if gc is None:
                continue
            x, y = gc
            mode = "hi_pass_resolution_spots" if "hi_pass_resolution_spots" in stat.spots.keys() else "all"
            d = getattr(stat.spots, "get_"+kind)(mode)
            xs.append(x)
            ys.append(y)
            ds.append(d)
            imgfs.append(imgf)

            if d == 0:
                zero_xs.append(x)
                zero_ys.append(y)

        if len(xs) == 0:
            return "", ""

        win = (max(xs)-min(xs)+1)*400/80*1.7 # ad-hoc scale
        hin = (max(ys)-min(ys)+1)*400/80

        fig = matplotlib.figure.Figure(figsize=(win,hin)) # figsize in inches
        ax = fig.add_subplot(111)
        p = ax.scatter(xs, ys, s=normalize_max(ds), c=ds, alpha=0.5) # s in points^2
        if max(ds) - min(ds) > 1e-5:
            fig.colorbar(p)
        ax.scatter(zero_xs, zero_ys, s=50, marker="x", c=[0]*len(zero_xs), alpha=0.5)
        ax.set_xlabel("horizontal [mm]")
        ax.set_ylabel("vertical [mm]")

        scaninfo = self.plot_data[f][0][1].scan_info
        if scaninfo is not None:
            vp, hp = scaninfo.vpoints, scaninfo.hpoints
            vs, hs = scaninfo.vstep, scaninfo.hstep

            if 1 in (vp, hp) or len(self.plot_data[f]) <= hp:
                ax.set_aspect("auto")
            else:
                ax.set_aspect("equal")

            if vp == hp == 1:
                ax.set_xlim(-1, 1)
                ax.set_ylim(-1, 1)
            elif vp == 1:
                ax.set_xlim(min(xs) - hs, max(xs) + hs)
                ax.set_ylim(-1, 1)
            elif hp == 1:
                ax.set_xlim(-1, 1)
                ax.set_ylim(min(ys) - vs, max(ys) + vs)
            else:
                ax.set_xlim(min(xs) - hs, max(xs) + hs)
                ax.set_ylim(min(ys) - vs, max(ys) + vs)
        else:
            # Should never reach here.. but should we set limit here?
            pass

        canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
        canvas.print_figure(pngout, dpi=80)
        img_width = fig.get_figwidth() * 80
        img_height = fig.get_figheight() * 80

        map_str = '<map name="%smap">\n' % scan_prefix
        for x, y, imgf in zip(xs, ys, imgfs):
            tx, ty = ax.transData.transform((x,y))
            map_str += '  <area shape="circle" coords="%.2f,%.2f,10" title="%s" onClick=\'plotClick("%s", "%s")\'>\n' % (tx, img_height-ty, os.path.basename(imgf), scan_prefix, os.path.basename(imgf))

        map_str += "</map>"
        return pngout, map_str
    # prepare_plot()

    def make_dat(self, wdir):
        self.plot_data = self.plotFrame.data

        datout = os.path.join(wdir, "summary.dat")
        ofs = open(datout, "w")
        kinds = map(lambda rb: rb.GetLabelText(), self.plotFrame.rb_kind)

        print >>ofs, "prefix x y kind data filename"
        for f in self.plot_data:
            for i, kind in enumerate(kinds):
                for imgf, stat in self.plot_data[f]:
                    gc = stat.grid_coord
                    if gc is None:
                        continue
                    x, y = gc
                    mode = "hi_pass_resolution_spots" if "hi_pass_resolution_spots" in stat.spots.keys() else "all"
                    d = getattr(stat.spots, "get_"+kind)(mode)
                    print >>ofs, f[:f.rindex("(")-1], x, y, kind, d, os.path.basename(imgf)
    # make_dat()

    def make(self, wdir, rotate=False):
        self.plot_data = self.plotFrame.data
        shikalog.info("Making HTML report for %s"%wdir)
        startt = time.time()

        htmlout = os.path.join(wdir, "report.html")
        if rotate:
            rotate_file(htmlout)

        kinds = map(lambda rb: rb.GetLabelText(), self.plotFrame.rb_kind)
        plots=""
        for f in self.plot_data:
            scan_prefix = f[:f.index(" ")] if " (phi=" in f else f

            info = self.plot_data[f][0][1].scan_info
            if info is None: info = bl_logfiles.ScanInfo() # Empty info
            plots += '<table border=0 style="margin-bottom:0px">\n  <tr><td>\n'
            plots += '  <table class="info"><tr><th>scan</th><td>%s</td></tr>\n' % scan_prefix
            plots += '    <tr><th>date</th><td>%s</td></tr>\n' % (info.date.strftime("%Y/%m/%d %H:%M:%S") if info.date!=0 else "??")

            if info.is_shutterless():
                plots += '    <tr><th>fixed spindle</th><td>%.2f&deg;</td></tr>\n' % info.fixed_spindle
                plots += '    <tr><th>frame rate</th><td>%.2f [Hz]</td></tr>\n' % info.frame_rate
            else:
                plots += '    <tr><th>osc. start</th><td>%.2f&deg;</td></tr>\n' % info.osc_start
                plots += '    <tr><th>osc. step</th><td>%.2f&deg;</td></tr>\n' % info.osc_step
                plots += '    <tr><th>exp. time</th><td>%.2f [sec]</td></tr>\n' % info.exp_time

            plots += '    <tr><th>beam size</th><td>h= %.1f, v= %.1f [&mu;m]</td></tr>\n' % (info.beam_hsize, info.beam_vsize)
            plots += '    <tr><th>attenuator</th><td>%s %.1f [&mu;m]</td></tr>\n' % info.attenuator
            plots += '    <tr><th>distance</th><td>%.2f [mm]</td></tr>\n' % info.distance
            plots += '    <tr><th>wavelength</th><td>%.4f [&#x212b;]</td></tr>\n' % info.wavelength
            plots += '    <tr><th>scan points</th><td>v=%d, h=%d</td></tr>\n' % (info.vpoints, info.hpoints)
            plots += '    <tr><th>scan steps</th><td>v=%.2f, h=%.2f [&mu;m]</td></tr>\n' % (info.vstep*1000., info.hstep*1000.)
            plots += '  </table>\n'
            for i, kind in enumerate(kinds):
                pngout, mapstr = self.prepare_plot(f, kind, wdir)
                adds = ""
                if i == 0:
                    plots += '  <td><img name="%s" src="%s" usemap="#%smap" /><br />\n' % (scan_prefix, os.path.basename(pngout), scan_prefix)
                    plots += '<form>\n'
                    adds = ' checked="checked"'
                plots += '<input type="radio" name="spot_mode" value="%s" onClick="changeplot(this, \'%s\')"%s />%s<br />\n' % (kind, scan_prefix, adds, kind)
            plots += '</form>%s</td></tr></table><br>\n\n' % mapstr # The last mapstr is used. This is dirty way, though.
            plots += '<table border=0 style="margin-bottom:20px">\n  <tr><td>\n'
            plots += '<td style="border:solid 1px #999"><canvas id="%scanvas" width=600 height=600></canvas>\n' % scan_prefix
            plots += '<td id="%sinfo" valign="top"></tr></table>\n\n' % scan_prefix

        with self.parent.ctrlFrame.dir_watcher.lock: # Really needed?
            result = self.diffscan_manager.stats.items()
            if len(result) == 0:
                shikalog.warning("No results found. Exiting. %s"% wdir)
                return

            spot_data = "var spot_data = {"
            for i, (f, stat) in enumerate(result):
                bf = os.path.basename(f)
                spot_mode = "hi_pass_resolution_spots" if "hi_pass_resolution_spots" in stat.spots.keys() else "all"
                spots = stat.spots.get_spots(spot_mode)
                spot_data += '"%s":[[' % os.path.basename(f)
                for spot in spots:
                    x, y = spot.max_pxl_y(), spot.max_pxl_x()
                    pos = stat.thumb_posmag[0:2]
                    mag = stat.thumb_posmag[2]
                    x, y = (x - pos[0])*mag, (y - pos[1])*mag
                    spot_data += "[%d,%d]," % (x, y)

                spot_data += "], %.1f, %.1f, %d]," % (stat.spots.get_total_integrated_signal(spot_mode),
                                                      stat.spots.get_median_integrated_signal(spot_mode),
                                                      stat.spots.get_n_spots(spot_mode))

            spot_data += "};"

            # Determine img picture extension
            img_ext = ".jpg" if os.path.exists(os.path.join(wdir, os.path.basename(result[0][0])+".jpg")) else ".png"

            ofs = open(htmlout, "w")
            ofs.write("""\
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>SHIKA report</title>
  <script type="text/javascript">
  <!--
    function changeplot(obj, name){
     document.images[name].src = "plot_"+name+obj.value+".png";
    }

    %(spot_data)s
    function plotClick(scanprefix, imgfile) {
        var f = imgfile;
        var data = spot_data[f];
        var img = new Image();
        img.src = f + "%(img_ext)s";
        img.onload = (function(fn){
          return function(){
            var td = document.getElementById(scanprefix+"info");
            td.innerHTML = "<table border=0><tr><td>File name: <td>" + imgfile + "<tr><td>total signal: <td>" + data[1] + "<tr><td>median signal: <td>" + data[2] + "<tr><td>N_spots: <td>" + data[3] + "</table>";

            var t = data[0];
            var canvas = document.getElementById(scanprefix+"canvas");
            var ctx = canvas.getContext('2d');
            ctx.clearRect(0,0,canvas.width,canvas.height);
            ctx.drawImage(this, 0, 0);
            for (var i = 0; i < t.length; i++) {
              ctx.rect(t[i][0]-6, t[i][1]-6, 12, 12);
            }
            ctx.strokeStyle = "red";
            ctx.lineWidth = 1;
            ctx.stroke();

            var center = [300,300];
            ctx.beginPath();
            ctx.strokeStyle = "blue";
            ctx.moveTo(center[0]-10, center[1]);
            ctx.lineTo(center[0]+10, center[1]);
            ctx.moveTo(center[0], center[1]-10);
            ctx.lineTo(center[0], center[1]+10);
            ctx.stroke();
          }
        }(f));
    }
  //-->
  </script>
  <style type="text/css">
  <!--
    table.info {
      border-collapse: separate;
      border-spacing: 7px;
    }
    table.info th {
      text-align: left;
    }

    table.images {
      border-collapse: collapse;
      border: solid 1px #999;
    }
    table.images caption {
      margin-top: 1em;
      text-align: left;
    }
    table.images th,
    table.images td {
      border: solid 1px #999;
    }
    table.images th {
      background: #E6E6E6;
      text-align: center;
      white-space: nowrap;
    }
  -->
  </style>
</head>

<body>
<h1>SHIKA report</h1>
<div align="right">
Created on %(date)s<br>
Original directory: %(wdir)s
</div>
<hr style="height: 1px;border: none;border-top: 1px #000000 dotted;" />

%(plots)s

</body>
</html>

""" % dict(spot_data=spot_data,
           plots=plots,
           date=datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
           wdir=wdir,
           img_ext=img_ext))

        delt = time.time() - startt
        shikalog.info("HTML making Done (took %f s). Open? firefox %s"% (delt, htmlout))
    # make()
# class ReportHTMLMakerThread

class ConfigManager:
    def __init__(self, use_cuda):
        self.items = collections.OrderedDict()
        self.set_item(beamline="BL32XU", detector="MX225HS", binning="2x2", extra=None,
                      params_str="""\
distl {
  detector_tiles = 3
  peripheral_margin = 10
  minimum_spot_area = 5
  minimum_signal_height = 2.
  minimum_spot_height = None
}
xds {
  strong_pixel = 4
  minimum_number_of_pixels_in_a_spot = 3
  background_pixel = None
}
software_binning = False
""")
        self.set_item(beamline="BL32XU", detector="MX225HS", binning="4x4", extra=None,
                      params_str="""\
distl {
  detector_tiles = 3
  peripheral_margin = 10
  minimum_spot_area = 2
  minimum_signal_height = 4.
  minimum_spot_height = None
}
xds {
  strong_pixel = 4
  minimum_number_of_pixels_in_a_spot = 3
  background_pixel = None
}
software_binning = False
""")
        self.set_item(beamline="BL32XU", detector="MX225HS", binning="8x8", extra=None,
                      params_str="""\
distl {
  detector_tiles = 3
  peripheral_margin = 5
  minimum_spot_area = 1
  minimum_signal_height = 4.
  minimum_spot_height = None
}
xds {
  strong_pixel = 4
  minimum_number_of_pixels_in_a_spot = 3
  background_pixel = None
}
software_binning = False
""")
        self.set_item(beamline="BL41XU", detector="PILATUS3 6M", binning=None, extra=None,
                      params_str="""\
distl {
  detector_tiles = None
  peripheral_margin = 10
  minimum_spot_area = 2
  minimum_signal_height = 4
  minimum_spot_height = None
}
xds {
  strong_pixel = 4
  minimum_number_of_pixels_in_a_spot = 3
  background_pixel = None
}
software_binning = False
""")

        if use_cuda:
            dic = dict(nproc=1, xds_like_background="True")
        else:
            dic = dict(nproc=get_number_of_processors(default=4),
                       xds_like_background="False")

        self.common_params_str = """\
engine = *distl xds
nproc = %(nproc)d
distl {
  res {
    outer = 5.
    inner = 30.
  }
  scanbox_windows = 101 51 51
}
xds {
  do_defpix = True
  value_range_for_trusted_detector_pixels = 9000. 30000
}
xds_like_background = %(xds_like_background)s

#bkg_image = /home/yam/work/smoothing_131114/xds_process_scan/BKGINIT.cbf
#gain_image = /home/yam/work/smoothing_131114/xds_process_scan/GAIN.cbf
#bkg_image = /home/yam/work/smoothing_131114/my_scan172/honki/bkginit_20_20_1.cbf
#gain_image = /home/yam/work/smoothing_131114/my_scan172/honki/test_rev_median5.cbf
#gain_image_nbxy = 3,3
""" % dic
    # __init__()

    def get_common_params_str(self): return self.common_params_str
    def set_common_params_str(self, s): self.common_params_str = s
    def get_specific_params_str(self, key): return self.items[key]
    def set_specific_params_str(self, key, s): self.items[key] = s

    def set_item(self, beamline, detector, binning, extra, params_str):
        self.items[(beamline, detector, binning, extra)] = params_str
    # set_item()

    def get_key_by_img(self, imgfile):
        im = XIO.Image(imgfile)
        if im.header["ImageType"] == "marccd":
            if im.header["SerialNumber"] in ("106", None): # None for 2013B
                if im.header["Height"] == im.header["Width"] == 1440:
                    return ("BL32XU", "MX225HS", "4x4", None)
                if im.header["Height"] == im.header["Width"] == 2880:
                    return ("BL32XU", "MX225HS", "2x2", None)
                if im.header["Height"] == im.header["Width"] == 720:
                    return ("BL32XU", "MX225HS", "8x8", None)

        if im.header["SerialNumber"] == "PILATUS3 6M, S/N 60-0125":
            return ("BL41XU", "PILATUS3 6M", None, None)

        raise Exception("We do not know such a detector")
    # get_key_by_img()

    def get_params_str_by_key(self, key):
        if key in self.items:
            return self.common_params_str + self.items[key]
        raise KeyError("We do not know such a detector.")
    # get_params_str_by_key()

    def get_params_str_by_img(self, imgfile):
        key = self.get_key_by_img(imgfile)
        return self.get_params_str_by_key(key)
    # get_params_str_by_img()

    def get_params_by_key(self, key):
        params_str = self.get_params_str_by_key(key)

        master_params = libtbx.phil.parse(spot_finder_for_grid_scan.master_params_str)
        working_params = master_params.fetch(sources=[libtbx.phil.parse(params_str)])
        working_params.show()
        return working_params.extract()
    # get_params_by_key()

    def check_phil_valid(self, phil_str):
        master_params = libtbx.phil.parse(spot_finder_for_grid_scan.master_params_str)
        try:
            working_params, alldef = master_params.fetch(sources=[libtbx.phil.parse(phil_str)],
                                                         track_unused_definitions=True)
            working_params.extract()
            if len(alldef) > 0:
                return "Unknown parameters: " + ", ".join(map(lambda x:x.path, alldef))
        except RuntimeError, e:
            return e.message
        return ""
    # check_phil_valid()

    def get_names(self):
        ret = []
        for k in self.items:
            s = "%s %s" % (k[0], k[1])
            ex = []
            if k[2] is not None:
                ex.append("%s bin" % k[2])
            if k[3] is not None:
                ex.append(k[3])
            if len(ex) > 0:
                s += " " + ", ".join(ex)

            ret.append((s, k))
        return ret
    # get_names()

# class ConfigManager

class ConfigFrame(wx.Frame):
    class CommonPanel(wx.Panel):
        def __init__(self, parent, manager):
            wx.Panel.__init__(self, parent)
            self.manager = manager
            sizer = wx.GridBagSizer()
            self.SetSizer(sizer)
            lab = wx.StaticText(self, wx.ID_ANY, "Common Settings")
            lab.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))
            self.txtctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
            self.btnRevert = wx.Button(self, wx.ID_ANY, "Revert")
            self.btnApply = wx.Button(self, wx.ID_ANY, "Apply")
            sizer.Add(lab, pos=(0,0), span=(1,2))
            sizer.Add(self.txtctrl, pos=(1,0), span=(1,2), flag=wx.EXPAND|wx.ALL, border=4)
            sizer.Add(self.btnRevert, pos=(2,0), flag=wx.EXPAND)
            sizer.Add(self.btnApply, pos=(2,1), flag=wx.EXPAND)
            sizer.AddGrowableRow(1)
            sizer.AddGrowableCol(0)
            sizer.AddGrowableCol(1)

            self.btnRevert.Bind(wx.EVT_BUTTON, self.btnRevert_onClick)
            self.btnApply.Bind(wx.EVT_BUTTON, self.btnApply_onClick)

            self.btnRevert_onClick(None)
        # __init__()

        def btnRevert_onClick(self, ev): self.txtctrl.SetValue(self.manager.get_common_params_str())

        def btnApply_onClick(self, ev):
            phil_str = self.txtctrl.GetValue()
            err = self.manager.check_phil_valid(phil_str)
            if err == "":
                self.manager.set_common_params_str(phil_str)
            else:
                wx.MessageDialog(None, "Wrong settings! Please resolve following error:\n\n"+err,
                                 "Error", style=wx.OK).ShowModal()
        # btnApply_onClick()
    # class CommonPanel

    class SpecificPanel(wx.Panel):
        def __init__(self, parent, manager, beamline):
            wx.Panel.__init__(self, parent)
            self.manager = manager
            sizer = wx.GridBagSizer()
            self.SetSizer(sizer)
            lab = wx.StaticText(self, wx.ID_ANY, "Specific Settings: ")
            lab.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))
            self.cmbDet = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_READONLY)
            self.txtctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
            self.btnRevert = wx.Button(self, wx.ID_ANY, "Revert")
            self.btnApply = wx.Button(self, wx.ID_ANY, "Apply")
            sizer.Add(lab, pos=(0,0))
            sizer.Add(self.cmbDet, pos=(0,1), flag=wx.EXPAND)
            sizer.Add(self.txtctrl, pos=(1,0), span=(1,2), flag=wx.EXPAND|wx.ALL, border=4)
            sizer.Add(self.btnRevert, pos=(2,0), flag=wx.EXPAND)
            sizer.Add(self.btnApply, pos=(2,1), flag=wx.EXPAND)
            sizer.AddGrowableRow(1)
            sizer.AddGrowableCol(0)
            sizer.AddGrowableCol(1)

            self.btnRevert.Bind(wx.EVT_BUTTON, self.btnRevert_onClick)
            self.btnApply.Bind(wx.EVT_BUTTON, self.btnApply_onClick)
            self.cmbDet.Bind(wx.EVT_COMBOBOX, self.btnRevert_onClick) # Just reverting works.

            self.set_names(beamline)
            self.btnRevert_onClick(None)
        # __init__()

        def set_names(self, beamline=None):
            self.keys = {}
            self.cmbDet.Clear()

            for name, key in self.manager.get_names():
                self.cmbDet.Append(name)
                self.keys[name] = key

            self.cmbDet.Select(0)

            if beamline == "32xu":
                fltr = filter(lambda x: "BL32XU" in x[1], enumerate(self.cmbDet.GetItems()))
                if len(fltr) > 0:
                    self.cmbDet.Select(fltr[0][0])
            elif beamline == "41xu":
                fltr = filter(lambda x: "BL41XU" in x[1], enumerate(self.cmbDet.GetItems()))
                if len(fltr) > 0:
                    self.cmbDet.Select(fltr[0][0])
            else:
                shikalog.warning("Unknown beamline: %s" %beamline)
        # set_names()

        def btnRevert_onClick(self, ev):
            key = self.keys[self.cmbDet.GetValue()]
            self.txtctrl.SetValue(self.manager.get_specific_params_str(key))
        # btnRevert_onClick()

        def btnApply_onClick(self, ev):
            key = self.keys[self.cmbDet.GetValue()]

            phil_str = self.txtctrl.GetValue()
            err = self.manager.check_phil_valid(phil_str)
            if err == "":
                self.manager.set_specific_params_str(key, phil_str)
            else:
                wx.MessageDialog(None, "Wrong settings! Please resolve following error:\n\n"+err,
                                 "Error", style=wx.OK).ShowModal()

        # btnApply_onClick()

    # class SpecificPanel

    def __init__(self, parent=None, use_cuda=False, beamline=None):
        wx.Frame.__init__(self, parent=parent, id=wx.ID_ANY, title="Settings",
                          size=(800,600))

        self.manager = ConfigManager(use_cuda)
        self.splitter = wx.SplitterWindow(self, id=wx.ID_ANY)
        self.splitter.SetSashGravity(0.5)
        self.panel1 = self.CommonPanel(self.splitter, self.manager)
        self.panel2 = self.SpecificPanel(self.splitter, self.manager, beamline)
        self.splitter.SplitVertically(self.panel1, self.panel2)
        self.splitter.SetSashPosition(400)

        self.Bind(wx.EVT_CLOSE, lambda e: self.Hide()) # Don't destroy this frame when closed
    # __init__()
# class ConfigFrame

class ControlPanel(wx.Panel):
    def __init__(self, mainFrame, params, parent=None, id=wx.ID_ANY):
        wx.Panel.__init__(self, parent=parent, id=id)
        self.mainFrame = mainFrame

        self.diffscan_manager = self.mainFrame.diffscan_manager
        self.current_target_dir = None
        self.vbox = vbox = wx.BoxSizer(wx.VERTICAL)

        self.treectrl = wx.TreeCtrl(self, size=(500, 450))
        self.il_for_treectrl = wx.ImageList(16,16)
        self.il_for_treectrl.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16,16)))
        self.il_for_treectrl.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16,16)))
        self.il_for_treectrl.Add(wx.ArtProvider.GetBitmap(wx.ART_NEW_DIR, wx.ART_OTHER, (16,16)))
        self.treectrl.AssignImageList(self.il_for_treectrl)
        self.dic_for_tree = {}
        vbox.Add(self.treectrl, flag=wx.EXPAND|wx.TOP, border=4)

        self.configFrame = ConfigFrame(self, use_cuda=params.cuda, beamline=params.bl)
        self.config_manager = self.configFrame.manager

        self.btnConfig = wx.Button(self, wx.ID_ANY, "Edit settings")
        self.btnUpdate = wx.Button(self, wx.ID_ANY, "Recalculate result (if you need)")
        self.btnShowPlot = wx.Button(self, wx.ID_ANY, "Show plot")
        self.btnShowPlot.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT,
                                         wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.btnSetExResRange = wx.Button(self, wx.ID_ANY, "Set exclude_resolution ranges (special)")
        self.exclude_resolution_ranges = []

        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        hbox0.Add(wx.StaticText(self, wx.ID_ANY, "TopDir: "), flag=wx.LEFT)
        self.txtTopDir = wx.TextCtrl(self, wx.ID_ANY, size=(400,25))
        self.txtTopDir.SetEditable(False)
        hbox0.Add(self.txtTopDir, flag=wx.EXPAND|wx.RIGHT)

        self.grpTarget = wx.StaticBox(self, wx.ID_ANY, "Target")
        self.vbox_grpTarget = wx.StaticBoxSizer(self.grpTarget, wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.StaticText(self, wx.ID_ANY, "Dir: "), flag=wx.LEFT)
        self.cmbTargetDir = wx.ComboBox(self, wx.ID_ANY, size=(350,25), style=wx.CB_DROPDOWN)
        #self.btnTargetDir = wx.Button(self, wx.ID_ANY, "...", size=(25,25))
        self.chkTargetDir = wx.CheckBox(self, wx.ID_ANY, "Autofind")
        hbox1.Add(self.cmbTargetDir, flag=wx.EXPAND|wx.LEFT)
        #hbox1.Add(self.btnTargetDir, flag=wx.EXPAND|wx.LEFT)
        hbox1.Add(self.chkTargetDir, flag=wx.EXPAND|wx.LEFT)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.chkWatchDir = wx.CheckBox(self, wx.ID_ANY, "Watch this directory every ")
        hbox3.Add(self.chkWatchDir)
        self.txtWatchInterval = wx.TextCtrl(self, wx.ID_ANY, "5", size=(50,25))
        hbox3.Add(self.txtWatchInterval)
        hbox3.Add(wx.StaticText(self, wx.ID_ANY, " seconds"), flag=wx.LEFT)
        self.chkTrackLatest = wx.CheckBox(self, wx.ID_ANY, "Track the latest result (auto-select scan)")
        self.vbox_grpTarget.Add(hbox1)
        self.vbox_grpTarget.Add(hbox3)
        self.vbox_grpTarget.Add(self.chkTrackLatest)

        vbox.Add(self.btnConfig, flag=wx.EXPAND|wx.TOP, border=4)
        vbox.Add(self.btnUpdate, flag=wx.EXPAND|wx.TOP, border=4)
        vbox.Add(self.btnSetExResRange, flag=wx.EXPAND|wx.TOP, border=4)
        vbox.Add(self.btnShowPlot, flag=wx.EXPAND|wx.TOP, border=4)
        vbox.Add(hbox0, flag=wx.EXPAND|wx.TOP, border=4)
        vbox.Add(self.vbox_grpTarget, flag=wx.EXPAND|wx.TOP, border=4)

        self.btnConfig.Bind(wx.EVT_BUTTON, self.btnConfig_onClick)
        self.btnUpdate.Bind(wx.EVT_BUTTON, self.btnUpdate_onClick)
        self.btnShowPlot.Bind(wx.EVT_BUTTON, self.btnShowPlot_click)
        self.btnSetExResRange.Bind(wx.EVT_BUTTON, self.btnSetExResRange_onClick)
        #self.btnTargetDir.Bind(wx.EVT_BUTTON, self.btnTargetDir_click)
        self.chkWatchDir.Bind(wx.EVT_CHECKBOX, self.chkWatchDir_onCheck)
        self.chkTrackLatest.Bind(wx.EVT_CHECKBOX, self.chkTrackLatest_onCheck)
        self.chkTargetDir.Bind(wx.EVT_CHECKBOX, self.chkTargetDir_onCheck)
        self.cmbTargetDir.Bind(wx.EVT_COMBOBOX, self.cmbTargetDir_onSelect)
        self.treectrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.treectrl_onSelChanged)
        # Radio button to toggle displayed spots
        self.vbox_rb = vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(vbox1, flag=wx.EXPAND, border=4)
        self.rbuttons = []

        self.SetSizer(vbox)

        self.dir_watcher = WatchDirThread(self)
        self.result_update_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_result_update_timer, self.result_update_timer)
        self.result_pool = []
        self.lock = threading.Lock()
        self.scanlog_watcher = WatchScanlogThread(self)
        self.Bind(EVT_RESULTS_UPDATED, self.onResultsUpdated)
        self.Bind(EVT_TARGET_DIR_CHANGED, self.onTargetDirChanged)
        self.Bind(EVT_SCANLOGS_UPDATED, self.onScanlogsUpdated)
        self.Bind(EVT_DIR_WATCHER_STOPPED, lambda e:self.chkWatchDir.SetValue(False))
        self.Bind(EVT_DIR_WATCHER_STARTED, lambda e:self.chkWatchDir.SetValue(True))
        self.Bind(EVT_LOG_WATCHER_STOPPED, lambda e:self.chkTargetDir.SetValue(False))
        self.Bind(EVT_LOG_WATCHER_STARTED, lambda e:self.chkTargetDir.SetValue(True))
    # __init__()

    def btnTargetDir_click(self, event):
        current_dir = os.path.join(self.txtTopDir.GetValue(), self.cmbTargetDir.GetValue())
        dlg = wx.DirDialog(None, message="Choose a directory to watch", defaultPath=current_dir)

        if dlg.ShowModal() == wx.ID_OK:
            dirsel = dlg.GetPath()
            if os.path.isdir(dirsel):
                if os.path.isfile(os.path.join(dirsel, "diffscan.log")):
                    wx.PostEvent(self, EventTargetDirChanged(target=dirsel))
                    self.scanlog_watcher.stop()
                else:
                    wx.MessageDialog(None, "diffscan.log does not exist!", "Error", style=wx.OK).ShowModal()
            else: # never reaches, maybe. it seems to automatically create new empty directory.. bleugh.
                wx.MessageDialog(None, "Directory does not exist!", "Error", style=wx.OK).ShowModal()
        dlg.Destroy()
    # btnTargetDir_click()

    def cmbTargetDir_onSelect(self, event):
        target_dir = os.path.join(self.txtTopDir.GetValue(), self.cmbTargetDir.GetValue())
        self.scanlog_watcher.stop()
        wx.PostEvent(self, EventTargetDirChanged(target=target_dir))
    # cmbTargetDir_onSelect()

    def treectrl_onSelChanged(self, event):
        item = event.GetItem()
        seldir = self.treectrl.GetPyData(item)

        target_dir = os.path.join(self.txtTopDir.GetValue(), seldir)
        if target_dir == self.current_target_dir:
            return # when selection changed from outside.

        self.scanlog_watcher.stop()
        wx.PostEvent(self, EventTargetDirChanged(target=target_dir))
    # treectrl_onSelChanged()

    def onTargetDirChanged(self, event, need_load=True):
        """
        event.target is the new target directory. It must be an absolute path.
        """

        new_target = os.path.abspath(event.target) # to remove /. or /../hoge
        if new_target == self.current_target_dir:
            return

        # Clear shown results. TODO this part need to move to other class.
        mainframe = self.mainFrame
        mainframe.data = collections.OrderedDict()

        mainframe.plotFrame.data = collections.OrderedDict()
        mainframe.plotFrame.reset_cmb_file()
        mainframe.plotFrame.plotPanel.reset()
        mainframe.plotFrame.splotFrame.reset()
        mainframe.grid.clear()

        scanlog = os.path.join(new_target, "diffscan.log")
        if not os.path.isfile(scanlog):
            shikalog.warning("NOT FOUND: %s"% scanlog)
            return

        # Update combo box
        cmb_items = self.cmbTargetDir.GetItems()
        new_path = os.path.relpath(new_target, self.txtTopDir.GetValue())
        if new_path in cmb_items:
            self.cmbTargetDir.Select(cmb_items.index(new_path))
        else:
            self.cmbTargetDir.Append(new_path)
            self.cmbTargetDir.Select(self.cmbTargetDir.GetCount()-1)

        # Stop timer (and will restart again if running)
        is_watcher_running = self.dir_watcher.is_running()
        if is_watcher_running:
            self.dir_watcher.stop()
            self.result_update_timer.Stop()

        # Register diffscan.log
        with self.dir_watcher.lock: # really needed?
            if new_target not in self.diffscan_manager.scanlog:
                self.diffscan_manager.add_scanlog(scanlog)

        self.current_target_dir = new_target

        # Select item in tree
        k = tuple(os.path.relpath(new_target, self.mainFrame.topdir).split(os.sep))
        if k in self.dic_for_tree:
            self.treectrl.EnsureVisible(self.dic_for_tree[k])
            self.treectrl.SelectItem(self.dic_for_tree[k])

        # Load .pkl data
        if need_load:
            mainframe.load_results()

        if is_watcher_running:
            self.chkWatchDir.SetValue(True)
            self.dir_watcher.start()
            self.result_update_timer.Start()
    # onTargetDirChanged()

    def onScanlogsUpdated(self, event):
        # Update directory tree
        dirs = map(lambda x: os.path.relpath(os.path.dirname(x[0]), self.mainFrame.topdir), event.scanlogs)
        dic = self.dic_for_tree
        for d in dirs:
            sp = d.split(os.sep)
            for i in xrange(len(sp)):
                key, keypar = tuple(sp[:i+1]), tuple(sp[:i])
                if key not in dic:
                    dic[key] = self.treectrl.AppendItem(dic[keypar], sp[i], image=0)
                    self.treectrl.SetPyData(dic[key], os.sep.join(sp[:i+1]))
    # onScanlogsUpdated()

    def btnShowPlot_click(self, event):
        self.mainFrame.plotFrame.Show()
        self.mainFrame.plotFrame.Raise()
    # btnShowPlot_click()

    def btnConfig_onClick(self, event):
        self.configFrame.Show()
        self.configFrame.Raise()
    # btnConfig_onClick()

    def chkWatchDir_onCheck(self, event):
        if event.IsChecked():
            print "Timer start"
            try:
                interval = float(self.txtWatchInterval.GetValue())
                if interval < .5:
                    raise
            except:
                shikalog.warning("Invalid value! Resetting to 1 second.")
                self.txtWatchInterval.SetValue("1")
                interval = 1

            self.dir_watcher.start(interval)
            self.result_update_timer.Start(3*1000) # TODO tweak this..
        else:
            self.dir_watcher.stop()
            self.result_update_timer.Stop()
    # chkWatchDir_onCheck()

    def chkTargetDir_onCheck(self, event):
        if event.IsChecked():
            print "Timer2 start"
            self.scanlog_watcher.start()
        else:
            self.scanlog_watcher.stop()
    # chkWatchDir_onCheck()

    def chkTrackLatest_onCheck(self, event):
        if event.IsChecked():
            self.mainFrame.track_latest_result()
    # chkTrackLatest_onCheck()

    def onResultsUpdated(self, ev):
        result = ev.result

        # When target directory is changed before the spotfinder is finished..
        if len(ev.result) > 0 and self.current_target_dir != os.path.dirname(ev.result[0][0]):
            shikalog.error("Mismatch!! %s %s" % (self.current_target_dir, ev.result[0][0]))
            return

        with self.lock:
            self.result_pool.extend(result)
    #  onResultsUpdated()

    def on_result_update_timer(self, ev):
        if len(self.result_pool) == 0:
            return

        self.result_update_timer.Stop()

        with self.lock:
            result = self.result_pool
            self.result_pool = []

        startt = time.time()
        d = wx.lib.agw.pybusyinfo.PyBusyInfo("Updating %d results.." % len(result), title="Busy SHIKA")
        try:
            try:
                wx.SafeYield()
            except:
                pass

            for f, stat in sorted(result):
                if f not in self.mainFrame.data:
                    item = MainFrame.Item(f)
                    self.mainFrame.data[f] = item

            #self.diffscan_manager.add_results(result) # Must be called before this function!
            #self.diffscan_manager.update_scanlogs() # Must be called outside!!
            self.update_rbuttons()
            self.mainFrame.update_result(append=True)
        finally:
            d = None

        shikalog.info("Updating took %f s. len(data)= %d, len(result)= %d." % (time.time() - startt, len(self.mainFrame.data), len(result)))
        self.result_update_timer.Start()
    # on_result_update_timer()

    def get_spot_draw_mode(self):
        for rbtn in self.rbuttons:
            if rbtn.GetValue():
                return rbtn.GetLabelText()
        return None
    # get_spot_draw_mode()

    def set_spot_draw_mode(self, mode):
        """
        Try to set mode (if found)
        """
        for rbtn in self.rbuttons:
            if rbtn.GetLabelText() == mode:
                rbtn.SetValue(True)
                return True
        return False
    # set_spot_draw_mode()

    def rb_clicked(self, event, call_from_runbutton=False, append=False):
        mode = self.get_spot_draw_mode()
        if mode is None:
            return

        self.mainFrame.grid.refresh_image() # To update spot drawing
        self.mainFrame.plotFrame.rb_clicked(None)

        if self.mainFrame.grid.current_img_file is None:
            self.mainFrame.grid.load(self.mainFrame.data.keys()[0])
        else:
            self.mainFrame.grid.update()
    # rb_clicked()

    def update_rbuttons(self):
        result = self.diffscan_manager.stats
        if len(result) < 1:
            return

        self.rbuttons = []
        self.vbox_rb.DeleteWindows()
        for i, k in enumerate(spotfinder_info.all_keys):
            if i == 0:
                self.rbuttons.append(wx.RadioButton(self, wx.ID_ANY, k, style=wx.RB_GROUP))
            else:
                self.rbuttons.append(wx.RadioButton(self, wx.ID_ANY, k))

        self.rbuttons.append(wx.RadioButton(self, wx.ID_ANY, "do not show spots"))

        for rb in self.rbuttons:
            self.vbox_rb.Add(rb)
            rb.Bind(wx.EVT_RADIOBUTTON, self.rb_clicked)

        self.Fit()
    # update_rbuttons()

    def btnUpdate_onClick(self, event):
        if len(self.mainFrame.data) == 0:
            shikalog.debug("Recalculation does not make sense because no data.")
            return

        shikalog.debug("Recalculation button pressed.")

        if wx.MessageDialog(None, "All results in this directory will be recalculated. Are you sure?",
                            "Confirm", style=wx.YES_NO).ShowModal() == wx.ID_NO:
            shikalog.debug("Recalculation canceled.")
            return

        # Duplicated code! see onTargetDirChanged.
        # Stop timer (and will restart again if running)
        is_watcher_running = self.dir_watcher.is_running()
        try:
            if is_watcher_running:
                shikalog.info("Stopping WatchDirThread.")

                self.dir_watcher.stop()
                self.result_update_timer.Stop()

            self.diffscan_manager.clear_results() # TODO Is it needed and really OK??
            self.diffscan_manager.update_scanlogs()

            # Group images by detector type.
            # TODO: too inefficient way. need speed up.
            img_files = {}
            for x in self.mainFrame.data.values():
                detkey = self.config_manager.get_key_by_img(x.img_file)
                img_files.setdefault(detkey, []).append(x.img_file)

            for key, imgs in img_files.items():
                params = self.config_manager.get_params_by_key(key)
                if params.work_dir is None:
                    params.work_dir = os.path.join(self.current_target_dir, "_spotfinder")
                if os.path.exists(params.work_dir):
                    assert os.path.isdir(params.work_dir)
                else:
                    os.mkdir(params.work_dir)

                shikalog.info("Start to process %d images" % len(self.mainFrame.data))
                startt = time.time()
                result = spot_finder_for_grid_scan.run(self.mainFrame.data.keys(), params)
                for f, res in result:
                    res.scan_info = self.diffscan_manager.get_scan_info(f)
                    res.grid_coord = self.diffscan_manager.get_grid_coord(f)

                delt = time.time() - startt
                shikalog.info("Time elapsed (Total %d images): %f s (%f s/frame)" % (len(self.mainFrame.data), delt, delt/len(self.mainFrame.data)))
                self.diffscan_manager.add_results(result)

            self.update_rbuttons()
            self.mainFrame.update_result()
        finally:
            if is_watcher_running:
                shikalog.info("Restarting WatchDirThread.")
                self.chkWatchDir.SetValue(True)
                self.dir_watcher.start()
                self.result_update_timer.Start()
    # btnUpdate_onClick()

    def btnSetExResRange_onClick(self, event):
        class Dlg(wx.Dialog):
            def __init__(self, parent, ranges):
                wx.Dialog.__init__(self, parent, wx.ID_ANY, "Exclude Resolution Ranges", size=(250, 150))

                vbox = wx.BoxSizer(wx.VERTICAL)
                self.txtComment = wx.TextCtrl(self, wx.ID_ANY, "", (95, 155), style=wx.TE_MULTILINE)
                hbox = wx.BoxSizer(wx.HORIZONTAL)
                btnOK = wx.Button(self, wx.ID_ANY, 'OK', size=(70, 30))
                btnCancel = wx.Button(self, wx.ID_ANY, 'Cancel', size=(70, 30))
                hbox.Add(btnOK, 1)
                hbox.Add(btnCancel, 1, wx.LEFT, 5)

                vbox.Add(wx.StaticText(self, wx.ID_ANY, "Exclude resolution ranges:"))
                vbox.Add(wx.StaticText(self, wx.ID_ANY, " e.g. 12.0 14.0"))
                vbox.Add(self.txtComment, 1, wx.GROW|wx.LEFT)
                vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
                #vbox.Add(wx.StaticText(self, wx.ID_ANY, "Note that this configuration\n does not affect html report."))
                self.SetSizer(vbox)

                self.txtComment.SetFocus()
                self.ranges = ranges
                self.txtComment.SetValue("\n".join(map(lambda r:"%.2f %.2f" % r, self.ranges))+"\n")

                btnOK.Bind(wx.EVT_BUTTON, self.btnOK_click)
                btnCancel.Bind(wx.EVT_BUTTON, lambda e: self.Destroy())
            # __init__()

            def btnOK_click(self, event):
                try:
                    newranges = []
                    for l in self.txtComment.GetValue().splitlines():
                        if l.strip() == "":
                            continue
                        sp = map(float, l.strip().split())
                        if len(sp) != 2:
                            raise Exception("More than or less than two numbers in line.")
                        if abs(sp[0] - sp[1]) < 1e-4:
                            raise Exception("Idential values.")
                        newranges.append((sp[0], sp[1]))
                except:
                    wx.MessageDialog(None, "Check inputs.\nSpecify two different real numbers in line.",
                                     "Error", style=wx.OK).ShowModal()
                    return

                del self.ranges[:]
                self.ranges.extend(newranges)
                self.Destroy()
            # btnOK_click()
        # class Dlg

        exc_range = copy.copy(self.exclude_resolution_ranges)
        dlg = Dlg(self, exc_range)
        dlg.ShowModal()

        if exc_range != self.exclude_resolution_ranges:
            self.exclude_resolution_ranges = exc_range
            shikalog.info("exclude_resolution_ranges = %s" % self.exclude_resolution_ranges)
            self.update_rbuttons()
            self.mainFrame.update_result()
        else:
            shikalog.debug("exclude_resolution_ranges not changed from %s" % self.exclude_resolution_ranges)
    # btnSetExResRange_onClick()
# class ControlPanel

class ScatterPlotFrame(wx.Frame):
    class ScatterPlotPanel(wx.Panel):
        def __init__(self, parent):
            wx.Panel.__init__(self, parent)#, size=(600,400))
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.SetSizer(self.sizer)

            self.figure = matplotlib.figure.Figure(None)
            self.subplot = self.figure.add_subplot(111)
            self.points = []

            self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg(self, wx.ID_ANY, self.figure)
            self.sizer.Add(self.canvas, 1, flag=wx.LEFT|wx.TOP|wx.GROW)

            self.reset()
        # __init__()

        def reset(self):
            for p in self.points:
                p.remove()

            self.points = []
            self.SetSize((self.Size[0],self.Size[1])) # Clear drawn plot
        # reset()

    # class ScatterPlotPanel

    def __init__(self, parent=None, id=wx.ID_ANY):
        wx.Frame.__init__(self, parent=parent, id=id, title="Plot",
                          size=(600,600))
        self.Bind(wx.EVT_CLOSE, lambda e: self.Hide()) # Don't destroy this frame when closed
        self.splotPanel = self.ScatterPlotPanel(self) # scatter plot (I vs d^-2)
        self.reset = self.splotPanel.reset
        self.statusbar = self.CreateStatusBar()
        self.splotPanel.canvas.mpl_connect('motion_notify_event', self.canvas_onMouseMove)
    # __init__()

    def plot(self, spots, mode, res_outer, filename=None):
        s2_formatter = lambda x,pos: "inf" if x == 0 else "%.2f" % (1./math.sqrt(x))
        log_formatter = lambda x,pos: "%.2e" % (10.**x)

        xs, ys = [], []
        mode_near = spots.find_nearest_key(mode)
        for d, i in zip(spots.resolutions[mode_near], spots.intensities[mode_near]):
            s2 = 1./d**2 if d > 0 else -1
            xs.append(s2)
            ys.append(math.log10(i))

        self.splotPanel.subplot.xaxis.set_major_formatter(FuncFormatter(s2_formatter))
        self.splotPanel.subplot.yaxis.set_major_formatter(FuncFormatter(log_formatter)) # set_yscale("log") didn't work.. why?
        p = self.splotPanel.subplot.scatter(xs, ys)
        self.splotPanel.points = [p]
        self.splotPanel.subplot.set_xlabel("resolution (s^2)")
        self.splotPanel.subplot.set_ylabel("intensity")
        if res_outer is not None:
            self.splotPanel.subplot.set_xlim(0, 1./res_outer**2)

        if filename is not None:
            self.SetTitle(os.path.basename(filename))
    # plot()

    def canvas_onMouseMove(self, event):
        if None not in (event.xdata, event.ydata):
            d = math.sqrt(1./event.xdata) if event.xdata > 0 else float("inf")
            self.statusbar.SetStatusText("d= %.2f, I= %.2f" % (d, 10**event.ydata))
        else:
            self.statusbar.SetStatusText("")
    # canvas_onMouseMove()
# class ScatterPlotFrame

class PlotFrame(wx.Frame):
    class PlotPanel(wx.Panel):
        def __init__(self, parent):
            wx.Panel.__init__(self, parent)#, size=(600,400))
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.SetSizer(self.sizer)

            #matplotlib figure
            self.figure = matplotlib.figure.Figure(None)
            self.figure.set_facecolor((0.7,0.7,1.))
            self.subplot = self.figure.add_subplot(111)
            self.colorbar = None
            self.points = []

            #canvas
            self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg(self, wx.ID_ANY, self.figure)
            self.canvas.SetBackgroundColour(wx.Color(100,255,255))
            self.canvas.mpl_connect('motion_notify_event', self.canvas_onMouseMove)
            self.canvas.mpl_connect('button_press_event', self.canvas_onMouseDown)
            self.sizer.Add(self.canvas, 1, flag=wx.LEFT|wx.TOP|wx.GROW)

            self.annotate = None
            self.reset()
        # __init__()

        def reset(self):
            for p in self.points:
                p.remove()

            self.points = []
            self.plotted_xy = None
            self.plotted_data = None
            self.kdtree = None # for fast lookup of nearest neighbour
            self.current_plotted_imgfs = []
            self.current_idx_mouse_on = None
            self.subplot.set_title("")
            self.remove_annotate()
            self.SetSize((self.Size[0],self.Size[1])) # Clear drawn plot
            #self.canvas.draw()
        # reset()

        def remove_annotate(self, refresh=True):
            if self.annotate is not None:
                #self.annotate.remove()
                #self.annotate = None
                self.annotate.set_visible(False)
                if refresh:
                    self.SetSize((self.Size[0],self.Size[1])) # Refresh drwan plot
        # remove_annotate()

        def canvas_onMouseMove(self, event):
            plotFrame = self.GetParent().GetParent()
            if None not in (event.xdata, event.ydata, self.plotted_xy):
                dist, idx = self.kdtree.query((event.xdata, event.ydata), k=1, p=1)
                x, y = self.plotted_xy[idx]
                imgf = os.path.basename(self.current_plotted_imgfs[idx])
                data = self.plotted_data[idx]
                mainframe = self.GetParent().GetParent().GetParent()
                scaninfo = plotFrame.find_data_by_filename(self.current_plotted_imgfs[idx]).scan_info
                vp, vs = scaninfo.vpoints, scaninfo.vstep
                hp, hs = scaninfo.hpoints, scaninfo.hstep
                dx, dy = abs(x-event.xdata), abs(y-event.ydata)
                if (vp==hp==1 and dx<.5 and dy<.5) or (vp==1 and dx < hs/2) or (hp==1 and dy < vs/2) or dx < hs/2 and dy < vs/2:
                    plotFrame.statusbar.SetStatusText("x= %.4f, y= %.4f, data= %.1f, file= %s" % (x, y, data, imgf))
                    self.current_idx_mouse_on = idx
                else:
                    plotFrame.statusbar.SetStatusText("")
                    self.current_idx_mouse_on = None
        # canvas_onMouseMove()

        def canvas_onMouseDown(self, event):
            # Sometimes 'button_press_event' does not seem to release mouse..
            # Does this fix a bug?
            if self.canvas.HasCapture():
                self.canvas.ReleaseMouse()

            idx = self.current_idx_mouse_on
            if idx is None:
                return

            plotFrame = self.GetParent().GetParent()
            mainFrame = plotFrame.GetParent()

            imgf = os.path.basename(self.current_plotted_imgfs[idx])
            print "Clicked:", imgf

            # Update main window
            mainFrame.grid.load(self.current_plotted_imgfs[idx])

            # Show scatter plot
            plotFrame.splotFrame.reset()

            f, kind = plotFrame.get_selected_f_kind()
            sel = filter(lambda x:os.path.basename(x[0])==imgf, plotFrame.data[f])
            if len(sel) == 0:
                return

            params = plotFrame.find_data_by_filename(self.current_plotted_imgfs[idx]).params
            res_outer = params.distl.res.outer

            plotFrame.splotFrame.plot(spots=sel[0][1].spots,
                                      mode=mainFrame.ctrlFrame.get_spot_draw_mode(),
                                      res_outer=res_outer,
                                      filename=self.current_plotted_imgfs[idx])
        # canvas_onMouseDown()

    # class PlotPanel

    def __init__(self, parent=None, id=wx.ID_ANY):
        wx.Frame.__init__(self, parent=parent, id=id, title="Plot",
                          size=(600,600))
        self.Bind(wx.EVT_CLOSE, lambda e: self.Hide()) # Don't destroy this frame when closed
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

        self.diffscan_manager = parent.diffscan_manager

        self.splitter = wx.SplitterWindow(self, id=wx.ID_ANY)
        self.splitter.SetSashGravity(1.0)
        self.plotPanel = self.PlotPanel(self.splitter)
        self.panel = panel = wx.Panel(self.splitter)
        self.splitter.SplitHorizontally(self.plotPanel, self.panel)
        self.splitter.SetSashPosition(500)

        vbox = wx.BoxSizer(wx.VERTICAL) # includes hbox and splotPanel

        hbox = wx.BoxSizer(wx.HORIZONTAL) # includes vbox11 and vbox12
        vbox.Add(hbox, 1, wx.EXPAND)

        vbox11 = wx.BoxSizer(wx.VERTICAL)
        vbox12 = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(vbox11, 1,flag=wx.EXPAND|wx.LEFT, border=4)
        hbox.Add(vbox12, 1,flag=wx.EXPAND|wx.LEFT, border=4)
        self.rb_kind, self.rb_file = [], []
        self.rb_kind.append(wx.RadioButton(panel, wx.ID_ANY, "total_integrated_signal", style=wx.RB_GROUP))
        self.rb_kind.append(wx.RadioButton(panel, wx.ID_ANY, "median_integrated_signal"))
        self.rb_kind.append(wx.RadioButton(panel, wx.ID_ANY, "n_spots"))
        self.rb_kind[-1].SetValue(True) # Set n_spot as default.
        for rb in self.rb_kind:
            vbox11.Add(rb)
            rb.Bind(wx.EVT_RADIOBUTTON, self.rb_clicked)

        self.CmbFile = wx.ComboBox(panel, wx.ID_ANY, size=(250,25), style=wx.CB_READONLY)
        vbox12.Add(self.CmbFile, 0, flag=wx.EXPAND|wx.LEFT)
        self.CmbFile.Bind(wx.EVT_COMBOBOX, self.rb_clicked)
        self.splotFrame = ScatterPlotFrame(self) # scatter plot (I vs d^-2)

        panel.SetSizer(vbox)

        self.data = collections.OrderedDict()

        self.statusbar = self.CreateStatusBar()
    # __init__()

    def find_data_by_filename(self, filename):
        # TODO probably inefficient way.
        # Better to find data in main frame?
        for fpref in self.data:
            fltr = filter(lambda s: s[0]==filename, self.data[fpref])
            if len(fltr) > 0:
                return fltr[0][1]
        return None
    # find_data_by_filename()

    def OnKeyUp(self,event):
        if event.ControlDown() and event.GetKeyCode() == ord("R"):
            self.splotFrame.Show()
            self.splotFrame.Raise()

    def rb_clicked(self, event):
        """
        Find selected radio button and make a plot.
        """

        f, kind = self.get_selected_f_kind()
        if None not in (f, kind):
            self.plot(f, kind)
        self.splitter.SizeWindows() # Fit plots
    # rb_clicked()

    def get_selected_f_kind(self):
        file_sel = self.CmbFile.GetValue()
        kind_sel = filter(lambda rb: rb.GetValue(), self.rb_kind)
        if file_sel != "" and len(kind_sel) > 0:
            f = file_sel
            kind = kind_sel[0].GetLabelText()
            return f, kind
        else:
            return None, None
    # get_selected_f_kind()

    def reset_cmb_file(self, append=False):
        current_f = None
        if append:
            current_f, kind = self.get_selected_f_kind()

        self.CmbFile.Clear()
        self.CmbFile.SetValue("")

        for i, k in enumerate(self.data):
            self.CmbFile.Append(k)
            if i == 0:
                self.CmbFile.Select(0)
            if current_f is not None and k == current_f:
                self.CmbFile.Select(self.CmbFile.GetCount()-1)
    #reset_cmb_file()


    def set_data(self, result, append=False):
        def find_changing_gonio_axis(gonios):
            if len(gonios) < 2:
                return [0]

            ret = [] # list of True/False
            for i in xrange(3):
                i_diff_max = max([g[i]-gonios[0][i] for g in gonios[1:]])
                if i_diff_max >= 1e-4:
                    ret.append(i)

            return ret
        # find_changing_gonio_axis()

        #changing_axis = find_changing_gonio_axis([stat.gonio for f,stat in result])
        #print "Changing=", changing_axis
        self.data = collections.OrderedDict()
        mainframe = self.GetParent()

        sorted_result = result.items()
        try:
            sorted_result.sort(key=lambda x:self.diffscan_manager.get_scan_info(x[0]).date)
        except:
            shikalog.warning("Can't sort result by date.")

        for f, stat in sorted_result:
            if os.path.dirname(f) != mainframe.ctrlFrame.current_target_dir:
                continue

            fpref = re_pref_num_ext.search(os.path.basename(f)).group(1)
            scaninfo = stat.scan_info
            if scaninfo is not None:
                if scaninfo.is_shutterless():
                    fpref += " (phi=%.2f)" % (scaninfo.fixed_spindle)
                else:
                    fpref += " (phi=%.2f)" % (scaninfo.osc_start)

            #self.data.setdefault(fpref, []).append((os.path.basename(f), stat))
            self.data.setdefault(fpref, []).append((f, stat))

        self.reset_cmb_file(append=append)
    # set_data()

    def annotate(self, imgf, lifetime=0):
        self.plotPanel.remove_annotate(refresh=False)

        if imgf not in self.plotPanel.current_plotted_imgfs:
            self.plotPanel.SetSize((self.plotPanel.Size[0], self.plotPanel.Size[1]))
            print "NON"
            return


        gc = self.find_data_by_filename(imgf)
        print "Annotating..", gc
        """
        # Round shape
        self.annotate = self.plotPanel.subplot.annotate(' ', xy=gc,  xycoords='data',
                                                        xytext=(35, 30), textcoords='offset points',
                                                        size=20, va="center",
                                                        bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec="none"),
                                                        arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                                                        fc=(1.0, 0.7, 0.7), ec="none",
                                                                        patchA=None,
                                                                        patchB=Ellipse((2, -1), 0.5, 0.5),
                                                                        relpos=(0.2, 0.5),
                                                                        )
                                                        )
        """
        if self.plotPanel.annotate is None:
            self.plotPanel.annotate = self.plotPanel.subplot.annotate('', xy=gc,  xycoords='data',
                                                                      xytext=(35, -30), textcoords='offset points',
                                                                      size=20, va="center",
                                                                      bbox=dict(boxstyle="round"),
                                                                      arrowprops=dict(arrowstyle="fancy",
                                                                                  fc=(1.0, 0.7, 0.7), ec=(0,0,0),
                                                                                      ),
                                                                      )
        else:
            self.plotPanel.annotate.xy = gc

        print dir(self.plotPanel.annotate)
        print self.plotPanel.annotate.get_window_extent()
        print self.plotPanel.annotate.clipbox
        print self.plotPanel.annotate.get_bbox_patch()

        bg = self.plotPanel.canvas.copy_from_bbox(self.plotPanel.figure.bbox)
        # How can we clear previous annotate? canvas.draw() is too slow!
        self.plotPanel.annotate.set_visible(True)
        print bg.get_extents()
        self.plotPanel.canvas.restore_region(bg)
        self.plotPanel.subplot.draw_artist(self.plotPanel.annotate)
        self.plotPanel.canvas.blit(self.plotPanel.subplot.bbox)


        if lifetime > 0:
            # Does not work!!
            endtimer = wx.Timer()
            endtimer.Bind(wx.EVT_TIMER, lambda e: self.annotate.remove())
            endtimer.Start(lifetime*1000, oneShot=True)
    # annotate()

    def plot(self, f, kind):
        def normalize(v, m=100., sd=60.):
            vm = float(sum(v))/float(len(v))
            vsd = math.sqrt(sum(map(lambda x:(x-vm)**2, v))/float(len(v)))
            if vsd < 1e-12:
                return [m for x in xrange(len(v))]
            return map(lambda x:sd*(x-vm)/vsd+m, v)
        # normalize()

        def normalize_max(v, maximum=400.):
            max_v = max(v)
            f = maximum / max_v if max_v > 0 else 1.
            return map(lambda x:f*x + 1., v) # add 1 to make zero-value pickable
        # normalize_max()

        if len(self.data) == 0:
            return

        ctrlframe = self.GetParent().ctrlFrame
        mode = ctrlframe.get_spot_draw_mode()

        if mode == "do not show spots":
            return

        # Clear plot
        self.plotPanel.reset()


        xs, ys, ds, imgfs = [], [], [], []
        zero_xs, zero_ys = [], [] # For values of zero
        for imgf, stat in self.data[f]:
            gc = stat.grid_coord
            if gc is None:
                shikalog.warning("gc is None! %s"%imgf)
                continue
            x, y = gc
            d = getattr(stat.spots, "get_"+kind)(mode, ctrlframe.exclude_resolution_ranges)
            xs.append(x)
            ys.append(y)
            ds.append(d)
            imgfs.append(imgf)

            if d == 0:
                zero_xs.append(x)
                zero_ys.append(y)

        if len(xs) == 0:
            return

        p1 = self.plotPanel.subplot.scatter(xs, ys, s=normalize_max(ds), c=ds, alpha=0.5)
        if max(ds) - min(ds) > 1e-5: # If all values equal (maybe), colorbar() will cause segmentation fault.
            cax = self.plotPanel.colorbar.ax if self.plotPanel.colorbar is not None else None
            self.plotPanel.colorbar = self.plotPanel.figure.colorbar(p1, cax=cax)

        p2 = self.plotPanel.subplot.scatter(zero_xs, zero_ys, s=50, marker="x", c=[0]*len(zero_xs), alpha=0.5)
        self.plotPanel.points = [p1, p2]

        self.plotPanel.subplot.set_xlabel("horizontal [mm]")
        self.plotPanel.subplot.set_ylabel("vertical [mm]")

        scaninfo = self.data[f][0][1].scan_info

        if scaninfo is not None:
            vp, hp = scaninfo.vpoints, scaninfo.hpoints
            vs, hs = scaninfo.vstep, scaninfo.hstep

            self.plotPanel.subplot.set_title("%d out of %d (h=%d,v=%d) processed" % (len(xs), vp*hp, hp, vp))

            if 1 in (vp, hp) or len(self.data[f]) <= hp:
                self.plotPanel.subplot.set_aspect("auto")
            else:
                self.plotPanel.subplot.set_aspect("equal")

            # Set limits
            if vp == hp == 1:
                self.plotPanel.subplot.set_xlim(-1, 1)
                self.plotPanel.subplot.set_ylim(-1, 1)
            elif vp == 1:
                self.plotPanel.subplot.set_xlim(-hs*hp/2 - hs, hs*hp/2 + hs)
                self.plotPanel.subplot.set_ylim(-1, 1)
            elif hp == 1:
                self.plotPanel.subplot.set_xlim(-1, 1)
                self.plotPanel.subplot.set_ylim(-vs*vp/2 - vs, vs*vp/2 + vs)
            else:
                self.plotPanel.subplot.set_xlim(-hs*hp/2 - hs, hs*hp/2 + hs)
                self.plotPanel.subplot.set_ylim(-vs*vp/2 - vs, vs*vp/2 + vs)
        else:
            # Should never reach here.. but should we set limit here?
            pass

        self.plotPanel.current_plotted_imgfs = imgfs
        self.plotPanel.plotted_xy = numpy.column_stack((xs, ys))
        self.plotPanel.kdtree = scipy.spatial.cKDTree(self.plotPanel.plotted_xy)
        self.plotPanel.plotted_data = ds
    # plot()
# class PlotFrame

class ImageSpotPanel(wx.Panel):
    def __init__(self, parent, size):
        wx.Panel.__init__(self, parent, size=size)
        self.parent = parent
        self.img = None
        self._imgin = None
        self._bitmap = None
        self.spots = None
        self._pos = None
        self._mag = None
        self.current_dmin, self.current_width = None, None
        self.Bind(wx.EVT_PAINT, self.Draw)
    # __init__()

    def set_image(self, imgin, posmag):
        #self._bitmap = wx.Bitmap(imgin) # This is very slow if many many images loaded!
        self._imgin = imgin
        self._pos = posmag[0:2]
        self._mag = posmag[2]
        self.Refresh()
    # set_image()

    def clear(self):
        self._imgin = None
        dc = wx.PaintDC(self)
        dc.Clear()
    # clear()

    def set_spots(self, spots):
        self.spots = spots
        self.Refresh()
    # set_spots()

    def Draw(self, ev):
        dc = wx.PaintDC(ev.GetEventObject())
        rect = self.GetClientRect()
        _bitmap = self._bitmap
        if _bitmap is None:
            if self._imgin is None:
                return
            elif os.path.isfile(self._imgin):
                _bitmap = wx.Bitmap(self._imgin)

        image = wx.MemoryDC()
        image.SelectObject(_bitmap)

        width, height = _bitmap.GetWidth(), _bitmap.GetHeight()
        if width > rect.width-2:
            width = rect.width-2
        if height > rect.height-2:
            height = rect.height-2

        draw_rect = wx.Rect(rect.x, rect.y, width, height)
        dc.Blit(draw_rect.x, draw_rect.y, draw_rect.width, draw_rect.height, image, 0, 0, wx.COPY, True)

        self.draw_spots(dc, draw_rect)
        self.draw_beamcenter(dc, draw_rect)
    # Draw()

    def draw_spots(self, dc, draw_rect):
        """
        draw_rect is the region of the diffraction image in the dc
        """
        if self.spots is None:
            return

        ctrlframe = self.parent.GetParent().GetParent().ctrlFrame
        mode = ctrlframe.get_spot_draw_mode()
        if mode == "do not show spots":
            return

        spots = self.spots.get_spots(mode, ctrlframe.exclude_resolution_ranges)

        dc.SetBrush(wx.Brush(wx.BLUE, wx.TRANSPARENT))
        dc.SetPen(wx.Pen("red"))
        w, h = 7, 7
        for spot in spots:
            x, y = spot.max_pxl_y(), spot.max_pxl_x() # XXX: care spot_convention!!
            x, y = draw_rect.x + (x - self._pos[0])*self._mag, draw_rect.y + (y - self._pos[1])*self._mag
            rect = (x-w, y-h, w*2+1, h*2+1)
            #if draw_rect.ContainsRect(rect):
            if draw_rect.Contains((x, y)):
                dc.DrawRectangleRect(rect)
    # draw_spots()

    def draw_beamcenter(self, dc, draw_rect):
        """
        Just add + mark on the center of image.
        NOTE that image is assumed to be centered on beam position!
        """
        l = 10
        w, h = draw_rect.width, draw_rect.height
        xc, yc = draw_rect.x + w/2, draw_rect.y + h/2
        dc.SetPen(wx.Pen("blue"))
        dc.DrawLine(xc - l, yc, xc + l, yc)
        dc.DrawLine(xc, yc - l, xc, yc + l)
    # draw_beamcenter()
# class ImageSpotPanel

class ImageResultPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.r2d = None # to be a function

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vbox)

        self.view1 = wx.html.HtmlWindow(self, style=wx.NO_BORDER, size=(600,90))
        self.view1.SetStandardFonts()

        self.panel1 = wx.Panel(self, size=(600, 10))
        panel1_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.panel1.SetSizer(panel1_hbox)
        self.dtxt = wx.StaticText(self.panel1, size=(200, 10))
        self.lbtn = wx.Button(self.panel1, wx.ID_ANY, "<")
        self.rbtn = wx.Button(self.panel1, wx.ID_ANY, ">")
        panel1_hbox.Add(self.dtxt, 1)
        panel1_hbox.Add(self.lbtn, 0, flag=wx.EXPAND|wx.ALIGN_RIGHT)
        panel1_hbox.Add(self.rbtn, 0, flag=wx.EXPAND|wx.ALIGN_RIGHT)

        self.panel2 = ImageSpotPanel(self, size=(600,600))

        self.view3 = wx.html.HtmlWindow(self, style=wx.NO_BORDER, size=(600,200))
        self.view3.SetStandardFonts()

        self.vbox.Add(self.view1, 1, flag=wx.EXPAND)
        self.vbox.Add(self.panel1, 0, flag=wx.EXPAND)
        self.vbox.Add(self.panel2, 0, flag=wx.EXPAND)
        self.vbox.Add(self.view3, 1, flag=wx.EXPAND)
        self.clear()

        self.lbtn.Bind(wx.EVT_BUTTON, lambda e: self.Scroll(+1))
        self.rbtn.Bind(wx.EVT_BUTTON, lambda e: self.Scroll(-1))
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.panel2.Bind(wx.EVT_MOTION, self.onMouseMoveInImage)
        self.panel2.Bind(wx.EVT_LEAVE_WINDOW, lambda e: self.dtxt.SetLabel(""))
    # __init__()

    def Scroll(self, inc):
        mainframe = self.GetParent().GetParent()
        if self.current_img_file is None or len(mainframe.data) < 2:
            return

        data = mainframe.data.keys()

        if self.current_img_file not in data:
            return

        idx = data.index(self.current_img_file)

        if 0<= idx + inc < len(data):
            self.load(data[idx+inc])
    # Scroll()

    def OnKeyUp(self, event):
        keycode = event.GetKeyCode()
        if keycode in (wx.WXK_UP, wx.WXK_DOWN):
            inc = -1 if keycode==wx.WXK_UP else 1
            self.Scroll(inc)
    # OnKeyUp()

    def clear(self):
        self.view3.SetPage("<b>Scan info</b><br><br>No scan selected.")
        self.view1.SetPage("<b>Image info</b><br><br>No image selected.")
        self.panel2.clear()
        self.current_img_file = None
    # clear()

    def update(self):
        mainframe = self.GetParent().GetParent()

        img_file = self.current_img_file
        if img_file is None:
            return

        if img_file in mainframe.data:
            item = mainframe.data[img_file]
            spot_mode = self.parent.GetParent().ctrlFrame.get_spot_draw_mode()
            if spot_mode == "do not show spots":
                return

            self.panel2.set_spots(item.stat.spots)
            self.show_image_info(os.path.basename(item.img_file), item.stat.spots, spot_mode)
            scaninfo = item.stat.scan_info
            self.prepare_resolution_calc(item.stat.params, scaninfo)
    # update()

    def load(self, img_file):
        mainframe = self.GetParent().GetParent()
        #mainframe.plotFrame.annotate(img_file) # Currently, not works well.

        self.current_img_file = img_file
        imgf = os.path.basename(img_file)
        if img_file in mainframe.data:
            item = mainframe.data[img_file]

            spot_mode = mainframe.ctrlFrame.get_spot_draw_mode()
            if spot_mode == "do not show spots":
                return

            self.panel2.set_spots(item.stat.spots)
            params = item.stat.params
            img_pics = filter(lambda f: os.path.exists(f),
                              [os.path.join(params.work_dir, os.path.basename(item.img_file)+ext) for ext in (".jpg",".png")])
            if len(img_pics) > 0:
                self.show_image(img_pics[0], item.stat.thumb_posmag)
            else:
                shikalog.warning("Image for display is not found: %s" % item.img_file)
            self.show_image_info(os.path.basename(item.img_file), item.stat.spots, spot_mode)

            scaninfo = item.stat.scan_info
            self.show_scan_info(scaninfo)
            self.prepare_resolution_calc(params, scaninfo)
        else:
            shikalog.error("Not found: " + img_file)

    # load()

    def refresh_image(self):
        self.panel2.Refresh()
    # refresh_image()

    def show_image(self, imgpic, thumb_posmag):
        self.panel2.set_image(imgpic, thumb_posmag)
    # show_image()

    def show_scan_info(self, info):
        html = "<b>Scan info</b><br>"  #"<h3>Scan info</h3>"
        html += "<table>\n"
        html += '<tr align="left"><th>scan</th><td>%s</td>\n' % info.filename_template
        html += '<th>date</th><td>%s</td></tr>\n' % (info.date.strftime("%Y/%m/%d %H:%M:%S") if info.date!=0 else "??")

        if info.is_shutterless():
            html += '    <tr align="left"><th>fixed spindle</th><td>%.2f&deg;</td>\n' % info.fixed_spindle
            html += '                     <th>frame rate</th><td>%.2f [Hz]</td></tr>\n' % info.frame_rate
        else:
            html += '    <tr align="left"><th>osc. start</th><td>%.2f&deg;</td>\n' % info.osc_start
            html += '                     <th>osc. step</th><td>%.2f&deg;</td></tr>\n' % info.osc_step
            html += '    <tr align="left"><th>exp. time</th><td>%.2f [sec]</td></tr>\n' % info.exp_time

        html += '    <tr align="left"><th>beam size</th><td>h= %.1f, v= %.1f [um]</td>\n' % (info.beam_hsize, info.beam_vsize)
        html += '                     <th>attenuator</th><td>%s %.1f [um]</td></tr>\n' % info.attenuator
        html += '    <tr align="left"><th>distance</th><td>%.2f [mm]</td>\n' % info.distance
        html += '                     <th>wavelength</th><td>%.4f [A]</td></tr>\n' % info.wavelength
        html += '    <tr align="left"><th>scan points</th><td>v=%d, h=%d</td>\n' % (info.vpoints, info.hpoints)
        html += '                     <th>scan steps</th><td>v=%.2f, h=%.2f [um]</td></tr>\n' % (info.vstep*1000., info.hstep*1000.)

        html += '  </table>\n'

        self.view3.SetPage(html)
    # show_scan_info()

    def show_image_info(self, filename, spots, spot_mode):
        med_sig = spots.get_median_integrated_signal(spot_mode)
        total_sig = spots.get_total_integrated_signal(spot_mode)
        n_spots = spots.get_n_spots(spot_mode)

        color = "black" if spot_mode in spots.keys() else "red"

        self.view1.SetPage("""\
<b>Image info</b><br>
<table>
<tr align="left"><th>File name</th><td>%(filename)s</td></tr>
<tr align="left"><th>Total integrated signal</th><td><font color="%(col)s">%(total_sig).1f</font></td></tr>
<tr align="left"><th>Median integrated signal</th><td><font color="%(col)s">%(med_sig).1f</font></td></tr>
<tr align="left"><th>N_spots</th><td><font color="%(col)s">%(n_spots)d</font></td></tr>
</table>
""" % dict(filename=filename, total_sig=total_sig, med_sig=med_sig, n_spots=n_spots, col=color))
    # show_image_info()

    def prepare_resolution_calc(self, params, scaninfo):
        """
        TODO:
        Currently, wavelength and distance are obtained from scaninfo.
        Probably they should be obtained from image header? or should be in params!
        """

        self.r2d = None
        dmin = params.distl.res.outer
        if dmin is None:
            return # FIXME! params.distl.res.outer should be always set?

        wavelen = scaninfo.wavelength
        distance = scaninfo.distance

        # conversion factor (pixel -> mm)
        f = 2. * distance / 600. * math.tan(2. * math.asin(wavelen/2./dmin))
        self.r2d = lambda r: wavelen / 2. / math.sin(.5 * math.atan2(f*r,distance))
    # prepare_resolution_calc()

    def onMouseMoveInImage(self, ev):
        width, height = 600, 600
        self.dtxt.SetLabel("")

        if self.r2d is None:
            return

        pt = ev.GetPosition()
        rect = self.panel2.GetClientRect()
        draw_rect = wx.Rect(rect.x, rect.y, width, height)

        if not draw_rect.Contains(pt):
            # Outside
            return

        # beam center
        xc, yc = draw_rect.x + width/2, draw_rect.y + height/2

        # resolution
        r = math.sqrt((pt.x - xc)**2 + (pt.y - yc)**2)
        d = self.r2d(r) if r > 1e-6 else float("inf")
        self.dtxt.SetLabel("d= %6.2f A" % d)
    # onMouseMoveInImage()
# class ImageResultPanel

class MainFrame(wx.Frame):
    class Item:
        def __init__(self, img_file):
            self.img_file = img_file # file name (absolute path)
            self.stat = None # distl_stat
    # class Item

    def __init__(self, parent=None, id=wx.ID_ANY, img_files=[], dsmanager=None, topdir=None, params=None):
        wx.Frame.__init__(self, parent=parent, id=id, title="SHIKA system",
                          size=(1110,950))
        self.diffscan_manager = dsmanager
        if self.diffscan_manager is None:
            self.diffscan_manager = DiffScanManager()

        self.adxv_proc = None # subprocess object
        self.adxv_port = 8100 # adxv's default port. overridden later.
        self.adxv_bin = params.adxv
        self.kuma_addr = params.kuma_addr
        self.imgview_host = params.imgview_host

        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.splitter = wx.SplitterWindow(self, id=wx.ID_ANY)
        self.ctrlFrame = ControlPanel(self, parent=self.splitter, params=params)

        self.grid = ImageResultPanel(self.splitter)
        self.splitter.SplitVertically(self.ctrlFrame, self.grid)
        self.splitter.SetSashPosition(500)

        self.topdir = topdir

        self.data = collections.OrderedDict() # Data shown in grid

        self.plotFrame = PlotFrame(self)

        self.html_maker_thread = ReportHTMLMakerThread(self)
        self.html_maker_thread.start()

        if self.topdir is not None:
            self.ctrlFrame.txtTopDir.SetValue(self.topdir)
            root = self.ctrlFrame.treectrl.AddRoot(self.topdir, image=0)
            self.ctrlFrame.treectrl.SetPyData(root, ".")
            self.ctrlFrame.dic_for_tree[()] = root
            wx.PostEvent(self.ctrlFrame, EventTargetDirChanged(target=self.topdir))
        elif len(self.diffscan_manager.scanlog) > 0:
            target_dir = self.diffscan_manager.scanlog.keys()[0]
            topdir = os.path.abspath(os.path.join(target_dir, ".."))
            self.ctrlFrame.txtTopDir.SetValue(topdir)
            self.ctrlFrame.onTargetDirChanged(EventTargetDirChanged(target=target_dir),
                                              need_load=(len(img_files)==0)) # You can't post event. it's delayed!

        for img_file in img_files:
            item = self.Item(img_file)
            self.data[img_file] = item

        self.ctrlFrame.cmbTargetDir.SetEditable(False) # This is a current limitation.

        self.grid.panel2.Bind(wx.EVT_LEFT_DCLICK, self.grid_OnDbClick)
        self.grid.panel2.Bind(wx.EVT_RIGHT_DOWN, self.grid_OnRightClick)

        self.Show()

    # __init__()

    def open_img_with_adxv(self, imgfile):
        """
        Start adxv and show image.
        If already started, just update image shown.
        There are maybe two ways to do this.
        1; use -autoload option and update a temporary file. (need two seconds to refresh)
        2; use -socket 8100 option and communicate ('load_image hoge.img').
        Which is better?
        """
        if self.adxv_bin is not None:
            adxv_comm = self.adxv_bin + " -socket %d"
        else:
            adxv_comm = "adxv -socket %d"

        if self.adxv_proc is None or self.adxv_proc.poll() is not None: # None means still running.
            # find available port number
            sock_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_test.bind(("localhost", 0))
            self.adxv_port = sock_test.getsockname()[1]
            sock_test.close()
            # start adxv
            self.adxv_proc = subprocess.Popen(adxv_comm%self.adxv_port, shell=True,
                                              cwd=os.path.dirname(imgfile))

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        for i in xrange(4): # try for 2 seconds.
            try:
                sock.connect(("localhost", self.adxv_port))
                break
            except socket.error:
                time.sleep(.5)
                continue

        sent = sock.send("load_image %s"%imgfile)
        shikalog.debug("adxv loading %s"%imgfile)
        if sent == 0:
            shikalog.error("adxv load failed! Close adxv and double-click again.")

        sock.close()
    # open_img_with_adxv

    def open_in_imgview(self, imgfile):
        if self.imgview_host is None:
            shikalog.error("imgview host is not configured!")
            return
        print "Trying",self.imgview_host, 5555

        import telnetlib
        telnet = telnetlib.Telnet(self.imgview_host, 5555)
        telnet.write("put/video_file/%s\n"%imgfile)
        #print "READ=", telnet.read_all()
        recv = telnet.read_until("/ok", timeout=3)
        if recv == "":
            print "ERROR: imgview not responding!"
            telnet.close()
            return
        #print "READ=", telnet.read_very_eager()
        telnet.write("put/video/disconnect\n")
        print "DONE."
        telnet.close()
        return

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3.)
        sock.connect((self.imgview_host, 5555))

        try:
            sock.sendall("put/video_file/%s\n"%imgfile)
        except:
            print "ERROR: imgview load failed!"
            sock.close()
            return

        time.sleep(1)
        recv = sock.recv(4096)
        print "recv=", recv

        sock.send("put/video/disconnect\n")
        sock.close()

    # open_in_imgview()

    def onClose(self, event):
        #self.ctrlFrame.dir_watcher.stop()
        #self.ctrlFrame.scanlog_watcher.stop()
        self.Destroy()
    # onClose()

    def grid_OnDbClick(self, event):
        """
        Start adxv
        """

        img_file = self.grid.current_img_file
        if img_file is None:
            print "No image"
            return

        self.open_img_with_adxv(img_file)
    # grid_OnDbClick()

    def grid_OnRightClick(self, event):
        img_file = self.grid.current_img_file
        if img_file is None:
            shikalog.error("No image")
            return

        #fltr = filter(lambda x: x.img_file == img_file, self.data)
        #if fltr != 1:
        #    shikalog.warning("Not found in data? %s"%img_file)

        with self.ctrlFrame.dir_watcher.lock: # FIXME need to add useful function to find gonio coords!
            gonio_xyz_phi = self.diffscan_manager.get_gonio_xyz_phi(img_file)

        shikalog.info("file, gonio= %s, %s" % (img_file, gonio_xyz_phi))

        if gonio_xyz_phi is None:
            shikalog.warning("gonio xyz and phi is unavailable for %s." % img_file)
        if None in gonio_xyz_phi:
            shikalog.warning("None in gonio xyz or phi")

        if self.kuma_addr is None:
            shikalog.warning("KUMA address (host and port) is not set.")

        menu = wx.Menu()
        menu.Append(0, os.path.basename(img_file))
        menu.Enable(0, False)
        menu.AppendSeparator()
        menu.Append(1, "Let KUMA know")
        menu.Enable(1, None not in (gonio_xyz_phi, self.kuma_addr))
        menu.Append(2, "Let KUMA know (quick)")
        menu.Enable(2, None not in (gonio_xyz_phi, self.kuma_addr))
        menu.Append(3, "Open with adxv")
        menu.Append(4, "Open in imgview")
        menu.Enable(4, self.imgview_host is not None)

        self.Bind(wx.EVT_MENU, lambda e: self.tell_kuma(gonio_xyz_phi, os.path.splitext(os.path.basename(img_file))[0]), id=1)
        self.Bind(wx.EVT_MENU, lambda e: self.tell_kuma(gonio_xyz_phi, os.path.splitext(os.path.basename(img_file))[0], False), id=2)
        self.Bind(wx.EVT_MENU, lambda e: self.open_img_with_adxv(img_file), id=3)
        self.Bind(wx.EVT_MENU, lambda e: self.open_in_imgview(img_file), id=4)
        self.PopupMenu(menu)
        menu.Destroy()

    # grid_OnRightClick()

    def tell_kuma(self, gonio_xyz_phi, comment, with_dialog=True):
        class Dlg(wx.Dialog):
            def __init__(self, parent, gonio_xyz_phi, comment, func):
                wx.Dialog.__init__(self, parent, wx.ID_ANY, "KUMA communicator", size=(250, 100))

                self.gonio_xyz_phi = gonio_xyz_phi
                self.func = func

                vbox = wx.BoxSizer(wx.VERTICAL)
                self.txtComment = wx.TextCtrl(self, wx.ID_ANY, comment, (95, 105))
                hbox = wx.BoxSizer(wx.HORIZONTAL)
                btnOK = wx.Button(self, wx.ID_ANY, 'OK', size=(70, 30))
                btnCancel = wx.Button(self, wx.ID_ANY, 'Cancel', size=(70, 30))
                hbox.Add(btnOK, 1)
                hbox.Add(btnCancel, 1, wx.LEFT, 5)

                vbox.Add(wx.StaticText(self, wx.ID_ANY, "Comment:"))
                vbox.Add(self.txtComment, 1, wx.GROW|wx.LEFT)
                vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
                self.SetSizer(vbox)

                self.txtComment.SetFocus()

                btnOK.Bind(wx.EVT_BUTTON, self.btnOK_click)
                btnCancel.Bind(wx.EVT_BUTTON, lambda e: self.Destroy())
            # __init__()
            def btnOK_click(self, event):
                try:
                    self.func(self.gonio_xyz_phi, self.txtComment.GetValue(), False)
                finally:
                    self.Destroy()
            # btnOK_click()
        # class Dlg

        if None in gonio_xyz_phi or gonio_xyz_phi is None:
            wx.MessageDialog(None, "Invalid gonio coordinate or phi",
                             "Error", style=wx.OK).ShowModal()
            return


        if with_dialog:
            dlg = Dlg(self, gonio_xyz_phi, comment, self.tell_kuma) # XXX Make sure this function is not called recursively!
            dlg.ShowModal()
            return

        #s = xmlrpclib.ServerProxy('http://192.168.163.2:1920')
        try:
            s = xmlrpclib.ServerProxy('http://%s'%self.kuma_addr)
            s.append_coords(gonio_xyz_phi, comment)
        except socket.error, e:
            shikalog.error("""\
Cannot communicate with KUMA: %s
       - Is KUMA up?
       - Is this address (%s) correct?
""" % (e, self.kuma_addr))
        print gonio_xyz_phi, comment
    # tell_kuma()

    def update_result(self, append=False):
        with self.ctrlFrame.dir_watcher.lock: # really needed?
            result = self.diffscan_manager.stats

            for f, stat in result.items():
                if f in self.data:
                    self.data[f].stat = stat

            self.plotFrame.set_data(result, append=append)

        self.ctrlFrame.set_spot_draw_mode("hi_pass_resolution_spots")
        self.ctrlFrame.rb_clicked(None, call_from_runbutton=True, append=append) # this calls plotFrame.rb_clicked()

        if self.ctrlFrame.chkTrackLatest.GetValue():
            self.track_latest_result()

        self.save_results(rotate=not append)

        with self.html_maker_thread.lock:
            self.html_maker_thread.queue.append((os.path.join(self.ctrlFrame.current_target_dir, "_spotfinder"),
                                                 not append))
        if not self.html_maker_thread.is_running():
            shikalog.debug("html_maker_thread was accidentally stopped. restarting.")
            self.html_maker_thread.start()
    # update_result()

    def save_results(self, rotate=False):
        pklout = os.path.join(self.ctrlFrame.current_target_dir, "_spotfinder", "result.pkl")
        if rotate:
            rotate_file(pklout)

        startt = time.time()
        with self.ctrlFrame.dir_watcher.lock:
            pickle.dump(self.diffscan_manager.stats, open(pklout, "wb"), 2)
        delt = time.time() - startt
        shikalog.info("Saved pickled data: %s (took %f sec)" % (pklout, delt))
    #  save_results(self)

    def load_results(self):
        with self.ctrlFrame.dir_watcher.lock:
            self.diffscan_manager.stats.clear() # This is important. If images in several directories exist, "Update Result" will fail. FIXME.

            if self.ctrlFrame.current_target_dir is None:
                return

            pklin = os.path.join(self.ctrlFrame.current_target_dir, "_spotfinder", "result.pkl")
            if os.path.isfile(pklin):
                shikalog.info("Loading pickled data: %s" % pklin)
                result = pickle.load(open(pklin, "rb")).items() # Convert OrderedDict -> [(key,val), ..]

                self.diffscan_manager.update_scanlogs()
                # for backward compatibility
                if len(result) > 0 and getattr(result[0][1], "scan_info", None) is None:
                    shikalog.info("Old type pickled data loaded: %s" % pklin)
                    for f, stat in result:
                        stat.scan_info = self.diffscan_manager.get_scan_info(f)
                        stat.grid_coord = self.diffscan_manager.get_grid_coord(f)

                self.diffscan_manager.add_results(result)
                self.ctrlFrame.onResultsUpdated(EventResultsUpdated(result=result))
                self.ctrlFrame.on_result_update_timer(None)
    # load_results()

    def track_latest_result(self):
        if self.plotFrame.CmbFile.GetCount() > 0:
            self.plotFrame.CmbFile.Select(self.plotFrame.CmbFile.GetCount()-1)
            self.plotFrame.rb_clicked(None)
    # track_latest_result()
# class MainFrame

if __name__ == "__main__":
    cmdline = iotbx.phil.process_command_line(args=sys.argv[1:],
                                              master_string=gui_phil_str)
    params = cmdline.work.extract()
    args = cmdline.remaining_args

    shikalog.config(params.bl)
    shikalog.info("Program started in %s." % os.getcwd())

    img_files = []
    logfile = None
    topdir = None
    re_addr = re.compile("^[0-9]{,3}\.[0-9]{,3}\.[0-9]{,3}\.[0-9]{,3}:[0-9]+$")
    re_host = re.compile("^[0-9]{,3}\.[0-9]{,3}\.[0-9]{,3}\.[0-9]{,3}$")

    for arg in args:
        if arg.endswith((".img", ".cbf")):
            img_files.append(os.path.abspath(arg))
        elif arg.endswith(".log"):
            logfile = os.path.abspath(arg)
        elif os.path.isdir(arg):
            topdir = os.path.abspath(arg)
        elif not os.path.exists(arg):
            shikalog.error("Given path does not exist: %s" % arg)
            quit()

    if params.force_ssh_from is not None:
        shikalog.info("SSH_CONNECTION= %s" % os.environ.get("SSH_CONNECTION", ""))
        if "SSH_CONNECTION" not in os.environ:
            print
            print "ERROR!! Cannot get host information! SHIKA cannot start."
            print "Please contact staff. Need to use ssh or change parameter."
            print
            quit()
        if os.environ["SSH_CONNECTION"].split()[0] != params.force_ssh_from:
            print
            print "ERROR!! Your host is not allowed! SHIKA cannot start here."
            print "Please contact staff. Need to access from the allowed host."
            print
            quit()

    if params.kuma_addr is not None:
        if not re_addr.search(params.kuma_addr):
            shikalog.error("Invalid address definition of KUMA: %s" % params.kuma_addr)
            quit()
        print "Config: KUMA addr=", params.kuma_addr

    if params.imgview_host is not None:
        if not re_host.search(params.imgview_host):
            shikalog.error("Invalid host definition of Imgview: %s" % params.imgview_host)
            quit()

        shikalog.info("Config: imgview host= %s" % params.imgview_host)

    print """\

SHIKA (Spot wo Hirotte Ichi wo Kimeru Application) is a spot finder application for diffraction based crystal centering based on distl by Nick Sauter et al.
This is an alpha-version. If you found something wrong, please let staff know! We would appreciate your feedback.

"""

    if logfile is None and topdir is None and len(img_files) == 0:
        print """\
* SHIKA Usage *
Case 1: all images exist."
        shika /where-images-exist/*.img"
        and push 'Update result' button."
Case 2: diffraction scan is running. "
        shika /where-images-are-being-written/diffscan.log"
        and click 'Watch this directory' check box."
Case 3: Just started experiment. Want to watch all subdirectories."
        shika /top_dir"
        and select subdirectory or click 'Autofind' checkbox.
"""
        sys.exit(1)

    dirnames = list(set(map(lambda x:os.path.dirname(x), img_files)))

    if len(dirnames) > 1:
        print "Sorry, currently images in more than one directory cannot be handled."
        print "Your images are in following directories:"
        for d in dirnames:
            print "  %s" % d
        sys.exit(1)

    if len(img_files) > 0 and logfile is None:
        logfile = os.path.join(dirnames[0], "diffscan.log")
        print "Guessing diffscan.log...", logfile

    if logfile is not None and not os.path.isfile(logfile):
        shikalog.error("diffscan.log does not exist or not found!")
        sys.exit(1)

    if topdir is not None and (logfile is not None or len(img_files) > 0):
        shikalog.error("You can specify either directory name or img files/diffscan.log. Not both.")
        sys.exit(1)

    dsm = DiffScanManager()
    if logfile is not None:
        dsm.add_scanlog(logfile)

    app = wx.App()
    app.TopWindow = MainFrame(parent=None, id=wx.ID_ANY, img_files=img_files,
                              dsmanager=dsm, topdir=topdir,
                              params=params)
    app.MainLoop()

    shikalog.info("Normal exit.")

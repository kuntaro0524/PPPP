from SimpleXMLRPCServer import SimpleXMLRPCServer
import os
import shutil
import glob
import wx
import re
import socket
import time
import threading
import pexpect
import subprocess

#from hiratalib.Gonio import Gonio
#from hiratalib.Capture import Capture
#from hiratalib.Motor import Motor
#from hiratalib.Zoom import Zoom
#from hiratalib.CoaxPint import CoaxPint
import inocclog

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

if __name__ == "__main__":
        self.camera_inf = read_camera_inf(os.path.join(os.environ["BLCONFIG"], "video", "camera.inf"))
        self.bss_config = read_bss_config(os.path.join(os.environ["BLCONFIG"], "bss", "bss.config"))

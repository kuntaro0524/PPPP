import sys,os,math,numpy,socket,time
import re
sys.path.append("/data/04.Prog/150611-CoCCO/Libs")
from Gonio import *
from Capture import *

############ settings
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

def read_bss_config(cfgin):
        ret = {}
        for l in open(cfgin):
                if "#" in l: l = l[:l.index("#")]
                if "Microscope_Zoom_Options:" in l:
                        ret["zoom_pulses"] = map(int, l[l.index(":")+1:].split())
        return ret

if __name__ == "__main__":
	camera_inf = read_camera_inf(os.path.join(os.environ["BLCONFIG"], "video", "camera.inf"))
	bss_config = read_bss_config(os.path.join(os.environ["BLCONFIG"], "bss", "bss.config"))
	coax_pulse2zoom = dict(zip(bss_config["zoom_pulses"], camera_inf["zoom_opts"]))
	coax_zoom2pulse = dict(zip(camera_inf["zoom_opts"], bss_config["zoom_pulses"]))
	coax_zoom2oshift = dict(zip(camera_inf["zoom_opts"], camera_inf["origin_shift"]))
	coax_zpulse2pint = {0:19985, -16000:19980, -32000:19974, -48000:20024} # zoom pulse to pint pulse

	print coax_pulse2zoom
	print coax_zoom2pulse
	print coax_zoom2oshift
	print coax_zpulse2pint

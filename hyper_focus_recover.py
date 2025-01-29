import sys,os,math,numpy
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")

import Device
import MyDate

mydate = MyDate.MyDate()

date_str = mydate.getNowMyFormat()

dev = Device.Device("172.24.242.41")
dev.init()

# AxesInfo .data is input file
axesinfo = sys.argv[1]

lines = open(axesinfo,"r").readlines()
ofile = open("recover_from_hyper_%s.log" % date_str, "w")

time_str = mydate.getToday()
ofile.write("Recover from %s at %s \n" % (axesinfo, time_str))

for line in lines:
    if line.rfind("Stage-y") != -1:
        print "Now stage-y"
        recover_pulse = int(line.split()[2])
        curr_pulse = dev.stage.getY()
        ofile.write("Recovering stage-y from %d to %d\n" % (curr_pulse, recover_pulse))
        dev.stage.moveY(recover_pulse)
        curr_pulse = dev.stage.getY()
        ofile.write("Recovered stage-y %d\n" % (curr_pulse))
    if line.rfind("Stage-z") != -1:
        print "Now stage-z"
        recover_pulse = int(line.split()[2])
        curr_pulse = dev.stage.getZ()
        ofile.write("Recovering stage-z from %d to %d\n" % (curr_pulse, recover_pulse))
        dev.stage.moveZ(recover_pulse)
        curr_pulse = dev.stage.getZ()
        ofile.write("Recovered stage-z: %d\n" % (curr_pulse))
    if line.rfind("VFM-ty") != -1:
        print "Now VFM-ty"
        print(line)
        recover_pulse = int(line.split()[2])
        curr_pulse = dev.mirror.getVFMin()
        ofile.write("Recovering VFM-ty from %d to %d\n" % (curr_pulse, recover_pulse))
        dev.mirror.setVFMin(recover_pulse)
        curr_pulse = dev.mirror.getVFMin()
        ofile.write("Recovered VFM-ty: %d\n" % (curr_pulse))
    if line.rfind("HFM-tz") != -1:
        print "Now HFM-tz"
        recover_pulse = int(line.split()[2])
        curr_pulse = dev.mirror.getHFMin()
        ofile.write("Recovering HFM-tz from %d to %d\n" % (curr_pulse, recover_pulse))
        dev.mirror.setHFMin(recover_pulse)
        curr_pulse = dev.mirror.getHFMin()
        ofile.write("Recovered HFM-tz: %d \n" % (curr_pulse))
    if line.rfind("VFM-z") != -1:
        print "Now VFM-z"
        recover_pulse = int(line.split()[2])
        curr_pulse = dev.mirror.getVFM_z()
        ofile.write("Recovering VFM-z from %d to %d\n" % (curr_pulse, recover_pulse))
        dev.mirror.setVFM_z(recover_pulse)
        curr_pulse = dev.mirror.getVFM_z()
        ofile.write("Recovered HFM-tz: %d \n" % (curr_pulse))

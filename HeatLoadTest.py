import sys,os,math,cv2,socket,time,copy,datetime
from MBS import *
from ID import *
from FES import *


if __name__=="__main__":
    host = '172.24.242.41'
    port = 10101
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))

    id=ID(s)
    mbs=MBS(s)
    fes=FES(s)

    gap=id.getGap()
    fesv,fesh=fes.getApert()
    print datetime.datetime.now().strftime("Start time; %H:%M:%S")
    print gap, fesv, fesh

    # Gap change to 7.4
    print "Gap change to 7.4"
    gap=7.4
    id.moveTillMove(gap,wait_interval=5,ntrial=10)

    # MBS close
    print "MBS Close"
    mbs.close()

    gap=id.getGap()
    fesv,fesh=fes.getApert()

    print gap, fesv, fesh

    # wait 10 min
    print datetime.datetime.now().strftime("wait start-01 %H:%M:%S")
    time.sleep(600)
    print datetime.datetime.now().strftime("%H:%M:%S")

    # set FES apert to 0.5 x 0.5mm
    print "set FES apert to 0.5 x 0.5mm"
    fes.setApert(0.5,0.5)
    # MBS open
    print "MBS Open"
    mbs.openTillOpen(wait_interval=5,ntrial=10)

    gap=id.getGap()
    fesv,fesh=fes.getApert()
    print gap, fesv, fesh

    print datetime.datetime.now().strftime("wait start-02 %H:%M:%S")
    # wait 20 min
    time.sleep(1200)
    print datetime.datetime.now().strftime("Finish time; %H:%M:%S")

    # Recover to Normal Conditions
    energy=12.3984
    fes.setApert(0.34,0.3)
    id.moveE(energy)
    print datetime.datetime.now().strftime("recovered at %H:%M:%S")
    gap=id.getGap()
    fesv,fesh=fes.getApert()
    print gap, fesv, fesh


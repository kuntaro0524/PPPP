from ScheduleBSS import *

if __name__=="__main__":
        t=ScheduleBSS()
        adstep=0.0

        startphi=0.0
        stepphi=1.0
        interval=1

        print "DIR THICKNESS cenX cenY cenZ"
        cenpos=(float(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5]))

        for i in range(0,5):
                t.setDir(sys.argv[1])
                t.setCameraLength(120)
                t.setAttThickness(600)
                t.stepAdvanced(svec,evec,adstep,1,startphi,stepphi,interval)
                t.setDataName("low_%02d"%i)
                t.make("tmp1%02d.sch"%i)


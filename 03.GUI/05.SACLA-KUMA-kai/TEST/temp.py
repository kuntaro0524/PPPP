        #class Schedule_HS_Re:
        t=Schedule_HS_Re()

        #Data directory
        outdir="/tmp/data/"
        wavelength=1.0 # Angstrom
        cameralength=200.0 #mm
        prefix="cco_demo"

        # Serial offset
        start_frame_number=10
        serial_offset=start_frame_number-1

        # N points
        npoints=12

        # Advector
        svec=array([0,0,0])
        evec=array([1,1,1])

        # Start PHI
        startphi=0.0
        stepphi=0.1
        endphi=startphi+float(npoints)*stepphi

        # Step length along this vector
        step=15.0
        adstep=step/cos(radians(startphi))
        print "A step=",adstep

        ################################
        # Setting parameters to 
        ################################
        # Static parameters
        t.setDir(outdir)
        t.setWL(1.0)
        t.setDataName(prefix)
        t.setCameraLength(cameralength)
        t.setOffset(serial_offset)
        t.setExpTime(1.0)
        t.setRotationCondition(startphi,endphi,stepphi)
        t.setAttIdx(0)
        t.setScanInt(1)
        t.sfrox(svec,evec,startphi,stepphi,npoints,adstep)

        t.make("./test.sch")


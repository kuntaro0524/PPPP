import sys, os, math
import datetime, time

class AnaBSSlog():
    def __init__(self, logdir="/isilon/BL32XU/BLsoft/PPPP/10.Zoo/ZooConfig/log/"):
        self.logdir=logdir
        self.now = datetime.datetime.now()
        self.strs = []
        self.isRead = False

        # number of raster scan
        self.n_raster = 0
        self.n_raster_images = 0
        self.n_datasets = 0

    def setDate(self, year, month, date):
        timstr = "%04d%02d%02d" % (year, month, date)
        self.now = datetime.datetime.strptime(timstr, '%Y%m%d')
        self.logname = self.now.strftime("bss_%Y%m%d.log")
        print self.logname

    def setLogFile(self, logname):
        self.logname = logname

    def readLogFile(self):
        self.logname = os.path.join(self.logdir, self.logname)
        #self.logname = "%s/%s" % (self.logdir, self.logname)
        self.loglines = open(self.logname, "r").readlines()
        #print "All of lines in %s: %10d" % (self.logname, len(self.loglines))
        self.isRead = True
        return

    def getNdatasets(self):
        if self.isRead == False: self.readLogFile()
        for line in self.loglines:
            if line.rfind("4D scan from") != -1:
                self.n_datasets += 1
        # print line
        print self.n_datasets

    # For lines of each raster scan bunch in a log file.
    def analyzeRaster(self):
        if self.isRead == False: self.readLogFile()
        for line in self.loglines:
            if line.rfind("JOB Raster scan started.") != -1:
                self.n_raster += 1
            if line.rfind("Raster scan status:") != -1:
                # print line
                cols = line.split()
                if cols[3] != None:
                    col1, col2 = cols[3].split('/')
                    if int(col1) == int(col2):
                        print cols[9], col1
                        self.n_raster_images += int(col1)
            # Raster scan status: 372/961 image acquisition finished. 2016/10/22 [Sat] 00:04:23:352
        print self.logname, self.n_raster, self.n_raster_images, float(self.n_raster_images) / 50.0, " sec/day"

    # Compare the job1 and job2 (stored in the first reading process)
    def isSameJob(self, job1, job2):
        id1, status1, timestr1, iline1 = job1
        id2, status2, timestr2, iline2 = job2

        # Check the Job ID and its 'status'
        if id1 == id2 and status1 != status2 and iline1 < iline2:
            print "SAME ID=", id1, id2
            #print "SAME Status=", status1, status2
            print "SAME Lines=", iline1, iline2
            return True
        else:
            return False

    def isOverJob(self, job1, job2):
        id1, status1, timestr1, iline1 = job1
        id2, status2, timestr2, iline2 = job2

        i_id1 = int(id1)
        i_id2 = int(id2)

        if i_id1 < i_id2:
            print "IDs=",i_id1,i_id2
            return True
        else:
            return False

    # Find the lines between the 'start' of the job and its end.
    def mergeJobInfo(self, job1, job2):
        # Starting line
        id1, status1, timestr1, iline1 = job1
        # Ending line
        id2, status2, timestr2, iline2 = job2
        jobid = int(id1)
        # Consuming time from start to end.
        dtime = (timestr2 - timestr1).seconds

        tmp_nlines = iline2 - iline1
        if tmp_nlines > 30000:
            print "The number of lines exceeds 30,000 in mergeJobInfo"
            sys.exit()
        line_indices = iline1, iline2

        # Storing a type of data collections
        for i in range(iline1, iline2+1):
            line = self.loglines[i]
            if line.rfind("Job mode") != -1:
                jobtype = line.split()[2] + line.split()[3]
                break

        return jobid, dtime, jobtype, line_indices

    def searchJobID(self):
        if self.isRead == False:
            self.readLogFile()

        joblist = []
        iline = 0
        initial_job_flag = False
        n_hits = 0

        # Storing all of jobs
        # At this stage, Job ID and start/end points are not treated integratedly.
        for line in self.loglines:
            if line.rfind('Job ID') != -1:
                cols = line.split()
                jobid_str = cols[2]
                status = cols[3]
                datestr = cols[5]
                timestr = cols[7]
                datetimestr = datestr+" "+timestr
                # Time string of each recorded point
                tstr = datetimestr[:datetimestr.rfind(":")]
                tt = datetime.datetime.strptime(tstr, "%Y/%m/%d %H:%M:%S")
                joblist.append((jobid_str,status,tt,iline))
                # The first job in this log file.
                if initial_job_flag == False:
                    if status == "Success" or status == "Failure":
                        print "the initial job would be from Yesterday"
                        continue
                    else:
                        print "This job starts today for the first time", jobid_str, iline
                        initial_job_id = jobid_str
                        initial_job_flag = True
                n_hits += 1
            iline += 1

        target_job_id = 0
        index = 0

        # Extract job information as 'same job' (from start to finished)
        job_info_list = []
        for sjob in joblist:
            id1, status1, timestr1, iline1 = sjob
            if status1 != "start":
                continue
            for ejob in joblist[index:]:
                id2, status2, timestr2, iline2 = ejob
                if status2 != "Success":
                    continue
                if self.isSameJob(sjob, ejob):
                    # returned values will be (jobid, dtime, jobtype, line_indices)
                    job_info_list.append(self.mergeJobInfo(sjob, ejob))
                    break
                elif self.isOverJob(sjob, ejob):
                    print "This job is overcannot found", sjob, ejob
                    break
            index += 1

        # Integrated information
        raster_info = []
        collect_info = []
        n_raster = 0
        n_collect = 0

        for jinfo in job_info_list:
            jobid, dtime, jobtype, line_indices = jinfo
            if jobtype == "RasterScan":
                frame_rate, hgrid, hstep, vgrid, vstep = self.getRasterInfo(line_indices)
                n_raster += 1
                raster_info.append((frame_rate, hgrid, hstep, vgrid, vstep))
            elif jobtype == "CrystalCheck":
                wedge_size, n_frames, exp_time, total_exptime = self.getCollectionInfo(line_indices)
                collect_info.append((wedge_size, n_frames, exp_time, total_exptime))
                n_collect += 1

        print "Today scan number = ", n_raster
        print "Today collect number = ", n_collect

        return n_raster, raster_info, n_collect, collect_info

    # Extracting raster scan information from lines between 'start' and 'ending' points
    def getRasterInfo(self, line_indices):
        for i in range(line_indices[0],line_indices[1]+1):
            line = self.loglines[i]
            if line.rfind("Frame rate") != -1:
                frame_rate = float(line.split()[3])
            elif line.rfind("Horizontal grid:") != -1:
                hori_grid = int(line.split()[2])
                hori_step = float(line.split()[5])
            elif line.rfind("Vertical grid:") != -1:
                vert_grid = int(line.split()[2])
                vert_step = float(line.split()[5])
                break

        return frame_rate, hori_grid, hori_step, vert_grid, vert_step

    def getCollectionInfo(self, line_indices):
        #print "LINE_INDICES", line_indices
        exp_mode = "None"
        n_ds = 0
        helical_vector = []
        hel_points = 0

        for i in range(line_indices[0],line_indices[1]+1):
            line = self.loglines[i]
            #print i,"LINE:",line
            cols = line.split()
            if line.rfind("scan_from =") != -1:
                start_phi = float(cols[2].replace("[deg]","").replace(",",""))
                end_phi = float(cols[5].replace("[deg]","").replace(",",""))
                step_phi = float(cols[8].replace("[deg]","").replace(",",""))
            elif line.rfind("wavelength =") != -1 and line.rfind("expose_time") != -1:
                wavelength = float(cols[2].replace(",",""))
                exp_time = float(cols[5].replace("[sec]",""))
            if line.rfind("mode =") != -1:
                exp_mode = cols[2].replace(",","")
            if exp_mode == "multiple_crystals" and line.rfind("center #") != -1:
                #print line
                n_ds += 1
            elif exp_mode == "vector_centering" and line.rfind("center #") != -1:
                hel_points += 1
                if hel_points == 2:
                    n_ds += 1

        wedge_size = end_phi - start_phi
        n_frames = wedge_size / step_phi
        total_exptime = float(n_frames) * exp_time
        #print "Number of datasets", wedge_size, " x ", n_ds

        return wedge_size, n_frames, n_ds, exp_time, total_exptime

    def getJobInfo(self):
        joblist = self.searchJobID()

    def getMountLog(self):
        self.n_mounts = 0

        if self.isRead == False: self.readLogFile()
        search_word = "Sample Changer is mounting"

        # Get time stamps on the SPACE mount
        self.mount_time_list = []
        for line in self.loglines:
            if line.rfind(search_word) != -1:
                self.n_mounts += 1
                cols = line.split()
                # Time stamp is the last column
                ymd = cols[len(cols) - 3]
                tim = cols[len(cols) - 1]
                tim_cols = tim.split(':')
                recst_tim_str = "%s %02d:%02d:%02d" % (ymd, int(tim_cols[0]), int(tim_cols[1]), int(tim_cols[2]))
                #print recst_tim_str
                tmp_datetime = datetime.datetime.strptime(recst_tim_str, '%Y/%m/%d %H:%M:%S')
                self.mount_time_list.append(tmp_datetime)

        savet = self.mount_time_list[0]
        self.duty_mins = []
        for mt in self.mount_time_list:
            duty_cycle = (mt - savet).seconds / 60.0
            print "Cycle=%5.1f mins" % (duty_cycle)
            self.duty_mins.append(duty_cycle)
            savet = mt

        last_mount = self.mount_time_list[-1]
        curr_time = datetime.datetime.now()
        diff_time = (curr_time - last_mount).seconds / 60.0
        cfile = open(".tmp", "w")
        if diff_time > 60.0:
            cfile.write("%s Users' experiment should be finished!!\n" % (curr_time))
        else:
            cfile.write("Still working: %s\n" % last_mount)
        cfile.close()

        command = "nkf -j .tmp | mail -s \"User experiment at BL32XU\" hirata@spring8.or.jp"
        os.system(command)

    def getTimeOfJob(self, jobline):
        cols = jobline.split()
        datestr = cols[5]
        timestr = cols[7]
        datetimestr = datestr+" "+timestr
        # Time string of each recorded point
        tstr = datetimestr[:datetimestr.rfind(":")]
        tt = datetime.datetime.strptime(tstr, "%Y/%m/%d %H:%M:%S")
        return tt


    def getJobType(self,line_indices):
        iline1,iline2 = line_indices
        # Storing a type of data collections
        for i in range(iline1, iline2+1):
            line = self.loglines[i]
            if line.rfind("Job mode") != -1:
                jobtype = line.split()[2] + line.split()[3]
                return jobtype

    def analyzeMeasurements(self):
        if self.isRead == False: self.readLogFile()

        nline = 0
        ifound = 0
        search_flag = False
        job_lines_list = []

        # Search log lines with "Job ID" string -> store
        for line in self.loglines:
            if search_flag == False and line.rfind("Job ID") != -1:
                cols = line.split()
                jobid = int(cols[2])
                status = cols[3].lower()

                if status == "start":
                    saved_id = jobid
                    saved_line = nline
                    search_flag = True
                    start_time = self.getTimeOfJob(line)
                    nline += 1
                    continue

            if search_flag == True and line.rfind("Job ID") != -1:
                cols = line.split()
                jobid = int(cols[2])
                status = cols[3].lower()
                if saved_id == jobid and status.lower() == "success":
                    line_indices = saved_line, nline
                    #print "JOBID,line_indices = ", jobid, line_indices
                    end_time = self.getTimeOfJob(line)
                    job_lines_list.append((saved_id,line_indices,start_time,end_time))
                    search_flag = False
                else:
                    nline+=1
                    continue
                
            nline += 1

        raster_info = []
        collect_info = []
        n_raster = 0
        n_collect = 0

        total_nds = 0
        total_scan_images = 0
        total_phi = 0.0

        njobs = len(job_lines_list)
        for jinfo in job_lines_list:
            saved_id,line_indices,start_time,end_time = jinfo
            time_sec = (end_time - start_time).seconds
            # Job check
            jobtype = self.getJobType(line_indices)
            #print "JOB=",saved_id,jobtype,line_indices
            if jobtype == "RasterScan":
                frame_rate, hgrid, hstep, vgrid, vstep = self.getRasterInfo(line_indices)
                n_raster += 1
                total_scan_images += hgrid * vgrid
                raster_info.append((saved_id,frame_rate, hgrid, hstep, vgrid, vstep, time_sec))
            elif jobtype == "CrystalCheck":
                wedge_size, n_frames, n_ds, exp_time, total_exptime = self.getCollectionInfo(line_indices)
                total_phi += wedge_size * float(n_ds)
                collect_info.append((saved_id,wedge_size, n_frames, n_ds, exp_time, total_exptime))
                total_nds += n_ds
                n_collect += 1

        n_lines = len(self.loglines)
        print "logname,num_jobs,n_collected,scan_images,total_phi,",
        print "%s,%d,%d,%d,%d,%8.1f"%(self.logname,n_lines,njobs,total_nds,total_scan_images,total_phi)

        return raster_info,collect_info

    # BSS log for manual measurements
    # Raster scan jobs seem to be different from the automated data collection
    # because manual measurements do not use 'schedule' file.
    def analyzeManual(self):
        if self.isRead == False: self.readLogFile()

        nline = 0
        ifound = 0
        search_flag = False
        job_lines_list = []

        # Search log lines with "Job ID" string -> store
        # They are logs for 'data collection' in manual measurements
        for line in self.loglines:
            if search_flag == False and line.rfind("Job ID") != -1:
                cols = line.split()
                jobid = int(cols[2])
                status = cols[3].lower()

                if status == "start":
                    saved_id = jobid
                    saved_line = nline
                    search_flag = True
                    start_time = self.getTimeOfJob(line)
                    nline += 1
                    continue

            if search_flag == True and line.rfind("Job ID") != -1:
                cols = line.split()
                jobid = int(cols[2])
                status = cols[3].lower()
                if saved_id == jobid and status.lower() == "success":
                    line_indices = saved_line, nline
                    #print "JOBID,line_indices = ", jobid, line_indices
                    end_time = self.getTimeOfJob(line)
                    job_lines_list.append((saved_id,line_indices,start_time,end_time))
                    search_flag = False
                else:
                    nline+=1
                    continue

            nline += 1

        print job_lines_list

        ############# Raster jobs
        raster_line_list = []
        for line in self.loglines:
            if search_flag == False and line.rfind("JOB Raster scan started") != -1:
                cols = line.split()
                saved_line = nline
                search_flag = True
                nline += 1
                continue

            if search_flag == True and line.rfind("Job Raster scan finished.") != -1:
                cols = line.split()
                line_indices = saved_line, nline
                raster_line_list.append(line_indices)
                search_flag = False
            else:
                nline+=1
                continue

            nline += 1

        print raster_line_list

        raster_info = []
        collect_info = []
        n_raster = 0
        n_collect = 0

        total_nds = 0
        total_scan_images = 0
        total_phi = 0.0

        # For data collection

        """
        njobs = len(job_lines_list)
        for jinfo in job_lines_list:
            saved_id,line_indices,start_time,end_time = jinfo
            time_sec = (end_time - start_time).seconds
            # Job check
            jobtype = self.getJobType(line_indices)
            #print "JOB=",saved_id,jobtype,line_indices
            if jobtype == "RasterScan":
                frame_rate, hgrid, hstep, vgrid, vstep = self.getRasterInfo(line_indices)
                n_raster += 1
                total_scan_images += hgrid * vgrid
                raster_info.append((saved_id,frame_rate, hgrid, hstep, vgrid, vstep, time_sec))
            elif jobtype == "CrystalCheck":
                wedge_size, n_frames, n_ds, exp_time, total_exptime = self.getCollectionInfo(line_indices)
                total_phi += wedge_size * float(n_ds)
                collect_info.append((saved_id,wedge_size, n_frames, n_ds, exp_time, total_exptime))
                total_nds += n_ds
                n_collect += 1

        n_lines = len(self.loglines)
        print "logname,num_jobs,n_collected,scan_images,total_phi,",
        print "%s,%d,%d,%d,%d,%8.1f"%(self.logname,n_lines,njobs,total_nds,total_scan_images,total_phi)

        return raster_info,collect_info
        """
        return 1

if __name__ == "__main__":
    logdir = sys.argv[1]

    bsslog = AnaBSSlog(logdir)

    yst = int(sys.argv[2])
    mst = int(sys.argv[3])
    dst = int(sys.argv[4])

    bsslog.setDate(yst, mst, dst)
    bsslog.test()
    #bsslog.getMountLog()
    # while(1):
    # bsslog.getMountLog()
    # time.sleep(1800)

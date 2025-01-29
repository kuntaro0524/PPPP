import os, sys, math, glob, numpy

sys.path.append("/isilon/BL32XU/BLsoft/PPPP/10.Zoo/Libs/")

import DBinfo
import ESA
import Raddose
import BSSmeasurementLog

class GatherExpInfo:
    def __init__(self, path, beamline):
        self.path = path
        self.isPrep = False
        self.n_good = 0
        #self.zoodb = zoodb
        self.imgindex = 0
        self.beamline = beamline
        # Only overviewing data collection parameters
        self.overview = True

    def mergeDBinfo(self):
        dbfiles = glob.glob("%s/zoo*db" % self.path)
        dicts_all = []

        num_db = 0
        for dbfile in dbfiles:
            esa = ESA.ESA(dbfile)
            conds = esa.getDict()
            n_good = 0
            n_processed = 0
    
            for each_db in conds:
                dbinfo = DBinfo.DBinfo(each_db)
    
                if dbinfo.getIsDone() == 0:
                    #print "NG!!"
                    continue
                else:
                    dicts_all.append(each_db)
                    n_processed += 1
    
                pinstr=dbinfo.getPinStr()
                good_flag = dbinfo.getGoodOrNot()
    
            num_db += 1

        return dicts_all
    
    def prep(self):
        # Reading CSV file
        self.conds = self.mergeDBinfo()
        self.isPrep = True

    def extractInfoFromBSSlog(self, cond):
        # BSS log file path
        dbinfo = DBinfo.DBinfo(cond)
        dbinfo.prepParams()
        data_index = dbinfo.n_mount

        # a dictionary of ZOODB (one line)
        dbdict = dbinfo.store2dict()
        puck_pin = dbinfo.puck_pin

        # bss log file path
        dc_dir = "%s/%s/data%02d/" % (dbinfo.root_dir, dbinfo.puck_pin, data_index)
        #print "searching log files in %s" % dc_dir
        logfiles = glob.glob('%s/*.log' % (dc_dir))

        # Only one analysis on log file is okay for overviewing

        if len(logfiles) == 0:
            pass
        else:
            for logfile in logfiles:
                if logfile.rfind("download_eiger") != -1:
                    continue
                else:
                    try:
                        #print "##### %s #####" % logfile
                        bssml = BSSmeasurementLog.BSSmeasurementLog(logfile)
                        # experimental parameters from BSS measurement log.
                        conds_dict = bssml.store2dict()
                    except Exception as e:
                        #print e.args
                        continue

                    beam_v = dbdict['ds_vbeam']
                    beam_h = dbdict['ds_hbeam']
                    flux = dbdict['flux']
                    exptime = conds_dict['exp_time']
                    en = 12.3984 / dbdict['wavelength']
                    att_factor = conds_dict['att_factor']
                    raddose = Raddose.Raddose()
                    att_flux = att_factor * flux

                    # Dose estimation case for helical
                    if (conds_dict['mode'] == "helical"):
                        code_ds = conds_dict['code_ds']
                        nds = 1
                        if len(code_ds) != 2:
                            print "it is difficult to estimate dose from this information"
                        else:
                            y_start = code_ds[0][1][1]
                            y_end = code_ds[1][1][1]
                            cry_len_y_um = numpy.abs(y_end - y_start) * 1000.0
                            num_iradds = cry_len_y_um / beam_h
                            dose = raddose.getDose(beam_h, beam_v, att_flux, exptime, energy=en)
                            num_of_frames = int(conds_dict['total_osc']/conds_dict['osc_width'])
                            total_dose = num_of_frames * dose / num_iradds
                            reduced_fact = dbdict['reduced_fact']
                            ntimes = dbdict['ntimes']
                            #print "%5d frames: Actual dose = %5.2f MGy" % (num_of_frames, total_dose)
                            print "%s," % dc_dir,
                            print "%(sample_name)s,%(mode)s, %(wavelength).5f, %(ds_vbeam).2f x %(ds_hbeam).2f, %(flux).3e," % dbdict,
                            print "%(total_osc).2f, %(osc_width).3f," % dbdict,
                            print "%(att_factor).4f, %(exp_time).3f,""" % conds_dict,
                            print "%8.3f,%8.3f,%8.5f,%3d,"%(dbdict['dose_ds'],total_dose, reduced_fact, ntimes),
                            print "%3d" % nds
                    # Dose estimation: case for multiple small wedge scheme
                    else:
                        code_ds = conds_dict['code_ds']
                        #print code_ds,len(code_ds)
                        nds = len(code_ds)
                        if nds == 0:
                            print "no crystal!"
                        else:
                            dose = raddose.getDose(beam_h, beam_v, att_flux, exptime, energy=en)
                            num_of_frames = int(conds_dict['total_osc']/conds_dict['osc_width'])
                            total_dose = num_of_frames * dose 
                            reduced_fact = dbdict['reduced_fact']
                            ntimes = dbdict['ntimes']
                            #print "%5d frames: Actual dose = %5.2f MGy" % (num_of_frames, total_dose)
                            print "%s," % dc_dir,
                            print "%(sample_name)s,%(mode)s, %(wavelength).5f, %(ds_vbeam).2f x %(ds_hbeam).2f, %(flux).3e," % dbdict,
                            print "%(total_osc).2f, %(osc_width).3f," % dbdict,
                            print "%(att_factor).4f, %(exp_time).3f,""" % conds_dict,
                            print "%8.3f,%8.3f,%8.5f,%3d,"%(dbdict['dose_ds'],total_dose, reduced_fact, ntimes),
                            print "%3d" % nds
                            if self.overview == True:
                                break
        #print logfiles

    def getFooter(self):

        footer_note = """
            </table>
            <h6>
            #DS: number of datasets collected from the pin.<br> "log comment" : Log comment from ZOO (easy check).<br>
            loop: a link to the picture of a loop before raster scan.<br>
            2D scan: a link to the picture of 2D raster heatmap.if<br>
            'X' appears on "loop" or "2D scan", there would not be crystals on the loop.<br>
            </h6></table>
            """

        return footer_note

    def makeHTML(self, html_prefix):
        if self.isPrep == False:
            self.prep()

        html_filename = "report_%s.html" % html_prefix
        ofile = open(html_filename, "w")
        self.makeBody(ofile)
        for p in self.conds:
            htmlstr = self.makeHTMLforCond(p)
            if htmlstr == "NO_INFO":
                continue
            ofile.write("%s\n"%htmlstr)

        footer_note = self.getFooter()
        ofile.write(footer_note)

        # Abs path
        abs_path = os.path.abspath(html_filename)

        return abs_path

    def makeOnMouse(self, picture, height, button):
        string = ""
        string += "<td><a href=%s " % picture
        string += "onmouseover=\"document.getElementById('ph-%ds').style.display='block';\" " % self.imgindex
        string += "onmouseout=\"document.getElementById('ph-%ds').style.display='none'; \"> %s </a> " % (
        self.imgindex, button)
        string += "<div style=\"position:absolute;\"> "
        string += "<img src=\"%s\" height=\"%d\" id=\"ph-%ds\"" % (picture, height, self.imgindex)
        string += " style=\"zindex: 10; position: absolute; top: 50px; display:none;\" /></td></div>"

        return string

    def pngFile(ppmfile, pngfile):
        command = "convert %s %s" % (ppmfile, pngfile)
        os.system(command)

    def makeBody(self, html_file):
        title = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">

        <style>
        .dataset_table {
            font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
            width: 100%%;
            border-collapse: collapse;
        }

        .dataset_table td, .dataset_table th {
            font-size: 1em;
            border: 1px solid #98bf21;
            text-align: center;
            padding: 3px 7px 2px 7px;
        }

        .dataset_table th {
            font-size: 1.1em;
            text-align: center;
            padding-top: 5px;
            padding-bottom: 4px;
            background-color: #A7C942;
            color: #ffffff;
        }

        .dataset_table tr.alt td {
            color: #000000;
            background-color: #EAF2D3;
        }   
            </style>
            <h4>Results</h4>
            <table class="dataset_table">
            <tr>
            <th>puckid</th> <th>pinid</th> <th>sample_name</th> <th>mode</th> <th>wavelength</th> <th>total phi</th>
            <th>osc width</th> <th>raster beam</th> <th>raster area(grids)</th> <th>#DS</th> <th>log comment</th> <th>meas time[min]</th>
            <th>loop</th><th>2D scan</th><th>SHIKA</th>
            </tr>

            """

        html_file.write(title)

        return True


    # For processing one condition in ESA
    def makeHTMLforCond(self, each_cond):
        dbinfo = DBinfo.DBinfo(each_cond)
        # 'isDS' is evaluated. -> normal termination : return 1
        self.n_good += dbinfo.getStatus()

        # is data collection completed?
        good_flag = dbinfo.getGoodOrNot()
        log_comment = dbinfo.getLogComment()

        # Common information for failed/succeeded pins
        puckid, pinid = dbinfo.getPinInfo()
        sample_name = dbinfo.sample_name
        wavelength = dbinfo.wavelength
        mode = dbinfo.mode
        data_index = dbinfo.n_mount

        total_osc = dbinfo.total_osc
        osc_width = dbinfo.osc_width

        # Writing common information
        dichtml = dict(puckid=puckid, pinid=pinid, sample_name=sample_name, wavelength=wavelength, mode=mode,
                       total_osc=total_osc, osc_width=osc_width)

        good_str = """
         <tr>
          <td>%(puckid)s</td> <td>%(pinid)s</td> <td>%(sample_name)s</td> <td>%(mode)s</td> <td>%(wavelength).4f</td> 
          <td>%(total_osc).1f</td> <td>%(osc_width).2f</td>
        """ % dichtml

        #print good_str
        if good_flag == True:
            ds_time = dbinfo.getDStime()
            mode = dbinfo.mode
            meas_time = dbinfo.getMeasTime()
            mount_time = dbinfo.getMountTime()
            raster_time = dbinfo.getRasterTime()
            center_time = dbinfo.getCenterTime()
            height, width, nv_raster, nh_raster, raster_vbeam, raster_hbeam, att_raster, exp_raster = dbinfo.getRasterConditions()
            sample_name = dbinfo.sample_name
            wavelength = dbinfo.wavelength
            mode = dbinfo.mode


            hel_cry_size = dbinfo.hel_cry_size
            #raster_png = "%s-%02d/scan%02d/2d/_spotfinder/plot_2d_n_spots.png" % (puckid, pinid, data_index)
            if self.beamline == "BL45XU":
                raster_png = "%s-%02d/scan%02d/2d/_spotfinder/plot_2d_n_spots.png" % (puckid, pinid, data_index)
            elif self.beamline == "BL32XU":
                raster_png = "%s-%02d/scan%02d/2d/_spotfinder/2d_selected_map.png" % (puckid, pinid, data_index)
                if os.path.exists(raster_png) == False:
                    raster_png = "%s-%02d/scan%02d/2d/_spotfinder/plot_2d_n_spots.png" % (puckid, pinid, data_index)

            # Crystal capture
            cap_image = "%s-%02d/raster.jpg" % (puckid, pinid)

            nds = dbinfo.getNDS()
            t_sukima_raster = (raster_time * 60.0 - nv_raster * exp_raster * nh_raster) / (nv_raster - 1)

            dichtml = dict(puckid=puckid, pinid=pinid, sample_name=sample_name, wavelength=wavelength,
                           mount_time=mount_time,
                           center_time=center_time, raster_time=raster_time, ds_time=ds_time, total_time=meas_time,
                           nds=nds,
                           raster_height=height, raster_width=width, nv_raster=nv_raster, nh_raster=nh_raster,
                           raster_vbeam=raster_vbeam,
                           raster_hbeam=raster_hbeam, att_raster=att_raster, exp_raster=exp_raster, comment=log_comment,
                           hel_cry_size=hel_cry_size,
                           total_osc=total_osc, osc_width=osc_width, raster_png=raster_png)

            on_mouse_str = ""
            on_mouse_str += self.makeOnMouse(cap_image, 400, "O")
            self.imgindex += 1
            on_mouse_str += self.makeOnMouse(raster_png, 400, "O")
            self.imgindex += 1

            # print "ONMOUSE=",on_mouse_str

            good_str += """
              <td>%(raster_hbeam).0f&times;%(raster_vbeam).0f (um) <td>%(raster_height).0f&times;%(raster_width).0f 
              (%(nv_raster)d&times;%(nh_raster)d grids)</td> <td>%(nds)d</td> <td>%(comment)s</td> <td>%(total_time).2f</td>\n""" % dichtml
            good_str += on_mouse_str

            # SHIKA report file
            if self.beamline == "BL45XU":
                shika_report_file = "%s/report.html" % dbinfo.getSHIKAdir()
            elif self.beamline == "BL32XU":
                shika_report_file = "%s/report_zoo.html" % dbinfo.getSHIKAdir()

            rel_path = os.path.relpath(shika_report_file)
            good_str += "\n<td><a href=\"%s\">MAP</a></td>" % rel_path

            good_str += "\n</tr>\n"

        # Not good pins
        else:
            meas_time = dbinfo.getMeasTime()
            mount_time = dbinfo.getMountTime()
            raster_time = dbinfo.getRasterTime()
            center_time = dbinfo.getCenterTime()
            height, width, nv_raster, nh_raster, raster_vbeam, raster_hbeam, att_raster, exp_raster = dbinfo.getRasterConditions()
            nds = 0
            ds_time = 0.0

            if self.beamline == "BL45XU":
                raster_png = "%s-%02d/scan%02d/2d/_spotfinder/plot_2d_n_spots.png" % (puckid, pinid, data_index)
            elif self.beamline == "BL32XU":
                raster_png = "%s-%02d/scan%02d/2d/_spotfinder/2d_selected_map.png" % (puckid, pinid, data_index)
                if os.path.exists(raster_png) == False:
                    raster_png = "%s-%02d/scan%02d/2d/_spotfinder/plot_2d_n_spots.png" % (puckid, pinid, data_index)

            dichtml = dict(puckid=puckid, pinid=pinid, mount_time=mount_time, center_time=center_time,
                           raster_time=raster_time, total_time=meas_time,
                           raster_height=height, raster_width=width, nv_raster=nv_raster, nh_raster=nh_raster,
                           raster_vbeam=raster_vbeam,
                           raster_hbeam=raster_hbeam, att_raster=att_raster, exp_raster=exp_raster, comment=log_comment,
                           nds=nds,
                           raster_png=raster_png)

            # Crystal capture
            cap_image = "%s-%02d/raster.jpg" % (puckid, pinid)

            on_mouse_str = ""
            on_mouse_str += self.makeOnMouse(cap_image, 400, "X")
            self.imgindex += 1
            on_mouse_str += self.makeOnMouse(raster_png, 400, "X")
            self.imgindex += 1

            good_str += """
              <td>%(raster_hbeam).0f&times;%(raster_vbeam).0f (um) <td>%(raster_height).0f&times;%(raster_width).0f 
              (%(nv_raster)d&times;%(nh_raster)d grids)</td> <td>%(nds)d</td> <td>%(comment)s</td> <td>%(total_time).2f</td>""" % dichtml
            good_str += on_mouse_str
            # SHIKA report file
            if self.beamline == "BL45XU":
                shika_report_file = "%s/report.html" % dbinfo.getSHIKAdir()
            elif self.beamline == "BL32XU":
                shika_report_file = "%s/report_zoo.html" % dbinfo.getSHIKAdir()
            rel_path = os.path.relpath(shika_report_file)
            good_str += "\n<td><a href=\"%s\">???</a></td>" % rel_path
            good_str += "\n</tr>\n"

        if dbinfo.isDone != 0:
            return good_str
        else:
            return "NO_INFO"

if __name__ == "__main__":

    gei = GatherExpInfo(sys.argv[1], sys.argv[2])
    gei.prep()

    for cond in gei.conds:
        #print cond
        gei.extractInfoFromBSSlog(cond)

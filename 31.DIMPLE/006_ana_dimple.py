import os, sys, math, logging, csv, glob 
#sys.path.append("/isilon/BL32XU/BLsoft/PPPP/10.Zoo/Libs")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/Libs")
import MyException
import Xds2Mtz
import ResolutionFromXscaleHKL
import ComRefine
import logging.config
import KstrHTML

beamline = "BL32XU"

def ana_dimple_log(dimple_log):
    save_line = ""

    # Check if this file exists
    if os.path.exists(dimple_log) == False:
        logging.error("dimple.log does not exists!!")
        return False, False, 999.999

    lines = open(dimple_log,"r").readlines()

    # Failure flag for MR
    isOkayMR = True
    isOkayBlobs = True

    for line in lines:
        #print line
        if line.rfind("free_r") != -1:
            save_line = line.strip()

        # Blob analysis failed
        if line.rfind("Unmodelled blobs not found.") != -1:
            logging.info("Blob analysis failed.")
            isOkayBlobs = True
        if line.rfind("INPUT ERROR: Unit Cell not compatible with Space Group") != -1:
            logging.info("unit cell is incompatible")
            isOkayMR = False

    if save_line == "":
        free_r = 999.999
        logging.info("Free-R value cannot be found in dimple.log")
    else:
        # Convertion
        free_r = float(save_line.split()[1]) * 100.0 #[unit] = "%"

    return isOkayMR, isOkayBlobs, free_r

if __name__ == "__main__":

    prep_csv = sys.argv[1]
    lines = open(prep_csv,"r").readlines()

    # Logging setting
    logname = "./ana_dimple.log"
    logging.config.fileConfig('/isilon/%s/BLsoft/PPPP/10.Zoo/Libs/logging.conf' % beamline, defaults={'logfile_name': logname})
    logger = logging.getLogger('ana_dimple')

    n_process = 0
    ref_refl = ""
    # read lines and stores information

    if len(sys.argv) != 0:
        html_name = "dimple_analysis.html"
    else:
        html_name = sys.argv[2]
       
    htmllog = open(html_name, "w")

    # header information
    header_info = """
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
 .dataset_table tr.alt td {
     color: #000000;
     background-color: #EAF2D3;
 }
</style>
<h4> Results </h4>

<table class="dataset_table">
<tr>
<th> puck_pin </th>
<th> sample_name </th>
<th> resolution </th>
<th> MR comment </th>
<th> Free-R (%)</th>
<th> Blob analysis(DIMPLE) </th>
<tr>
    """
    htmllog.write("%s\n" % header_info)
    kstrhtml = KstrHTML.KstrHTML()
    log_index = 0

    for line in lines[1:]:
        #logger.info("LIST:%s" % line,)
        logger.info("########### Analysis started #############################")
        cols = line.split(',')
        # dictionary for making a HTML file
        html_dict = {}
        if len(cols) != 5:
            logging.info("This line is not suitable for process. %s ncols = %5d"% (line, len(cols)))
        else:
            puck_pin, sample_name, refl_name, model_name, symm = line.split(',')
            symm = symm.strip()
            logging.info("puck_pin= %s" %(puck_pin))
            logging.info("sample= %s" %(sample_name))
            logging.info("refl_name=%s" % refl_name) 
            logging.info("model_name=%s" % model_name) 
            logging.info("symm=%s" % symm) 

            # Preparation
            proc_dir = refl_name[:refl_name.rfind("/")]
            logging.info("reflection file directory: %s" % proc_dir)
            dimple_dir = os.path.join(proc_dir,"dimple/")
            logging.info("DIMPLE directory: %s" % dimple_dir)

            # making a DIMPLE directory
            if os.path.exists(dimple_dir) == False:
                os.makedirs(dimple_dir)
                logging.error("No DIMPLE directory: skipping %s" % dimple_dir)
                continue

            # Resolution calculation from XDS_ASCII.HKL
            resol_calculator = ResolutionFromXscaleHKL.ResolutionFromXscaleHKL(refl_name)
            html_dict['puck_pin'] =puck_pin
            html_dict['sample_name'] = sample_name

            try:
                dmin = resol_calculator.get_resolution()
                logging.info("resolution limit = %8.3f A" % dmin)
                html_dict["resol_flag"] = True
                html_dict["resolution"] = dmin

            except MyException.GetResolutionFailed as e:
                logging.error("Exception in resolution estimation from HKL file. %s" % e.args)
                logging.error("Data analysis is skipped for this dataset")
                html_dict["resolution"] = 999.999
                html_dict["resol_flag"] = False
                #continue
        
            # Do dimple refinement
            dimple_logfile = os.path.join(dimple_dir,"dimple.log")
            try:
                mr_flag, blob_flag , free_r = ana_dimple_log(dimple_logfile)
                if mr_flag == False:
                    logging.info("Molecular replacement was not conducted.\n" )
                    html_dict["mr_comment"] = "failed."
                    html_dict["freer"] = 99.9999
                    html_dict["jpegs"] = ""
                else:
                    html_dict["mr_comment"] = "succeeded."
                    # Refinement information
                    logging.info("%s Free-R = %8.5f\n" % (dimple_logfile, free_r))
                    html_dict["freer"] = free_r
                    # Blob analysis
                    if blob_flag == True:
                        # Blob jpeg files
                        jpeg_files = glob.glob("%s/*jpeg" % dimple_dir)
                        html_dict['jpegs'] = jpeg_files

            except MyException.GetFreeRflag as e:
                logging.error("%s" % e.args)

            logger.info("HTML_LOG=%s" % html_dict)
            # The top of one line of HTML table
            #text = "<tr><td>{sample}</td> <td>{resol}</td><td>{mr_comment}</td><td> {free_r}</td>"
            #result = text.format(sample=html_dict['sample_name'],resol = html_dict['resolution'], mr_comment = html_dict['mr_comment'], free_r=html_dict['freer'])
            html_str = """
              <td>%(puck_pin)s</td><td>%(sample_name)s</td><td>%(resolution).2f (A)</td> <td>%(mr_comment)s</td> <td> %(freer).2f</td>""" % html_dict
            # mouse over strings for blob analysis
            if len(html_dict['jpegs']) != 0:
                html_str += "<td>"
                blob_index = 0
                for jpeg_file in html_dict['jpegs']:
                    rel_path = os.path.relpath(jpeg_file, "./")
                    result_str = jpeg_file[jpeg_file.rfind("/")+1:].replace(".jpeg","")
                    mouse_over_html = kstrhtml.makeOnMouse(log_index, rel_path, 500, result_str)
                    html_str += mouse_over_html
                    html_str += "\n"
                    log_index += 1
                html_str += "</td>"
            else:
                html_str += "<td>X</td>"
            # The end of one line of HTML table
            html_str += "</tr>"
            htmllog.write("%s\n" % html_str)
            log_index += 1

    htmllog.write("</table>\n")

"""
out=test.html
cat <<+ > $out
<html>
<head></head>
<body>
<table>
+

#for d in */cluster_*/run_03/ccp4/refine0
#for d in *3.4*/cluster_*/run_03/ccp4/refine0
for d in 200214_*_ono/_kamoproc/CPS*/data*/cry00_*/ccp4/dimple
do
 log=$d/screen.log
 r_wf=`grep "R/Rfree" $log`
 cat <<+ >> $out
<tr>
 <td>name<br>$r_wf</td>
 <td><img src="$d/blob1v1.png" width=320></td>
 <td><img src="$d/blob2v2.png" width=320></td>
</tr>
+
done
cat <<+ >> $out

</table>
</body>
+
"""

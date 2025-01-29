import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import glob,numpy
import DirectoryProc
import AnaCORRECT
import LibSPG

head = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title> KAMO scaling results </title>
    <link rel = "stylesheet" href="contents/style.css">
  </head>
  <body>
"""

style_strings = """
h1 {color: red;
font-size:18px;
font-family: "Courier New";
}
h2 {color: blue;
font-size:18px;
font-family: "Courier New";
}

div {background: #FFFACD; 
width:1000px; 
border: 1px solid #D3D3D3; 
height:100%;
padding-left:10px;
padding-right:10px; 
padding-top:10px; 
padding-bottom:10px;
}

pre {background: #FFFACD;
font-size:15px;
font-family: "Courier New";
}

p1 {background: yellow;
border: 2px solid orange; 
height:100%; 
padding-left:5px; 
padding-right:5px; 
padding-top:5px; 
padding-bottom:5px;
line-height: 200%
}

p2 {
height:100%; 
border-bottom: solid 3px orange;
padding-left:2px; 
padding-right:2px; 
padding-top:2px; 
font-size:18px;
font-family:"Courier New";
line-height:20px;
line-height: 150%
}

p3 {
border-bottom: solid 3px #87CEFA;
height:100%;
padding-left:2px; 
padding-right:2px; 
padding-top:2px; 
font-size:18px;
font-family:"Courier New";
line-height:20px;
line-height: 150%
}

hr {
  border-top: 10px solid #bbb;
  border-bottom: 3px solid #fff;
}

body {
line-height: 1.2;
}
"""

class XSCALEReporter():
    def __init__(self, root_path):
        # Finding xscale.mtz
        self.rootdir = os.path.abspath(root_path)
        self.dp=DirectoryProc.DirectoryProc(self.rootdir)
        self.corrlp_list,self.path_list=self.dp.findTarget("XSCALE.LP")
        self.libspg = LibSPG.LibSPG()

    def makeLogText(self,logfile="xscale.txt"):
        # Log file
        logf=open(logfile,"w")
        exec_dir = os.path.abspath("../../")
        self.corrlp_list.sort()

        # find CORRECT.LP and analyze
        for corrlp in self.corrlp_list:
            ac=AnaCORRECT.AnaCORRECT(corrlp)
            total_rmeas=ac.getTotalRmeas()
            compl,redun,rmeas,isigi,cchalf = ac.getOuterShellInfo()
        
            nds= ac.countDatasets()
            lines=ac.getStatsTableAsItIs()

            logf.write("###########################\n")
            relpath = os.path.relpath(corrlp, exec_dir)
            logf.write("%s\n"%relpath)
            for line in lines:
                logf.write("%s"%line)

    def makeHTML(self,logfile="xscale.html",figdpi=60,skipMulti=True):
        # Log file
        logf=open(logfile,"w")
        exec_dir = os.path.abspath("../../")
        logf.write("%s\n" %  head)

        # Making contents directory
        contents_dir = "%s/contents/" % self.rootdir
        if os.path.exists(contents_dir) != True:
            os.makedirs(contents_dir)

        self.corrlp_list.sort()

        # Making the style file for correct.html
        style_file = os.path.join(contents_dir, "style.css")
        sfile = open(style_file, "w")
        sfile.write("%s" % style_strings)

        # find CORRECT.LP and analyze
        for corrlp in self.corrlp_list:
            figname = os.path.relpath(corrlp,"./").replace("/","-").replace("CORRECT.LP","")[:-1]+".png"
            figpath = os.path.join(contents_dir, figname)
            print "LOG=", corrlp
            print "Figure_path=", figpath
            if skipMulti == True:
                if corrlp.rfind("multi_") != -1:
                    print "Skipping %s because it is multiple small wedge data" % corrlp
                    continue
            ac=AnaCORRECT.AnaCORRECT(corrlp)
            total_rmeas=ac.getTotalRmeas()
            compl,redun,rmeas,isigi,cchalf = ac.getOuterShellInfo()

            # Cell dimensions
            cell_str = "cell: %8.3f %8.3f %8.3f %8.2f %8.2f %8.2f" %(ac.getCellParm())
            # SPG
            spgnum = ac.getFinalSPG()
            spg_str = "Space group(XDS) = %s" % self.libspg.search_spgnum(spgnum)

            # Making figure of XDS stats from CORRECT.LP
            ac.makePlot(figpath,figdpi)

            # Log figure from AnaCORRECT.LP is 15:3 ratio (H:V)
            fig_h = 15
            fig_v = 3
            ratio = fig_h / fig_v
            hpix = int(figdpi * 18)
            vpix = int(hpix / ratio)

            # ISa
            isa = ac.getISa()
            isa_str = "ISa(XDS) = %5.1f" % isa
            logstr = "%s, %s" % (spg_str, cell_str)
        
            nds= ac.countDatasets()
            lines=ac.getStatsTableAsItIs()

            relpath = os.path.relpath(corrlp, exec_dir)
            figpath_rel = "contents/%s" % figname
            logf.write("<p1>%s<br></p1>\n"%relpath)
            logf.write("<p2>%s<br></p2>\n" % logstr)
            logf.write("<p3>%s<br></p3>\n" % isa_str)
            logf.write("<pre>\n")
            for line in lines:
                logf.write("%s"%line)
            logf.write("</pre>\n")
            logf.write("<img src=\"%s\" width=\"%dpx\" height=\"%dpx\" alt=\"XDS stats\">\n" % (figpath_rel,hpix,vpix))
            logf.write("<hr>\n")
        logf.write("</body>\n")
        logf.close()

if __name__ == "__main__":
    xdsr = XSCALEReporter(sys.argv[1])
    xdsr.makeHTML(figdpi=65)
    #xdsr.makePlots()
    #xdsr.makePlots()

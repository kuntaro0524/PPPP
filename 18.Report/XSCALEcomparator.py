import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import glob,numpy
import DirectoryProc
import AnaCORRECT
import LibSPG

class XSCALEcomparator():
    def __init__(self):
        self.xscale_list = []

    def append(self, xscalelp_path):
        abs_path = os.path.abspath(xscalelp_path)
        self.xscale_list.append(abs_path)

    def doComparison(self, outfig = "test.png"):
        # find CORRECT.LP and analyze
        if len(self.xscale_list) == 0:
            print "No XSCALE.LP"
            sys.exit()

        print "Processing %5d" % len(self.xscale_list)
        n_xscale = len(self.xscale_list)
        data_index = 0
        # PLOTTER
        import matplotlib.pyplot as plt
        import numpy as np

        rmeas_list = []
        cchalf_list = []
        isigi_list = []
        compl_list = []

        for corrlp in self.xscale_list:
            ac=AnaCORRECT.AnaCORRECT(corrlp)
            ds2, cc_half = ac.getCChalf()
            ds2, isigi = ac.getIsigI()
            ds2, rmeas = ac.getRmeas()
            ds2, compl = ac.getCompleteness()

            cchalf_list.append((ds2, cc_half))
            isigi_list.append((ds2, isigi))
            rmeas_list.append((ds2, rmeas))
            compl_list.append((ds2, compl))

        print "LLLLLLLLLLLLLLLLLLL", len(compl_list)
        # cc_half plot
        fig = plt.figure(facecolor="lightgreen", figsize=(15, 3), dpi=600)

        ax1 = fig.add_axes([0.05, 0.15, 0.14, 0.75])
        ax2 = fig.add_axes([0.25, 0.15, 0.14, 0.75])
        ax3 = fig.add_axes([0.45, 0.15, 0.14, 0.75])
        ax4 = fig.add_axes([0.65, 0.15, 0.14, 0.75])
        ax5 = fig.add_axes([0.85, 0.15, 0.14, 0.75])

        ax1.grid()
        ax2.grid()
        ax3.grid()
        ax4.grid()
        ax5.grid()
        ax1.set_xlabel("$d^{*2}$")
        ax2.set_xlabel("$d^{*2}$")
        ax3.set_xlabel("$d^{*2}$")
        ax4.set_xlabel("$d^{*2}$")
        ax5.set_xlabel("<I/sigI>")
        # Limitation
        ax1.set_ylim(0, 100)
        ax1.set_title("$d*{^2}$ .vs. Completeness")
        ax2.set_title("$d*{^2}$ .vs. Rmeas")
        ax3.set_title("$d*{^2}$ .vs. <I/sigI>")
        ax4.set_title("$d*{^2}$ .vs. CC(1/2)")
        ax4.set_ylim(0, 100)
        ax5.set_title("<I/sigI> .vs. CC(1/2)")
        # ax5.set_yscale('log')
        ax5.set_xscale('log')
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend(loc="center left")
        ax5.legend()

        color = ["blue", "red", "orange"]
        idx=0
        for ds2, compl in compl_list:
            ax1.plot(ds2, compl, label="Completeness", color=color[idx], marker="o")
            ax1.set_ylabel("Completeness[%]")
            idx += 1
        idx=0
        for ds2, rmeas in rmeas_list:
            ax2.plot(ds2, rmeas, label="Rmeas", color=color[idx], marker="h")
            ax2.set_ylabel("Rmeas")
            idx += 1
        idx=0
        for ds2, isigi in isigi_list:
            ax3.plot(ds2, isigi, label="<I/sigI>", color=color[idx], marker="<")
            ax3.set_ylabel("<I/sigI>")
            idx += 1
        idx=0
        for ds2, cc_half in cchalf_list:
            ax4.plot(ds2, cc_half, label="CC(1/2)", color=color[idx], marker=">")
            ax4.set_ylabel("CC(1/2) [%]")
            idx += 1
        idx=0
        for (ds2, isigi), (ds2_2, cc_half) in zip(isigi_list, cchalf_list):
            ax5.plot(isigi, cc_half, label="CC(1/2)", color=color[idx], marker="D")
            ax5.set_ylabel("CC(1/2)")
            idx += 1

        # Figure save
        png_file = "test%02d.png" % data_index
        fig.savefig(png_file)

if __name__ == "__main__":
    xsc = XSCALEcomparator()

    nfile = len(sys.argv)
    for idx in range(1, nfile):
        filename = sys.argv[idx]
        print "APPENDING",filename
        xsc.append(filename)

    xsc.doComparison()
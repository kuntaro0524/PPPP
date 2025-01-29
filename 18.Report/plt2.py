import sys,os
import numpy
import AnaCORRECT

if __name__=="__main__":
        ac=AnaCORRECT.AnaCORRECT(sys.argv[1])
        print "###",sys.argv[1]
        outfile=sys.argv[1].replace(".LP",".csv")
        ofile=open(outfile,"w")
        for logstr in ac.getStatsTable():
            ofile.write("%s"%logstr)

        lines = ac.getStatsTableAsItIs()
        for line in lines:
            print line
        print ac.getISa()
        stats_list = ac.getStatsLists()
        for li in stats_list:
            #list_stat.append((dmin,compl,ds2,rfact,isigi,cc_half))
            dmin,compl,ds2,rfact,isigi,cc_half = li
        #return self.ds2, self.rmeas, self.isigi, self.cchalf

        # PLOTTER
        import matplotlib.pyplot as plt
        import numpy as np

        # cc_half plot
        fig = plt.figure(facecolor="lightgreen",figsize=(15,3),dpi=200)
        #ax1 = fig.add_subplot(141)
        #ax2 = fig.add_subplot(142)
        #ax3 = fig.add_subplot(143)
        #ax4 = fig.add_subplot(144)

        ax1 = fig.add_axes([0.05,0.15,0.14,0.75])
        ax2 = fig.add_axes([0.25,0.15,0.14,0.75])
        ax3 = fig.add_axes([0.45,0.15,0.14,0.75])
        ax4 = fig.add_axes([0.65,0.15,0.14,0.75])
        ax5 = fig.add_axes([0.85,0.15,0.14,0.75])

        ds2,cc_half = ac.getCChalf()
        ds2,isigi = ac.getIsigI()
        ds2,rmeas = ac.getRmeas()
        ds2,compl = ac.getCompleteness()

        ax1.grid()
        ax2.grid()
        ax3.grid()
        ax4.grid()
        ax5.grid()
        ax1.set_xlabel("d**2")
        ax2.set_xlabel("d**2")
        ax3.set_xlabel("d**2")
        ax4.set_xlabel("d**2")
        ax5.set_xlabel("<I/sigI>")

        # Limitation
        ax1.set_title("d**2 .vs. CC(1/2)")
        ax1.set_ylim(0,100)
        ax2.set_title("d**2 .vs. <I/sigI>")
        ax3.set_title("d**2 .vs. Rmeas")
        ax4.set_title("d**2 .vs. Completeness")
        ax4.set_ylim(0,100)
        ax5.set_title("<I/sigI> .vs. CC(1/2)")
        #ax5.set_yscale('log')
        ax5.set_xscale('log')


        ax1.plot(ds2, cc_half, label="CC(1/2)", color="blue",marker="x")
        ax1.set_ylabel("CC(1/2) [%]")
        ax2.plot(ds2, isigi, label="<I/sigI>", color="red", marker="o")
        ax2.set_ylabel("<I/sigI>")
        ax3.plot(ds2, rmeas, label="Rmeas", color="black", marker="o")
        ax3.set_ylabel("Rmeas")
        ax4.plot(ds2, compl, label="Completeness", color="brown", marker="o")
        ax4.set_ylabel("Completeness[%]")
        ax5.plot(isigi, cc_half, label="CC(1/2)", color="green", marker="o")
        ax5.set_ylabel("CC(1/2)")

        ax1.legend(loc="center left")
        ax2.legend()
        ax3.legend()
        ax4.legend()
        ax5.legend()
        #plt.show()
        fig.savefig("test.png")

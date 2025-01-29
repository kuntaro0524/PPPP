import XDS_ASCII,sys

if __name__=="__main__":
    xdsas=XDS_ASCII.XDS_ASCII(sys.argv[1])
    print "%s %10.1f"%(sys.argv[1],xdsas.calcDP())

import xmlrpclib

def run(binning):
    s = xmlrpclib.ServerProxy('http://127.0.0.1:1921')
    s.set_binning(binning)

if __name__ == "__main__":
    import sys
    run(int(sys.argv[1]))

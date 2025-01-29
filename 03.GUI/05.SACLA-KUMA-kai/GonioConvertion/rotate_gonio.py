import xmlrpclib

def run(deltaphi):
    s = xmlrpclib.ServerProxy('http://127.0.0.1:1921')
    s.rotate(float(deltaphi))

if __name__ == "__main__":
    import sys
    run(int(sys.argv[1]))

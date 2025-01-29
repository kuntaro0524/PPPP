import xmlrpclib

def run(zoom):
    s = xmlrpclib.ServerProxy('http://127.0.0.1:1921')
    s.set_zoom(zoom)

if __name__ == "__main__":
    import sys
    run(int(sys.argv[1]))

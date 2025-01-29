import xmlrpclib

def run():
    s = xmlrpclib.ServerProxy('http://127.0.0.1:1921')
    print s.get_pixel_size()

if __name__ == "__main__":
    #import sys
    #zoom = float(sys.argv[1])
    #run(zoom)
    run()

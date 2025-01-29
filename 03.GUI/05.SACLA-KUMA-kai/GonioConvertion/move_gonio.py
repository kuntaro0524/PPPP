import xmlrpclib

def run(deltax, deltay):
    s = xmlrpclib.ServerProxy('http://127.0.0.1:1921')
    s.move(deltax, deltay)

if __name__ == "__main__":
    import sys
    run(float(sys.argv[1]), float(sys.argv[2]))

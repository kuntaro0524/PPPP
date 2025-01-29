import xmlrpclib

def run(phi, x, y, z):
    s = xmlrpclib.ServerProxy('http://127.0.0.1:1921')
    s.move_gonio_abs(phi, x, y, z)

if __name__ == "__main__":
    import sys
    run(*map(float, sys.argv[1:]))

import xmlrpclib

def run():
    s = xmlrpclib.ServerProxy('http://127.0.0.1:1921')
    phi, gx, gy, gz = s.get_axes_info()
    print phi, gx, gy, gz


if __name__ == "__main__":
    run()

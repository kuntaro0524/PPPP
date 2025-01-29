import xmlrpclib

def run(imgout):
    s = xmlrpclib.ServerProxy('http://127.0.0.1:1921')
    #imgout = "/isilon/users/target/target/QQQQ/Yam/tmp/test.ppm"
    s.get_coax_image(imgout)
    print "done?", imgout


if __name__ == "__main__":
    import sys
    import os

    imgout = sys.argv[1]

    if not imgout.startswith(os.sep):
        imgout = os.path.abspath(imgout)

    run(imgout)

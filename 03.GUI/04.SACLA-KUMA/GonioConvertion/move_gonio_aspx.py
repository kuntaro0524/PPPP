import xmlrpclib

def run(sx, sy): # shinoda x,y
    s = xmlrpclib.ServerProxy('http://127.0.0.1:1921')
    s.move_by_img_px(sx,sy)

if __name__ == "__main__":
    import sys
    run(int(sys.argv[1]), int(sys.argv[2]))

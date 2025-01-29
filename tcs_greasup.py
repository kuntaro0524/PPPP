import time
import socket
import sys

# import Motor as Motor
from File import *
from Motor import *

if __name__ == "__main__":
    host = '172.24.242.41'
    port = 10101
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    upper=Motor(s, "bl_32in_tc1_slit_1_upper", "pulse").getPosition()
    lower=Motor(s, "bl_32in_tc1_slit_1_lower", "pulse").getPosition()
    ring=Motor(s, "bl_32in_tc1_slit_1_ring", "pulse").getPosition()
    hall=Motor(s, "bl_32in_tc1_slit_1_hall", "pulse").getPosition()

    print("slit upper\t:%12s%7s" % upper)
    print("slit lower\t:%12s%7s" % lower)
    print("slit ring\t:%12s%7s" % ring)
    print("slit hall\t:%12s%7s" % hall)

    for num in range(10):
        print("\nnum %d\n" % num)

        print("slit hall set to 17633 pulse")
        Motor(s, "bl_32in_tc1_slit_1_hall", "pulse").move(17633)
        print("slit hall\t:%12s%7s\n" % Motor(s, "bl_32in_tc1_slit_1_hall", "pulse").getPosition())
        print("slit ring set to 16850 pulse")
        Motor(s, "bl_32in_tc1_slit_1_ring", "pulse").move(16850)
        print("slit ring\t:%12s%7s\n" % Motor(s, "bl_32in_tc1_slit_1_ring", "pulse").getPosition())
    
        print("slit upper set to 20292 pulse")
        Motor(s, "bl_32in_tc1_slit_1_upper", "pulse").move(20292)
        print("slit upper\t:%12s%7s\n" % Motor(s, "bl_32in_tc1_slit_1_upper", "pulse").getPosition())
        print("slit lower set to 20820 pulse")
        Motor(s, "bl_32in_tc1_slit_1_lower", "pulse").move(20820)
        print("slit lower\t:%12s%7s\n" % Motor(s, "bl_32in_tc1_slit_1_lower", "pulse").getPosition())

        #exit()
        #time.sleep(300)

        print("slit ring set to -24878 pulse")
        Motor(s, "bl_32in_tc1_slit_1_ring", "pulse").move(-24878)
        print("slit ring\t:%12s%7s\n" % Motor(s, "bl_32in_tc1_slit_1_ring", "pulse").getPosition())
        print("slit hall set to -23216 pulse")
        Motor(s, "bl_32in_tc1_slit_1_hall", "pulse").move(-23216)
        print("slit hall\t:%12s%7s\n" % Motor(s, "bl_32in_tc1_slit_1_hall", "pulse").getPosition())

        print("slit lower set to -20570 pulse")
        Motor(s, "bl_32in_tc1_slit_1_lower", "pulse").move(-20570)
        print("slit lower\t:%12s%7s\n" % Motor(s, "bl_32in_tc1_slit_1_lower", "pulse").getPosition())
        print("slit upper set to -20930 pulse")
        Motor(s, "bl_32in_tc1_slit_1_upper", "pulse").move(-20930)
        print("slit upper\t:%12s%7s\n" % Motor(s, "bl_32in_tc1_slit_1_upper", "pulse").getPosition())

    Motor(s, "bl_32in_tc1_slit_1_hall", "pulse").move(hall[0])
    Motor(s, "bl_32in_tc1_slit_1_ring", "pulse").move(ring[0])
    Motor(s, "bl_32in_tc1_slit_1_upper", "pulse").move(upper[0])
    Motor(s, "bl_32in_tc1_slit_1_lower", "pulse").move(lower[0])


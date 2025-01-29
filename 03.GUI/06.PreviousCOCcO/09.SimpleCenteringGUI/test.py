import sys,os,math
sys.path.append("/data/03.Sacla/SSSS/BLctrl")
from Gonio import *

# end wxGlade
host = '172.30.102.141'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

gonio=Gonio(s)
print gonio.getXYZmm()

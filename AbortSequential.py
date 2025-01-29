import socket
import Shutter
import MXserver

#host = '192.168.163.1'
host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

shutter=Shutter.Shutter(s)

print shutter.isOpen()
shutter.close()
print shutter.isOpen()

mxs=MXserver.MXserver()
mxs.getState()
mxs.abort()

s.close()

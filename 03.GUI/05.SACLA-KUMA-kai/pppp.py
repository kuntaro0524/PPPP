import Inocc2,socket
import CryImageProc


ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ms.connect(("192.168.163.1", 10101))
crycen=Inocc2.crycen(ms)

phi,cenx,ceny,cenz=crycen.get_axes_info_float()
print phi,cenx,ceny,cenz

filename="/isilon/BL32XU/BLsoft/PPPP/03.GUI/04.SACLA-KUMA/test.ppm"
crycen.get_coax_image(filename, convert=False)
#grav_x,grav_y,xylist=dpm.run(filename)

cip=CryImageProc.CryImageProc(filename)

a=cip.best_codes(filename)
for b in a:
        print b

ms.close()

import sys,math,numpy,socket,datetime,time
import threading
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import Gonio,Count

class TestThread(threading.Thread):
	def __init__(self,file_pointer):
		super(TestThread,self).__init__()
		self.file_pointer=file_pointer

	def run(self):
        	gonio=Gonio.Gonio(s)
        	curr_phi=gonio.getPhi()
        	#before_time=datetime.datetime.now()
		target_phi=curr_phi+180.0
		if target_phi > 360.0:
			target_phi=target_phi-360.0
		print "ROTATE"
        	gonio.rotatePhiNageppa(target_phi)

def runrun(file_pointer):
        prev_time=datetime.datetime.now()
        counter=Count.Count(s,0,3)
        file_pointer.write("logging start: %s\n"%prev_time)
        for i in range(0,100):
		print i
                t=datetime.datetime.now()
                ic,pin=counter.getCountMsec(10)
                dt=t-prev_time
                self.file_pointer.write("%s %s %s %s\n"%(t,ic,pin,dt))
                prev_time=t

if __name__=="__main__":
        #host = '192.168.163.1'
        import Gonio
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	logf=open(sys.argv[1],"w")

	print "STARTING"
 	thread=TestThread(logf)
	thread.start()
	print "ROTATIN"

	runrun(logf)

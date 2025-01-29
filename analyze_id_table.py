from AnalyzePeak import *
if __name__=="__main__":
                host = '172.24.242.41'
                port = 10101
                ##s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #s.connect((host,port))

                ana=AnalyzePeak(sys.argv[1])

                px,py=ana.prepData2(0,1)
                dx,dy=ana.spline(px,py,100000)

		i=0
		for x in dx:
			print "%8.4f %8.3f"%(x,dy[i])
			i+=1

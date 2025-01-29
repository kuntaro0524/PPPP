
from Count import *

if __name__=="__main__":
	host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	if len(sys.argv)!=5:
		print "Usage: program CHANNEL1 CHANNEL2 TOTAL_TIME[sec] INTEGTIME[msec]\n"
		sys.exit(1)


	ch1=int(sys.argv[1])
	ch2=int(sys.argv[2])
	total_time=float(sys.argv[3])
	integ_time=float(sys.argv[4])

        counter=Count(s,3,0)
        f=File("./")

        # Total time

        prefix="%03d"%f.getNewIdx3()
        ofilename="%s_time.scn"%prefix
        of=open(ofilename,"w")

        # initialization
        starttime=time.time()
        of.write("#### %s\n"%datetime.datetime.now())
        of.write("#### Total %5.1f[sec] %5.1f[msec]\n"%(total_time,integ_time))
        ttime=0
	
	# observed taple
	ltime=[]
	obs1=[]
	obs2=[]
        while (ttime <= total_time ):
                #currtime=datetime.datetime.now()
                currtime=time.time()
		ttime=currtime-starttime
                ltime.append(ttime)
                ch1,ch2=counter.getCountMsec(integ_time)
		obs1.append(ch1)
		obs2.append(ch2)

	# writing file
	for i in range(0,len(obs1)):
                of.write("12345 %8.4f %12d %12d\n" %(ltime[i],obs1[i],obs2[i]))
		i+=1
        of.close()

        # file open
        ana=AnalyzePeak(ofilename)
        x,y1,y2=ana.prepData3(1,2,3)

        py1=ana.getPylabArray(y1)
        py2=ana.getPylabArray(y2)

        mean1=py1.mean()
        mean2=py2.mean()
        std1=py1.std()
        std2=py2.std()

        of=open(ofilename,"a")
        of.write("\n## COUNTER1:%5d Average: %12.5f Std.:%12.5f (%8.3f perc.)\n"%(3,py1.mean(),py1.std(),py1.std()/py1.mean()*100.0))
        of.write("## COUNTER2:%5d Average: %12.5f Std.:%12.5f (%8.3f perc.)\n"%(0,py2.mean(),py2.std(),py2.std()/py2.mean()*100.0))
	of.close()

"""
Usage:
python mydaq2.py "2014/05/30 10:00:00.000000" "2014/06/01 10:00:00.000000"
"""
import sys
import urllib
import urllib2
import re
import datetime
import numpy

re_title = re.compile("<h1>(.*)</h1>")
#re_data = re.compile("<textarea.*>(.*)</textarea>", re.MULTILINE)


class MyDaq:
	def __init__(self):
		self.url = "http://okutsu3.spring8.or.jp/cgi-bin/MyDAQ2/mydaq2_data.py?"

	def getTime(self,timestr):
		# Target = "2014-06-01 09:59:41.315362"
		# Removing time shorter than 1.0 sec
		timestr=timestr[:timestr.rfind(".")]
		tdatetime = datetime.datetime.strptime(timestr, '%Y/%m/%d %H:%M:%S')
		# UnixTime
		#unixtime=datetime.datetime.ctdatetime
		return tdatetime

	def get_data(self,bdate, edate, sig, col):
		self.url = "http://okutsu3.spring8.or.jp/cgi-bin/MyDAQ2/mydaq2_data.py?"
		query = [("sig", sig),
			("col", col),
			("b", bdate),
			("e", edate),
			("bel", "be"),
			("format", "text"),
			("s", "submit")
			]
		self.url += urllib.urlencode(dict(query))
		response = urllib2.urlopen(self.url)
	
		html = response.read()
		#print "SIG=", sig
		#print "COL=", col
		l = html.splitlines()
		m = filter(lambda s: "textarea" in s[1], enumerate(l))
		if len(m) != 2:
			return None, None

		title = re_title.search(html).group(1)
		return title, l[m[0][0]+1:m[1][0]]

	def run(self, bdate, edate):
		R_style = False
		if R_style:
			print "date sig col value"
	
		for sig in "BL32XU_MX100", "BL32XU_EXP2":
		#for sig in "BL32XU_EXP2":
			#for col in xrange(1, 42):
			for col in xrange(2, 3):
				title, data = self.get_data(bdate, edate, sig, "c%d"%col)
				if data is None:
					continue
	
				print "#", title
				print "# begin:", bdate
				print "# end:", edate
				print "# sig, col:", sig, col
				if R_style:
					for l in data:
						sp = l.strip().split()
						if sp[2] == "None":
							sp[2] = "nan"
						print sp[1]
						print '"%s %s" %s %d %s'%(sp[0].replace("/","-"), sp[1], sig, col, sp[2])
				else:
					tlist=[]
					for l in data:
						sp = l.strip().split()
						if sp[2] == "None":
							sp[2] = "nan"
						tstr="%s %s"%(sp[0],sp[1])
						tim=self.getTime(tstr)

						data=tim,sig,col,sp[2]
						tlist.append(data)
						#print '"%s %s" %s %d %s'%(sp[0].replace("/","-"), sp[1], sig, col, sp[2])

					#print data
					#print "\n".join(data)
					a=numpy.array(tlist)

					if len(tlist)!=0:
						print "BEFORE"
						for t in a:
							print t
						p=tlist.sort(key=lambda x:x[0])
						print p
						print "AFTER"
						#for t in p:
							#print t
  	
if __name__ == "__main__":
	bdate, edate = sys.argv[1], sys.argv[2]
	my=MyDaq()
	my.run(bdate, edate)
	#i= my.getTime("2014-06-01 09:59:41.315362")
	#print type(i)
